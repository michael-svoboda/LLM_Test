// src/index.tsx
import React from 'react';
import ReactDOM from 'react-dom';
import { ThemeProvider } from '@mui/material/styles';
import darkTheme from './theme'; // Import the dark theme
import App from './App';
import 'bootstrap/dist/css/bootstrap.min.css'; // Keep Bootstrap for layout

ReactDOM.render(
  <React.StrictMode>
    <ThemeProvider theme={darkTheme}>
      <App />
    </ThemeProvider>
  </React.StrictMode>,
  document.getElementById('root')
);

