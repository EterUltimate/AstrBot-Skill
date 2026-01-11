import { defineConfig } from "vitepress";

export default defineConfig({
  title: "AstrBot Docs",
  description: "AstrBot 开发文档",
  srcDir: "docs",
  base: process.env.VITEPRESS_BASE || "/",
  themeConfig: {
    nav: [
      { text: "核心概念", link: "/design_standards/core_concepts" },
      { text: "消息模型", link: "/messages/model" },
      { text: "插件配置", link: "/plugin_config/schema" },
      { text: "平台适配", link: "/platform_adapters/adapter_interface" },
      { text: "快照", link: "/snapshots/" },
    ],
  },
});

