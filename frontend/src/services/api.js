import axios from 'axios'

const api = axios.create({
  baseURL: `${import.meta.env.VITE_API_ENDPOINT}users`
})

export const session = async () => {
  return await api.get('/session')
}

export const login = async ({ username, password }) => {
  return await api.post('/login', { username, password })
}

export const register = async ({ username, password, password2 }) => {
  return await api.post('/', { username, password, password2 })
}

export const logout = async () => {
  return await api.get('/logout')
}

export const getProfile = async (id) => {
  return await api.get(`/${id}`)
}

export const updateProfile = async ({ id, first_name, last_name, birth_date, gender }, csrf) => {
  return await api.put(
    `/${id}`,
    { first_name, last_name, birth_date, gender },
    { headers: { 'X-CSRFToken': csrf } }
  )
}
