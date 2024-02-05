import axios from 'axios'

const api = axios.create({
  baseURL: `${import.meta.env.VITE_API_ENDPOINT}users`
})

export const getSession = async () => {
  return api.get('/session', {
    method: 'GET'
  })
}

export const login = async ({ username, password }) => {
  return api.post('/login', { username, password })
}

export const register = async ({ username, password, password2 }) => {
  console.log(username, password)
  return api.post('/', { username, password, password2 })
}
