/**
 * Phase 6: Feedback, Evaluation, and Improvement Loop - API Services
 * Frontend API integration for feedback, metrics, A/B testing, and monitoring
 */

import axios from 'axios';
import {
  UserFeedback,
  FeedbackInsights,
  FeedbackAggregation,
  FeedbackSubmission,
  MetricValue,
  MetricAggregation,
  SystemPerformance,
  PerformanceReport,
  MetricsQuery,
  Experiment,
  ExperimentResult,
  ExperimentCreation,
  PromptTemplate,
  LogEntry,
  Alert,
  HealthCheck,
  SystemHealth,
  Phase6Dashboard,
  AlertConfiguration
} from '../types/phase6';

// API base URL from environment variable
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const phase6Api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for authentication
phase6Api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
phase6Api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('Phase 6 API Error:', error);
    return Promise.reject(error);
  }
);

// ==================== Feedback API ====================

export const feedbackApi = {
  /**
   * Submit user feedback
   */
  submitFeedback: async (feedback: FeedbackSubmission): Promise<UserFeedback> => {
    const response = await phase6Api.post<UserFeedback>('/feedback', feedback);
    return response.data;
  },

  /**
   * Submit batch feedback
   */
  submitBatchFeedback: async (feedbackItems: FeedbackSubmission[]): Promise<UserFeedback[]> => {
    const response = await phase6Api.post<UserFeedback[]>('/feedback/batch', {
      feedback_items: feedbackItems,
    });
    return response.data;
  },

  /**
   * Get user feedback history
   */
  getUserFeedback: async (userId: string, limit?: number): Promise<UserFeedback[]> => {
    const response = await phase6Api.get<UserFeedback[]>(`/feedback/user/${userId}`, {
      params: { limit },
    });
    return response.data;
  },

  /**
   * Get feedback for a specific recommendation
   */
  getRecommendationFeedback: async (recommendationId: string): Promise<UserFeedback[]> => {
    const response = await phase6Api.get<UserFeedback[]>(`/feedback/recommendation/${recommendationId}`);
    return response.data;
  },

  /**
   * Get feedback insights and analytics
   */
  getInsights: async (): Promise<FeedbackInsights> => {
    const response = await phase6Api.get<FeedbackInsights>('/feedback/insights');
    return response.data;
  },

  /**
   * Get aggregated feedback by restaurant
   */
  getAggregations: async (restaurantId?: string): Promise<FeedbackAggregation[]> => {
    const params = restaurantId ? { restaurant_id: restaurantId } : {};
    const response = await phase6Api.get<FeedbackAggregation[]>('/feedback/aggregations', { params });
    return response.data;
  },

  /**
   * Export feedback data
   */
  exportFeedback: async (format: 'json' | 'csv'): Promise<Blob> => {
    const response = await phase6Api.get('/feedback/export', {
      params: { format },
      responseType: 'blob',
    });
    return response.data;
  },
};

// ==================== Metrics API ====================

export const metricsApi = {
  /**
   * Get real-time system metrics
   */
  getRealTimeMetrics: async (): Promise<SystemPerformance> => {
    const response = await phase6Api.get<SystemPerformance>('/metrics/realtime');
    return response.data;
  },

  /**
   * Query metrics with filters
   */
  queryMetrics: async (query: MetricsQuery): Promise<MetricValue[]> => {
    const response = await phase6Api.post<MetricValue[]>('/metrics/query', query);
    return response.data;
  },

  /**
   * Get aggregated metrics
   */
  getAggregations: async (query: MetricsQuery): Promise<MetricAggregation[]> => {
    const response = await phase6Api.post<MetricAggregation[]>('/metrics/aggregations', query);
    return response.data;
  },

  /**
   * Get performance report
   */
  getPerformanceReport: async (startDate?: string, endDate?: string): Promise<PerformanceReport> => {
    const params: Record<string, string> = {};
    if (startDate) params.start_date = startDate;
    if (endDate) params.end_date = endDate;
    
    const response = await phase6Api.get<PerformanceReport>('/metrics/report', { params });
    return response.data;
  },

  /**
   * Get metric trends
   */
  getTrends: async (metricType: string, days: number = 7): Promise<MetricValue[]> => {
    const response = await phase6Api.get<MetricValue[]>(`/metrics/trends/${metricType}`, {
      params: { days },
    });
    return response.data;
  },

  /**
   * Export metrics data
   */
  exportMetrics: async (format: 'json' | 'csv'): Promise<Blob> => {
    const response = await phase6Api.get('/metrics/export', {
      params: { format },
      responseType: 'blob',
    });
    return response.data;
  },
};

// ==================== Experiments API ====================

export const experimentsApi = {
  /**
   * Get all experiments
   */
  getExperiments: async (status?: string): Promise<Experiment[]> => {
    const params = status ? { status } : {};
    const response = await phase6Api.get<Experiment[]>('/experiments', { params });
    return response.data;
  },

  /**
   * Get experiment by ID
   */
  getExperiment: async (experimentId: string): Promise<Experiment> => {
    const response = await phase6Api.get<Experiment>(`/experiments/${experimentId}`);
    return response.data;
  },

  /**
   * Create new experiment
   */
  createExperiment: async (experiment: ExperimentCreation): Promise<Experiment> => {
    const response = await phase6Api.post<Experiment>('/experiments', experiment);
    return response.data;
  },

  /**
   * Update experiment
   */
  updateExperiment: async (experimentId: string, updates: Partial<Experiment>): Promise<Experiment> => {
    const response = await phase6Api.put<Experiment>(`/experiments/${experimentId}`, updates);
    return response.data;
  },

  /**
   * Start an experiment
   */
  startExperiment: async (experimentId: string): Promise<Experiment> => {
    const response = await phase6Api.post<Experiment>(`/experiments/${experimentId}/start`);
    return response.data;
  },

  /**
   * Pause an experiment
   */
  pauseExperiment: async (experimentId: string): Promise<Experiment> => {
    const response = await phase6Api.post<Experiment>(`/experiments/${experimentId}/pause`);
    return response.data;
  },

  /**
   * Stop an experiment
   */
  stopExperiment: async (experimentId: string): Promise<ExperimentResult> => {
    const response = await phase6Api.post<ExperimentResult>(`/experiments/${experimentId}/stop`);
    return response.data;
  },

  /**
   * Get experiment results
   */
  getExperimentResults: async (experimentId: string): Promise<ExperimentResult> => {
    const response = await phase6Api.get<ExperimentResult>(`/experiments/${experimentId}/results`);
    return response.data;
  },

  /**
   * Get all prompt templates
   */
  getPromptTemplates: async (): Promise<PromptTemplate[]> => {
    const response = await phase6Api.get<PromptTemplate[]>('/prompts/templates');
    return response.data;
  },

  /**
   * Create prompt template
   */
  createPromptTemplate: async (template: Omit<PromptTemplate, 'id' | 'createdAt' | 'updatedAt'>): Promise<PromptTemplate> => {
    const response = await phase6Api.post<PromptTemplate>('/prompts/templates', template);
    return response.data;
  },

  /**
   * Update prompt template
   */
  updatePromptTemplate: async (templateId: string, updates: Partial<PromptTemplate>): Promise<PromptTemplate> => {
    const response = await phase6Api.put<PromptTemplate>(`/prompts/templates/${templateId}`, updates);
    return response.data;
  },

  /**
   * Get active prompt for user (A/B testing assignment)
   */
  getActivePrompt: async (userId: string, promptType: string): Promise<PromptTemplate> => {
    const response = await phase6Api.get<PromptTemplate>('/prompts/active', {
      params: { user_id: userId, prompt_type: promptType },
    });
    return response.data;
  },
};

// ==================== Monitoring API ====================

export const monitoringApi = {
  /**
   * Get recent logs
   */
  getLogs: async (options: {
    level?: string;
    limit?: number;
    startTime?: string;
    endTime?: string;
    source?: string;
  } = {}): Promise<LogEntry[]> => {
    const response = await phase6Api.get<LogEntry[]>('/monitoring/logs', {
      params: options,
    });
    return response.data;
  },

  /**
   * Get all alerts
   */
  getAlerts: async (activeOnly: boolean = false): Promise<Alert[]> => {
    const response = await phase6Api.get<Alert[]>('/monitoring/alerts', {
      params: { active_only: activeOnly },
    });
    return response.data;
  },

  /**
   * Acknowledge an alert
   */
  acknowledgeAlert: async (alertId: string): Promise<Alert> => {
    const response = await phase6Api.post<Alert>(`/monitoring/alerts/${alertId}/acknowledge`);
    return response.data;
  },

  /**
   * Resolve an alert
   */
  resolveAlert: async (alertId: string): Promise<Alert> => {
    const response = await phase6Api.post<Alert>(`/monitoring/alerts/${alertId}/resolve`);
    return response.data;
  },

  /**
   * Create alert configuration
   */
  createAlert: async (config: AlertConfiguration): Promise<Alert> => {
    const response = await phase6Api.post<Alert>('/monitoring/alerts', config);
    return response.data;
  },

  /**
   * Get system health status
   */
  getSystemHealth: async (): Promise<SystemHealth> => {
    const response = await phase6Api.get<SystemHealth>('/monitoring/health');
    return response.data;
  },

  /**
   * Get health check for specific component
   */
  getHealthCheck: async (component: string): Promise<HealthCheck> => {
    const response = await phase6Api.get<HealthCheck>(`/monitoring/health/${component}`);
    return response.data;
  },

  /**
   * Get monitoring dashboard data
   */
  getDashboard: async (): Promise<Phase6Dashboard> => {
    const response = await phase6Api.get<Phase6Dashboard>('/monitoring/dashboard');
    return response.data;
  },
};

// ==================== Dashboard API ====================

export const dashboardApi = {
  /**
   * Get comprehensive Phase 6 dashboard
   */
  getPhase6Dashboard: async (): Promise<Phase6Dashboard> => {
    const response = await phase6Api.get<Phase6Dashboard>('/dashboard/phase6');
    return response.data;
  },

  /**
   * Get feedback section data
   */
  getFeedbackSection: async (): Promise<{
    insights: FeedbackInsights;
    recent: UserFeedback[];
    aggregations: FeedbackAggregation[];
  }> => {
    const response = await phase6Api.get('/dashboard/phase6/feedback');
    return response.data;
  },

  /**
   * Get metrics section data
   */
  getMetricsSection: async (): Promise<{
    realTime: SystemPerformance;
    aggregations: MetricAggregation[];
    reports: PerformanceReport[];
  }> => {
    const response = await phase6Api.get('/dashboard/phase6/metrics');
    return response.data;
  },

  /**
   * Get experiments section data
   */
  getExperimentsSection: async (): Promise<{
    active: Experiment[];
    recentResults: ExperimentResult[];
    draftExperiments: Experiment[];
  }> => {
    const response = await phase6Api.get('/dashboard/phase6/experiments');
    return response.data;
  },

  /**
   * Get monitoring section data
   */
  getMonitoringSection: async (): Promise<{
    logs: LogEntry[];
    alerts: Alert[];
    health: SystemHealth;
  }> => {
    const response = await phase6Api.get('/dashboard/phase6/monitoring');
    return response.data;
  },
};

// ==================== WebSocket for Real-time Updates ====================

export class Phase6WebSocket {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private listeners: Map<string, ((data: unknown) => void)[]> = new Map();

  connect() {
    const wsUrl = API_BASE_URL.replace('http', 'ws');
    this.ws = new WebSocket(`${wsUrl}/ws/phase6`);

    this.ws.onopen = () => {
      console.log('Phase 6 WebSocket connected');
      this.reconnectAttempts = 0;
    };

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.handleMessage(data);
    };

    this.ws.onclose = () => {
      console.log('Phase 6 WebSocket disconnected');
      this.attemptReconnect();
    };

    this.ws.onerror = (error) => {
      console.error('Phase 6 WebSocket error:', error);
    };
  }

  private handleMessage(data: { type: string; payload: unknown }) {
    const listeners = this.listeners.get(data.type) || [];
    listeners.forEach((callback) => callback(data.payload));
  }

  private attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      setTimeout(() => this.connect(), 1000 * this.reconnectAttempts);
    }
  }

  subscribe(eventType: string, callback: (data: unknown) => void) {
    if (!this.listeners.has(eventType)) {
      this.listeners.set(eventType, []);
    }
    this.listeners.get(eventType)?.push(callback);
  }

  unsubscribe(eventType: string, callback: (data: unknown) => void) {
    const listeners = this.listeners.get(eventType) || [];
    const index = listeners.indexOf(callback);
    if (index > -1) {
      listeners.splice(index, 1);
    }
  }

  disconnect() {
    this.ws?.close();
  }
}

// Export singleton instance
export const phase6WebSocket = new Phase6WebSocket();

// ==================== Export all APIs ====================

export default {
  feedback: feedbackApi,
  metrics: metricsApi,
  experiments: experimentsApi,
  monitoring: monitoringApi,
  dashboard: dashboardApi,
  websocket: phase6WebSocket,
};
