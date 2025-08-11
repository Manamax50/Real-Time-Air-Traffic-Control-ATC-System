import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Dashboard } from './components/Dashboard';
import { CreatePlaneForm } from './components/Plane/CreatePlaneForm';
import { PlaneDetails } from './components/Plane/PlaneDetails';
import { Box, AppBar, Toolbar, Typography } from '@mui/material';

const App: React.FC = () => {
  return (
    <Router>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6">ATC System</Typography>
        </Toolbar>
      </AppBar>
      
      <Box sx={{ p: 3 }}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/create-plane" element={<CreatePlaneForm />} />
          <Route path="/plane/:planeId" element={<PlaneDetails />} />
        </Routes>
      </Box>
    </Router>
  );
};
export default App;