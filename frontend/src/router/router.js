import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '@/components/log/login.vue'
import Register from '@/components/log/register.vue'
import Reset from '@/components/log/account_reset.vue'
import MainPage from '@/components/pages/mainpage.vue'
Vue.use(VueRouter)

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/account_reset', component: Reset },
  { path: '/mainpage', component: MainPage },
]
const router = new VueRouter({
  routes
})
export default router
