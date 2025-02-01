import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "AstrBot",
  description: "AstrBot",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: '主页', link: '/' },
      { text: '简介', link: '/what-is-astrbot' },
      { text: '快速开始', link: '/get-started' }
    ],

    sidebar: [
      {
        text: '简介',
        items: [
          { text: '什么是 AstrBot', link: '/what-is-astrbot' },
          { text: '社区', link: '/community' }
        ]
      },
      {
        text: '部署',
        base: '/deploy',
        collapsed: false,
        items: [
          {
            text: '部署 AstrBot', 
            base: '/deploy/astrbot',
            collapsed: true,
            items: [
              { text: 'Docker部署', link: '/docker' },
              { text: 'Windows一键安装', link: '/windows' },
              { text: '手动部署', link: '/cli' }
            ]
          },
          { 
            text: '部署消息平台', 
            base: '/deploy/platform',
            collapsed: true,
            items: [
              {
                text: 'aiocqhttp(QQ, 推荐)', 
                base: '/deploy/platform/aiocqhttp',
                collapsed: true,
                items: [
                  { text: '使用 NapCat', link: '/napcat' },
                  { text: '使用 Lagrange', link: '/lagrange'},
                  { text: '使用其他端', link: '/others'}
                ]
              },
              { text: 'qqofficial(QQ官方)', link: '/qqofficial' },
              { text: 'gewechat(微信,推荐)', link: '/gewechat' },
              { text: 'vchat(微信)', link: '/vchat' },
              { text: 'Telegram', link: '/telegram'}
            ]
          },
          {
            text: '部署好后...', 
            link: '/when-deployed'
          },
        ]
      },
      {
        text: '配置',
        base: '/config',
        collapsed: false,
        items: [
          {
            text: 'AstrBot 配置文件', 
            link: '/astrbot-config'
          },
          {
            text: '大语言模型提供商', 
            link: '/provider'
          },
          {
            text: '接入 Ollama 使用 DeepSeek-R1 等模型',
            link: '/provider-ollama'
          },
          {
            text: '消息平台适配器', 
            link: '/platform'
          },
        ]
      },
      {
        text: '使用',
        base: '/use',
        collapsed: false,
        items: [
          {
            text: '管理面板', 
            link: '/webui'
          },
          {
            text: 'AstrBot Star(插件)', 
            link: '/plugin'
          },
          {
            text: '内置指令', 
            link: '/command'
          },
          {
            text: '沙箱化代码执行器(beta)',
            link: '/code-interpreter'
          },
          {
            text: '接入 Whisper 语音转文字',
            link: '/whisper'
          },
          {
            text: '更新管理面板',
            link: '/update-webui'
          }
        ]
      },
      {
        text: '开发',
        base: '/dev', 
        collapsed: false,
        items: [
          {
            text: '插件基础开发', 
            link: '/plugin'
          },
          {
            text: '接入平台适配器', 
            link: '/plugin-platform-adapter'
          }
        ]
      },
      {
        text: '其他',
        base: '/others',
        collapsed: false,
        items: [
          {
            text: '接入 OneAPI', 
            link: '/oneapi'
          },
          {
            text: '接入 Dify',
            link: '/dify'
          },
          {
            text: "自部署文转图",
            link: '/self-host-t2i'
          }
        ]
      },
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/Soulter/AstrBot' }
    ]
  }
})
