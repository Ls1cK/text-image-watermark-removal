<template>
  <div class="funscontainer-aw">
    <div class="left">
      <p><h2 >添加水印</h2><span style="color:black;">支持文本水印、图像水印（不可同时添加）。</span></p>
      <div id="loadimg">
        <div class="input-group">
          <span class="input-group-btn">
            <span class="btn btn-primary btn-file"
              >浏览...<input type="file" class="filebtn" id="target"
            /></span>
          </span>
          <input type="text" class="form-control" id="image-name" readonly placeholder="选择你需要添加水印的图片"/>
        </div>
        <div class="input-group">
          <span class="input-group-btn">
            <span
              id="watermark-button"
              type="button"
              class="btn btn-primary btn-file"
              disabled>浏览...<input type="file" id="watermarkImage" class="filebtn" disabled/>
            </span>
          </span>
          <input
            type="text"
            class="form-control"
            id="watermark-name"
            readonly placeholder="选择图片水印，在此上传..."/>
        </div>
      </div>
      <div class="input-group">
          <input id="watermarkText" class="form-control"  placeholder="选择文本水印，在此输入文本..."  disabled/>
      </div>
      <div class="textSize" >
         <span class="textSize">设置文本字体大小(默认64px)</span>
         <el-slider id="watermarkTextSize" v-model="textSize" :min="0" :max="128" :disabled="banSlider"></el-slider>
      </div>
      <div class="textSize" >
         <span class="textSize">设置文本字体粗度（默认50）</span>
         <el-slider id="watermarkTextWeight" v-model="textWeight" :min="0" :max="100" :disabled="banSlider"></el-slider>
      </div>
      <div id="setpos">
        <div class="inputgroup">
          <h3>添加的图像水印位置设置</h3>
          <div class="row" id="positions">
            <div class="radio">
              <label><input
                  checked
                  type="radio"
                  name="position"
                  value="lowerRight"
                  disabled
                />右下</label
              >
            </div>
            <div class="radio">
              <label
                ><input
                  type="radio"
                  name="position"
                  value="lowerLeft"
                  disabled
                />左下</label
              >
            </div>
            <div class="radio">
              <label
                ><input
                  type="radio"
                  name="position"
                  value="upperRight"
                  disabled
                />右上</label
              >
            </div>
            <div class="radio">
              <label
                ><input
                  type="radio"
                  name="position"
                  value="upperLeft"
                  disabled
                />左上</label
              >
            </div>
            <div class="radio">
              <label
                ><input
                  type="radio"
                  name="position"
                  value="center"
                  disabled
                />中间</label
              >
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="right">
      <h2>预览</h2>
      <div class="preview" id="preview" ></div>
    </div>
  </div>
</template>

<script>
import watermark from "watermarkjs"

export default {
  data() {
    return {
      textSize:64,
      textWeight:50,
      banSlider:true,
      changeMd:true,
      original:null
    }
  },
  methods: {
    formatTooltip(val) {
        return val / (0.78125);
    },
    enableFields(ids) {
    ids.forEach(function(id) {
      document.getElementById(id).removeAttribute('disabled');
    })
  },

  /**
   * Given a file input, set the value of the readonly text input associated with it
   */
    setText(input) {
    var group = input.parentNode.parentNode.parentNode;
    group.querySelector('.form-control').value = input.files[0].name;
  },

  /**
   * A listener that fires when the target image is selected
   */
setTarget(file) {
    this.enableFields(['watermark-button']);
    this.enableFields(['watermarkImage']);
    this.enableFields(['watermarkText']);
    
    Array.prototype.forEach.call(document.querySelectorAll('input[type=radio]'), function (radio) {
      radio.removeAttribute('disabled');
    });
    watermark([file])
      .image(function(target) { return target;  })
      .then(function (img) {
        document.getElementById('preview').appendChild(img);
      });
  },

  /**
   * A listener that fires when the watermark image has been selected
   */
   setWatermark(file) {
    var preview = document.getElementById('preview'),
        img = preview.querySelector('img'),
        position = document.querySelector('input[type=radio]:checked').value;
        
    if (! this.original) {
      this.original = img;
    }
    watermark([this.original, file])
      .image(watermark.image[position](1))
      .then(function(marked) {
        preview.replaceChild(marked, img);
      });

  },
  /**
   * A listener that fires when the Text watermark image has been selected
   */
   setTextWatermark(textWatermark,font_size,font_weight) {
    var preview = document.getElementById('preview'),
        img = preview.querySelector('img'),
        fontsetting = font_size +"px" + " Josefin Slab",
        position = document.querySelector('input[type=radio]:checked').value;

    if (! this.original) {
      this.original = img;
    }
    //upperRight,upperLeft需要手动设置高度：为了和左下右下一致，高度设置与字体大小一致
    // so we manually provide a y value of 48 here
    if(position==="upperRight" || position==="upperLeft"){
      watermark([this.original])
      .image(watermark.text[position](textWatermark, fontsetting , 'black', font_weight, 48))
      .then(function(marked) {
        preview.replaceChild(marked, img);
      });
    }else{
    watermark([this.original])
      .image(watermark.text[position](textWatermark, fontsetting , 'black', font_weight))
      .then(function(marked) {
        preview.replaceChild(marked, img);
      });
    }
  
  },

  /**
   * Check if the watermark has been selected
   */
   isWatermarkSelected() {
    var watermark = document.getElementById('watermark-name');
    return !!watermark.value;
  },

   /**
   * Check if the text watermark has been selected
   */
    isTextWatermarkSelected() {
      var watermark = document.getElementById('watermarkText');
      return !!watermark.value;
    }
  },
  mounted() {
  this.original = null;
    // 更新水印后图片监听器
  let that = this;
  document
      .querySelector(".funscontainer-aw")
      .addEventListener("change", function(e) {
        var input = e.target;
        if (input.type === "file" ) {
          that.setText(input);
          input.id === "target"
            ? that.setTarget(input.files[0])
            : that.setWatermark(input.files[0]);
        }
        if (input.type === "radio" && that.isWatermarkSelected()) {
          that.setWatermark(document.getElementById("watermarkImage").files[0]);
        }
        if (that.isTextWatermarkSelected()) {
          that.banSlider = false;
        }       
        if (input.type === "radio" && that.isTextWatermarkSelected()) {
          let weight_text = that.textWeight/100;
          that.setTextWatermark(document.getElementById("watermarkText").value,that.textSize,weight_text);
        }
      });
  },
};
</script>

<style scoped>
.funscontainer-aw {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: space-around;
  color: rgb(255, 255, 255);
}
.right,
.left {
  position: relative;
  height: 568px;
  text-align: left;
}
.right{
  text-align:center;
}
.left h4 {
  margin-top: 40px;
}

.preview {
  position: relative;
  top:30px;
  width: 600px;
  height: 400px;
}
.right h2{
  position: relative;
  top: 30px;
}
#loadimg {
  margin-top: 60px;
}
#setpos {
  color: rgb(255, 255, 255);
  border-radius: 6px;
  margin-top: 20px;
  text-align: center;
  border-radius: 5px;
}
#positions {
  display: flex;
  justify-content: space-around;
}
.textSize{
  margin-block-start: 20px;
}
.filebtn {
  position: absolute;
  top: 0;
  left: 0;
  width: 70px;
  height: 36px;
  opacity: 0;
  outline: none;
  cursor: pointer;
}
.input-group{
  margin-block-start: 10px;
}
.btn .btn-primary .btn-file {
  cursor: pointer;
}
.btn-primary {
  background: rgba(123, 213, 255, 0.7);
  border: 0;
}
.btn-primary[disabled]{
  background: rgba(123, 213, 255, 0.3);
  background-image: none;
}
.form-control {
  border: 1px solid #ccc;
  border-radius: 4px;
  height: 36px;
}
/* 莫名其妙只能在global.css（./assets/css)来生效 */
/* #preview > img {
  border: 10px solid #fff;
  box-shadow: 3px 6px 5px rgba(0, 0, 0, 0.3);
  max-width: 100%;
} */
.radio label {
  color: #fff;
}

.rightHeader {
  width: 260px;
  position: absolute;
  top: 10px;
  right: 10%;
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
  right: -94px;
  bottom: 12px;
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
</style>
