import axios from 'axios'

const API_BASE_URL = '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // You can add authentication headers here if needed
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      console.error('Unauthorized access')
    }
    return Promise.reject(error)
  }
)

export default api

// API functions
export const getIdentities = () => {
  return api.get('/identities')
}

export const getGraphData = () => {
  return api.get('/identities/graph')
}

export const getIdentityById = (id) => {
  return api.get(`/identities/${id}`)
}

export const getPaths = (source, target = null) => {
  const params = { source }
  if (target) {
    params.target = target
  }
  return api.get('/paths', { params })
}

export const getHighRiskIdentities = () => {
  return api.get('/risk/high-risk-identities')
}