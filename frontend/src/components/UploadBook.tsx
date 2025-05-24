import React, { useRef } from 'react';
import { Button, Box, Typography } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

interface UploadBookProps {
  onUpload: (file: File) => void;
  loading?: boolean;
}

const UploadBook: React.FC<UploadBookProps> = ({ onUpload, loading }) => {
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      onUpload(e.target.files[0]);
    }
  };

  return (
    <Box display="flex" flexDirection="column" alignItems="center" gap={2}>
      <input
        type="file"
        accept=".pdf,.docx,.txt"
        style={{ display: 'none' }}
        ref={inputRef}
        onChange={handleFileChange}
        disabled={loading}
      />
      <Button
        variant="contained"
        color="primary"
        startIcon={<CloudUploadIcon />}
        onClick={() => inputRef.current?.click()}
        disabled={loading}
        sx={{ minWidth: 200 }}
      >
        {loading ? 'Enviando...' : 'Enviar Livro/Capítulo'}
      </Button>
      <Typography variant="body2" color="text.secondary">
        Aceita PDF, DOCX ou TXT
      </Typography>
    </Box>
  );
};

export default UploadBook; 