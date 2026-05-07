/**
 * Color theme configuration based on screen designs
 */

export const colors = {
  primary: {
    main: '#FF6B35',      // Primary orange from screens
    light: '#FF8A65',      // Light orange
    dark: '#E55100',       // Dark orange
    gradient: 'linear-gradient(135deg, #FF6B35 0%, #FF8A65 100%)',
  },
  secondary: {
    main: '#2E7D32',      // Secondary green
    light: '#4CAF50',      // Light green
    dark: '#1B5E20',      // Dark green
  },
  background: {
    primary: '#FFFFFF',      // White background
    secondary: '#F5F5F5',    // Light gray
    dark: '#1A1A1A',      // Dark background
  },
  text: {
    primary: '#212121',      // Dark text
    secondary: '#666666',    // Gray text
    light: '#FFFFFF',      // White text
    muted: '#999999',      // Muted text
  },
  accent: {
    blue: '#2196F3',       // Accent blue
    purple: '#9C27B0',      // Accent purple
    pink: '#E91E63',       // Accent pink
    yellow: '#FFC107',      // Accent yellow
  },
  semantic: {
    success: '#4CAF50',      // Success green
    warning: '#FF9800',      // Warning orange
    error: '#F44336',       // Error red
    info: '#2196F3',       // Info blue
  },
  restaurant: {
    card: '#FFFFFF',      // Restaurant card background
    rating: '#FFC107',      // Rating stars
    price: '#4CAF50',       // Price indicator
    cuisine: '#9C27B0',      // Cuisine tags
  },
  recommendation: {
    card: '#F8F9FA',      // Recommendation card
    badge: '#FF6B35',      // Recommendation badge
    explanation: '#E3F2FD',     // Explanation background
  },
  feedback: {
    like: '#4CAF50',       // Like button
    dislike: '#F44336',      // Dislike button
    bookmark: '#FFC107',      // Bookmark button
    share: '#2196F3',       // Share button
  },
  charts: {
    line: '#FF6B35',       // Chart lines
    fill: '#FF8A65',       // Chart fills
    grid: '#E0E0E0',       // Chart grid
  },
  ui: {
    border: '#E0E0E0',      // UI borders
    shadow: 'rgba(0, 0, 0, 0.1)', // UI shadows
    hover: 'rgba(255, 107, 14, 0.1)', // Hover states
  },
} as const;

export type ColorKeys = keyof typeof colors;
export type ColorShades = typeof colors.primary;
