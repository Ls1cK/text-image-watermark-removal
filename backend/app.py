from datetime import datetime
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import *
import os
import os.path
import glob

#导入数据库模块
import pymysql
import traceback  

##邮箱验证码
from flask_mail import Message,Mail


##去水印
import sys
from tensorflow import keras
import tensorflow as tf
import matplotlib.pyplot as plt
import scipy.misc
from tensorflow.keras.models import *
from tensorflow.keras.layers import *
from tensorflow.keras.optimizers import *
from tensorflow.keras.callbacks import ModelCheckpoint, LearningRateScheduler
import math
from PIL import Image
import random
import argparse
import numpy as np
from pathlib import Path
import cv2
from model import get_model
from noise_model_test import get_noise_model
#GPU显存设置有问题，需要设置为仅在需要时申请显存 Name: tensorflow Version: 1.9.0
os.environ["CUDA_VISIBLE_DEVICES"] = '0'   #指定第一块GPU可用
config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.5  # 程序最多只能占用指定gpu50%的显存
config.gpu_options.allow_growth = True      #程序按需申请内存
sess = tf.Session(config=config)

##图像质量
from skimage.metrics import mean_squared_error
from skimage.metrics import peak_signal_noise_ratio
from skimage.measure import compare_ssim


app = Flask(__name__)

# Flask Mail
app.config.update(
     DEBUG = True,
     MAIL_SERVER='smtp.qq.com',
     MAIL_PROT= 465,
     MAIL_USE_TLS = True,
     MAIL_USE_SSL = False,
     MAIL_USERNAME = 'chris12138@qq.com',
     MAIL_PASSWORD = 'sbmfyfhopdbudddf',
     MAIL_DEBUG = True
 )
mail=Mail(app)

# # 获取当前位置的绝对路径
basedir = os.path.abspath(os.path.dirname(__file__))

# #跨域解决
CORS(app, supports_credentials=True)

## -------------------------------------------------------------------------------
## 以下模块为 User 图像处理相关

## 文本图像水印去除

input_size = (256,256,1)

def unet(pretrained_weights = None,input_size = input_size):
    inputs = Input(input_size)
    conv1 = Conv2D(64, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(inputs)
    conv1 = Conv2D(64, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv1)
    pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)
    conv2 = Conv2D(128, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool1)
    conv2 = Conv2D(128, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv2)
    pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)
    conv3 = Conv2D(256, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool2)
    conv3 = Conv2D(256, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv3)
    pool3 = MaxPooling2D(pool_size=(2, 2))(conv3)
    conv4 = Conv2D(256, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool3)
    conv4 = Conv2D(256, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv4)
    drop4 = Dropout(0.5)(conv4)
    pool4 = MaxPooling2D(pool_size=(2, 2))(drop4)

    conv5 = Conv2D(512, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool4)
    conv5 = Conv2D(512, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv5)
    drop5 = Dropout(0.5)(conv5)

    up6 = Conv2D(512, 2, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(UpSampling2D(size = (2,2))(drop5))

    merge6 = concatenate ([drop4,up6])
    conv6 = Conv2D(512, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(merge6)
    conv6 = Conv2D(512, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv6)

    up7 = Conv2D(256, 2, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(UpSampling2D(size = (2,2))(conv6))
    merge7 = concatenate ([conv3,up7])
    conv7 = Conv2D(256, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(merge7)
    conv7 = Conv2D(256, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv7)

    up8 = Conv2D(128, 2, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(UpSampling2D(size = (2,2))(conv7))
    merge8 = concatenate ([conv2,up8])
    conv8 = Conv2D(128, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(merge8)
    conv8 = Conv2D(128, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv8)

    up9 = Conv2D(64, 2, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(UpSampling2D(size = (2,2))(conv8))
    merge9 = concatenate ([conv1,up9])  
    conv9 = Conv2D(64, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(merge9)
    conv9 = Conv2D(64, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv9)
    conv9 = Conv2D(2, 3, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv9)
    conv10 = Conv2D(1, 1, activation = 'sigmoid')(conv9)

    model = Model(inputs = inputs, outputs = conv10)
    
    
    return model
    
def split2(dataset,size,h,w):
    newdataset=[]
    nsize1=256
    nsize2=256
    for i in range (size):
        im=dataset[i]
        for ii in range(0,h,nsize1):
            for iii in range(0,w,nsize2): 
                newdataset.append(im[ii:ii+nsize1,iii:iii+nsize2,:])
    
    return np.array(newdataset) 
def merge_image2(splitted_images, h,w):
    image=np.zeros(((h,w,1)))
    nsize1=256
    nsize2=256
    ind =0
    for ii in range(0,h,nsize1):
        for iii in range(0,w,nsize2):
            image[ii:ii+nsize1,iii:iii+nsize2,:]=splitted_images[ind]
            ind=ind+1
    return np.array(image)  

@app.route("/unwatermark/TW", methods = ['GET', 'POST'])
def unwatermarkTW():
    deg_image_path_dir = "./static/file/inputdir"
    save_dir = "./static/file/outputdir"

    # 在创建model后，先使用一遍 model.predict()，参数的大小和真实大小一致
    # a = np.ones(1,256,256,1)
    # generator.predict(a)

    if save_dir:
        output_path = Path(save_dir)
        output_path.mkdir(parents=True, exist_ok=True)

    deg_image_paths = list(Path(deg_image_path_dir).glob("*.*"))

    for deg_image_path in deg_image_paths:
        deg_image = Image.open(deg_image_path)# /255.0
        deg_image = deg_image.convert('L')
        deg_image.save('./static/file/curImg/cur_image.png')

        test_image = plt.imread('./static/file/curImg/cur_image.png')

        h =  ((test_image.shape [0] // 256) +1)*256 
        w =  ((test_image.shape [1] // 256 ) +1)*256

        test_padding=np.zeros((h,w))+1
        test_padding[:test_image.shape[0],:test_image.shape[1]]=test_image

        test_image_p=split2(test_padding.reshape(1,h,w,1),1,h,w)
        predicted_list=[]
        for l in range(test_image_p.shape[0]):
            with graph_dg.as_default():
                predicted_list.append(generator.predict(test_image_p[l].reshape(1,256,256,1)))
        predicted_image = np.array(predicted_list)#.reshape()
        predicted_image=merge_image2(predicted_image,h,w)

        predicted_image=predicted_image[:test_image.shape[0],:test_image.shape[1]]
        predicted_image=predicted_image.reshape(predicted_image.shape[0],predicted_image.shape[1])

        output_dir = str(output_path.joinpath(deg_image_path.name))[:-4] + "cleaned" + ".png"
        plt.imsave(output_dir, predicted_image,cmap='gray')
    
    unTW_mes = 'true'
    return unTW_mes , 200

## -----------------------------------------------------------------------------------------------
## 自然图像水印去除

def get_args():
    parser = argparse.ArgumentParser(description="Test trained model",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--model", type=str, default="srresnet",
                        help="model architecture ('srresnet' or 'unet')")
    parser.add_argument("--test_noise_model", type=str, default="text,0,25",
                        help="noise model for test images")
    args = parser.parse_args()
    return args

def get_image(image):
    image = np.clip(image, 0, 255)
    return image.astype(dtype=np.uint8)

## 自然图像水印去除
@app.route("/unwatermark/IW", methods = ['GET', 'POST'])
def unwatermarkIW():
##去水印
    args = get_args()
    image_dir = "./static/file/inputdir"
    result_dir = "./static/file/outputdir"

    val_noise_model = get_noise_model(args.test_noise_model)

    # 每次预测完成之前，清空session之后，之后重新加载模型
    ## 确实有作用，二次调用Noise2Noise时，添加此代码可避免OOM
    ## 但是 先使用DE_GAN,再使用Noise2Noise 依然会引发OOM
    ## 二次调用DE_GAN 1.训练模型不起作用，输出原带水印图 
    ## 2.报错 TypeError: Cannot interpret feed_dict key as Tensor:Tensor Tensor is not an element of this graph.
    # keras.backend.clear_session()

    # #获取模型 Noise2Noise
    # model = get_model(args.model)
    # model_n2n = model
    # model_n2n.load_weights("./static/file/weights/Watermark.hdf5")

    if result_dir:
        output_dir = Path(result_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    image_paths = list(Path(image_dir).glob("*.*"))

    for image_path in image_paths:
        image = cv2.imread(str(image_path))
        h, w, _ = image.shape
        #image = image[:(h // 16) * 16, :(w // 16) * 16]  # for stride (maximum 16)
        h, w, _ = image.shape

        out_image = np.zeros((h, w * 1, 3), dtype=np.uint8)
        noise_image = val_noise_model(image)

        with graph_n2n.as_default():
            pred = model_n2n.predict(np.expand_dims(noise_image, 0))

        denoised_image = get_image(pred[0])
        out_image[:, :w] = denoised_image

        if result_dir:
            cv2.imwrite(str(output_dir.joinpath(image_path.name))[:-4] + "cleaned" + ".png", out_image)
        else:
            cv2.imshow("result", out_image)
            key = cv2.waitKey(-1)
            # "q": quit
            if key == 113:
                return 0

    un_mes = 'true'
    return un_mes , 200


## 图像质量比较
@app.route("/comp", methods = ['GET', 'POST'])
def image_psnr_ssim():
    file_path = basedir + "/static/file/inputdir/"
    filelist = os.listdir(file_path)

    img1 = cv2.imread('./static/file/inputdir/'+filelist[0])
    img2 = cv2.imread('./static/file/inputdir/'+filelist[1])

    PSNR = peak_signal_noise_ratio(img1, img2)
    SSIM = compare_ssim(img1, img2, multichannel=True)

    p=round(PSNR, 2);
    s=round(SSIM, 2);

    result = jsonify([p,s])
    return result,200


## -------------------------------------------------------------------------------
## 以下模块为 User 文件处理相关

## 删除服务器可能残余图像
def delfile(path):
#   read all the files under the folder
    fileNames = glob.glob(path + r'\*')
    
    for fileName in fileNames:
        try:
#           delete file
            os.remove( fileName)
        except:
            try:
#               delete empty folders 
                os.rmdir( fileName)
            except:
#               Not empty, delete files under folders  
                delfile( fileName)
#               now, folders are empty, delete it  
                os.rmdir( fileName)


# 上传照片接口
@app.route("/upload", methods = ['GET', 'POST'])
def upload():
    f = request.files.get('file')
    # 获取安全的文件名 正常的文件名
    filename = secure_filename(f.filename)
    print(filename + "已保存到本地./static/file/inputdir/")

    # 生成随机数
    random_num = random.randint(0, 100)

    # f.filename.rsplit('.', 1)[1] 获取文件的后缀
    # 把文件重命名
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + "_" + str(random_num) + "." + filename.rsplit('.', 1)[1]

    # 保存的目标绝对地址
    file_path = basedir + "/static/file/inputdir/"

    # 判断文件夹是否存在 不存在则创建
    if not os.path.exists(file_path):
        os.makedirs(file_path, 755)

    # 保存文件到目标文件夹
    f.save(file_path + filename)

    mes = 'true'
    return mes , 200

##返回照片接口
@app.route("/revert", methods = ['GET'])
def revert():
    file_path = basedir + "/static/file/outputdir/"

    filelist = os.listdir(file_path)
    imglist = ['http://127.0.0.1:5000/static/file/outputdir/'+x for x in filelist]

    revertJson = jsonify(imglist);
    return revertJson, 200

##删除照片接口
@app.route("/clearFile", methods = ['Post'])
def clearFile():
    ## 删除本地缓存图片
    file_path_1 = basedir + "/static/file/inputdir/"
    file_path_2 = basedir + "/static/file/outputdir/"
    delfile(file_path_1)
    delfile(file_path_2)

    print("本地缓存已清除")
    clear_mes = "true"
    return clear_mes,200
## -------------------------------------------------------------------------------
## 以下模块为 User 登录注册相关


##邮箱验证码
##isnum用来控制是纯数字还是数字加字母组合
def generate_verification_code(isnum):
    ''' 随机生成6位的验证码 '''
    code_list = []
    if isnum==True:
        for i in range(10): # 0-9数字
            code_list.append(str(i))
    else:
        for i in range(10): # 0-9数字
            code_list.append(str(i))
        for i in range(65, 91): # A-Z
            code_list.append(chr(i))
        for i in range(97, 123): # a-z
            code_list.append(chr(i))
    myslice = random.sample(code_list, 6)  # 从list中随机获取6个元素，作为一个片断返回
    verification_code = ''.join(myslice) # list to string
    return verification_code


@app.route('/ver_code',methods = ['POST'])
def getSendCodeRequest():
    email = request.json.get('username')
    if not email:
        return jsonify({'code': 400, 'msg': 'no email'})
    '''
    生成随机验证码，保存到memcache中，然后发送验证码，与用户提交的验证码对比
    '''
    captcha = generate_verification_code("false")  # 随机生成6位验证码
    print(captcha)
    sender = "chris12138@qq.com"
    mail_code = '验证码 %s' % captcha

    # 给用户提交的邮箱发送邮件
    msg = Message("SWJTU@LQ,欢迎来到我的网站", sender= sender, recipients = [email])
    msg.body = mail_code
    msg.html = mail_code
    try:   
        mail.send(msg)  # 发送
        return jsonify({'code': 200, 'msg': 'sended', 'captcha':captcha})
    except Exception as e:
        print(e)
        return jsonify({'code': 500, 'msg': 'fail to send'})

#获取登录参数及处理
@app.route('/login',methods = ['POST'])
def getLoginRequest():
#查询用户名及密码是否匹配及存在
    username = request.json.get('username')
    password = request.json.get('password')
    #连接数据库,此前在数据库中创建数据库
    if username and password:
        # 连接数据库
        connection = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='patimages', charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        # 创建游标
        cursor = connection.cursor()
        # 操作sql
        selectUserSql = "SELECT `username`, `password` FROM `account` WHERE username='" + username + "'"
        print (selectUserSql)
        cursor.execute(selectUserSql)
        result = cursor.fetchone()
        print (result)
        if result and result['password'] == password:
            return jsonify({'code': 200, 'msg': 'success', 'token': username})
    return jsonify({'code': 400, 'msg': 'error'})

#获取密码重置参数及处理
@app.route('/reset_account', methods=['POST'])
def reset_account():
    username = request.json.get('username')
    password = request.json.get('password')
    if username and password:
        # 连接数据库
        connection = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='patimages', charset='utf8',cursorclass=pymysql.cursors.DictCursor)
        # 创建游标
        cursor = connection.cursor()
        # 更新数据
        updateSql =  "UPDATE `account` SET password=  '" + password + "' WHERE username='" + username + "'"
        print (updateSql)
        cursor.execute(updateSql)
        # 提交
        connection.commit()
        return  jsonify({'code': 200})
    return jsonify({'code': 400})

#获取注册参数及处理
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    if username and password:
        # 连接数据库
        connection = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='patimages', charset='utf8',cursorclass=pymysql.cursors.DictCursor)
        # 创建游标
        cursor = connection.cursor()
        # 插入数据
        insertSql = "INSERT INTO `account` (`username`, `password`) VALUES ( '"+username + "','" + password + "')"
        print (insertSql)
        cursor.execute(insertSql)
        # 提交
        connection.commit()
        return  jsonify({'code': 200})
    return jsonify({'code': 400})

    
if __name__ == '__main__':
    # generator : DE-GAN 模型加载  model : Noise2Noise 模型加载  全局
    global graph_dg, generator, graph_n2n, model_n2n
    graph_dg = tf.get_default_graph()

    graph_n2n = tf.get_default_graph()

    #获取模型 DE-GAN
    generator = unet()
    generator.load_weights("./static/file/weights/watermark_rem_weights.h5")

    args = get_args()
    #获取模型 Noise2Noise
    model_n2n = get_model(args.model)
    model_n2n.load_weights("./static/file/weights/Watermark.hdf5")

    app.run()