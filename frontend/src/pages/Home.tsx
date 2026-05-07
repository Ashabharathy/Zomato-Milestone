import React from 'react';
import {
  Container,
  Typography,
  Box,
  Button,
  Grid,
  Card,
  CardContent,
  useTheme,
  alpha,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import RestaurantIcon from '@mui/icons-material/Restaurant';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import StarIcon from '@mui/icons-material/Star';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import PsychologyIcon from '@mui/icons-material/Psychology';

const Home: React.FC = () => {
  const theme = useTheme();
  const navigate = useNavigate();

  const features = [
    {
      icon: <LocationOnIcon sx={{ fontSize: 40, color: 'primary.main' }} />,
      title: 'Smart Location Search',
      description: 'Find restaurants near you with intelligent location-based recommendations',
    },
    {
      icon: <StarIcon sx={{ fontSize: 40, color: 'primary.main' }} />,
      title: 'AI-Powered Ratings',
      description: 'Get personalized recommendations based on your preferences and dining history',
    },
    {
      icon: <PsychologyIcon sx={{ fontSize: 40, color: 'primary.main' }} />,
      title: 'LLM Intelligence',
      description: 'Advanced AI reasoning provides detailed explanations for every recommendation',
    },
    {
      icon: <TrendingUpIcon sx={{ fontSize: 40, color: 'primary.main' }} />,
      title: 'Continuous Learning',
      description: 'System improves with every interaction to provide better recommendations',
    },
  ];

  return (
    <Box>
      {/* Hero Section */}
      <Box
        sx={{
          background: `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.8)}, ${alpha(theme.palette.secondary.main, 0.8)})`,
          color: 'white',
          py: { xs: 8, md: 12 },
          textAlign: 'center',
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        <Container maxWidth="lg">
          <RestaurantIcon sx={{ fontSize: 80, mb: 4 }} />
          <Typography
            variant="h1"
            component="h1"
            gutterBottom
            sx={{
              fontSize: { xs: '2.5rem', md: '4rem' },
              fontWeight: 'bold',
              mb: 3,
            }}
          >
            AI Restaurant Recommendations
          </Typography>
          <Typography
            variant="h4"
            component="p"
            sx={{
              fontSize: { xs: '1.2rem', md: '1.5rem' },
              mb: 4,
              maxWidth: 800,
              mx: 'auto',
              opacity: 0.9,
            }}
          >
            Discover your perfect dining experience with personalized AI-powered recommendations
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
            <Button
              variant="contained"
              size="large"
              onClick={() => navigate('/register')}
              sx={{
                px: 4,
                py: 2,
                fontSize: '1.1rem',
                backgroundColor: 'white',
                color: 'primary.main',
                '&:hover': {
                  backgroundColor: alpha(theme.palette.common.white, 0.9),
                },
              }}
            >
              Get Started
            </Button>
            <Button
              variant="outlined"
              size="large"
              onClick={() => navigate('/login')}
              sx={{
                px: 4,
                py: 2,
                fontSize: '1.1rem',
                borderColor: 'white',
                color: 'white',
                '&:hover': {
                  borderColor: 'white',
                  backgroundColor: alpha(theme.palette.common.white, 0.1),
                },
              }}
            >
              Sign In
            </Button>
          </Box>
        </Container>
      </Box>

      {/* Features Section */}
      <Container maxWidth="lg" sx={{ py: { xs: 6, md: 10 } }}>
        <Typography
          variant="h2"
          component="h2"
          textAlign="center"
          gutterBottom
          sx={{ mb: 6 }}
        >
          Why Choose Our AI Recommendations?
        </Typography>
        <Grid container spacing={4}>
          {features.map((feature, index) => (
            <Grid item xs={12} sm={6} md={3} key={index}>
              <Card
                sx={{
                  height: '100%',
                  textAlign: 'center',
                  p: 3,
                  transition: 'transform 0.2s, box-shadow 0.2s',
                  '&:hover': {
                    transform: 'translateY(-8px)',
                    boxShadow: theme.shadows[8],
                  },
                }}
              >
                <CardContent sx={{ p: 2 }}>
                  <Box sx={{ mb: 3 }}>
                    {feature.icon}
                  </Box>
                  <Typography
                    variant="h6"
                    component="h3"
                    gutterBottom
                    sx={{ fontWeight: 'bold', mb: 2 }}
                  >
                    {feature.title}
                  </Typography>
                  <Typography
                    variant="body2"
                    color="text.secondary"
                    sx={{ lineHeight: 1.6 }}
                  >
                    {feature.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* How It Works Section */}
      <Box
        sx={{
          backgroundColor: alpha(theme.palette.primary.main, 0.05),
          py: { xs: 6, md: 10 },
        }}
      >
        <Container maxWidth="lg">
          <Typography
            variant="h2"
            component="h2"
            textAlign="center"
            gutterBottom
            sx={{ mb: 6 }}
          >
            How It Works
          </Typography>
          <Grid container spacing={4} alignItems="center">
            <Grid item xs={12} md={6}>
              <Typography variant="h4" component="h3" gutterBottom sx={{ mb: 3 }}>
                Simple Steps to Perfect Recommendations
              </Typography>
              <Box sx={{ mb: 3 }}>
                <Typography variant="h6" component="p" gutterBottom>
                  <strong>1. Tell Us Your Preferences</strong>
                </Typography>
                <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
                  Share your location, budget, cuisine preferences, and dietary requirements
                </Typography>
              </Box>
              <Box sx={{ mb: 3 }}>
                <Typography variant="h6" component="p" gutterBottom>
                  <strong>2. AI Analysis</strong>
                </Typography>
                <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
                  Our advanced AI analyzes thousands of restaurants to find the perfect matches
                </Typography>
              </Box>
              <Box sx={{ mb: 3 }}>
                <Typography variant="h6" component="p" gutterBottom>
                  <strong>3. Get Personalized Recommendations</strong>
                </Typography>
                <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
                  Receive detailed recommendations with explanations for each choice
                </Typography>
              </Box>
              <Button
                variant="contained"
                size="large"
                onClick={() => navigate('/register')}
                sx={{ mt: 2 }}
              >
                Start Your Journey
              </Button>
            </Grid>
            <Grid item xs={12} md={6}>
              <Box
                sx={{
                  display: 'flex',
                  justifyContent: 'center',
                  alignItems: 'center',
                  height: '100%',
                }}
              >
                <Card
                  sx={{
                    p: 4,
                    background: `linear-gradient(135deg, ${theme.palette.primary.light}, ${theme.palette.secondary.light})`,
                    color: 'white',
                    textAlign: 'center',
                  }}
                >
                  <PsychologyIcon sx={{ fontSize: 80, mb: 2 }} />
                  <Typography variant="h5" component="p" gutterBottom>
                    Powered by Advanced AI
                  </Typography>
                  <Typography variant="body1">
                    Our recommendation engine uses cutting-edge LLM technology to understand your preferences and provide truly personalized dining experiences.
                  </Typography>
                </Card>
              </Box>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* CTA Section */}
      <Container maxWidth="md" sx={{ py: { xs: 6, md: 8 } }}>
        <Card
          sx={{
            textAlign: 'center',
            p: { xs: 4, md: 6 },
            background: `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.1)}, ${alpha(theme.palette.secondary.main, 0.1)})`,
          }}
        >
          <Typography variant="h3" component="h2" gutterBottom sx={{ mb: 3 }}>
            Ready to Discover Your Next Favorite Restaurant?
          </Typography>
          <Typography variant="h6" component="p" color="text.secondary" sx={{ mb: 4 }}>
            Join thousands of users who have found their perfect dining experiences with our AI-powered recommendations.
          </Typography>
          <Button
            variant="contained"
            size="large"
            onClick={() => navigate('/register')}
            sx={{
              px: 6,
              py: 2,
              fontSize: '1.2rem',
            }}
          >
            Get Started Now
          </Button>
        </Card>
      </Container>
    </Box>
  );
};

export default Home;
