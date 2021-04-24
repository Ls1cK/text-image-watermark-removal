<template>
  <div id="reset_container">
    <div class="reset_card">
      <div class="reset_img"></div>
      <div class="reset_form_container">
        <div class="reset_form_box">
          <h1>密码重置</h1>
          <el-form
            :model="resetForm"
            :rules="loginFormRules"
            class="form_container"
          >
            <el-form-item class="reset_form" prop="account">
              <el-input
                type="text"
                v-model="resetForm.account"
                placeholder="输入您注册的邮箱账户..."
                suffix-icon="el-icon-user"
              ></el-input>
            </el-form-item>
            <el-form-item class="reset_form" prop="ver_code">
              <el-input
                type="text"
                v-model="resetForm.ver_code"
                placeholder="输入邮箱验证码..."
                suffix-icon="el-icon-d-arrow-right"
              ></el-input>
            </el-form-item>
            <el-form-item class="reset_form" prop="password">
              <el-input
                type="password"
                v-model="resetForm.password"
                placeholder="输入新密码..."
                show-password
                suffix-icon="el-icon-lock"
              ></el-input>
            </el-form-item>
            <el-form-item class="sendVCode">
              <el-button size="mini" :plain="true" @click="sendVCode"
                >发送验证码...</el-button
              >
            </el-form-item>
          </el-form>
          <el-button round class="reset_btn" @click="goLogin">
            找回密码
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "account_reset",
  data() {
    return {
      resetForm: {
        ver_code: "",
        account: "s1ckgo@126.com",
        password: "",
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
          username: that.resetForm.account,
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
        text: "正在找回密码...",
        spinner: "el-icon-loading",
        background: "rgba(255, 255, 255, 0.7)",
        target: document.querySelector(".reset_btn"),
      });
      let that = this;

      let cur_captcha = sessionStorage.getItem("captcha");
      if (cur_captcha === that.resetForm.ver_code) {
        that.$http
          .post("http://127.0.0.1:5000/reset_account", {
            username: that.resetForm.account,
            password: that.resetForm.password,
          })
          .then(function(response) {
            console.log(response.data);
            if (parseInt(response.data.code) === 200) {
              setTimeout(() => {
                loading.close();
                that.$router.push({ path: "/login" });
                that.$notify({
                  title: "密码找回成功!",
                  message: "欢迎~",
                  type: "success",
                });
              }, 500);
            }
          })
          .catch(function(error) {
            console.log(error);
          });
      }else{
      loading.close()
      that.$notify({
        title: '密码找回失败!',
        message: '请检查验证码是否~',
        type: 'warning'
        })
      }
    },
  },
};
</script>

<style scoped>
#reset_container {
  /* 设置背景渐变 */
  background-image: linear-gradient(to left, #a7c5eb, #4a94e9);
  display: flex;
  justify-content: center;
  width: 100vw;
  height: 100vh;
}
.reset_card {
  position: relative;
  top: 100px;
  width: 1100px;
  height: 550px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.8);
  display: flex;
}
.reset_img {
  width: 800px;
  height: 550px;
  background-image: url("../../assets/img/202012251522001756.jpg");
  /* 让图片适应大小 */
  background-size: cover;
}
.reset_form_container {
  width: 300px;
  height: 550px;
  background-color: white;
  display: flex;
  justify-content: center;
  align-items: center;
}
.reset_form_box {
  width: 250px;
  height: 500px;
}
.form_container {
  margin: 40px auto;
}
.reset_form_box h1 {
  color: #330066;
}
.reset_form {
  width: 230px;
  margin: 20px 0;
  padding: 10px;
  border-top: 3px solid rgb(80, 80, 170);
}
.sendVCode {
  float: right;
}
.reset_btn {
  position: absolute;
  margin: 20px;
  bottom: 40px;
  display: block;
  width: 200px;
  height: 60px;
  font-size: 24px;
  color: #330066;
  text-decoration: none;
  /* line-height: 60px; 改用了el-button*/
  text-align: center;
  /* 文字的行高和容器的高度相同,设置文字垂直居中 */
  background-image: linear-gradient(to left, #a7c5eb, #4a94e9);
  border: 0;
}
</style>
