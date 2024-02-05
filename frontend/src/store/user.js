import { defineStore } from 'pinia'
import { session, login, register, logout, updateProfile, getProfile } from '@/services/api.js'

export const useUserStore = defineStore('user', {
  state: () => ({
    csrf: null,
    userId: null,
    isAuthenticated: false,
    newRegistered: false,
    profileData: null
  }),
  getters: {
    getCSRF: (state) => state.csrf,
    getUserIsAuth: (state) => state.isAuthenticated,
    getUserNewRegistered: (state) => state.newRegistered,
    getUserId: (state) => state.userId,
    getProfileData: (state) => state.profileData
  },
  actions: {
    setCSRF(csrf) {
      this.csrf = csrf
    },
    setUserId(userId) {
      this.userId = userId
    },
    setUserIsAuth(isAuthenticated) {
      this.isAuthenticated = isAuthenticated
    },
    setNewRegistered(newRegistered) {
      this.newRegistered = newRegistered
    },
    setProfileData(profileData) {
      this.profileData = profileData
    },
    async userIsAuthenticated() {
      try {
        const { status, data, headers } = await session()
        if (status === 200) {
          this.setUserIsAuth(data['is_authenticated'])
          if (data['is_authenticated']) {
            this.setUserId(data['user_id'])
            this.setCSRF(headers['x-csrftoken'])
          }
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
    },
    async logoutUser() {
      try {
        const { status } = await logout()
        if (status === 200) {
          this.setUserIsAuth(false)
          this.setUserId(null)
          return {
            success: true
          }
        }
      } catch (error) {
        return {
          success: false
        }
      }
      return {
        success: false
      }
    },
    async getProfile(id) {
      if (id === undefined) {
        id = this.getUserId
      }
      try {
        const { status, data } = await getProfile(id)
        if (status === 200) {
          this.setProfileData(data)
          return {
            success: true,
            data: data
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
    async updateProfile({ id, first_name, last_name, birth_date, gender }) {
      if (id === undefined) {
        id = this.getUserId
      }
      try {
        const { status, data } = await updateProfile(
          {
            id,
            first_name,
            last_name,
            birth_date,
            gender
          },
          this.getCSRF
        )
        if (status === 200) {
          this.setProfileData(data)
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
