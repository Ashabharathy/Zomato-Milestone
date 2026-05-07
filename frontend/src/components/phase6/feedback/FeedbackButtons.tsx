'use client';

import React, { useState } from 'react';
import {
  Box,
  IconButton,
  Tooltip,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Rating,
  Typography,
  Stack,
} from '@mui/material';
import {
  ThumbUp,
  ThumbDown,
  Bookmark,
  BookmarkBorder,
  Share,
  Close,
} from '@mui/icons-material';
import { FeedbackType, FeedbackSubmission } from '../../../types/phase6';
import { feedbackApi } from '../../../services/phase6';

interface FeedbackButtonsProps {
  recommendationId: string;
  restaurantId: string;
  restaurantName: string;
  userId: string;
  sessionId: string;
  onFeedbackSubmitted?: (type: FeedbackType) => void;
  size?: 'small' | 'medium' | 'large';
  showLabels?: boolean;
  vertical?: boolean;
}

const FEEDBACK_REASONS: Record<FeedbackType, string[]> = {
  [FeedbackType.LIKE]: ['Great food', 'Good ambiance', 'Excellent service', 'Perfect match', 'Will visit again'],
  [FeedbackType.DISLIKE]: ['Food was bad', 'Poor service', 'Not as described', 'Too expensive', 'Wrong location'],
  [FeedbackType.NEUTRAL]: ['Average experience', 'Nothing special', 'Mixed feelings', 'Okay but not great'],
  [FeedbackType.BOOKMARK]: ['Want to try later', 'Saving for special occasion', 'Looks interesting'],
  [FeedbackType.VISIT]: ['Visited recently', 'Plan to visit soon', 'Regular customer'],
  [FeedbackType.SKIP]: ['Not interested', 'Doesn\'t match preference', 'Already visited'],
  [FeedbackType.SHARE]: ['Recommend to friends', 'Worth sharing', 'Great find'],
  [FeedbackType.RATING]: [],
};

export const FeedbackButtons: React.FC<FeedbackButtonsProps> = ({
  recommendationId,
  restaurantId,
  restaurantName,
  userId,
  sessionId,
  onFeedbackSubmitted,
  size = 'medium',
  showLabels = true,
  vertical = false,
}) => {
  const [bookmarked, setBookmarked] = useState(false);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [selectedType, setSelectedType] = useState<FeedbackType | null>(null);
  const [rating, setRating] = useState<number | null>(null);
  const [comment, setComment] = useState('');
  const [selectedReasons, setSelectedReasons] = useState<string[]>([]);
  const [submitting, setSubmitting] = useState(false);

  const handleFeedback = async (type: FeedbackType) => {
    if (type === FeedbackType.BOOKMARK) {
      const newBookmarkState = !bookmarked;
      setBookmarked(newBookmarkState);
      
      try {
        await feedbackApi.submitFeedback({
          userId,
          sessionId,
          recommendationId,
          restaurantId,
          feedbackType: type,
        });
        onFeedbackSubmitted?.(type);
      } catch (error) {
        console.error('Error submitting bookmark:', error);
        setBookmarked(!newBookmarkState);
      }
      return;
    }

    if (type === FeedbackType.LIKE || type === FeedbackType.DISLIKE) {
      setSelectedType(type);
      setDialogOpen(true);
      return;
    }

    // For other feedback types, submit immediately
    try {
      await feedbackApi.submitFeedback({
        userId,
        sessionId,
        recommendationId,
        restaurantId,
        feedbackType: type,
      });
      onFeedbackSubmitted?.(type);
    } catch (error) {
      console.error('Error submitting feedback:', error);
    }
  };

  const handleDetailedSubmit = async () => {
    if (!selectedType) return;

    setSubmitting(true);
    try {
      await feedbackApi.submitFeedback({
        userId,
        sessionId,
        recommendationId,
        restaurantId,
        feedbackType: selectedType,
        rating: rating || undefined,
        comment: comment || undefined,
        reasons: selectedReasons.length > 0 ? selectedReasons : undefined,
      });
      onFeedbackSubmitted?.(selectedType);
      handleCloseDialog();
    } catch (error) {
      console.error('Error submitting detailed feedback:', error);
    } finally {
      setSubmitting(false);
    }
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setSelectedType(null);
    setRating(null);
    setComment('');
    setSelectedReasons([]);
  };

  const toggleReason = (reason: string) => {
    setSelectedReasons((prev) =>
      prev.includes(reason)
        ? prev.filter((r) => r !== reason)
        : [...prev, reason]
    );
  };

  const iconSize = size === 'small' ? 18 : size === 'large' ? 28 : 22;

  return (
    <>
      <Stack
        direction={vertical ? 'column' : 'row'}
        spacing={1}
        alignItems="center"
      >
        <Tooltip title="Like">
          <IconButton
            onClick={() => handleFeedback(FeedbackType.LIKE)}
            size={size}
            color="success"
          >
            <ThumbUp sx={{ fontSize: iconSize }} />
          </IconButton>
        </Tooltip>

        <Tooltip title="Dislike">
          <IconButton
            onClick={() => handleFeedback(FeedbackType.DISLIKE)}
            size={size}
            color="error"
          >
            <ThumbDown sx={{ fontSize: iconSize }} />
          </IconButton>
        </Tooltip>

        <Tooltip title={bookmarked ? 'Remove bookmark' : 'Bookmark'}>
          <IconButton
            onClick={() => handleFeedback(FeedbackType.BOOKMARK)}
            size={size}
            color={bookmarked ? 'primary' : 'default'}
          >
            {bookmarked ? (
              <Bookmark sx={{ fontSize: iconSize }} />
            ) : (
              <BookmarkBorder sx={{ fontSize: iconSize }} />
            )}
          </IconButton>
        </Tooltip>

        <Tooltip title="Share">
          <IconButton
            onClick={() => handleFeedback(FeedbackType.SHARE)}
            size={size}
          >
            <Share sx={{ fontSize: iconSize }} />
          </IconButton>
        </Tooltip>
      </Stack>

      <Dialog
        open={dialogOpen}
        onClose={handleCloseDialog}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          <Box display="flex" alignItems="center" justifyContent="space-between">
            <Typography variant="h6">
              {selectedType === FeedbackType.LIKE ? 'What did you like?' : 'What went wrong?'}
            </Typography>
            <IconButton onClick={handleCloseDialog} size="small">
              <Close />
            </IconButton>
          </Box>
        </DialogTitle>

        <DialogContent>
          <Stack spacing={3}>
            <Box>
              <Typography variant="subtitle2" gutterBottom>
                Rate your experience (optional)
              </Typography>
              <Rating
                value={rating}
                onChange={(_, value) => setRating(value)}
                size="large"
              />
            </Box>

            <Box>
              <Typography variant="subtitle2" gutterBottom>
                Select reasons (optional)
              </Typography>
              <Box display="flex" flexWrap="wrap" gap={1}>
                {selectedType &&
                  FEEDBACK_REASONS[selectedType]?.map((reason) => (
                    <Chip
                      key={reason}
                      label={reason}
                      onClick={() => toggleReason(reason)}
                      color={selectedReasons.includes(reason) ? 'primary' : 'default'}
                      variant={selectedReasons.includes(reason) ? 'filled' : 'outlined'}
                      clickable
                    />
                  ))}
              </Box>
            </Box>

            <TextField
              label="Additional comments (optional)"
              multiline
              rows={3}
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              placeholder="Tell us more about your experience..."
              fullWidth
            />
          </Stack>
        </DialogContent>

        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button
            onClick={handleDetailedSubmit}
            variant="contained"
            disabled={submitting}
          >
            {submitting ? 'Submitting...' : 'Submit Feedback'}
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default FeedbackButtons;
