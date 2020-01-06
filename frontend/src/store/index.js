import Vue from 'vue'
import Vuex from 'vuex'
import { register, login, getUserInfo } from '@/api/auth'
import { getProjectInfo } from '@/api/project'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    token: localStorage.getItem('token') || null,
    user: null,
    collapse: localStorage.getItem('collapse-aside') === 'true'
  },
  mutations: {
    setUser (state, payload) {
      state.user = payload.user
    },
    setToken (state, payload) {
      state.token = payload.token
      localStorage.setItem('token', payload.token)
    },
    removeToken (state) {
      state.token = null
      state.user = null
      localStorage.removeItem('token')
    },
    setActiveProject(state, project) {
      state.user.active_project = project
    },
    setCollapse (state, collapseState) {
      state.collapse = collapseState
      localStorage.setItem('collapse-aside', collapseState)
    }
  },
  actions: {
    getUserInfo (context) {
      return new Promise((resolve, reject) => {
        getUserInfo(context.state.token)
          .then(res => {
            let userData = {
              'user': res.data.user
            }
            context.commit('setUser', userData)
            resolve(userData)
          })
          .catch(err => {
            reject(err)
          })
      })
    },
    login (context, userData) {
      return new Promise((resolve, reject) => {
        login(userData)
          .then(res => {
            if (res.data.error_code === 0) {
              context.commit('setToken', { 'token': res.data.token })
              resolve(res.data)
            } else {
              reject(res.data.msg)
            }
          })
          .catch(error => {
            reject(error)
          })
      })
    },
    register (context, userData) {
      return new Promise((resolve, reject) => {
        register(userData)
          .then(res => {
            if (res.data.error_code === 0) {
              context.dispatch('login', userData)
                .then(() => {
                  return context.dispatch('getUserInfo')
                })
                .then(() => {
                  resolve(res.data)
                })
            } else {
              reject(res.data.msg)
            }
          })
          .catch(error => {
            reject(error)
          })
      })
    },
    logout (context) {
      return new Promise((resolve, reject) => {
        context.commit('removeToken')
        resolve()
      })
    },
    setActiveProject (context, projectName) {
      getProjectInfo({project_name: projectName}).then(res => {
        if (res.data.project.masters.includes(context.state.user.username)) {
          context.commit('setActiveProject', {
            id: res.data.project.id,
            name: res.data.project.name,
            is_master: true
          })
        } else if (res.data.project.users.includes(context.state.user.username)) {
          context.commit('setActiveProject', {
            id: res.data.project.id,
            name: res.data.project.name,
            is_master: false
          })
        }
      })
    },
    switchCollapse (context) {
      if (context.state.collapse) {
        context.commit('setCollapse', false)
      } else {
        context.commit('setCollapse', true)
      }
    }
  },
  modules: {
  }
})
