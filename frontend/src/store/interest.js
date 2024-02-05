import { defineStore } from 'pinia'
import { getInterests } from '@/services/api.js'

export const useInterestsStore = defineStore('interests', {
  actions: {
    async getInterests() {
      try {
        const { status, data } = await getInterests()
        if (status === 200) {
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
    }
  }
})
