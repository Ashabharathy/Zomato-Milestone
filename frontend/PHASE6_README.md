# Phase 6 Next.js Implementation

## Overview

This directory contains the Next.js frontend implementation of **Phase 6: Feedback, Evaluation, and Improvement Loop** for the AI-Powered Restaurant Recommendation System.

## Architecture

Phase 6 provides a comprehensive dashboard for:
- **Feedback Collection**: UI components for collecting and analyzing user feedback
- **Metrics Tracking**: Real-time performance monitoring and analytics
- **A/B Testing**: Experiment management and results visualization
- **System Monitoring**: Alerts, health checks, and system metrics

## Directory Structure

```
frontend/src/
├── app/phase6/
│   └── page.tsx              # Main Phase 6 Dashboard page
├── components/phase6/
│   ├── feedback/
│   │   ├── FeedbackButtons.tsx    # Like/Dislike/Bookmark buttons with dialog
│   │   └── FeedbackInsights.tsx   # Feedback analytics dashboard
│   ├── metrics/
│   │   ├── MetricsChart.tsx       # Chart visualization for metrics
│   │   └── RealTimeMetrics.tsx    # Live system metrics display
│   ├── experiments/
│   │   └── ExperimentCard.tsx     # A/B test experiment cards
│   ├── monitoring/
│   │   └── AlertPanel.tsx         # System alerts and notifications
│   └── index.ts                   # Component exports
├── services/
│   └── phase6.ts                  # API integration layer
└── types/
    └── phase6.ts                  # TypeScript type definitions
```

## Components

### 1. Feedback Collection

#### FeedbackButtons
Interactive buttons for collecting user feedback:
- Like/Dislike with detailed feedback dialog
- Bookmark functionality
- Share option
- Rating input
- Reason selection chips
- Comment text area

**Props:**
```typescript
{
  recommendationId: string;
  restaurantId: string;
  restaurantName: string;
  userId: string;
  sessionId: string;
  onFeedbackSubmitted?: (type: FeedbackType) => void;
}
```

#### FeedbackInsights
Dashboard showing feedback analytics:
- Total feedback count
- Average rating
- Satisfaction rate
- Top rated restaurants
- Most discussed aspects
- Common issues and improvement areas

### 2. Metrics Tracking

#### MetricsChart
Chart component for visualizing metrics over time:
- Line charts and area charts
- Time granularity selector (hourly, daily, weekly)
- Multiple metric types supported
- Responsive design

**Supported Metrics:**
- Precision@K
- Recall@K
- Satisfaction Score
- Response Latency
- Click-Through Rate
- Conversion Rate
- And more...

#### RealTimeMetrics
Live system monitoring dashboard:
- CPU usage
- Memory usage
- Disk usage
- Response time
- Active connections
- Queue depth
- Error rate
- Real-time WebSocket updates

### 3. A/B Testing

#### ExperimentCard
Card component for displaying experiment information:
- Experiment status (Active, Paused, Completed, etc.)
- Progress indicator
- Traffic split visualization
- Winner announcement
- Start/Pause/Stop controls
- View details button

**Features:**
- Statistical significance indicators
- P-value display
- Confidence intervals
- Sample size tracking

### 4. Monitoring

#### AlertPanel
Real-time alert management panel:
- Active alerts list
- Severity indicators (Critical, High, Medium, Low)
- Acknowledge and resolve actions
- Real-time updates via WebSocket

## Services

### API Integration (`services/phase6.ts`)

Complete API layer for Phase 6 backend integration:

#### Feedback API
- `submitFeedback()` - Submit user feedback
- `submitBatchFeedback()` - Submit multiple feedback items
- `getInsights()` - Get feedback analytics
- `getAggregations()` - Get aggregated feedback data

#### Metrics API
- `getRealTimeMetrics()` - Get current system metrics
- `queryMetrics()` - Query historical metrics
- `getPerformanceReport()` - Generate performance reports
- `getTrends()` - Get metric trends

#### Experiments API
- `getExperiments()` - List all experiments
- `createExperiment()` - Create new A/B test
- `startExperiment()` - Start an experiment
- `stopExperiment()` - Stop and analyze results
- `getPromptTemplates()` - Manage prompt templates

#### Monitoring API
- `getLogs()` - View system logs
- `getAlerts()` - Get active alerts
- `acknowledgeAlert()` - Acknowledge an alert
- `getSystemHealth()` - Get health status

#### WebSocket Support
Real-time updates for:
- System metrics
- New alerts
- Experiment status changes

## TypeScript Types

Complete type definitions in `types/phase6.ts`:

### Feedback Types
- `UserFeedback` - Individual feedback item
- `FeedbackType` - Enum for feedback types
- `FeedbackSource` - Enum for feedback sources
- `FeedbackInsights` - Aggregated insights

### Metrics Types
- `MetricType` - Enum for metric types
- `MetricValue` - Individual metric data point
- `SystemPerformance` - Real-time system metrics
- `PerformanceReport` - Comprehensive report

### Experiment Types
- `Experiment` - A/B test definition
- `ExperimentStatus` - Status enum
- `ExperimentResult` - Test results
- `PromptTemplate` - Prompt template definition

### Monitoring Types
- `LogEntry` - System log entry
- `Alert` - Alert definition
- `AlertSeverity` - Severity levels
- `HealthCheck` - Component health status

## Main Dashboard Page

### Phase6DashboardPage (`app/phase6/page.tsx`)

Comprehensive dashboard with 5 tabs:

1. **Overview** - Summary cards, recent feedback, quick stats
2. **Feedback** - Full feedback insights dashboard
3. **Metrics** - Real-time metrics and historical charts
4. **A/B Testing** - Active experiments and results
5. **Monitoring** - Alerts and health checks

## Dependencies

Required packages (added to package.json):

```json
{
  "@emotion/react": "^11.11.1",
  "@emotion/styled": "^11.11.0",
  "@mui/icons-material": "^5.14.13",
  "@mui/material": "^5.14.13",
  "axios": "^1.5.0",
  "next": "^14.0.0",
  "recharts": "^2.9.0"
}
```

## Usage

### Installing Dependencies

```bash
cd frontend
npm install
```

### Running the Application

```bash
npm run dev
```

Navigate to `http://localhost:3000/phase6` to view the dashboard.

### Using Feedback Buttons

```tsx
import { FeedbackButtons } from './components/phase6';

<FeedbackButtons
  recommendationId="rec-123"
  restaurantId="rest-456"
  restaurantName="Tasty Bistro"
  userId="user-789"
  sessionId="session-abc"
  onFeedbackSubmitted={(type) => console.log('Feedback:', type)}
/>
```

### Using Metrics Chart

```tsx
import { MetricsChart } from './components/phase6';
import { MetricType } from './types/phase6';

<MetricsChart
  metricType={MetricType.SATISFACTION_SCORE}
  title="User Satisfaction"
  days={14}
/>
```

## Backend Integration

The frontend expects a REST API at `/api/v1/` with these endpoints:

### Feedback Endpoints
- `POST /feedback` - Submit feedback
- `GET /feedback/insights` - Get insights
- `GET /feedback/aggregations` - Get aggregations

### Metrics Endpoints
- `GET /metrics/realtime` - Real-time metrics
- `POST /metrics/query` - Query metrics
- `GET /metrics/report` - Performance report

### Experiments Endpoints
- `GET /experiments` - List experiments
- `POST /experiments` - Create experiment
- `POST /experiments/:id/start` - Start experiment
- `POST /experiments/:id/stop` - Stop experiment

### Monitoring Endpoints
- `GET /monitoring/logs` - Get logs
- `GET /monitoring/alerts` - Get alerts
- `GET /monitoring/health` - Health status

### WebSocket
- `ws://localhost:8000/ws/phase6` - Real-time updates

## Features

### Real-Time Updates
- WebSocket connection for live metrics
- Auto-refresh intervals for different data types
- Alert notifications in real-time

### Responsive Design
- Mobile-first approach
- Material-UI Grid system
- Collapsible panels for small screens

### Interactive Charts
- Recharts integration
- Hover tooltips
- Time range selection
- Multiple chart types

### User Experience
- Loading states with skeletons
- Error handling with alerts
- Success confirmations
- Intuitive navigation

## Customization

### Theming
Components use Material-UI's theming system. Customize colors in your theme:

```tsx
const theme = createTheme({
  palette: {
    primary: { main: '#FF6B35' },
    secondary: { main: '#C1272D' },
  },
});
```

### API Configuration
Configure API base URL via environment variable:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Next Steps

1. **Install dependencies** with `npm install`
2. **Configure backend API** URL
3. **Test components** individually
4. **Integrate with main app** navigation
5. **Add authentication** guards if needed
6. **Deploy** to production

## Support

For issues or questions:
- Check backend API connectivity
- Verify WebSocket connection
- Review browser console for errors
- Ensure all dependencies are installed

---

*Phase 6 Next.js Implementation - Complete Feedback, Evaluation, and Improvement Loop*
