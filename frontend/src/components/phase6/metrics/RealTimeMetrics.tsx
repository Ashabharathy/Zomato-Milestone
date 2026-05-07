'use client';

import React, { useEffect, useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  LinearProgress,
  Chip,
  Alert,
  CircularProgress,
} from '@mui/material';
import {
  Speed,
  Memory,
  Storage,
  People,
  Queue,
  Error,
} from '@mui/icons-material';
import { SystemPerformance } from '../../../types/phase6';
import { metricsApi, phase6WebSocket } from '../../../services/phase6';

export const RealTimeMetrics: React.FC = () => {
  const [metrics, setMetrics] = useState<SystemPerformance | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

  useEffect(() => {
    // Initial fetch
    fetchMetrics();

    // Connect to WebSocket for real-time updates
    phase6WebSocket.connect();
    phase6WebSocket.subscribe('system_metrics', (data) => {
      setMetrics(data as SystemPerformance);
      setLastUpdate(new Date());
    });

    // Poll every 30 seconds as fallback
    const interval = setInterval(fetchMetrics, 30000);

    return () => {
      phase6WebSocket.disconnect();
      clearInterval(interval);
    };
  }, []);

  const fetchMetrics = async () => {
    try {
      const data = await metricsApi.getRealTimeMetrics();
      setMetrics(data);
      setLastUpdate(new Date());
      setError(null);
    } catch (err) {
      setError('Failed to load real-time metrics');
      console.error('Error fetching metrics:', err);
    } finally {
      setLoading(false);
    }
  };

  const getHealthColor = (value: number, thresholds: { good: number; warning: number }) => {
    if (value <= thresholds.good) return 'success';
    if (value <= thresholds.warning) return 'warning';
    return 'error';
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" p={4}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ m: 2 }}>
        {error}
      </Alert>
    );
  }

  if (!metrics) {
    return (
      <Alert severity="info" sx={{ m: 2 }}>
        No metrics data available
      </Alert>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h5" fontWeight="bold">
          Real-Time System Metrics
        </Typography>
        <Chip
          label={`Updated: ${lastUpdate.toLocaleTimeString()}`}
          size="small"
          color="primary"
          variant="outlined"
        />
      </Box>

      <Grid container spacing={3}>
        {/* CPU Usage */}
        <Grid item xs={12} sm={6} md={4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <Speed color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6">CPU Usage</Typography>
              </Box>
              <Typography variant="h3" component="div" gutterBottom>
                {metrics.cpuUsage.toFixed(1)}%
              </Typography>
              <LinearProgress
                variant="determinate"
                value={metrics.cpuUsage}
                color={getHealthColor(metrics.cpuUsage, { good: 50, warning: 80 })}
              />
            </CardContent>
          </Card>
        </Grid>

        {/* Memory Usage */}
        <Grid item xs={12} sm={6} md={4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <Memory color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6">Memory Usage</Typography>
              </Box>
              <Typography variant="h3" component="div" gutterBottom>
                {metrics.memoryUsage.toFixed(1)}%
              </Typography>
              <LinearProgress
                variant="determinate"
                value={metrics.memoryUsage}
                color={getHealthColor(metrics.memoryUsage, { good: 60, warning: 85 })}
              />
            </CardContent>
          </Card>
        </Grid>

        {/* Disk Usage */}
        <Grid item xs={12} sm={6} md={4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <Storage color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6">Disk Usage</Typography>
              </Box>
              <Typography variant="h3" component="div" gutterBottom>
                {metrics.diskUsage.toFixed(1)}%
              </Typography>
              <LinearProgress
                variant="determinate"
                value={metrics.diskUsage}
                color={getHealthColor(metrics.diskUsage, { good: 70, warning: 90 })}
              />
            </CardContent>
          </Card>
        </Grid>

        {/* Response Time */}
        <Grid item xs={12} sm={6} md={4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <Speed color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6">Response Time</Typography>
              </Box>
              <Typography variant="h3" component="div" gutterBottom>
                {metrics.responseTime.toFixed(0)}ms
              </Typography>
              <Chip
                label={metrics.responseTime < 200 ? 'Fast' : metrics.responseTime < 500 ? 'Normal' : 'Slow'}
                size="small"
                color={getHealthColor(metrics.responseTime, { good: 200, warning: 500 })}
              />
            </CardContent>
          </Card>
        </Grid>

        {/* Active Connections */}
        <Grid item xs={12} sm={6} md={4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <People color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6">Active Users</Typography>
              </Box>
              <Typography variant="h3" component="div" gutterBottom>
                {metrics.activeConnections}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Currently connected
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Queue Depth */}
        <Grid item xs={12} sm={6} md={4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <Queue color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6">Queue Depth</Typography>
              </Box>
              <Typography variant="h3" component="div" gutterBottom>
                {metrics.queueDepth}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Pending requests
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Error Rate */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <Error color="error" sx={{ mr: 1 }} />
                <Typography variant="h6">Error Rate</Typography>
              </Box>
              <Box display="flex" alignItems="center">
                <Typography variant="h3" component="div" mr={2}>
                  {(metrics.errorRate * 100).toFixed(2)}%
                </Typography>
                <Chip
                  label={metrics.errorRate < 0.01 ? 'Healthy' : metrics.errorRate < 0.05 ? 'Warning' : 'Critical'}
                  color={metrics.errorRate < 0.01 ? 'success' : metrics.errorRate < 0.05 ? 'warning' : 'error'}
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default RealTimeMetrics;
