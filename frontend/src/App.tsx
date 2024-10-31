import React, { useState } from 'react';
import ChatPage from './pages/ChatPage';
import UploadPage from './pages/UploadPage';
import TopBar from './components/TopBar';
import { Box } from '@mui/material';
import './App.css';

const App: React.FC = () => {
  const [page, setPage] = useState('chat');

  return (
    <Box sx={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <TopBar setPage={setPage} />
      {page === 'chat' ? <ChatPage /> : <UploadPage />}
    </Box>
  );
};

export default App;

