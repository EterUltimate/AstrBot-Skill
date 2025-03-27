import { defineConfig } from "vitepress";

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "AstrBot",
  description: "AstrBot",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: "主页", link: "/" },
      { text: "开始", link: "/what-is-astrbot" },
    ],

    search: {
      provider: "local",
    },

    sidebar: [
      {
        text: "简介",
        items: [
          { text: "什么是 AstrBot", link: "/what-is-astrbot" },
          { text: "社区", link: "/community" },
          { text: "常见问题", link: "/faq" },
        ],
      },
      {
        text: "部署",
        base: "/deploy",
        collapsed: false,
        items: [
          {
            text: "部署 AstrBot",
            base: "/deploy/astrbot",
            collapsed: true,
            items: [
              { text: "Docker 部署", link: "/docker" },
              { text: "Windows 一键部署", link: "/windows" },
              { text: "手动部署", link: "/cli" },
              { text: "宝塔面板部署", link: "/btpanel" },
              { text: "CasaOS 部署", link: "/casaos" },
              { text: "一键脚本(Linux, 社区提供)", link: "/linux-one" },
            ],
          },
          {
            text: "部署消息平台(协议端)",
            base: "/deploy/platform",
            collapsed: true,
            items: [
              {
                text: "QQ 官方接口(qqofficial)",
                base: "/deploy/platform/qqofficial",
                collapsed: true,
                items: [
                  { text: "Webhook 方式", link: "/webhook" },
                  { text: "Websockets 方式", link: "/websockets" },
                ],
              },
              {
                text: "QQ 个人号(aiocqhttp)",
                base: "/deploy/platform/aiocqhttp",
                collapsed: true,
                items: [
                  { text: "使用 NapCat", link: "/napcat" },
                  { text: "使用 Lagrange", link: "/lagrange" },
                  { text: "使用其他端", link: "/others" },
                ],
              },
              { text: "企业微信", link: "/wecom" },
              { text: "微信个人号(gewechat)", link: "/gewechat" },
              { text: "飞书", link: "/lark" },
              { text: "钉钉", link: "/dingtalk" },
              { text: "Telegram", link: "/telegram" },
            ],
          },
          {
            text: "部署好后...",
            link: "/when-deployed",
          },
        ],
      },
      {
        text: "配置",
        base: "/config",
        collapsed: false,
        items: [
          {
            text: "接入大模型服务",
            base: "/config/providers",
            collapsed: true,
            items: [
              { text: "接入 OpenAI、DeepSeek 等各种模型", link: "/llm" },
              {
                text: "接入 Dify",
                link: "/dify",
              },
              {
                text: "接入 阿里云百炼应用",
                link: "/dashscope",
              },
              {
                text: "接入 Ollama 使用 DeepSeek-R1 等模型",
                link: "/provider-ollama",
              },
              {
                text: "接入 LMStudio 使用 DeepSeek-R1 等模型",
                link: "/provider-lmstudio",
              },
              {
                text: "接入 OneAPI",
                link: "/oneapi",
              },
            ],
          },
          {
            text: "AstrBot 配置文件",
            link: "/astrbot-config",
          },
          {
            text: "自定义温度等模型参数",
            link: "/model-config",
          },
        ],
      },
      {
        text: "使用",
        base: "/use",
        collapsed: false,
        items: [
          {
            text: "管理面板",
            link: "/webui",
          },
          {
            text: "AstrBot Star(插件)",
            link: "/plugin",
          },
          {
            text: "内置指令",
            link: "/command",
          },
          {
            text: "函数调用",
            link: "/function-calling",
          },
          {
            text: 'MCP', 
            link: '/mcp'
          },
          {
            text: '网页搜索',
            link: '/websearch'
          },
          {
            text: "沙箱化代码执行器(beta)",
            link: "/code-interpreter",
          },
          {
            text: "配置 Whisper 语音转文字",
            link: "/whisper",
          },
          {
            text: "配置文字转语音(TTS)",
            link: "/tts",
          },
          {
            text: "更新管理面板",
            link: "/update-webui",
          },
        ],
      },
      {
        text: "开发",
        base: "/dev",
        collapsed: false,
        items: [
          {
            text: "核心代码解释",
            base: "/dev/core",
            collapsed: true,
            items: [
              { text: "整体架构", link: "/overall_architecture" },
              { text: "运行流程", link: "/overall_operation_process" }
            ],
          },
          {
            text: "插件开发",
            base: "/dev/star",
            collapsed: true,
            items: [{ text: "插件基础开发", link: "/plugin" }],
          },
          {
            text: "插件基础开发",
            link: "/plugin",
          },
          {
            text: "接入平台适配器",
            link: "/plugin-platform-adapter",
          },
        ],
      },
      {
        text: "其他",
        base: "/others",
        collapsed: false,
        items: [
          {
            text: "配置文件-大语言模型提供商",
            link: "/provider",
          },
          {
            text: "配置文件-消息平台适配器",
            link: "/platform",
          },
          {
            text: "自部署文转图",
            link: "/self-host-t2i",
          },
        ],
      },
    ],

    socialLinks: [
      { icon: "github", link: "https://github.com/Soulter/AstrBot" },
    ],
  },
});
