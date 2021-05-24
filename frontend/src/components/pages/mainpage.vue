<template>
  <div class="mainBody">
    <div class="back2top">
      <!-- Element ui 返回顶部按钮 -->
      <el-backtop class="top"></el-backtop>
      <!-- 精灵 -->
      <div class="ghost">
        <div class="asa-g-e"></div>
        <div class="asa-g-d"></div>
        <div class="asa-p-e"></div>
        <div class="asa-p-d"></div>
        <div class="corpo"></div>
      </div>
    </div>
    <header class="l-head">
      <div class="container">
        <div class="row">
          <div class="col-md-12">
            <nav class="navi navbar" role="navigation">
              <a href="#/login" class="logo">Pat imagEs</a>
              <ul class="menu nav nav-pills navbar-right">
                <li class="menu__item is-itemHov" @click="goUp">主页</li>
                <li class="menu__item is-itemHov" @click="goAdd">添加水印</li>
                <li class="menu__item is-itemHov" @click="goUnwm">水印去除</li>
                <li class="menu__item is-itemHov" @click="goComp">图像质量比较</li>
                <li class="menu__item is-itemHov" @click="logout" v-loading.fullscreen.lock="fullscreenLoading">注销</li>
              </ul>
              <div class="avatarBox">
                <el-tooltip class="item" effect="light" :content="muser" placement="bottom-end">
                  <el-avatar :size="40" :src="circleUrl"></el-avatar>
                </el-tooltip>
              </div>
            </nav>
          </div>
        </div>
      </div>
    </header>
    <main class="l-main">
      <div class="container section-1">
        <div class="row">
          <div class="main-msg jumbotron">
            <div>
              <h3>基于深度学习文本图像水印去除算法仿真系统</h3>
            </div>
            <div class="imgEmp" style="margin:40px 0;">
              <img src="../../assets/img/563.png" alt="clean" />
              <div class="el-icon-right arrow"></div>
              <img src="../../assets/img/563w.png" alt="watermarked" />
              <div class="el-icon-right arrow"></div>
              <img src="../../assets/img/563c.png" alt="cleaned" />
            </div>
            <div>
              <a
                class="btn main-msg__btn is-itemHov"
                href="https://github.com/Ls1cK/PatImages-TextImageWatermarkRemoval-"
                role="button"
                target="_blank"
                >在GitHub上查看</a
              >
              <a
                class="btn main-msg__btn is-itemHov"
                @click="goAdd"
                role="button"
                >开始探索</a
              >
            </div>
          </div>
        </div>
      </div>
    </main>
    <section class="funs-contianer">
      <section class="funs">
        <div class="container section-2">
          <div class="row">
            <addwatermark id="addWatermark" :key="awKey"></addwatermark>
          </div>
          <div class="resetImg">
               <el-button @click="resetAddImg" type="success" plain >移除现有图片</el-button>
          </div>
        </div>
      </section>
      <section class="funs">
        <div class="container section-3">
          <div class="row">
            <unwatermark id="unWatermark"></unwatermark>
          </div>
        </div>
      </section>
      <section class="funs">
        <div class="container section-4">
          <div class="row">
            <comp id="comp"></comp>
          </div>
        </div>
      </section>
    </section>
  </div>
</template>

<script>
import addwatermark from "./addwatermark.vue";
import unwatermark from "./unwatermark.vue";
import comp from "./comp.vue";
export default {
  name: "mainpage",
  data() {
    return {
      muser: "色波",
      fullscreenLoading: false,
      awKey:1,
      circleUrl: "http://localhost:5000/static/file/user/cur_user.png",
    };
  },
  components: {
    addwatermark,
    unwatermark,
    comp,
  },
  methods: {
    logout() {
      this.fullscreenLoading = true;
      setTimeout(() => {
        this.fullscreenLoading = false;
        this.$router.push({ path: "/login" });
        this.$notify({
          title: "注销成功!",
          message: "欢迎下次再来~",
          type: "success",
        });
      }, 500);
    },
    goUp() {
      document
        .querySelector(".back2top")
        .scrollIntoView({ block: "start", behavior: "smooth" });
    },
    goAdd() {
      document
        .querySelector(".section-2")
        .scrollIntoView({ block: "center", behavior: "smooth" });
    },
    goUnwm() {
      document
        .querySelector(".section-3")
        .scrollIntoView({ block: "center", behavior: "smooth" });
    },
    goComp() {
      document
        .querySelector(".section-4")
        .scrollIntoView({ block: "center", behavior: "smooth" });
    },
    resetAddImg(){
      ++this.awKey;
    }
  },
  //页面加载钩子函数
  mounted() {
    //获取当前登录用户Token
    if (sessionStorage.getItem("token")) {
      this.muser = sessionStorage.getItem("token");
    }
    // Header卷动方法
    window.addEventListener("scroll", function() {
      var header = document.querySelector("header"),
        nav = document.querySelector(".menu"),
        scrolling = window.scrollY,
        cutOff = 10;
      if (cutOff < scrolling) {
        header.classList.add("is-menuSmaller");
        nav.style.backgroundColor = "transparent";
      } else {
        header.classList.remove("is-menuSmaller");
        nav.style.backgroundColor = "rgba(225, 225, 225, .6)";
      }
    });
  },
};
</script>
<style scoped>
/* Base Styles*/
*,
*:before,
*:after {
  box-sizing: border-box;
}

a:link {
  text-decoration: none;
}
a:visited {
  text-decoration: none;
}
a:hover {
  color: white;
}
a:active {
  text-decoration: none;
}
.mainBody {
  width: 100%;
  height: auto;
  background-repeat: repeat;
  background-size: unset;
}
/* Layout Styles*/
.l-head {
  position: fixed;
  padding-top: 20px;
  width: 100%;
  height: 100px;
  transition: all 1s;
  color: #fff;

  z-index: 3;
}

.l-main {
  width: 100%;
  background: url("../../assets/img/mainbg.jpg");
  background-repeat: no-repeat;
  background-size: cover;
}
.funs-contianer {
  width: 100%;
  background: url("../../assets/img/background.png");
  background-repeat: repeat;
}
.navbar {
  padding: 0 1rem;
}
.avatarBox{
  position:absolute;
  right: -40px;
}

/* Modules Styles*/
.logo {
  display: inline-block;
  margin-top: -15px;
  color: white;
  font-size: 35px;
  font-weight: bold;
  letter-spacing: 3px;
  text-shadow: 5px 2px 2px rgb(46, 45, 45);
}

.menu {
  padding: 0px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 5px;
  transition: all 2s;
}
.menu__item {
  margin: 0px;
  padding: 10px 20px;
  font-weight: bold;
  text-align: center;
  color: rgb(59, 59, 59);
  cursor: pointer;
}

/* 示例图片 */
.imgEmp {
  display: flex;
  justify-content: space-around;
}
.imgEmp img {
  max-width: 20%;
}

/* 主页 */
.section-1 {
  height: 768px;
  transition: all 2s;
}
.funs {
  height: 768px;
  display: flex;
  justify-content: center;
  align-items: center;
}
/* 功能模块 */
.section-2 {
  min-height: 568px;
  padding: 0px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 5px;
  transition: all 2s;
  position: relative;
}
.resetImg{
  position:absolute;
  right: 5%;
  bottom: 5%;
}
.section-3 {
  height: 568px;
  padding: 0px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 5px;
  transition: all 2s;
}

.section-4 {
  height: 568px;
  padding: 0px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 5px;
  transition: all 2s;
}

.main-msg {
  color: rgb(255, 255, 255);
  margin-top: 100px;
  text-align: center;
  background: rgba(225, 225, 225, 0.1);
}
.main-msg__btn {
  margin: 20px;
  padding: 10px 20px;
  color: inherit;
  font-weight: bold;
  text-align: center;
  background: rgba(123, 213, 255, 0.7);
}

/* State Styles*/
.is-menuSmaller {
  padding-top: 5px;
  height: 50px;
  background: rgba(151, 182, 197, 0.666);
}

.is-itemHov:hover {
  background: rgba(123, 213, 255, 0.3);
}

/*# sourceMappingURL=2.css.map */

/* 小精灵特效CSS */
.ghost {
  position: absolute;
  height: 300px;
  width: 500px;
  left: 10%;
  margin-left: -250px;
  top: 5%;
  animation: voo 6s ease-in-out infinite;
}

@keyframes voo {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-45px);
  }
}

.corpo {
  position: absolute;
  height: 90px;
  width: 90px;
  background: #d5edf5;
  border-radius: 50%;
  top: 100px;
  left: 50%;
  opacity: 0.98;
  margin-left: -45px;
  box-shadow: 0 0 20px #a08bf7, 0 0 40px rgba(187, 177, 230, 1),
    0 0 60px rgba(187, 177, 230, 0.6), 0 0 80px rgba(187, 177, 230, 0.9),
    0 0 30px 70px rgba(250, 232, 130, 0.1);
  animation: cresce 1s infinite;
}

@keyframes cresce {
  50% {
    transform: scale(1.04);
  }
}

.asa-g-e {
  position: absolute;
  height: 95px;
  width: 65px;
  background: #fff;
  border-radius: 100% 5px 100% 10%;
  top: 18px;
  left: 195px;
  transform: rotate(-45deg);
  opacity: 0.7;
  box-shadow: 0 0 40px rgba(187, 177, 230, 1);
  animation: asa 3s infinite;
  transform-origin: 50% 100%;
}

@keyframes asa {
  0% {
    transform: rotate(-65deg);
  }
  12.5% {
    transform: rotate(-90deg);
  }
  25% {
    transform: rotate(-65deg);
  }
  50% {
    transform: rotate(-90deg);
  }
  100% {
    transform: rotate(-65deg);
  }
}

.asa-g-d {
  position: absolute;
  height: 95px;
  width: 65px;
  background: #fff;
  border-radius: 5px 100% 10%;
  top: 18px;
  left: 238px;
  opacity: 0.7;
  box-shadow: 0 0 40px rgba(187, 177, 230, 1);
  animation: asa-e 3s infinite;
  transform-origin: 50% 100%;
}

@keyframes asa-e {
  0% {
    transform: rotate(65deg);
  }
  12.5% {
    transform: rotate(90deg);
  }
  25% {
    transform: rotate(65deg);
  }
  50% {
    transform: rotate(90deg);
  }
  100% {
    transform: rotate(65deg);
  }
}

.asa-p-e {
  position: absolute;
  height: 40px;
  width: 30px;
  background: #fff;
  border-radius: 180% 30% 130% 25%;
  top: 178px;
  left: 202px;
  opacity: 0.7;
  box-shadow: 0 0 40px rgba(187, 177, 230, 1);
  animation: asa-p-e 3s linear infinite;
  transform-origin: 100% 0%;
}

@keyframes asa-p-e {
  0% {
    transform: rotate(15deg);
  }
  12.5% {
    transform: rotate(30deg);
  }
  25% {
    transform: rotate(15deg);
  }
  50% {
    transform: rotate(30deg);
  }
  100% {
    transform: rotate(15deg);
  }
}

.asa-p-d {
  position: absolute;
  height: 40px;
  width: 30px;
  background: #fff;
  border-radius: 30% 180% 25% 130%;
  top: 174px;
  left: 266px;
  opacity: 0.7;
  box-shadow: 0 0 40px rgba(187, 177, 230, 1);
  animation: asa-p-d 3s linear infinite;
  transform-origin: 50% 0%;
}

@keyframes asa-p-d {
  0% {
    transform: rotate(-15deg);
  }
  12.5% {
    transform: rotate(-30deg);
  }
  25% {
    transform: rotate(-15deg);
  }
  50% {
    transform: rotate(-30deg);
  }
  100% {
    transform: rotate(-15deg);
  }
}
</style>
