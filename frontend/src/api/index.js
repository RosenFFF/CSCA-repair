import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

// Add admin token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('admin_token')
  if (token && config.url.startsWith('/admin')) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const getActivities = () => api.get('/activities')
export const createSignup = (data) => api.post('/signups', data)
export const adminLogin = (password) => api.post('/admin/login', { password })
export const getAdminSignups = (params) => api.get('/admin/signups', { params })
export const deleteSignup = (id) => api.delete(`/admin/signups/${id}`)
export const getAdminStats = () => api.get('/admin/stats')
export const exportExcel = (params) =>
  api.get('/admin/export', { params, responseType: 'blob' })
