import React, { useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import UploadBook from './components/UploadBook';
import ProcessingStatus from './components/ProcessingStatus';
import AudiobookResult from './components/AudiobookResult';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#00bcd4',
    },
    background: {
      default: '#181c24',
      paper: '#23283a',
    },
  },
  typography: {
    fontFamily: 'Roboto, Arial, sans-serif',
  },
});

function App() {
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [isComplete, setIsComplete] = useState(false);
  const [audioResult, setAudioResult] = useState<{
    title: string;
    duration: number;
    audioUrl?: string;
  } | null>(null);

  // Fluxo simulado
  const simulateProcessing = () => {
    const steps = [25, 45, 65, 85, 100];
    let currentIndex = 0;
    const interval = setInterval(() => {
      if (currentIndex < steps.length) {
        setProgress(steps[currentIndex]);
        setCurrentStep(currentIndex);
        currentIndex++;
      } else {
        clearInterval(interval);
        setIsComplete(true);
        setLoading(false);
        setAudioResult({
          title: 'Seu Audiobook',
          duration: 1800, // 30 minutos
          audioUrl: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3'
        });
      }
    }, 1500);
  };

  const handleUpload = (file: File) => {
    setLoading(true);
    setProgress(0);
    setCurrentStep(0);
    setError(null);
    setIsComplete(false);
    setAudioResult(null);
    simulateProcessing();
  };

  const handleDownload = () => {
    if (audioResult?.audioUrl) {
      window.open(audioResult.audioUrl, '_blank');
    }
  };

  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <AppBar position="static" color="primary" elevation={2}>
        <Toolbar>
          <CloudUploadIcon sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Audiobook AI
          </Typography>
        </Toolbar>
      </AppBar>
      <Container maxWidth="md" sx={{ mt: 6 }}>
        <Paper elevation={3} sx={{ p: 4, borderRadius: 3 }}>
          <Box display="flex" flexDirection="column" alignItems="center" gap={3}>
            <Typography variant="h4" gutterBottom>
              Crie seu Audiobook com IA
            </Typography>
            <UploadBook 
              onUpload={handleUpload} 
              loading={loading} 
            />
            {loading && (
              <ProcessingStatus
                currentStep={currentStep}
                progress={progress}
                error={error}
                isComplete={isComplete}
              />
            )}
            {audioResult && (
              <AudiobookResult
                title={audioResult.title}
                duration={audioResult.duration}
                audioUrl={audioResult.audioUrl}
                onDownload={handleDownload}
              />
            )}
            {error && (
              <Typography color="error" sx={{ mt: 2 }}>{error}</Typography>
            )}
          </Box>
        </Paper>
      </Container>
    </ThemeProvider>
  );
}

export default App; 