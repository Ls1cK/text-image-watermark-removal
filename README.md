# PatImages-TextImageWatermarkRemoval-2021西南交通大学计算机与人工智能学院毕业设计

## 前后端分离，涉及的技术内容：Vue + Flask + Vue-router + ElementUI + Noise2Noise + Watermark.js。
Vue:https://cn.vuejs.org/
Flask:https://palletsprojects.com/p/flask/
Vue-router:https://router.vuejs.org/zh/
ElementUI:https://element.eleme.io/#/zh-CN
Watermark.js:http://brianium.github.io/watermarkjs/
Noise2Noise:https://github.com/NVlabs/noise2noise

## 水印去除算法参考开源技术Noise2Noise修改得到 

[1] Jaakko Lehtinen, Jacob Munkberg, Jon Hasselgren, et al. Noise2Noise: Learning Image Restoration without Clean Data [C]. ICML, 2018.

官方Code: https://github.com/NVlabs/noise2noise

## Usage
frontend:
$ cd tiwr
$ npm install
$ npm run dev

backend:
安装python + tensorflow 环境，配置好环境变量
安装相关依赖 ：
参考：
##去水印
keras
argparse
nump
pathlib
openCV
argparse
PIL(pillow)

##图像质量
skimage_image
