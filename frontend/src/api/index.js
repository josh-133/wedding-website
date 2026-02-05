import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('admin_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Events
export const getEvents = () => api.get('/events')
export const getEvent = (slug) => api.get(`/events/${slug}`)

// RSVP
export const submitRsvp = (data) => api.post('/rsvp', data)

// Registry
export const getRegistry = () => api.get('/registry')

// Admin
export const adminLogin = (password) => api.post('/admin/login', { password })
export const getAdminRsvps = (eventSlug = null) => {
  const params = eventSlug ? { event_slug: eventSlug } : {}
  return api.get('/admin/rsvps', { params })
}
export const getAdminStats = () => api.get('/admin/stats')
export const deleteRsvp = (rsvpId) => api.delete(`/admin/rsvps/${rsvpId}`)
export const exportRsvps = (eventSlug = null) => {
  const params = eventSlug ? { event_slug: eventSlug } : {}
  return api.get('/admin/rsvps/export', {
    params,
    responseType: 'blob',
  })
}

export default api
