# Dynamicwallpaper
## 🍑 详细介绍
[python学习笔记 | macOS Big Sur动态壁纸食用指南 ](https://billie52707.cn/2020/06/python%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0-macos-big-sur%E5%8A%A8%E6%80%81%E5%A3%81%E7%BA%B8%E9%A3%9F%E7%94%A8%E6%8C%87%E5%8D%97/)

环境要求
---
- python3
- 科学上网


项目简介
---
- 项目中用到的python模块，如网络请求（requests）以及文本解析（etree）皆为python源码自带的模块，无需配置更多环境<br>
- 本项目爬取的网站：[https://dynamicwallpaper.club](https://dynamicwallpaper.club "click me")由于服务器在国外，因此全程需要科学上网进行使用


功能简介
---
- 爬取目标网站所有动态壁纸的下载链接
- 根据下载链接，下载并保存动态壁纸至本地heic文件（多线程）


爬取思路
---
- 使用浏览器的开发者工具，捕捉到真实的壁纸下载链接<br>
- 分析真实的下载链接的url参数（共有三个）<br>
- 分步获取各个参数<br>
- 访问壁纸链接，保存其返回的二进制文本至本地文件


改进
---
- 此网站有不同类型的壁纸可选，可制作GUI图形界面，让用户以下拉框选择的形式，自行选择下载哪一个类型的壁纸


更多
---
- 此网站所有的壁纸下载链接分享：[https://download.billie52707.cn/true_heic_urls.html](https://download.billie52707.cn/true_heic_urls.html "click me")
- 详细介绍请戳 [python学习笔记 | macOS Big Sur动态壁纸食用指南 ](https://billie52707.cn/2020/06/python%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0-macos-big-sur%E5%8A%A8%E6%80%81%E5%A3%81%E7%BA%B8%E9%A3%9F%E7%94%A8%E6%8C%87%E5%8D%97/)

    
