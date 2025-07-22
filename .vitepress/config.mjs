import { defineConfig } from "vitepress";
import { themeConfig } from "./config/theme";
import {head} from "./config/head";

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "AstrBot",
  description: "AstrBot",
  head: head,
  themeConfig,

  sitemap: {
    hostname: "https://docs.astrbot.app",
  },

  lastUpdated: true,
  ignoreDeadLinks: true,
  cleanUrls: true,
  metaChunk: true,

})
