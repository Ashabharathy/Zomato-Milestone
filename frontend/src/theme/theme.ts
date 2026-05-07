/**
 * Theme configuration for Restaurant Recommendation System
 */

import { colors } from './colors';

export const theme = {
  palette: {
    mode: 'light' as const,
    primary: {
      main: colors.primary.main,
      light: colors.primary.light,
      dark: colors.primary.dark,
      contrastText: '#FFFFFF',
    },
    secondary: {
      main: colors.secondary.main,
      light: colors.secondary.light,
      dark: colors.secondary.dark,
      contrastText: '#FFFFFF',
    },
    background: {
      default: colors.background.primary,
      paper: colors.background.secondary,
    },
    text: {
      primary: colors.text.primary,
      secondary: colors.text.secondary,
      disabled: colors.text.muted,
    },
    error: {
      main: colors.semantic.error,
    },
    warning: {
      main: colors.semantic.warning,
    },
    info: {
      main: colors.semantic.info,
    },
    success: {
      main: colors.semantic.success,
    },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundColor: colors.restaurant.card,
          boxShadow: colors.ui.shadow,
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          backgroundColor: colors.primary.main,
          '&:hover': {
            backgroundColor: colors.primary.light,
          },
        },
      },
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 600,
      color: colors.text.primary,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 500,
      color: colors.text.primary,
    },
    h3: {
      fontSize: '1.5rem',
      fontWeight: 500,
      color: colors.text.secondary,
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.6,
      color: colors.text.primary,
    },
    body2: {
      fontSize: '0.875rem',
      lineHeight: 1.5,
      color: colors.text.secondary,
    },
  },
  breakpoints: {
    values: {
      xs: 0,
      sm: 600,
      md: 960,
      lg: 1280,
      xl: 1920,
    },
  },
};

export type Theme = typeof theme;
export default theme;
