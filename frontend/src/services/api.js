import axios from 'axios'

const api = axios.create({
  baseURL: `${import.meta.env.VITE_API_ENDPOINT}`
})

export const session = async () => {
  return await api.get('users/session')
}

export const login = async ({ username, password }) => {
  return await api.post('users/login', { username, password })
}

export const register = async ({ username, password, password2 }) => {
  return await api.post('users/', { username, password, password2 })
}

export const logout = async () => {
  return await api.get('users/logout')
}

export const getProfile = async (id) => {
  return await api.get(`users/${id}`)
}

export const updateProfile = async ({ id, first_name, last_name, birth_date, gender }, csrf) => {
  return await api.put(
    `users/${id}`,
    { first_name, last_name, birth_date, gender },
    { headers: { 'X-CSRFToken': csrf } }
  )
}

export const getJobPreference = async (id) => {
  return await api.get(`userprofiles/${id}`)
}

export const updateJobPreference = async ({ id, experience_level, expected_salary }, csrf) => {
  return await api.put(
    `userprofiles/${id}`,
    { experience_level, expected_salary },
    { headers: { 'X-CSRFToken': csrf } }
  )
}

export const getAllInterests = async () => {
  return await api.get(`interests`)
}

export const getUserInterests = async (id) => {
  return await api.get(`user-interests/${id}`)
}

export const updateUserInterests = async ({ id, interests }, csrf) => {
  return await api.put(`user-interests/${id}`, { interests }, { headers: { 'X-CSRFToken': csrf } })
}
