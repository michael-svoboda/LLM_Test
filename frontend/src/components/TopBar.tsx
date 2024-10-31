import React from 'react';
import { AppBar, Toolbar, Typography, IconButton } from '@mui/material';
import { Chat as ChatIcon, Upload as UploadIcon } from '@mui/icons-material';

const TopBar: React.FC<{ setPage: (page: string) => void }> = ({ setPage }) => (
  <AppBar position="fixed" sx={{ height: 64 }}> {/* Fixed height */}
    <Toolbar>
      <Typography variant="h6" sx={{ flexGrow: 1 }}>
        LLM App
      </Typography>
      <IconButton color="inherit" onClick={() => setPage('chat')}>
        <ChatIcon />
      </IconButton>
      <IconButton color="inherit" onClick={() => setPage('upload')}>
        <UploadIcon />
      </IconButton>
    </Toolbar>
  </AppBar>
);

export default TopBar;

