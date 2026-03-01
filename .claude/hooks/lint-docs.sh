#!/bin/bash
# lint-docs.sh -- Lint .mdx/.md files for Chaster docs tone violations
#
# Usage:
#   lint-docs.sh <file>           # Lint a single file
#   lint-docs.sh                  # Lint all .mdx files in docs/
#
# Exit codes:
#   0 -- no violations found
#   1 -- violations found (details on stdout)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DOCS_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)/docs"
HAS_ERRORS=0

lint_file() {
    local file="$1"
    local file_has_errors=0

    # Rule 1: Em dash detection (U+2014)
    local emdash_lines
    emdash_lines=$(grep -n $'\u2014' "$file" 2>/dev/null || true)
    if [ -n "$emdash_lines" ]; then
        while IFS= read -r line; do
            echo "ERROR [$file] $line"
            echo "  Em dash (U+2014) found. Use commas, colons, periods, or parentheses instead."
        done <<< "$emdash_lines"
        file_has_errors=1
    fi

    # Rule 2: Title case heuristic in headings
    # Flags headings where 2+ words (after the first) are capitalized,
    # excluding known proper nouns
    local proper_nouns="Chaster|Plus|API|OAuth|Discord|Safari|Chrome|iOS|Android|PWA|GitHub|HTTP|HTTPS|JSON|REST|DM|FAQ|ID|URL|UI|UX|Findom|Chaster Plus"
    while IFS= read -r line; do
        local linenum="${line%%:*}"
        local heading="${line#*:}"
        # Strip markdown heading prefix
        heading=$(echo "$heading" | sed 's/^#\+[[:space:]]*//')
        # Get words after the first
        local rest
        rest=$(echo "$heading" | cut -d' ' -f2-)
        if [ -z "$rest" ]; then
            continue
        fi
        # Count capitalized words that aren't proper nouns
        local caps=0
        for word in $rest; do
            # Skip proper nouns
            if echo "$word" | grep -qE "^($proper_nouns)"; then
                continue
            fi
            # Skip words with special chars (markdown bold, links, etc.)
            if echo "$word" | grep -qE '^\*|^\[|^\(|^`'; then
                continue
            fi
            # Check if word starts with uppercase
            if echo "$word" | grep -qE '^[A-Z]'; then
                caps=$((caps + 1))
            fi
        done
        if [ "$caps" -ge 2 ]; then
            echo "WARNING [$file:$linenum] Possible title case: $heading"
        fi
    done < <(grep -n '^##' "$file" 2>/dev/null || true)

    return $file_has_errors
}

# Determine what to lint
if [ $# -ge 1 ]; then
    FILE="$1"
    if [[ "$FILE" == *.mdx ]] || [[ "$FILE" == *.md ]]; then
        if ! lint_file "$FILE"; then
            HAS_ERRORS=1
        fi
    fi
else
    while IFS= read -r -d '' file; do
        if ! lint_file "$file"; then
            HAS_ERRORS=1
        fi
    done < <(find "$DOCS_DIR" -name '*.mdx' -print0 2>/dev/null)
fi

if [ "$HAS_ERRORS" -gt 0 ]; then
    exit 1
fi

exit 0
