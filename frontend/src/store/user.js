import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    csrf: null,
    userId: null,
    isAuthenticated: false,
    newRegistered: false
  }),
  getters: {
    userIsAuth: (state) => state.isAuthenticated,
    userNewRegistered: (state) => state.newRegistered
  },
  actions: {
    setUserIsAuth(isAuthenticated) {
      this.isAuthenticated = isAuthenticated
    },
    setNewRegistered(newRegistered) {
      this.newRegistered = newRegistered
    }
  }
})
