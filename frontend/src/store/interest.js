import { defineStore } from 'pinia'
import { getAllInterests } from '@/services/api.js'

export const useInterestsStore = defineStore('interests', {
  actions: {
    async getAllInterests() {
      try {
        const { status, data } = await getAllInterests()
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
