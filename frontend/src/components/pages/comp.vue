<template>
  <div class="funscontainer">
    <div class="compBox">
      <div class="compInfo">
      <p>
        <h3>PSNR-峰值信噪比</h3><b>一个衡量图像失真或是噪声水平的客观标准评价结果以dB（分贝）为单位表示，两个图像间，PSNR值越大，则越趋于无劣化，劣化程度较大时，PSNR值趋于0dB。</b>
        <br />
        <h3>SSIM结构相似性</h3><b>即亮度 (luminance)、对比度 (contrast) 和结构(structure)，SSIM取值范围[0,1]，值越大，表示图像失真越小。</b>
      </p>
      </div>
      <el-upload
      class="upload-revert"
      ref="upload"
      list-type="picture-card"
      action="http://127.0.0.1:5000/upload"
      multiple
      :limit="2"
      :on-remove="handleRemove"
      :on-preview="handlePictureCardPreview"
      :file-list="fileList"
      :on-exceed="overload"
      :auto-upload="false">
      <div>
        <i class="el-icon-plus"></i>
      </div>
    </el-upload>
    <el-dialog :visible.sync="dialogVisible">
      <img width="100%" :src="dialogImageUrl" alt="preview" />
    </el-dialog>
      <h2>[PSNR,SSIM] 结果如下：{{imgdata}}</h2>
     <div class="compbtn">
      <el-button type="success"  plain @click="submitUpload" icon="el-icon-upload2">上传到服务器</el-button>
      <el-button  type="success" plain @click="getData" icon="el-icon-magic-stick">图像质量数据</el-button>
      </div>
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
      imgdata:null,
      };
    },
    methods: {
    submitUpload() {
       //上传之前，先清除缓存
      this.$http.post("http://127.0.0.1:5000/clearFile");

      this.$refs.upload.submit();
      },
      handleRemove(file, fileList) {
        console.log(file, fileList);
      },
    handlePictureCardPreview(file) {
      this.dialogImageUrl = file.url;
      this.dialogVisible = true;
    },
      handlePreview(file) {
        console.log(file);
      },
      getData(){
        this.$http.get("http://127.0.0.1:5000/comp").then(response => (this.imgdata = response.data));
      },
      overload(){
        const h = this.$createElement;

        this.$notify({
          title: '关于图像对比',
          message: h('i', { style: 'color: teal'}, '超出上传限制。图像对比仅能上传2张图片')
        });
      }
    }
  }
</script>

<style scoped>
.funscontainer{
   margin: 0 auto;
}
.compBox {
  color: #fff;
  margin-left: 100px;
  margin-block-start: 30px;
  text-align:center;
}
.compInfo{
  text-align: left;
  width: 60%;
}
.compbtn{
  display: flex;
  justify-content: space-around;
  transition: all 1s;
}
</style>
