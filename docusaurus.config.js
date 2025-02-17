module.exports = {
  title: "Chaster",
  tagline:
    "Explore a new chastity experience, with custom time-based locks and adventures made for you.",
  url: "https://docs.chaster.app",
  baseUrl: "/",
  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "warn",
  favicon: "img/favicon.ico",
  organizationName: "chaster",
  projectName: "docs",
  themeConfig: {
    colorMode: {
      defaultMode: "dark",
      disableSwitch: true,
    },
    navbar: {
      title: "Chaster Docs",
      logo: {
        alt: "Chaster Logo",
        src: "img/logo.png",
      },
      items: [
        {
          to: "/",
          activeBasePath: "docs",
          label: "User guide",
          position: "left",
        },
        {
          to: "/api/basics/introduction",
          label: "API",
          position: "left",
        },
        {
          href: "https://chaster.app",
          label: "Website",
          position: "right",
        },
      ],
    },
    footer: {
      style: "dark",
      links: [
        {
          title: "Community",
          items: [
            {
              label: "Discord",
              href: "https://discord.gg/rDhfywB",
            },
            {
              label: "Twitter",
              href: "https://twitter.com/chasterapp_",
            },
          ],
        },
        {
          title: "More",
          items: [
            {
              label: "Changelog",
              href: "https://chaster.app/changelogs",
            },
            {
              label: "Developers",
              href: "https://chaster.app/developers",
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Chaster.`,
    },
  },
  presets: [
    [
      "@docusaurus/preset-classic",
      {
        docs: {
          sidebarPath: require.resolve("./sidebars.json"),
          routeBasePath: "/",
        },
        theme: {
          customCss: require.resolve("./src/css/custom.css"),
        },
      },
    ],
  ],
  plugins: [require.resolve('docusaurus-lunr-search')],
};
