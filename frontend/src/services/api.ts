import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { LoginCredentials, RegisterData, LoginResponse, RefreshTokenResponse, User } from '../types/auth';

// Create axios instance
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (credentials: LoginCredentials): Promise<AxiosResponse<LoginResponse>> =>
    api.post('/auth/login', credentials),
  
  register: (userData: RegisterData): Promise<AxiosResponse<User>> =>
    api.post('/auth/register', userData),
  
  getCurrentUser: (): Promise<AxiosResponse<User>> =>
    api.get('/auth/me'),
  
  logout: (): Promise<AxiosResponse<void>> =>
    api.delete('/auth/logout'),
  
  refreshToken: (refreshToken: string): Promise<AxiosResponse<RefreshTokenResponse>> =>
    api.post('/auth/refresh', { refresh_token: refreshToken }),
};

// Users API
export const usersAPI = {
  getProfile: (): Promise<AxiosResponse<User>> =>
    api.get('/users/profile'),
  
  updateProfile: (data: Partial<User>): Promise<AxiosResponse<User>> =>
    api.put('/users/profile', data),
  
  getPreferences: (): Promise<AxiosResponse<any>> =>
    api.get('/users/preferences'),
  
  updatePreferences: (data: any): Promise<AxiosResponse<any>> =>
    api.post('/users/preferences', data),
};

// Restaurants API
export const restaurantsAPI = {
  getRestaurants: (params?: any): Promise<AxiosResponse<any>> =>
    api.get('/restaurants', { params }),
  
  getRestaurant: (id: number): Promise<AxiosResponse<any>> =>
    api.get(`/restaurants/${id}`),
  
  searchRestaurants: (params: any): Promise<AxiosResponse<any>> =>
    api.get('/restaurants/search', { params }),
  
  getSuggestions: (params: any): Promise<AxiosResponse<any>> =>
    api.get('/restaurants/suggestions', { params }),
};

// Recommendations API
export const recommendationsAPI = {
  getRecommendations: (preferences: any): Promise<AxiosResponse<any>> =>
    api.post('/recommendations', preferences),
  
  getRecommendationHistory: (): Promise<AxiosResponse<any>> =>
    api.get('/recommendations/history'),
  
  submitFeedback: (data: any): Promise<AxiosResponse<any>> =>
    api.post('/recommendations/feedback', data),
};

// Analytics API
export const analyticsAPI = {
  getUserAnalytics: (): Promise<AxiosResponse<any>> =>
    api.get('/analytics/user'),
  
  getSystemAnalytics: (): Promise<AxiosResponse<any>> =>
    api.get('/analytics/system'),
  
  trackEvent: (event: any): Promise<AxiosResponse<any>> =>
    api.post('/analytics/events', event),
};

export default api;
