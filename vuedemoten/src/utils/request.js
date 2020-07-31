import axios from 'axios'
import { MessageBox, Message } from 'element-ui'
import store from '@/store'
import { getToken } from '@/utils/auth'

// create an axios instance
const service = axios.create({
  // baseURL: process.env.VUE_APP_BASE_API, // url = base url + request url
  baseURL: "/api", // url = base url + request url
  // baseURL: "", 
  // withCredentials: true, // send cookies when cross-domain requests
  timeout: 5000 // request timeout
})

// request interceptor
service.interceptors.request.use(
  config => {
    // console.log("config",config)
    // 解决ie缓存问题，ie缓存会导致数据显示错误
    if(config.method!=="get"){
      config.transformRequest=[function(data){
        if(typeof(data)==="object"){
          data.ran = encodeURIComponent(Math.random())
          return JSON.stringify(data)
        }else if(typeof(data)==="string"){
          const newdata = eval("("+data+")");
          newdata.ran = encodeURIComponent(Math.random())
          return JSON.stringify(newdata)
        }else{
          return data
        }
      }]
    }else{
      // console.log("get看",config.url)
      const neturl = config.url + "?ran=" + encodeURIComponent(Math.random())
      config.url = neturl
    }
    if (store.getters.token) {
      // let each request carry token
      // ['X-Token'] is a custom headers key
      // please modify it according to the actual situation
      config.headers['authorization'] = getToken()
    }
    return config
  },
  error => {
    // do something with request error
    console.log(error) // for debug
    return Promise.reject(error)
  }
)

// response interceptor
service.interceptors.response.use(
  /**
   * If you want to get http information such as headers or status
   * Please return  response => response
  */

  /**
   * Determine the request status by custom code
   * Here is just an example
   * You can also judge the status by HTTP Status Code
   */
  response => {
    // const res = response.data
    // console.log("response.data",response.data)
    const { data, status } = response
    const statusCode = ["200", "201", "202", "203", "204"]
    const result1 = statusCode.indexOf(status.toString())
    if (result1 === -1) {
      store.dispatch('user/resetToken').then(() => {
        location.reload()
      })
    }
    const result2 = statusCode.indexOf(data.code.toString())
    if (result2 === -1) {
      if (data.code.toString() === "401") {
        store.dispatch('user/resetToken').then(() => {
          location.reload()
        })
      }
    }
    return data
  },
  error => {
    console.log('err' + error) // for debug
    console.log('err' + error.response) // for debug
    console.log('err' + error.response.data) // for debug
    Message({
      message: error.message,
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export default service
