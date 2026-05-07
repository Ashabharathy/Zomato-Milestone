'use client';

import React, { useEffect, useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Chip,
  IconButton,
  Button,
  Alert,
  CircularProgress,
  Badge,
} from '@mui/material';
import {
  Notifications,
  CheckCircle,
  Error,
  Warning,
  Info,
  Check,
  Delete,
} from '@mui/icons-material';
import { Alert as AlertType, AlertSeverity } from '../../../types/phase6';
import { monitoringApi, phase6WebSocket } from '../../../services/phase6';

export const AlertPanel: React.FC = () => {
  const [alerts, setAlerts] = useState<AlertType[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchAlerts();

    // Subscribe to real-time alerts
    phase6WebSocket.subscribe('alert', (data) => {
      setAlerts((prev) => [data as AlertType, ...prev]);
    });

    // Refresh every minute
    const interval = setInterval(fetchAlerts, 60000);
    return () => clearInterval(interval);
  }, []);

  const fetchAlerts = async () => {
    try {
      const data = await monitoringApi.getAlerts(true);
      setAlerts(data);
      setError(null);
    } catch (err) {
      setError('Failed to load alerts');
      console.error('Error fetching alerts:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAcknowledge = async (alertId: string) => {
    try {
      await monitoringApi.acknowledgeAlert(alertId);
      setAlerts((prev) =>
        prev.map((alert) =>
          alert.id === alertId
            ? { ...alert, acknowledgedAt: new Date().toISOString() }
            : alert
        )
      );
    } catch (err) {
      console.error('Error acknowledging alert:', err);
    }
  };

  const handleResolve = async (alertId: string) => {
    try {
      await monitoringApi.resolveAlert(alertId);
      setAlerts((prev) => prev.filter((alert) => alert.id !== alertId));
    } catch (err) {
      console.error('Error resolving alert:', err);
    }
  };

  const getSeverityIcon = (severity: AlertSeverity) => {
    switch (severity) {
      case AlertSeverity.CRITICAL:
        return <Error color="error" />;
      case AlertSeverity.HIGH:
        return <Warning color="error" />;
      case AlertSeverity.MEDIUM:
        return <Warning color="warning" />;
      case AlertSeverity.LOW:
        return <Info color="info" />;
      default:
        return <Info color="info" />;
    }
  };

  const getSeverityColor = (severity: AlertSeverity) => {
    switch (severity) {
      case AlertSeverity.CRITICAL:
        return 'error';
      case AlertSeverity.HIGH:
        return 'error';
      case AlertSeverity.MEDIUM:
        return 'warning';
      case AlertSeverity.LOW:
        return 'info';
      default:
        return 'default';
    }
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

  const criticalCount = alerts.filter((a) => a.severity === AlertSeverity.CRITICAL).length;
  const activeCount = alerts.filter((a) => !a.acknowledgedAt).length;

  return (
    <Card>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Box display="flex" alignItems="center">
            <Badge badgeContent={activeCount} color="error" sx={{ mr: 2 }}>
              <Notifications color="action" />
            </Badge>
            <Typography variant="h6">Active Alerts</Typography>
          </Box>
          {criticalCount > 0 && (
            <Chip
              label={`${criticalCount} Critical`}
              color="error"
              size="small"
            />
          )}
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {alerts.length === 0 ? (
          <Box textAlign="center" py={4}>
            <CheckCircle color="success" sx={{ fontSize: 48, mb: 2 }} />
            <Typography color="textSecondary">
              No active alerts
            </Typography>
          </Box>
        ) : (
          <List dense>
            {alerts.slice(0, 10).map((alert) => (
              <ListItem
                key={alert.id}
                secondaryAction={
                  !alert.acknowledgedAt && (
                    <Box>
                      <Tooltip title="Acknowledge">
                        <IconButton
                          edge="end"
                          size="small"
                          onClick={() => handleAcknowledge(alert.id)}
                          sx={{ mr: 1 }}
                        >
                          <Check />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Resolve">
                        <IconButton
                          edge="end"
                          size="small"
                          onClick={() => handleResolve(alert.id)}
                        >
                          <Delete />
                        </IconButton>
                      </Tooltip>
                    </Box>
                  )
                }
              >
                <ListItemIcon>
                  {getSeverityIcon(alert.severity)}
                </ListItemIcon>
                <ListItemText
                  primary={
                    <Box display="flex" alignItems="center" gap={1}>
                      <Typography variant="body2" fontWeight="bold">
                        {alert.name}
                      </Typography>
                      <Chip
                        label={alert.severity}
                        size="small"
                        color={getSeverityColor(alert.severity)}
                      />
                    </Box>
                  }
                  secondary={
                    <>
                      <Typography variant="caption" display="block">
                        {alert.description}
                      </Typography>
                      <Typography variant="caption" color="textSecondary">
                        Current: {alert.currentValue} | Threshold: {alert.threshold}
                      </Typography>
                    </>
                  }
                />
              </ListItem>
            ))}
          </List>
        )}

        {alerts.length > 10 && (
          <Box textAlign="center" mt={2}>
            <Button variant="text" size="small">
              View all {alerts.length} alerts
            </Button>
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default AlertPanel;
