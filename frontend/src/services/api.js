/**
 * API service layer — Axios instance with JWT auth interceptor.
 */
import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
});

// Attach JWT token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle 401 responses
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Don't trigger a hard redirect if we are already trying to login/register
      // so the user can actually see the "Invalid credentials" error message.
      if (!window.location.pathname.includes('/login') && !window.location.pathname.includes('/register')) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// ——— Auth ———
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getMe: () => api.get('/auth/me'),
};

// ——— Students ———
export const studentAPI = {
  updateProfile: (data) => api.put('/students/profile', data),
  uploadResume: (file) => {
    const form = new FormData();
    form.append('file', file);
    return api.post('/students/resume', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  getProfile: (userId) => api.get(`/students/profile/${userId}`),
};

// ——— Companies ———
export const companyAPI = {
  updateProfile: (data) => api.put('/companies/profile', data),
  getProfile: () => api.get('/companies/profile'),
};

// ——— Jobs ———
export const jobAPI = {
  list: (status = 'active', search = '') =>
    api.get('/jobs', { params: { status, search } }),
  listMyJobs: () => api.get('/jobs/my'),
  create: (data) => api.post('/jobs', data),
  update: (id, data) => api.put(`/jobs/${id}`, data),
  delete: (id) => api.delete(`/jobs/${id}`),
  getCandidates: (jobId) => api.get(`/jobs/${jobId}/candidates`),
  getRecommendations: () => api.get('/jobs/recommendations/student'),
};

// ——— Applications ———
export const applicationAPI = {
  apply: (data) => api.post('/applications', data),
  listMine: () => api.get('/applications'),
  updateStatus: (id, status) =>
    api.patch(`/applications/${id}/status`, { status }),
};

// ——— Admin ———
export const adminAPI = {
  getAnalytics: () => api.get('/admin/analytics'),
  listUsers: (role = '', search = '') =>
    api.get('/admin/users', { params: { role, search } }),
  toggleUser: (userId) => api.patch(`/admin/users/${userId}/toggle`),
  listPlacements: () => api.get('/admin/placements'),
};

// ——— Notifications ———
export const notificationAPI = {
  list: () => api.get('/notifications'),
  markRead: (id) => api.patch(`/notifications/${id}/read`),
  markAllRead: () => api.patch('/notifications/read-all'),
};

export default api;
