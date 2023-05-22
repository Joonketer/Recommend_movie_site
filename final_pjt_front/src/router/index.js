import Vue from 'vue'
import VueRouter from 'vue-router'
import ArticleView from '@/views/ArticleView'
import CreateView from '@/views/CreateView'
import DetailView from '@/views/DetailView'
import DetailSearchView from '@/views/DetailSearchView'
import SignUpView from '@/views/SignUpView'
import LogInView from '@/views/LogInView'
import RecommendView from '@/views/RecommendView'


Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'ArticleView',
    component: ArticleView
  },

  {
    path: '/recommend',
    name: 'RecommendView',
    component: RecommendView
  },

  {
    path: '/create',
    name: 'CreateView',
    component: CreateView
  },

  {
    path: '/signup',
    name: 'SignUpView',
    component: SignUpView
  },

  {
    path: '/login',
    name: 'LogInView',
    component: LogInView
  },

  {
    path: '/:id',
    name: 'DetailView',
    component: DetailView,
  },

  {
    path: '/search/:id',
    name: 'DetailSearchView',
    component: DetailSearchView,
  },

]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
