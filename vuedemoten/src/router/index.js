import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },


  // 404 page must be placed at the end !!!
  // { path: '*', redirect: '/404', hidden: true }
]


export const asyncRouters = [
   {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '系统首页', icon: 'dashboard' }
    }]
  },

  {
    path: '/system',
    component: Layout,
    redirect: '/system/peoples',
    name: 'System',
    meta: { title: '管理系统', icon: 'example' },
    children: [
      {
        path: 'menus',
        name: 'Menus',
        component: () => import('@/views/system/menus/index'),
        meta: { title: '菜单管理', icon: 'tree' }
      },
      {
        path: 'permissions',
        name: 'Permissions',
        component: () => import('@/views/system/permissions/index'),
        meta: { title: '权限管理', icon: 'form' }
      },
      {
        path: 'roles',
        name: 'Roles',
        component: () => import('@/views/system/roles/index'),
        meta: { title: '角色管理', icon: 'link' }
      },
      {
        path: 'peoples',
        name: 'Peoples',
        component: () => import('@/views/system/peoples/index'),
        meta: { title: '用户管理', icon: 'table' }
      },
    ]
  },

  {
    path: '/record',
    component: Layout,
    redirect: '/record/management',
    name: 'record',
    meta: { title: '记录系统', icon: 'example' },
    children: [
      {
        path: 'management',
        name: 'Management',
        component: () => import('@/views/record/management/index'),
        meta: { title: '记录管理', icon: 'tree' }
      },
      {
        path: 'process',
        name: 'Process',
        component: () => import('@/views/record/process/index'),
        meta: { title: '操作处理', icon: 'form' }
      },
      {
        path: 'displaystand',
        name: 'displaystand',
        component: () => import('@/views/record/displaystand/index'),
        meta: { title: '展示搜索', icon: 'link' }
      },
      {
        path: 'failsearch',
        name: 'failsearch',
        component: () => import('@/views/record/failsearch/index'),
        meta: { title: '失败搜索', icon: 'table' }
      },
    ]
  },

]


const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
