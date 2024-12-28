import axios from 'axios'
import { MessageBox, Message } from 'element-ui'
import store from '@/store'
import { getToken } from '@/utils/auth'

// create an axios instance
const service = axios.create({
  baseURL: process.env.NODE_ENV === 'production' 
    ? 'http://backend:8000'  // 使用容器名称
    : 'http://127.0.0.1:8000',
  timeout: 30000,  // 增加超时时间到 30 秒
  withCredentials: true  // 允许跨域请求携带凭证
})

// request interceptor
service.interceptors.request.use(
  config => {
    // do something before request is sent

    if (store.getters.token) {
      // let each request carry token
      // ['X-Token'] is a custom headers key
      // please modify it according to the actual situation
      config.headers['X-Token'] = getToken()
    }
    return config
  },
  error => {
    console.log(error)
    return Promise.reject(error)
  }
)


service.interceptors.response.use(

  response => {
 
    return response
  },
  error => {
    console.log('err' + error)
    Message({
      message: error.message,
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export default service
