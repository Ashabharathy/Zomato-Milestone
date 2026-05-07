'use client';

import React, { useEffect, useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Chip,
  LinearProgress,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  Alert,
  CircularProgress,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  TrendingFlat,
  Star,
  SentimentSatisfied,
  SentimentDissatisfied,
  SentimentNeutral,
  ThumbUp,
} from '@mui/icons-material';
import { FeedbackInsights as FeedbackInsightsType } from '../../../types/phase6';
import { feedbackApi } from '../../../services/phase6';

interface FeedbackInsightsProps {
  refreshInterval?: number; // in seconds
}

export const FeedbackInsights: React.FC<FeedbackInsightsProps> = ({
  refreshInterval = 300, // 5 minutes default
}) => {
  const [insights, setInsights] = useState<FeedbackInsightsType | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchInsights();

    if (refreshInterval > 0) {
      const interval = setInterval(fetchInsights, refreshInterval * 1000);
      return () => clearInterval(interval);
    }
  }, [refreshInterval]);

  const fetchInsights = async () => {
    try {
      const data = await feedbackApi.getInsights();
      setInsights(data);
      setError(null);
    } catch (err) {
      setError('Failed to load feedback insights');
      console.error('Error fetching insights:', err);
    } finally {
      setLoading(false);
    }
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

  if (!insights) {
    return (
      <Alert severity="info" sx={{ m: 2 }}>
        No feedback data available
      </Alert>
    );
  }

  const getSentimentIcon = (sentiment: string) => {
    switch (sentiment) {
      case 'positive':
        return <SentimentSatisfied color="success" />;
      case 'negative':
        return <SentimentDissatisfied color="error" />;
      default:
        return <SentimentNeutral color="warning" />;
    }
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom fontWeight="bold">
        Feedback Insights
      </Typography>

      <Grid container spacing={3}>
        {/* Summary Cards */}
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Feedback
              </Typography>
              <Typography variant="h3" component="div">
                {insights.totalFeedback.toLocaleString()}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Average Rating
              </Typography>
              <Box display="flex" alignItems="center">
                <Typography variant="h3" component="div">
                  {insights.averageRating.toFixed(1)}
                </Typography>
                <Star color="warning" sx={{ ml: 1 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Satisfaction Rate
              </Typography>
              <Typography variant="h3" component="div" color="success.main">
                {insights.satisfactionRate.toFixed(1)}%
              </Typography>
              <LinearProgress
                variant="determinate"
                value={insights.satisfactionRate}
                color="success"
                sx={{ mt: 1 }}
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Feedback Rate
              </Typography>
              <Typography variant="h3" component="div">
                {insights.userEngagementMetrics.feedbackRate.toFixed(1)}%
              </Typography>
              <Typography variant="caption" color="textSecondary">
                Response rate: {insights.userEngagementMetrics.responseRate.toFixed(1)}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Top Rated Restaurants */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Top Rated Restaurants
              </Typography>
              <List dense>
                {insights.topRatedRestaurants.map((restaurant, index) => (
                  <ListItem key={restaurant.restaurantId}>
                    <ListItemIcon>
                      <Chip
                        label={`#${index + 1}`}
                        size="small"
                        color={index < 3 ? 'primary' : 'default'}
                      />
                    </ListItemIcon>
                    <ListItemText
                      primary={restaurant.name}
                      secondary={`${restaurant.rating} ★ • ${restaurant.reviewCount} reviews`}
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Most Discussed Aspects */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Most Discussed Aspects
              </Typography>
              <List dense>
                {insights.mostDiscussedAspects.map((aspect) => (
                  <ListItem key={aspect.aspect}>
                    <ListItemIcon>{getSentimentIcon(aspect.sentiment)}</ListItemIcon>
                    <ListItemText
                      primary={aspect.aspect}
                      secondary={`${aspect.count} mentions`}
                    />
                    <Chip
                      label={aspect.sentiment}
                      size="small"
                      color={
                        aspect.sentiment === 'positive'
                          ? 'success'
                          : aspect.sentiment === 'negative'
                          ? 'error'
                          : 'warning'
                      }
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Common Issues */}
        {insights.commonIssues.length > 0 && (
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom color="error">
                  Common Issues
                </Typography>
                <List dense>
                  {insights.commonIssues.map((issue, index) => (
                    <ListItem key={index}>
                      <ListItemIcon>
                        <TrendingDown color="error" />
                      </ListItemIcon>
                      <ListItemText primary={issue} />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Grid>
        )}

        {/* Improvement Areas */}
        {insights.improvementAreas.length > 0 && (
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom color="info">
                  Improvement Opportunities
                </Typography>
                <List dense>
                  {insights.improvementAreas.map((area, index) => (
                    <ListItem key={index}>
                      <ListItemIcon>
                        <TrendingUp color="info" />
                      </ListItemIcon>
                      <ListItemText primary={area} />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Grid>
        )}
      </Grid>
    </Box>
  );
};

export default FeedbackInsights;
