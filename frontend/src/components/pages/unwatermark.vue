<template>
  <div class="funscontainer-uw">
    <div class="funsSteps">
      <!-- progressbar -->
      <el-steps :active="active" finish-status="success" direction="vertical">
        <el-step title="上传"></el-step>
        <el-step title="处理"></el-step>
        <el-step title="更新"></el-step>
      </el-steps>
    </div>
    <div class="left picUpload">
      <div class="funssuccess">
        <div class="funssuccessContent">
          <p><h2 >水印去除</h2><span>支持批量处理，无论是文本图像，还是自然图像，均可去水印。</span></p>
        </div>
      </div>
      <div class="unwmBox">
        <el-upload
          class="upload-revert"
          ref="upload"
          list-type="picture-card"
          action="http://127.0.0.1:5000/upload"
          multiple
          :limit="30"
          :on-remove="handleRemove"
          :on-preview="handlePictureCardPreview"
          :file-list="fileList"
          :auto-upload="false"
        >
          <div>
            <i class="el-icon-plus"></i>
          </div>
        </el-upload>
      </div>
      <el-dialog :visible.sync="dialogVisible">
        <img width="100%" :src="dialogImageUrl" alt="previewImg" />
      </el-dialog>
      <div class="btnBox">
        <el-button
          v-if="this.changeMd === true"
          class="unwmBtn"
          type="success"
          plain
          @click="submitUpload"
          icon="el-icon-upload2"
          style="margin-left:10px"
          >上传图片</el-button
        >
        <el-button
          v-if="this.changeMd === true"
          class="unwmBtn"
          type="success"
          plain
          @click="revert"
          icon="el-icon-download"
          >更新图片</el-button
        >
                <el-button
          v-if="this.changeMd === false"
          class="unwmBtn"
          type="success"
          @click="submitUpload"
          icon="el-icon-upload2"
          style="margin-left:10px"
          >上传图片</el-button
        >
        <el-button
          v-if="this.changeMd === false"
          class="unwmBtn"
          type="success"
          @click="revert"
          icon="el-icon-download"
          >更新图片</el-button
        >
      </div>
    </div>
    <div class="right picManipulate">
      <div class="rightHeader">
          <el-tooltip
          class="item"
          effect="light"
          content="点我切换模式"
          placement="right-start">
          <div class="button r" id="button-6">
            <input type="checkbox" class="checkbox" @click="changeModel()"/>
            <div class="knobs"></div>
            <div class="layer"></div>
          </div>
          </el-tooltip>
          <div class="changesuccess">
            <el-alert
              v-if="this.changeMd === true"
              title="欢迎使用水印去除功能"
              description="现在的水印去除模式为-文本图像"
              type="success"
              center
              show-icon
              :closable="false">
            </el-alert>
            <el-alert
              v-if="this.changeMd === false"
              title="欢迎使用水印去除功能"
              description="现在的水印去除模式为-自然图像"
              type="success"
              center
              show-icon
              :closable="false"
              effect = "dark">
            </el-alert>
          </div>
      </div>
      <div class="loader">
        <div class="loader-inner" id="loader-inner">
          <div class="loader-line-wrap">
            <div class="loader-line"></div>
          </div>
          <div class="loader-line-wrap">
            <div class="loader-line"></div>
          </div>
          <div class="loader-line-wrap">
            <div class="loader-line"></div>
          </div>
          <div class="loader-line-wrap">
            <div class="loader-line"></div>
          </div>
          <div class="loader-line-wrap">
            <div class="loader-line"></div>
          </div>
        </div>
      </div>
      <el-button
          v-if="this.changeMd === true"
          class="unwatermarkBtn"
          type="success"
          plain
          @click="submitUnwatermarkTW"
          :icon="cur_icon"
          >{{ loadingBtn ? "去水印中.." : "开始去水印" }}</el-button
        >
        <el-button
          v-if="this.changeMd === false"
          class="unwatermarkBtn"
          type="success"
          @click="submitUnwatermarkIW"
          :icon="cur_icon"
          >{{ loadingBtn ? "去水印中.." : "开始去水印" }}</el-button
        >
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      fileList: [],
      dialogImageUrl: "",
      dialogVisible: false,
      loadingBtn:false,
      cur_icon:"el-icon-mouse",
      changeMd: true,
      active: 0,
    };
  },
  methods: {
    submitUpload() {
      //上传之前，先清除缓存
      this.$http.post("http://127.0.0.1:5000/clearFile");

      this.$refs.upload.submit();

      this.active = 1;
    },
    submitUnwatermarkTW() {
      this.loadingBtn = true;
      this.cur_icon = "el-icon-loading";
      let loaders = document.getElementsByClassName("loader-line-wrap");
      for(let i = 0;i < loaders.length; i++){
        loaders[i].style.animationPlayState = "running";
      }
      this.$http
      .get("http://127.0.0.1:5000/unwatermark/TW")
      .then(this.processingImg);
    },
    submitUnwatermarkIW() {
      this.loadingBtn = true;
      this.cur_icon = "el-icon-loading";
      let loaders = document.getElementsByClassName("loader-line-wrap");
      for(let i = 0;i < loaders.length; i++){
        loaders[i].style.animationPlayState = "running";
      }
      this.$http
      .get("http://127.0.0.1:5000/unwatermark/IW")
      .then(this.processingImg);
    },
    processingImg(response){
      let mes = response.data;
      this.loadingBtn = !mes;
      let loaders = document.getElementsByClassName("loader-line-wrap");
      for(let i = 0;i < loaders.length; i++){
        loaders[i].style.animationPlayState = "paused";
      }
      this.active = 2;
      this.cur_icon = "el-icon-finished"
    },
    getData(response) {
      let res = response.data;
      for (let i = 0; i < res.length; i++) {
        this.fileList.push({
          name: i + ".png",
          url: res[i],
        });
      }
    },
    revert() {
      this.fileList = [];
      this.$http.get("http://127.0.0.1:5000/revert").then(this.getData);
      this.active = 3;
      this.cur_icon = "el-icon-mouse";
    },
    handleRemove(file, fileList) {
      console.log(file, fileList);
    },
    handlePictureCardPreview(file) {
      this.dialogImageUrl = file.url;
      this.dialogVisible = true;
    },
    changeModel() {
      this.fileList = [];

      this.changeMd = !this.changeMd;

      this.active = 0;

      this.cur_icon = "el-icon-mouse";
    }
  },
};
</script>

<style scoped>
.funscontainer-uw {
  width: 100%;
  position: relative;
  height: 568px;
  transition: all 1s;
  display: flex;
}
.funsSteps {
  position: absolute;
  left: -70px;
  top: 30px;
  height: 80%;
}
.left {
  position: relative;
  width: 70%;
  height: 100%;
}

.funssuccess {
  position: relative;
  left: 2%;
  text-align: left;
  height: 20%;
  margin: 0 auto;
}
.funssuccessContent {
  position: relative;
  left: 50px;
  top: 10px;

  color: rgb(48, 46, 46);
  font-size: 15px;
}
.funssuccessContent h2 {
  color: rgb(255, 255, 255);
  font-size: 25px;
  font-weight: bold;
  letter-spacing: 3px;
  text-shadow: 5px 2px 2px rgb(0, 0, 0);
}
.unwmBox {
  position: relative;
  left: 2%;
  height: 60%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 5px;
  transition: all 2s;
}

.btnBox {
  position: relative;
  left: 2%;
  width: 100%;
  height: 20%;
  display: flex;
  justify-content: space-around;
  align-items: center;
}

.right {
  position: relative;
  width: 30%;
  height: 100%;
}
.changeBtn{
  position: relative;
  height: 10%;
  background: rgb(185, 164, 164);
}
.changeBtn h2 {
  color: rgb(255, 255, 255);
  font-size: 25px;
  font-weight: bold;
  letter-spacing: 1px;
  text-shadow: 1px 1px 1px rgb(0, 0, 0);
}
.rightHeader {
  width: 90%;
  position: absolute;
  top: 10px;
  left: 5%;
}
.unwatermarkBtn{
  position: absolute;
  bottom: 5%;
  left: 20%;
  width: 60%;
}

.knobs,
.layer {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
}

.button {
  position: absolute;
  right: 0;
  bottom: -42px;
  width: 74px;
  height: 36px;
  overflow: hidden;
}

.button.r,
.button.r .layer {
  border-radius: 100px;
}

.button.b2 {
  border-radius: 2px;
}
.checkbox {
  position: relative;
  width: 100%;
  height: 100%;
  padding: 0;
  margin: 0;
  opacity: 0;
  cursor: pointer;
  z-index: 3;
}
.knobs {
  z-index: 2;
}
.layer {
  width: 100%;
  background-color: #ebf7fc;
  transition: 0.3s ease all;
  z-index: 1;
}
/* Button 6 */
#button-6 {
  overflow: visible;
}

#button-6 .knobs:before {
  content: "TW";
  position: absolute;
  top: 4px;
  left: 4px;
  width: 28px;
  height: 28px;
  color: #fff;
  font-size: 8px;
  font-weight: bold;
  text-align: center;
  line-height: 1;
  padding: 9px 4px;
  background-color: #03a9f4;
  border-radius: 50%;
}

#button-6 .layer,
#button-6 .knobs,
#button-6 .knobs:before {
  transform: rotateZ(0);
  transition: 0.4s cubic-bezier(0.18, 0.89, 0.35, 1.15) all;
}

#button-6 .checkbox:checked + .knobs {
  transform: rotateZ(-180deg);
}

#button-6 .checkbox:checked + .knobs:before {
  content: "IW";
  background-color: #f44336;
  transform: rotateZ(180deg);
}

#button-6 .checkbox:checked ~ .layer {
  background-color: #fcebeb;
  transform: rotateZ(180deg);
}

.loader-inner {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    margin: auto;   /* 水平垂直居中*/;
    width: 100px;
    height: 100px;
}
.loader-line-wrap {
    animation: 
		spin 2000ms cubic-bezier(.175, .885, .32, 1.275) infinite;
    animation-play-state:paused; 
    box-sizing: border-box;
    height: 50px;
    left: 0;
    overflow: hidden;
    position: absolute;
    top: 0;
    transform-origin: 50% 100%;
    width: 100px;
}
.loader-line {
    border: 4px solid transparent;
    border-radius: 100%;
    box-sizing: border-box;
    height: 100px;
    left: 0;
    margin: 0 auto;
    position: absolute;
    right: 0;
    top: 0;
    width: 100px;
}
.loader-line-wrap:nth-child(1) { animation-delay: -50ms; }
.loader-line-wrap:nth-child(2) { animation-delay: -100ms; }
.loader-line-wrap:nth-child(3) { animation-delay: -150ms; }
.loader-line-wrap:nth-child(4) { animation-delay: -200ms; }
.loader-line-wrap:nth-child(5) { animation-delay: -250ms; }

.loader-line-wrap:nth-child(1) .loader-line {
    border-color: hsl(226, 100%, 64%);
    height: 90px;
    width: 90px;
    top: 7px;
}
.loader-line-wrap:nth-child(2) .loader-line {
    border-color: hsl(0, 0%, 100%);
    height: 76px;
    width: 76px;
    top: 14px;
}
.loader-line-wrap:nth-child(3) .loader-line {
    border-color: hsl(214, 74%, 59%);
    height: 62px;
    width: 62px;
    top: 21px;
}
.loader-line-wrap:nth-child(4) .loader-line {
    border-color: hsl(0, 0%, 100%);
    height: 48px;
    width: 48px;
    top: 28px;
}
.loader-line-wrap:nth-child(5) .loader-line {
    border-color: hsl(226, 100%, 64%);
    height: 34px;
    width: 34px;
    top: 35px;
}

@keyframes spin {
    0%, 15% {
		transform: rotate(0);
	}
	100% {
		transform: rotate(360deg);
	}
}
</style>
