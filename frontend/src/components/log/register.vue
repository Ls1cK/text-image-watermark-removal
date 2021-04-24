<template>
  <div id="register_container">
    <div class="register_card">
      <div class="register_img"></div>
      <div class="register_form_container">
        <div class="register_form_box">
          <h1>注册</h1>
          <el-form
            :model="registerForm"
            :rules="loginFormRules"
            class="form_container"
          >
            <el-form-item class="register_form" prop="account">
              <el-input
                type="text"
                v-model="registerForm.account"
                placeholder="输入您要注册的邮箱账户..."
                suffix-icon="el-icon-user"
              ></el-input>
            </el-form-item>
            <el-form-item class="register_form" prop="password">
              <el-input
                type="password"
                v-model="registerForm.password"
                placeholder="输入密码..."
                show-password
                suffix-icon="el-icon-lock"
              ></el-input>
            </el-form-item>
            <el-form-item class="register_form" prop="ver_code">
              <el-input
                type="text"
                v-model="registerForm.ver_code"
                placeholder="输入邮箱验证码..."
                suffix-icon="el-icon-d-arrow-right"
              ></el-input>
            </el-form-item>
            <el-form-item class="sendVCode">
              <el-button size="mini" :plain="true" @click="sendVCode"
                >发送验证码...</el-button
              >
            </el-form-item>
          </el-form>
          <el-button round @click="goLogin" class="register_btn">
            完成注册
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "register",
  data() {
    return {
      registerForm: {
        account: "",
        password: "",
        ver_code: "",
      },
      loginFormRules: {
        account: [
          {
            required: true,
            message: "邮箱地址不能为空",
            trigger: "blur",
          },
          {
            pattern: /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/,
            message: "请输入正确的邮箱地址格式",
            trigger: "blur",
          },
        ],
        password: [
          {
            required: true,
            message: "密码不能为空",
            trigger: "blur",
          },
          {
            min: 6,
            max: 25,
            message: "请输入6以上字符密码",
            trigger: "blur",
          },
        ],
        ver_code: [
          {
            required: true,
            message: "验证码不能为空",
            trigger: "blur",
          },
          {
            min: 6,
            max: 6,
            message: "请输入6位字符验证码",
            trigger: "blur",
          },
        ],
      },
    };
  },
  methods: {
    sendVCode() {
      const loading = this.$loading({
        lock: true,
        text: "Sending",
        spinner: "el-icon-loading",
        background: "rgba(255, 255, 255, 0.7)",
        target: document.querySelector(".sendVCode"),
      });
      let that = this;
      that.$http
        .post("http://127.0.0.1:5000/ver_code", {
          username: that.registerForm.account,
        })
        .then(function(response) {
          if (parseInt(response.data.code) === 200) {
            loading.close();
            that.$message("验证码已发送至您邮箱，请注意查收~");
            sessionStorage.setItem("captcha", response.data.captcha);
          } else {
            loading.close();
            that.$message("验证码发送失败");
          }
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    goLogin() {
      const loading = this.$loading({
        lock: true,
        text: "注册中...",
        spinner: "el-icon-loading",
        background: "rgba(255, 255, 255, 0.7)",
        target: document.querySelector(".register_btn"),
      });
      let that = this;
      let cur_captcha = sessionStorage.getItem("captcha");
      if (cur_captcha === that.registerForm.ver_code) {
        that.$http
          .post("http://127.0.0.1:5000/register", {
            username: that.registerForm.account,
            password: that.registerForm.password,
          })
          .then(function(response) {
            if (parseInt(response.data.code) === 200) {
              loading.close();
              that.$router.push({ path: "/login" });
              that.$notify({
                title: "注册成功!",
                message: "欢迎~",
                type: "success",
              });
            }
          })
          .catch(function(error) {
            console.log(error);
          });
      } else {
        loading.close();
        that.$notify({
          title: "注册失败!",
          message: "请检查验证码是否正确~",
          type: "warning",
        });
      }
    },
  },
};
</script>

<style scoped>
#register_container {
  /* 设置背景渐变 */
  background-image: linear-gradient(to left, #a7c5eb, #4a94e9);
  display: flex;
  justify-content: center;
  width: 100vw;
  height: 100vh;
}
.register_card {
  position: relative;
  top: 100px;
  width: 1100px;
  height: 550px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.8);
  display: flex;
}
.register_img {
  width: 800px;
  height: 550px;
  background-image: url("../../assets/img/202012251518376191.jpg");
  /* 让图片适应大小 */
  background-size: cover;
}
.register_form_container {
  width: 300px;
  height: 550px;
  background-color: white;
  display: flex;
  justify-content: center;
  align-items: center;
}
.register_form_box {
  width: 250px;
  height: 500px;
}
.form_container {
  margin: 40px auto;
}
.register_form_box h1 {
  color: #330066;
}
.register_form {
  width: 230px;
  margin: 20px 0;
  padding: 10px;
  border-top: 3px solid rgb(80, 80, 170);
}
.sendVCode {
  float: right;
}
.register_btn {
  position: absolute;
  margin: 20px;
  bottom: 40px;
  display: block;
  width: 200px;
  height: 60px;
  font-size: 24px;
  color: #330066;
  text-decoration: none;
  text-align: center;
  /* line-height: 60px; 改用了el-button*/
  /* 文字的行高和容器的高度相同,设置文字垂直居中 */
  background-image: linear-gradient(to left, #a7c5eb, #6c9dd4);
  border: 0;
}
</style>
