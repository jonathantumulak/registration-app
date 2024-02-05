import { defineStore } from 'pinia'
import {
  session,
  login,
  register,
  logout,
  updateProfile,
  getProfile,
  updateJobPreference,
  getJobPreference,
  getUserInterests,
  updateUserInterests
} from '@/services/api.js'

export const useUserStore = defineStore('user', {
  state: () => ({
    csrf: null,
    userId: null,
    isAuthenticated: false,
    newRegistered: false,
    profileData: null,
    jobPreferenceData: null,
    userInterestsData: null,
    completedWelcome: false
  }),
  getters: {
    getCSRF: (state) => state.csrf,
    getUserIsAuth: (state) => state.isAuthenticated,
    getUserNewRegistered: (state) => state.newRegistered,
    getUserId: (state) => state.userId,
    getCompletedWelcome: (state) => state.completedSteps,
    getProfileData: (state) => state.profileData,
    getJobPreferenceData: (state) => state.jobPreferenceData,
    getUserInterestsData: (state) => state.userInterestsData,
    isProfileDataSubmitted: (state) => {
      if (state.profileData) {
        const { first_name, last_name, birth_date, gender } = state.profileData
        return !(first_name === '' || last_name === '' || birth_date === null || gender === null)
      }

      return false
    },
    isJobPreferenceDataSubmitted: (state) => {
      if (state.jobPreferenceData) {
        const { experience_level, expected_salary } = state.jobPreferenceData
        return !(experience_level === null && expected_salary === null)
      }

      return false
    },
    isUserInterestsDataSubmitted: (state) => {
      if (state.userInterestsData) {
        const { interests } = state.userInterestsData
        return !(interests === [])
      }

      return false
    }
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
    setCompletedWelcome(completedWelcome) {
      this.completedWelcome = completedWelcome
    },
    setProfileData(profileData) {
      this.profileData = profileData
    },
    setJobPreferenceData(jobPreferenceData) {
      this.jobPreferenceData = jobPreferenceData
    },
    setUserInterestsData(userInterestsData) {
      this.userInterestsData = userInterestsData
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
          this.setCompletedWelcome(data['completed_welcome'])
          this.setProfileData(data)
          return {
            success: true,
            completed_welcome: data['completed_welcome'],
            errors: null
          }
        }
      } catch (error) {
        let message = error.response.data
        if (error.response.status === 404) {
          message = ['User not found']
        }
        return {
          success: false,
          errors: message
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
          this.setCSRF(null)
          this.setUserIsAuth(false)
          this.setUserId(null)
          this.setNewRegistered(false)
          this.setCompletedWelcome(false)
          this.setProfileData(null)
          this.setUserInterestsData(null)
          this.setJobPreferenceData(null)
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
    },
    async getJobPreference(id) {
      if (id === undefined) {
        id = this.getUserId
      }
      try {
        const { status, data } = await getJobPreference(id)
        if (status === 200) {
          this.setJobPreferenceData(data)
          return {
            success: true,
            data: data
          }
        }
      } catch (error) {
        console.log(error)
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
    async updateJobPreference({ id, experience_level, expected_salary }) {
      if (id === undefined) {
        id = this.getUserId
      }
      try {
        const { status, data } = await updateJobPreference(
          {
            id,
            experience_level,
            expected_salary
          },
          this.getCSRF
        )
        if (status === 200) {
          this.setJobPreferenceData(data)
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
    async getUserInterests(id) {
      if (id === undefined) {
        id = this.getUserId
      }
      try {
        const { status, data } = await getUserInterests(id)
        if (status === 200) {
          this.setUserInterestsData(data['interests'])
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
    async updateUserInterests({ id, interests }) {
      if (id === undefined) {
        id = this.getUserId
      }
      try {
        const { status } = await updateUserInterests(
          {
            id,
            interests
          },
          this.getCSRF
        )
        if (status === 200) {
          this.setCompletedWelcome(true)
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
