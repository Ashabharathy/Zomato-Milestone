/**
 * Phase 6: Feedback, Evaluation, and Improvement Loop - TypeScript Types
 * Frontend type definitions for the feedback and analytics system
 */

// ==================== Feedback Types ====================

export enum FeedbackType {
  LIKE = 'like',
  DISLIKE = 'dislike',
  NEUTRAL = 'neutral',
  BOOKMARK = 'bookmark',
  VISIT = 'visit',
  SKIP = 'skip',
  SHARE = 'share',
  RATING = 'rating'
}

export enum FeedbackSource {
  UI_BUTTON = 'ui_button',
  SURVEY = 'survey',
  INTERVIEW = 'interview',
  AUTOMATIC = 'automatic',
  API = 'api',
  EMAIL = 'email'
}

export interface UserFeedback {
  id: string;
  userId: string;
  sessionId: string;
  recommendationId: string;
  restaurantId: string;
  restaurantName: string;
  feedbackType: FeedbackType;
  feedbackSource: FeedbackSource;
  rating?: number;
  helpfulness?: number;
  comment?: string;
  reasons?: string[];
  context?: Record<string, unknown>;
  timestamp: string;
  processed: boolean;
}

export interface FeedbackAggregation {
  restaurantId: string;
  restaurantName: string;
  totalFeedback: number;
  positiveCount: number;
  negativeCount: number;
  neutralCount: number;
  averageRating: number;
  helpfulnessScore: number;
  commonReasons: Array<{ reason: string; count: number }>;
  sentimentTrend: 'improving' | 'declining' | 'stable';
  lastUpdated: string;
}

export interface FeedbackInsights {
  totalFeedback: number;
  averageRating: number;
  satisfactionRate: number;
  topRatedRestaurants: Array<{
    restaurantId: string;
    name: string;
    rating: number;
    reviewCount: number;
  }>;
  mostDiscussedAspects: Array<{ aspect: string; count: number; sentiment: 'positive' | 'negative' | 'neutral' }>;
  commonIssues: string[];
  improvementAreas: string[];
  userEngagementMetrics: {
    feedbackRate: number;
    responseRate: number;
    averageTimeToFeedback: number;
  };
}

// ==================== Metrics Types ====================

export enum MetricType {
  PRECISION_AT_K = 'precision_at_k',
  RECALL_AT_K = 'recall_at_k',
  SATISFACTION_SCORE = 'satisfaction_score',
  RESPONSE_LATENCY = 'response_latency',
  CLICK_THROUGH_RATE = 'click_through_rate',
  CONVERSION_RATE = 'conversion_rate',
  DIVERSITY_SCORE = 'diversity_score',
  NOVELTY_SCORE = 'novelty_score',
  COVERAGE = 'coverage',
  ERROR_RATE = 'error_rate',
  TOKEN_EFFICIENCY = 'token_efficiency',
  USER_ENGAGEMENT = 'user_engagement'
}

export enum TimeGranularity {
  HOURLY = 'hourly',
  DAILY = 'daily',
  WEEKLY = 'weekly',
  MONTHLY = 'monthly'
}

export interface MetricValue {
  id: string;
  metricType: MetricType;
  value: number;
  timestamp: string;
  context: Record<string, unknown>;
  granularity: TimeGranularity;
  sampleSize: number;
  confidenceInterval?: [number, number];
}

export interface MetricAggregation {
  metricType: MetricType;
  values: MetricValue[];
  average: number;
  min: number;
  max: number;
  trend: 'up' | 'down' | 'stable';
  changePercent: number;
  timeRange: { start: string; end: string };
}

export interface SystemPerformance {
  cpuUsage: number;
  memoryUsage: number;
  diskUsage: number;
  responseTime: number;
  activeConnections: number;
  queueDepth: number;
  errorRate: number;
  timestamp: string;
}

export interface PerformanceReport {
  reportId: string;
  generatedAt: string;
  timeRange: { start: string; end: string };
  metrics: MetricAggregation[];
  systemHealthScore: number;
  recommendations: string[];
  topIssues: Array<{ issue: string; severity: 'low' | 'medium' | 'high' | 'critical' }>;
  trends: Array<{
    metricType: MetricType;
    direction: 'improving' | 'declining' | 'stable';
    changePercent: number;
  }>;
}

// ==================== A/B Testing Types ====================

export enum PromptType {
  RANKING_PROMPT = 'ranking_prompt',
  SUMMARIZATION_PROMPT = 'summarization_prompt',
  EXPLANATION_PROMPT = 'explanation_prompt',
  QUERY_UNDERSTANDING_PROMPT = 'query_understanding_prompt',
  PERSONALIZATION_PROMPT = 'personalization_prompt'
}

export enum ExperimentStatus {
  DRAFT = 'draft',
  ACTIVE = 'active',
  PAUSED = 'paused',
  COMPLETED = 'completed',
  FAILED = 'failed'
}

export enum VariantType {
  CONTROL = 'control',
  TREATMENT = 'treatment'
}

export interface PromptTemplate {
  id: string;
  name: string;
  description: string;
  promptType: PromptType;
  template: string;
  variables: string[];
  version: string;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
  performance?: {
    avgResponseTime: number;
    successRate: number;
    userSatisfaction: number;
  };
}

export interface Experiment {
  id: string;
  name: string;
  description: string;
  promptType: PromptType;
  controlTemplateId: string;
  controlTemplateName: string;
  treatmentTemplateIds: string[];
  treatmentTemplateNames: string[];
  trafficSplit: Record<string, number>;
  status: ExperimentStatus;
  startDate?: string;
  endDate?: string;
  sampleSize: number;
  targetSampleSize: number;
  confidenceLevel: number;
  successCriteria: {
    metric: MetricType;
    minImprovement: number;
  };
  createdAt: string;
  updatedAt: string;
}

export interface ExperimentResult {
  experimentId: string;
  experimentName: string;
  status: ExperimentStatus;
  winner?: string;
  winnerVariant?: VariantType;
  statisticalSignificance: boolean;
  pValue: number;
  confidenceInterval: number;
  sampleSize: number;
  metrics: Record<string, {
    control: number;
    treatment: number;
    improvement: number;
  }>;
  recommendations: string[];
  completedAt?: string;
}

// ==================== Monitoring Types ====================

export enum LogLevel {
  DEBUG = 'debug',
  INFO = 'info',
  WARNING = 'warning',
  ERROR = 'error',
  CRITICAL = 'critical'
}

export enum AlertSeverity {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical'
}

export enum MetricCategory {
  SYSTEM = 'system',
  APPLICATION = 'application',
  BUSINESS = 'business',
  USER = 'user',
  API = 'api',
  DATABASE = 'database',
  LLM = 'llm'
}

export interface LogEntry {
  id: string;
  timestamp: string;
  level: LogLevel;
  message: string;
  source: string;
  context?: Record<string, unknown>;
  userId?: string;
  sessionId?: string;
  traceId?: string;
}

export interface Alert {
  id: string;
  name: string;
  description: string;
  severity: AlertSeverity;
  category: MetricCategory;
  condition: string;
  threshold: number;
  currentValue: number;
  isActive: boolean;
  triggeredAt?: string;
  resolvedAt?: string;
  acknowledgedBy?: string;
  acknowledgedAt?: string;
  notificationChannels: string[];
}

export interface HealthCheck {
  component: string;
  status: 'healthy' | 'degraded' | 'unhealthy';
  responseTime: number;
  lastChecked: string;
  message?: string;
  details?: Record<string, unknown>;
}

export interface SystemHealth {
  overallStatus: 'healthy' | 'degraded' | 'unhealthy';
  healthChecks: HealthCheck[];
  activeAlerts: number;
  criticalAlerts: number;
  lastUpdated: string;
}

export interface MonitoringDashboard {
  systemMetrics: SystemPerformance;
  healthStatus: SystemHealth;
  recentLogs: LogEntry[];
  activeAlerts: Alert[];
  performanceTrends: MetricAggregation[];
}

// ==================== Dashboard Types ====================

export interface Phase6Dashboard {
  feedback: {
    summary: FeedbackInsights;
    recent: UserFeedback[];
    aggregations: FeedbackAggregation[];
  };
  metrics: {
    summary: PerformanceReport;
    realTime: SystemPerformance;
    trends: MetricAggregation[];
  };
  experiments: {
    active: Experiment[];
    recentResults: ExperimentResult[];
    draftExperiments: Experiment[];
  };
  monitoring: MonitoringDashboard;
  generatedAt: string;
}

// ==================== API Response Types ====================

export interface FeedbackSubmission {
  userId: string;
  sessionId: string;
  recommendationId: string;
  restaurantId: string;
  feedbackType: FeedbackType;
  rating?: number;
  comment?: string;
  reasons?: string[];
}

export interface MetricsQuery {
  metricTypes?: MetricType[];
  granularity?: TimeGranularity;
  startDate?: string;
  endDate?: string;
  userId?: string;
  restaurantId?: string;
  sessionId?: string;
}

export interface ExperimentCreation {
  name: string;
  description: string;
  promptType: PromptType;
  controlTemplateId: string;
  treatmentTemplateIds: string[];
  trafficSplit?: Record<string, number>;
  sampleSize: number;
  confidenceLevel: number;
  successCriteria: {
    metric: MetricType;
    minImprovement: number;
  };
}

export interface AlertConfiguration {
  name: string;
  description: string;
  severity: AlertSeverity;
  category: MetricCategory;
  condition: {
    metric: MetricType | string;
    operator: '>' | '<' | '=' | '>=' | '<=';
    threshold: number;
  };
  notificationChannels: string[];
}

// ==================== Component Props Types ====================

export interface FeedbackCardProps {
  feedback: UserFeedback;
  onClick?: (feedback: UserFeedback) => void;
  showActions?: boolean;
}

export interface MetricChartProps {
  data: MetricValue[];
  metricType: MetricType;
  title: string;
  timeRange?: { start: string; end: string };
  showTrend?: boolean;
}

export interface ExperimentCardProps {
  experiment: Experiment;
  onViewResults?: (experimentId: string) => void;
  onPause?: (experimentId: string) => void;
  onResume?: (experimentId: string) => void;
  onStop?: (experimentId: string) => void;
}

export interface AlertBadgeProps {
  alert: Alert;
  onAcknowledge?: (alertId: string) => void;
  onDismiss?: (alertId: string) => void;
}

export interface HealthIndicatorProps {
  health: HealthCheck;
  showDetails?: boolean;
}

// ==================== State Types ====================

export interface Phase6State {
  feedback: {
    items: UserFeedback[];
    insights: FeedbackInsights | null;
    aggregations: FeedbackAggregation[];
    isLoading: boolean;
    error: string | null;
  };
  metrics: {
    realTime: SystemPerformance | null;
    aggregations: MetricAggregation[];
    reports: PerformanceReport[];
    isLoading: boolean;
    error: string | null;
  };
  experiments: {
    list: Experiment[];
    results: ExperimentResult[];
    templates: PromptTemplate[];
    isLoading: boolean;
    error: string | null;
  };
  monitoring: {
    logs: LogEntry[];
    alerts: Alert[];
    health: SystemHealth | null;
    isLoading: boolean;
    error: string | null;
  };
  dashboard: Phase6Dashboard | null;
}
