<template>
  <div id="login_container">
    <div class="login_card">
      <div class="login_img"></div>
      <div class="login_form_container">
        <div class="login_form_box">
          <h1 readonly>登入</h1>
          <el-form
            ref="loginFormRef"
            :model="loginForm"
            :rules="loginFormRules"
            class="form_container"
          >
            <el-form-item class="login_form" prop="account">
              <el-input
                type="text"
                v-model="loginForm.account"
                placeholder="输入您注册的邮箱账户..."
                suffix-icon="el-icon-user"
              ></el-input>
            </el-form-item>
            <el-form-item class="login_form" prop="password">
              <el-input
                type="password"
                v-model="loginForm.password"
                placeholder="输入密码..."
                show-password
                suffix-icon="el-icon-lock"
              ></el-input>
            </el-form-item>
          </el-form>
          <div class="link_container">
            <el-button round size="small" @click="resetLoginForm" class="clear"
              >重置输入</el-button
            >
            <el-link href="#/register" class="go">没有账户?</el-link>
            <el-link href="#/account_reset" class="go">忘记密码?</el-link>
          </div>
          <el-button
            round
            class="login_btn"
            @click="loginToMainPage"
            v-loading.fullscreen.lock="fullscreenLoading"
            >登录</el-button
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "login",
  data() {
    return {
      loginForm: {
        account: "swjtusk@my.swjtu.edu.cn",
        password: "2017112388LQ",
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
      },
      fullscreenLoading: false,
    };
  },
  methods: {
    loginToMainPage() {
      this.$refs.loginFormRef.validate(async valid =>{
        console.log("表单验证:"+valid);
        let that = this;

        await that.$http.post('http://127.0.0.1:5000/login', {
          username: that.loginForm.account,
          password: that.loginForm.password
        }).then(function (response) {
          if(parseInt(response.data.code) === 400){
            //登录失败
            that.$notify({
            title: "账户密码验证失败",
            message: "请核实后重新登录。",
            type: 'warning'
            });
          }else if (parseInt(response.data.code) === 200){
            // 存token
            that.fullscreenLoading = true;
            sessionStorage.setItem('token', response.data.token);
            that.$notify({
            title: "账户密码验证成功!",
            message: "欢迎~",
            type: "success",
            });
            // 登录成功,跳转到index
            setTimeout(() => {
            that.fullscreenLoading = false;
            that.$router.push({ path: "/mainpage" });
          }, 600);
          }
        }).catch(function (error) {
            console.log(error)
        })
      });
    },
    resetLoginForm() {
      setTimeout(() => {
        this.$refs.loginFormRef.resetFields();
      }, 500);
      setTimeout(() => {
        this.$notify({
          title: "重置输入成功!",
          message: "请重新输入~",
          type: "success",
        });
      }, 600);
    },
  },
};
</script>

<style scoped>
#login_container {
  /* 设置背景渐变 */
  background-image: linear-gradient(to left, #a7c5eb, #4a94e9);
  display: flex;
  justify-content: center;
  width: 100vw;
  height: 100vh;
}
.login_card {
  position: relative;
  top: 100px;
  width: 1100px;
  height: 550px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.8);
  display: flex;
}
.login_img {
  width: 800px;
  height: 550px;
  background-image: url("../../assets/img/202012251526258728.jpg");
  /* 让图片适应大小 */
  background-size: cover;
}
.login_form_container {
  width: 300px;
  height: 550px;
  background-color: white;
  display: flex;
  justify-content: center;
  align-items: center;
}
.login_form_box {
  width: 250px;
  height: 500px;
}
.login_form_box h1 {
  color: #330066;
}
.form_container {
  margin: 30px auto;
}
.login_form {
  width: 230px;
  margin: 20px 0;
  padding: 10px;
  border-top: 3px solid rgb(80, 80, 170);
}
.link_container {
  display: grid;
  justify-content: flex-end;
}
.link_container a{
  text-decoration: none;
}
.go {
  margin: 10px 0;
  color: rgb(80, 80, 170);
}
@font-face {
    font-family: PingFang-Light;
    src: url("../../assets/fonts/PingFang-Light.ttf");
}
.clear {
  margin: 10px;
  color: #330066;
  background-image: linear-gradient(to left, #a7c5eb, #6c9dd4);
  width: 86px;
  text-align: center;
  border-radius: 10px;
  font-weight: 800;
  font-size: 14px;
  font-family: PingFang-Light;
}
.login_btn {
  position: absolute;
  margin: 20px;
  bottom: 40px;
  display: block;
  width: 200px;
  height: 60px;
  font-size: 24px;
  color: #330066;
  /* line-height: 60px; 改用了el-button*/
  text-align: center;
  /* 文字的行高和容器的高度相同,设置文字垂直居中 */
  background-image: linear-gradient(to left, #a7c5eb, #4a94e9);
  cursor: pointer;
  border: 0;
}
</style>
