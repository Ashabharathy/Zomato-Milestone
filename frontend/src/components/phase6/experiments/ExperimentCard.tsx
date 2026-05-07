'use client';

import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  LinearProgress,
  Button,
  IconButton,
  Tooltip,
  Divider,
  Grid,
} from '@mui/material';
import {
  PlayArrow,
  Pause,
  Stop,
  Visibility,
  Science,
  TrendingUp,
  Group,
  CalendarToday,
} from '@mui/icons-material';
import { Experiment, ExperimentStatus, ExperimentResult } from '../../../types/phase6';

interface ExperimentCardProps {
  experiment: Experiment;
  result?: ExperimentResult;
  onViewDetails: (experimentId: string) => void;
  onStart?: (experimentId: string) => void;
  onPause?: (experimentId: string) => void;
  onStop?: (experimentId: string) => void;
}

export const ExperimentCard: React.FC<ExperimentCardProps> = ({
  experiment,
  result,
  onViewDetails,
  onStart,
  onPause,
  onStop,
}) => {
  const getStatusColor = (status: ExperimentStatus) => {
    switch (status) {
      case ExperimentStatus.ACTIVE:
        return 'success';
      case ExperimentStatus.PAUSED:
        return 'warning';
      case ExperimentStatus.COMPLETED:
        return 'info';
      case ExperimentStatus.FAILED:
        return 'error';
      default:
        return 'default';
    }
  };

  const getStatusIcon = (status: ExperimentStatus) => {
    switch (status) {
      case ExperimentStatus.ACTIVE:
        return <TrendingUp />;
      case ExperimentStatus.PAUSED:
        return <Pause />;
      case ExperimentStatus.COMPLETED:
        return <Science />;
      default:
        return <Science />;
    }
  };

  const progress = Math.min((experiment.sampleSize / experiment.targetSampleSize) * 100, 100);

  return (
    <Card variant="outlined">
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
          <Box>
            <Typography variant="h6" component="div" gutterBottom>
              {experiment.name}
            </Typography>
            <Typography variant="body2" color="textSecondary">
              {experiment.description}
            </Typography>
          </Box>
          <Chip
            icon={getStatusIcon(experiment.status)}
            label={experiment.status.toUpperCase()}
            color={getStatusColor(experiment.status)}
            size="small"
          />
        </Box>

        <Grid container spacing={2} mb={2}>
          <Grid item xs={6}>
            <Box display="flex" alignItems="center">
              <Group fontSize="small" color="action" sx={{ mr: 1 }} />
              <Typography variant="body2" color="textSecondary">
                {experiment.sampleSize.toLocaleString()} / {experiment.targetSampleSize.toLocaleString()} users
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={6}>
            <Box display="flex" alignItems="center">
              <CalendarToday fontSize="small" color="action" sx={{ mr: 1 }} />
              <Typography variant="body2" color="textSecondary">
                {experiment.startDate
                  ? new Date(experiment.startDate).toLocaleDateString()
                  : 'Not started'}
              </Typography>
            </Box>
          </Grid>
        </Grid>

        {/* Progress Bar */}
        <Box mb={2}>
          <Box display="flex" justifyContent="space-between" mb={1}>
            <Typography variant="body2" color="textSecondary">
              Progress
            </Typography>
            <Typography variant="body2" fontWeight="bold">
              {progress.toFixed(0)}%
            </Typography>
          </Box>
          <LinearProgress
            variant="determinate"
            value={progress}
            sx={{ height: 8, borderRadius: 4 }}
          />
        </Box>

        {/* Traffic Split */}
        <Box mb={2}>
          <Typography variant="body2" color="textSecondary" gutterBottom>
            Traffic Split
          </Typography>
          <Box display="flex" gap={1}>
            {Object.entries(experiment.trafficSplit).map(([variant, percentage]) => (
              <Chip
                key={variant}
                label={`${variant}: ${(percentage * 100).toFixed(0)}%`}
                size="small"
                variant="outlined"
              />
            ))}
          </Box>
        </Box>

        {/* Results Preview */}
        {result && result.statisticalSignificance && (
          <Box mb={2} p={2} bgcolor="success.light" borderRadius={1}>
            <Typography variant="body2" color="success.dark" fontWeight="bold">
              Winner: {result.winner}
            </Typography>
            <Typography variant="caption" color="success.dark">
              P-value: {result.pValue.toFixed(4)} | Confidence: {(result.confidenceInterval * 100).toFixed(0)}%
            </Typography>
          </Box>
        )}

        <Divider sx={{ my: 2 }} />

        {/* Actions */}
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Box>
            {experiment.status === ExperimentStatus.DRAFT && (
              <Button
                variant="contained"
                size="small"
                startIcon={<PlayArrow />}
                onClick={() => onStart?.(experiment.id)}
              >
                Start
              </Button>
            )}
            {experiment.status === ExperimentStatus.ACTIVE && (
              <>
                <Tooltip title="Pause">
                  <IconButton
                    size="small"
                    color="warning"
                    onClick={() => onPause?.(experiment.id)}
                    sx={{ mr: 1 }}
                  >
                    <Pause />
                  </IconButton>
                </Tooltip>
                <Tooltip title="Stop">
                  <IconButton
                    size="small"
                    color="error"
                    onClick={() => onStop?.(experiment.id)}
                  >
                    <Stop />
                  </IconButton>
                </Tooltip>
              </>
            )}
            {experiment.status === ExperimentStatus.PAUSED && (
              <Button
                variant="contained"
                size="small"
                startIcon={<PlayArrow />}
                onClick={() => onStart?.(experiment.id)}
              >
                Resume
              </Button>
            )}
          </Box>

          <Button
            variant="outlined"
            size="small"
            startIcon={<Visibility />}
            onClick={() => onViewDetails(experiment.id)}
          >
            View Details
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
};

export default ExperimentCard;
