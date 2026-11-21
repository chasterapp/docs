"""Verify the five guides against a downloaded T03 contract bundle.

Run: python3 openspec/changes/partner-ai-review-docs/verify_examples.py BUNDLE_DIR
Requires the host's jsonschema package. No network or runtime mutations.
"""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

from jsonschema import Draft4Validator, FormatChecker, RefResolver

bundle = Path(sys.argv[1])
manifest = json.loads((bundle / "manifest.json").read_text())
for key in ("openapi", "fixtures", "schemaExcerpt"):
    entry = manifest[key]
    assert hashlib.sha256((bundle / entry["file"]).read_bytes()).hexdigest() == entry["sha256"]
api = json.loads((bundle / "api.json").read_text())
fixtures = json.loads((bundle / "fixtures.json").read_text())
excerpt = json.loads((bundle / "partner-schemas.json").read_text())
for path in manifest["schemaPaths"].values():
    value = api
    for segment in path.split("."):
        value = value[segment]
    assert value == excerpt[path.split(".")[-1]]


def normalize(value):
    """Translate OpenAPI 3.0 nullable to JSON Schema without relaxing fields."""
    if isinstance(value, list):
        return [normalize(item) for item in value]
    if not isinstance(value, dict):
        return value
    result = {key: normalize(item) for key, item in value.items() if key != "nullable"}
    if value.get("nullable"):
        return {"anyOf": [result, {"type": "null"}]}
    return result


schema = normalize(api)
resolver = RefResolver.from_schema(schema)


def validate(value, name):
    Draft4Validator(schema["components"]["schemas"][name], resolver=resolver,
                    format_checker=FormatChecker()).validate(value)


prefix = Path("docs/api/extensions-api")
peer = prefix / "create-your-extension/peer-verifications.mdx"
webhooks = prefix / "create-your-extension/webhooks.mdx"
native = prefix / "interact-with-extensions/verification-picture.mdx"
paths = [peer, webhooks, native, Path("docs/extensions/verification-picture.mdx"),
         Path("docs/extensions/tasks.mdx")]
pattern = r"```json\n(.*?)\n```"
parsed = {path: [json.loads(text) for text in re.findall(pattern, path.read_text(), re.S)]
          for path in paths}
matched = set()
for path, examples in parsed.items():
    for index, example in enumerate(examples, 1):
        label = None
        if "verificationTypes" in example:
            # This is an intentional settings fragment, not a full update DTO.
            assert example == {"verificationTypes": [{"key": "photo", "label": "Photo review",
                               "description": "Review a submitted synthetic photo."}]}
            label = "unchanged illustrative settings fragment"
        elif "attachmentToken" in example:
            validate(example, "CreatePartnerPeerVerificationDto")
            for kind, request in fixtures["requests"].items():
                if example == request:
                    label = "requests." + kind
                    matched.add(label)
        elif "_id" in example:
            validate(example, "PartnerPeerVerificationResponseDto")
            if example == fixtures["created"]["body"]:
                label = "created.body"
                matched.add(label)
        elif "statusCode" in example:
            for kind in ("denied", "missingKeyholder"):
                if example == fixtures[kind]["body"]:
                    label = kind + ".body"
                    matched.add(label)
            assert label, "Unknown error example"
        elif "results" in example:
            validate(example, "PartnerPeerVerificationHistoryPageDto")
            for row in example["results"]:
                if row["status"] == "unavailable":
                    reason = row["unavailableReason"]
                    assert row in fixtures["history"]["results"]
                    assert example == {"results": [row], "hasMore": False}
                    assert row["nbVerifiedVotes"] == row["nbRejectedVotes"] == 0
                    assert row["voteCounts"] == {"verified": 0, "rejected": 0}
                    assert row["rejectionReasons"] == [] and row["endedAt"]
                    for check in row["checkResults"]:
                        assert check["approved"] == check["rejected"] == 0
                        assert check["rejectionReasons"] == []
                    label = "history.results." + reason
                    matched.add(label)
        elif "criteria" in example:
            validate(example, "SearchPartnerPeerVerificationsDto")
            assert "unavailable" in example["criteria"]["statuses"]
        elif "event" in example:
            validate(example, "PeerVerificationEnded")
            for kind in ("provider_error", "eligibility_revoked"):
                if example == fixtures["callbacks"][kind]:
                    label = "callbacks." + kind
                    matched.add(label)
            if example["data"]["status"] != "unavailable":
                assert "unavailableReason" not in example["data"]
        elif "actor" in example:
            validate(example, "PartnerVerificationPictureRequestDto")
            assert example == {"actor": "extension"}
        else:
            raise AssertionError((str(path), index, "Unmapped example"))
        # Schema validation rejects shape drift; fixtures reject untested fields.
        assert not re.search(r'"(?:feedback|voterId|model|provider|prompt|machineVoter)"',
                             json.dumps(example))
        print(f"{path}: JSON {index}: {label or 'merged OpenAPI shape'} PASS")

expected = {"requests.builtin", "requests.generic", "created.body", "denied.body",
            "missingKeyholder.body", "history.results.provider_error",
            "history.results.eligibility_revoked", "callbacks.provider_error",
            "callbacks.eligibility_revoked"}
assert matched == expected
# All six tested callback variants validate, with identical human/AI business data.
for callback in fixtures["callbacks"].values():
    validate(callback, "PeerVerificationEnded")
for status in ("verified", "rejected"):
    assert fixtures["callbacks"]["human_" + status]["data"] == fixtures["callbacks"]["ai_" + status]["data"]
# Preserve all original human JSON values except additive status filters.
for path in paths:
    old = subprocess.check_output(["git", "show", f"origin/main:{path}"], text=True)
    for text in re.findall(pattern, old, re.S):
        example = json.loads(text)
        if "criteria" in example:
            example["criteria"]["statuses"].append("unavailable")
        assert example in parsed[path], (str(path), "Existing human example changed")
assert fixtures["denied"]["effects"] == {"reviewsCreated": 0, "attachmentValidated": False,
                                         "expirationChanged": False, "jobEnqueued": False}
assert fixtures["missingKeyholder"]["statusCode"] == 409
print(f"PASS: hashes, seven schemas, {sum(map(len, parsed.values()))} JSON fences, "
      "nine fixture mappings, six callback variants and preserved human examples")
