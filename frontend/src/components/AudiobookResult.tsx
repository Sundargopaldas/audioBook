import React from 'react';
import { Box, Typography, Button } from '@mui/material';

interface AudiobookResultProps {
  title: string;
  duration: number; // em segundos
  audioUrl?: string;
  onDownload?: () => void;
}

function formatDuration(seconds: number) {
  const min = Math.floor(seconds / 60);
  const sec = seconds % 60;
  return `${min}m ${sec}s`;
}

const AudiobookResult: React.FC<AudiobookResultProps> = ({ title, duration, audioUrl, onDownload }) => {
  return (
    <Box textAlign="center" mt={4}>
      <Typography variant="h5" gutterBottom>{title}</Typography>
      <Typography variant="body2" color="text.secondary" gutterBottom>
        Duração: {formatDuration(duration)}
      </Typography>
      {audioUrl && (
        <audio controls src={audioUrl} style={{ width: '100%', margin: '16px 0' }} />
      )}
      {onDownload && (
        <Button variant="contained" color="secondary" onClick={onDownload}>
          Baixar Audiobook
        </Button>
      )}
    </Box>
  );
};

export default AudiobookResult; 