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
              { text: 'vchat(微信)', link: '/vchat' }
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
        ]
      },
      {
        text: '开发',
        base: '/dev',
        collapsed: false,
        items: [
          {
            text: '几行代码实现一个插件', 
            link: '/plugin'
          },
        ]
      },
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/Soulter/AstrBot' }
    ]
  }
})
