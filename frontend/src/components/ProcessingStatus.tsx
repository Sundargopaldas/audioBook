import React from 'react';
import { Box, LinearProgress, Typography } from '@mui/material';

interface ProcessingStatusProps {
  currentStep: number;
  progress: number;
  error?: string | null;
  isComplete?: boolean;
}

const steps = [
  'Analisando arquivo',
  'Extraindo texto',
  'Gerando narração',
  'Adicionando trilha sonora',
  'Finalizando audiobook'
];

const ProcessingStatus: React.FC<ProcessingStatusProps> = ({ currentStep, progress, error, isComplete }) => {
  if (error) {
    return (
      <Box textAlign="center" color="error.main">
        <Typography variant="h6">Erro: {error}</Typography>
      </Box>
    );
  }
  if (isComplete) {
    return (
      <Box textAlign="center" color="success.main">
        <Typography variant="h6">Audiobook gerado com sucesso!</Typography>
      </Box>
    );
  }
  return (
    <Box width="100%" mt={2}>
      <Typography variant="body1" gutterBottom>
        {steps[currentStep] || 'Processando...'}
      </Typography>
      <LinearProgress variant="determinate" value={progress} />
      <Typography variant="body2" color="text.secondary" mt={1}>
        {progress}%
      </Typography>
    </Box>
  );
};

export default ProcessingStatus; 