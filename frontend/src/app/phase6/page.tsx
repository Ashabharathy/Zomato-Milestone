'use client';

import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Tabs,
  Tab,
  Paper,
  Grid,
  Alert,
  CircularProgress,
} from '@mui/material';
import {
  Feedback,
  Assessment,
  Science,
  MonitorHeart,
  Dashboard,
} from '@mui/icons-material';

// Import Phase 6 components
import { FeedbackButtons } from '../../components/phase6/feedback/FeedbackButtons';
import { FeedbackInsights } from '../../components/phase6/feedback/FeedbackInsights';
import { MetricsChart } from '../../components/phase6/metrics/MetricsChart';
import { RealTimeMetrics } from '../../components/phase6/metrics/RealTimeMetrics';
import { ExperimentCard } from '../../components/phase6/experiments/ExperimentCard';
import { AlertPanel } from '../../components/phase6/monitoring/AlertPanel';

// Import theme
import { colors } from '../../theme/colors';

// Import types and services
import { Phase6Dashboard, MetricType, ExperimentStatus } from '../../types/phase6';
import { dashboardApi } from '../../services/phase6';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

const TabPanel: React.FC<TabPanelProps> = ({ children, value, index }) => (
  <div hidden={value !== index} role="tabpanel">
    {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
  </div>
);

export default function Phase6DashboardPage() {
  const [activeTab, setActiveTab] = useState(0);
  const [dashboard, setDashboard] = useState<Phase6Dashboard | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Apply theme colors to components
  const getThemeColor = (colorKey: keyof typeof colors) => {
    const colorMap = {
      primary: colors.primary.main,
      secondary: colors.secondary.main,
      success: colors.semantic.success,
      warning: colors.semantic.warning,
      error: colors.semantic.error,
      info: colors.semantic.info,
    };
    return colorMap[colorKey] || colors.text.primary;
  };

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      const data = await dashboardApi.getPhase6Dashboard();
      setDashboard(data);
      setError(null);
    } catch (err) {
      setError('Failed to load Phase 6 dashboard data');
      console.error('Error fetching dashboard:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  if (loading) {
    return (
      <Container maxWidth="xl" sx={{ py: 4 }}>
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="xl" sx={{ py: 4 }}>
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom fontWeight="bold">
        Phase 6: Feedback, Evaluation & Improvement Loop
      </Typography>
      <Typography variant="body1" color="textSecondary" gutterBottom>
        Monitor feedback, track metrics, run A/B tests, and continuously improve recommendation quality.
      </Typography>

      <Paper sx={{ mt: 3 }}>
        <Tabs
          value={activeTab}
          onChange={handleTabChange}
          variant="scrollable"
          scrollButtons="auto"
          indicatorColor="primary"
          textColor="primary"
        >
          <Tab icon={<Dashboard />} label="Overview" />
          <Tab icon={<Feedback />} label="Feedback" />
          <Tab icon={<Assessment />} label="Metrics" />
          <Tab icon={<Science />} label="A/B Testing" />
          <Tab icon={<MonitorHeart />} label="Monitoring" />
        </Tabs>

        {/* Overview Tab */}
        <TabPanel value={activeTab} index={0}>
          <Grid container spacing={3}>
            {/* Summary Cards */}
            <Grid item xs={12} md={3}>
              <Paper sx={{ p: 2, textAlign: 'center' }}>
                <Typography variant="h6" color="textSecondary">
                  Total Feedback
                </Typography>
                <Typography variant="h3" color="primary">
                  {dashboard?.feedback.summary.totalFeedback.toLocaleString() || 0}
                </Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} md={3}>
              <Paper sx={{ p: 2, textAlign: 'center' }}>
                <Typography variant="h6" color="textSecondary">
                  Avg Rating
                </Typography>
                <Typography variant="h3" color="primary">
                  {dashboard?.feedback.summary.averageRating.toFixed(1) || 0}
                </Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} md={3}>
              <Paper sx={{ p: 2, textAlign: 'center' }}>
                <Typography variant="h6" color="textSecondary">
                  Active Experiments
                </Typography>
                <Typography variant="h3" color="primary">
                  {dashboard?.experiments.active.length || 0}
                </Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} md={3}>
              <Paper sx={{ p: 2, textAlign: 'center' }}>
                <Typography variant="h6" color="textSecondary">
                  Active Alerts
                </Typography>
                <Typography variant="h3" color={dashboard?.monitoring.activeAlerts.length ? 'error' : 'success'}>
                  {dashboard?.monitoring.activeAlerts.length || 0}
                </Typography>
              </Paper>
            </Grid>

            {/* Recent Feedback */}
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 2 }}>
                <Typography variant="h6" gutterBottom>
                  Recent Feedback
                </Typography>
                <Box sx={{ maxHeight: 300, overflow: 'auto' }}>
                  {dashboard?.feedback.recent.slice(0, 5).map((feedback) => (
                    <Box key={feedback.id} sx={{ py: 1, borderBottom: '1px solid #eee' }}>
                      <Typography variant="body2" fontWeight="bold">
                        {feedback.restaurantName}
                      </Typography>
                      <Typography variant="caption" color="textSecondary">
                        {feedback.feedbackType} • {new Date(feedback.timestamp).toLocaleDateString()}
                      </Typography>
                    </Box>
                  ))}
                </Box>
              </Paper>
            </Grid>

            {/* Quick Stats */}
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 2 }}>
                <Typography variant="h6" gutterBottom>
                  System Health
                </Typography>
                <Box>
                  <Typography variant="body2">
                    Status: {dashboard?.monitoring.healthStatus.overallStatus || 'Unknown'}
                  </Typography>
                  <Typography variant="body2">
                    CPU: {dashboard?.metrics.realTime.cpuUsage.toFixed(1)}%
                  </Typography>
                  <Typography variant="body2">
                    Memory: {dashboard?.metrics.realTime.memoryUsage.toFixed(1)}%
                  </Typography>
                  <Typography variant="body2">
                    Response Time: {dashboard?.metrics.realTime.responseTime.toFixed(0)}ms
                  </Typography>
                </Box>
              </Paper>
            </Grid>
          </Grid>
        </TabPanel>

        {/* Feedback Tab */}
        <TabPanel value={activeTab} index={1}>
          <FeedbackInsights />
        </TabPanel>

        {/* Metrics Tab */}
        <TabPanel value={activeTab} index={2}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <RealTimeMetrics />
            </Grid>
            <Grid item xs={12} md={6}>
              <MetricsChart
                metricType={MetricType.PRECISION_AT_K}
                title="Recommendation Precision"
                days={14}
                color="#4CAF50"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <MetricsChart
                metricType={MetricType.SATISFACTION_SCORE}
                title="User Satisfaction"
                days={14}
                color="#FF6B35"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <MetricsChart
                metricType={MetricType.RESPONSE_LATENCY}
                title="Response Time"
                days={7}
                color="#2196F3"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <MetricsChart
                metricType={MetricType.CLICK_THROUGH_RATE}
                title="Click-Through Rate"
                days={14}
                color="#9C27B0"
              />
            </Grid>
          </Grid>
        </TabPanel>

        {/* A/B Testing Tab */}
        <TabPanel value={activeTab} index={3}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom>
                Active Experiments
              </Typography>
            </Grid>
            {dashboard?.experiments.active.map((experiment) => (
              <Grid item xs={12} md={6} key={experiment.id}>
                <ExperimentCard
                  experiment={experiment}
                  onViewDetails={(id) => console.log('View experiment:', id)}
                />
              </Grid>
            ))}
            {dashboard?.experiments.active.length === 0 && (
              <Grid item xs={12}>
                <Alert severity="info">No active experiments. Start one to optimize your prompts!</Alert>
              </Grid>
            )}

            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom sx={{ mt: 4 }}>
                Recent Results
              </Typography>
            </Grid>
            {dashboard?.experiments.recentResults.map((result) => (
              <Grid item xs={12} md={6} key={result.experimentId}>
                <Paper sx={{ p: 2 }}>
                  <Typography variant="h6">{result.experimentName}</Typography>
                  <Typography variant="body2" color="textSecondary">
                    Winner: {result.winner || 'No clear winner'}
                  </Typography>
                  <Typography variant="body2">
                    Statistical Significance: {result.statisticalSignificance ? 'Yes' : 'No'}
                  </Typography>
                  <Typography variant="caption">
                    P-value: {result.pValue.toFixed(4)}
                  </Typography>
                </Paper>
              </Grid>
            ))}
          </Grid>
        </TabPanel>

        {/* Monitoring Tab */}
        <TabPanel value={activeTab} index={4}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={8}>
              <RealTimeMetrics />
            </Grid>
            <Grid item xs={12} md={4}>
              <AlertPanel />
            </Grid>
            <Grid item xs={12}>
              <Paper sx={{ p: 2 }}>
                <Typography variant="h6" gutterBottom>
                  Health Checks
                </Typography>
                <Box display="flex" gap={2} flexWrap="wrap">
                  {dashboard?.monitoring.healthStatus.healthChecks.map((check) => (
                    <Paper
                      key={check.component}
                      sx={{
                        p: 2,
                        minWidth: 200,
                        borderLeft: 4,
                        borderColor:
                          check.status === 'healthy'
                            ? 'success.main'
                            : check.status === 'degraded'
                            ? 'warning.main'
                            : 'error.main',
                      }}
                    >
                      <Typography variant="body1" fontWeight="bold">
                        {check.component}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        Status: {check.status}
                      </Typography>
                      <Typography variant="caption">
                        Response: {check.responseTime.toFixed(0)}ms
                      </Typography>
                    </Paper>
                  ))}
                </Box>
              </Paper>
            </Grid>
          </Grid>
        </TabPanel>
      </Paper>
    </Container>
  );
}
