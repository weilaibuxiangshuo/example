import { login, logout, getInfo } from '@/api/user'
import { getToken, setToken, removeToken } from '@/utils/auth'
import { resetRouter,constantRoutes,asyncRouters } from '@/router'
import Layout from '@/layout'
import path, { resolve } from 'path'

const getDefaultState = () => {
  return {
    token: getToken(),
    name: '',
    avatar: '',
    defrou:constantRoutes,
    allpath:'',
  }
}

const state = getDefaultState()

const mutations = {
  RESET_STATE: (state) => {
    Object.assign(state, getDefaultState())
  },
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_NAME: (state, name) => {
    state.name = name
  },
  SET_AVATAR: (state, avatar) => {
    state.avatar = avatar
  },
  SET_ROUTER:(state,newRou)=>{
    state.defrou = state.defrou.concat(newRou)
  },
  SET_ALLPATH:(state,allpath)=>{
    state.allpath = allpath
  },
}

// 深度拷贝
const deepobj = (data) => {
  const obj = data.constructor === Array ? [] : {}
  for (let n in data) {
    if (data[n].constructor === Array) {
      obj[n] = deepobj(data[n])
    } else {
      obj[n] = data[n]
    }
  }
  return obj
}

// 拼接路由
const menugenerate = (data, defaultpath = "/") => {
  const lis = []
  for (let n in data) {
    const newpath = path.join(defaultpath, data[n].path)
    let dic = {}
    if (data[n].level === 1) {
      if (data[n].path === "/dashboard") {
        dic = {
          path: "/",
          component: Layout,
          redirect: newpath,
          children: [
            {
              path: "/dashboard",
              component: resolve => require([`@/views${data[n].path}`], resolve),
              name: data[n].title,
              meta: { title: data[n].title, icon: data[n].icon, permission: data[n].role },
            }
          ]
        }
      } else {
        dic = {
          path: newpath,
          component: Layout,
          name: data[n].title,
          meta: { title: data[n].title, icon: data[n].icon, permission: data[n].role },
        }
        
        if (data[n].children && data[n].children.length > 0) {
          dic.redirect = path.join(newpath, data[n].children[0].path)
          dic.children = menugenerate(data[n].children, newpath)
        }
      }
    } else {
      dic = {
        path: newpath,
        component: resolve => require([`@/views${newpath}`], resolve),
        name: data[n].title,
        meta: { title: data[n].title, icon: data[n].icon, permission: data[n].role },
      }
      if (data[n].children && data[n].children > 0) {
        dic.redirect = path.join(newpath, data[n].children[0].path)
        dic.children = menugenerate(data[n].children, newpath)
      }
    }
    lis.push(dic)
  }
  return lis
}

// 获取所有路由路径
const allRoutePath = (data) =>{
  let routeObj = []
  for (let n in data) {
    const resObj = []
    if (!!data[n].children) {
      let temp  = allRoutePath(data[n].children)
      routeObj.push(...temp)
    }
    routeObj.push(data[n].path)
  }
  return routeObj
}


const actions = {
  // user login
  login({ commit }, userInfo) {
    const { username, password } = userInfo
    const sha256 = require('js-sha256').sha256
    return new Promise((resolve, reject) => {
      login({ username: username.trim(), password: sha256(password) }).then(response => {
        const { authorization } = response
        commit('SET_TOKEN', authorization)
        setToken(authorization)
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // get user info
  getInfo({ commit }) {
    return new Promise((resolve, reject) => {
      getInfo().then(response => {
        const { username, menudata } = response
        const deepres = deepobj(menudata)
        const rou = menugenerate(deepres)
        const allpath = allRoutePath(rou)
        commit('SET_NAME', username)
        commit('SET_ROUTER', rou)
        commit('SET_ALLPATH', allpath)
        resolve(rou)
      }).catch(error => {
        reject(error)
      })
    })
  },

  // user logout
  logout({ commit, state }) {
    return new Promise((resolve, reject) => {
      logout(state.token).then(() => {
        removeToken() // must remove  token  first
        resetRouter()
        commit('RESET_STATE')
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // remove token
  resetToken({ commit }) {
    return new Promise(resolve => {
      removeToken() // must remove  token  first
      commit('RESET_STATE')
      resolve()
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}

