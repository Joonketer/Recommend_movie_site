import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '@/views/HomeView'
import ArticleView from '@/views/ArticleView'
import CreateView from '@/views/CreateView'
import DetailView from '@/views/DetailView'
import DetailSearchView from '@/views/DetailSearchView'
import SignUpView from '@/views/SignUpView'
import LogInView from '@/views/LogInView'
import RecommendView from '@/views/RecommendView'
import SearchView from '@/views/SearchView'
import ProfileView from '@/views/ProfileView'
import BoxOfficeView from '@/views/BoxOfficeView'
import TagSearchView from '@/views/TagSearchView'
import CommunityView from '@/views/CommunityView'
import CommunityArticleDetailView from '@/views/CommunityArticleDetailView.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'HomeView',
    component: HomeView
  },

  {
    path: '/totalmovie',
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
    path: '/search/:id',
    name: 'DetailSearchView',
    component: DetailSearchView,
  },

  {
    path: '/search_detail/',
    name: 'SearchView',
    component: SearchView,
  },

  {
    path: '/boxoffice',
    name: 'BoxOfficeView',
    component: BoxOfficeView,
  },

  {
    path: '/tagsearch',
    name: 'TagSearchView',
    component: TagSearchView,
  },

  {
    path: '/proflie/me',
    name: 'ProfileView',
    component: ProfileView,
  },

  {
    path: '/community',
    name: 'CommunityView',
    component: CommunityView,
  },

  {
    path: '/community/boards/:id',
    name: 'CommunityArticleDetailView',
    component: CommunityArticleDetailView,
    props: true
  },

  {
    path: '/:id',
    name: 'DetailView',
    component: DetailView,
  },

]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
