import { defineStore } from 'pinia'
import { session, login, register } from '@/services/api.js'

export const useUserStore = defineStore('user', {
  state: () => ({
    csrf: null,
    userId: null,
    isAuthenticated: false,
    newRegistered: false
  }),
  getters: {
    getUserIsAuth: (state) => state.isAuthenticated,
    getUserNewRegistered: (state) => state.newRegistered,
    getUserId: (state) => state.userId
  },
  actions: {
    setUserId(userId) {
      this.userId = userId
    },
    setUserIsAuth(isAuthenticated) {
      this.isAuthenticated = isAuthenticated
    },
    setNewRegistered(newRegistered) {
      this.newRegistered = newRegistered
    },
    async userIsAuthenticated() {
      try {
        const { status, data } = await session()
        if (status === 200) {
          this.setUserIsAuth(data['is_authenticated'])
          return data['is_authenticated']
        } else {
          return false
        }
      } catch (error) {
        return false
      }
    },
    async registerUser({ username, password, password2 }) {
      try {
        const { status } = await register({
          username,
          password,
          password2
        })
        if (status === 201) {
          this.setNewRegistered(true)
          return {
            success: true,
            errors: null
          }
        }
      } catch (error) {
        return {
          success: false,
          errors: error.response.data
        }
      }
      return {
        success: false,
        errors: ['Internal Server Error']
      }
    },
    async loginUser({ username, password }) {
      try {
        const { status, data } = await login({
          username,
          password
        })
        if (status === 200) {
          this.setUserIsAuth(true)
          this.setUserId(data['id'])
          return {
            success: true,
            errors: null
          }
        }
      } catch (error) {
        return {
          success: false,
          errors: error.response.data
        }
      }
      return {
        success: false,
        errors: ['Internal Server Error']
      }
    }
  }
})
