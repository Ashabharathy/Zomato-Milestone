'use client';

import React, { useEffect, useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  ToggleButton,
  ToggleButtonGroup,
  Alert,
  CircularProgress,
} from '@mui/material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  AreaChart,
  Area,
} from 'recharts';
import { MetricType, MetricValue, TimeGranularity } from '../../../types/phase6';
import { metricsApi } from '../../../services/phase6';

interface MetricsChartProps {
  metricType: MetricType;
  title: string;
  days?: number;
  showArea?: boolean;
  color?: string;
  height?: number;
}

export const MetricsChart: React.FC<MetricsChartProps> = ({
  metricType,
  title,
  days = 7,
  showArea = false,
  color = '#FF6B35',
  height = 300,
}) => {
  const [data, setData] = useState<MetricValue[]>([]);
  const [granularity, setGranularity] = useState<TimeGranularity>(TimeGranularity.DAILY);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchMetrics();
  }, [metricType, days, granularity]);

  const fetchMetrics = async () => {
    try {
      setLoading(true);
      const endDate = new Date().toISOString();
      const startDate = new Date(Date.now() - days * 24 * 60 * 60 * 1000).toISOString();

      const metrics = await metricsApi.queryMetrics({
        metricTypes: [metricType],
        granularity,
        startDate,
        endDate,
      });

      setData(metrics);
      setError(null);
    } catch (err) {
      setError('Failed to load metrics data');
      console.error('Error fetching metrics:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleGranularityChange = (
    _event: React.MouseEvent<HTMLElement>,
    newGranularity: TimeGranularity
  ) => {
    if (newGranularity) {
      setGranularity(newGranularity);
    }
  };

  const formatChartData = () => {
    return data.map((metric) => ({
      timestamp: new Date(metric.timestamp).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: granularity === TimeGranularity.HOURLY ? 'numeric' : undefined,
      }),
      value: metric.value,
      sampleSize: metric.sampleSize,
    }));
  };

  const formatMetricValue = (value: number) => {
    if (metricType === MetricType.RESPONSE_LATENCY) {
      return `${value.toFixed(0)}ms`;
    }
    if (metricType === MetricType.PRECISION_AT_K || metricType === MetricType.RECALL_AT_K) {
      return `${(value * 100).toFixed(1)}%`;
    }
    if (value < 1) {
      return `${(value * 100).toFixed(1)}%`;
    }
    return value.toFixed(2);
  };

  if (loading) {
    return (
      <Card>
        <CardContent>
          <Box display="flex" justifyContent="center" p={4}>
            <CircularProgress />
          </Box>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardContent>
          <Alert severity="error">{error}</Alert>
        </CardContent>
      </Card>
    );
  }

  const chartData = formatChartData();
  const avgValue = data.length > 0 ? data.reduce((sum, d) => sum + d.value, 0) / data.length : 0;

  return (
    <Card>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Box>
            <Typography variant="h6" gutterBottom>
              {title}
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Average: {formatMetricValue(avgValue)}
            </Typography>
          </Box>
          <ToggleButtonGroup
            value={granularity}
            exclusive
            onChange={handleGranularityChange}
            size="small"
          >
            <ToggleButton value={TimeGranularity.HOURLY}>Hourly</ToggleButton>
            <ToggleButton value={TimeGranularity.DAILY}>Daily</ToggleButton>
            <ToggleButton value={TimeGranularity.WEEKLY}>Weekly</ToggleButton>
          </ToggleButtonGroup>
        </Box>

        <Box height={height}>
          <ResponsiveContainer width="100%" height="100%">
            {showArea ? (
              <AreaChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="timestamp" />
                <YAxis />
                <Tooltip
                  formatter={(value: number) => [formatMetricValue(value), title]}
                />
                <Legend />
                <Area
                  type="monotone"
                  dataKey="value"
                  stroke={color}
                  fill={color}
                  fillOpacity={0.3}
                  name={title}
                />
              </AreaChart>
            ) : (
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="timestamp" />
                <YAxis />
                <Tooltip
                  formatter={(value: number) => [formatMetricValue(value), title]}
                />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="value"
                  stroke={color}
                  strokeWidth={2}
                  dot={false}
                  name={title}
                />
              </LineChart>
            )}
          </ResponsiveContainer>
        </Box>

        <Box mt={2} display="flex" justifyContent="space-between">
          <Typography variant="caption" color="textSecondary">
            {data.length} data points
          </Typography>
          <Typography variant="caption" color="textSecondary">
            Last updated: {new Date().toLocaleTimeString()}
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};

export default MetricsChart;
