import React, { useEffect, useState } from 'react';
import { 
  Box, 
  Typography, 
  CircularProgress,
  Button 
} from '@mui/material';
import axios from 'axios'; // Add this import
import { getSystemStatus, SystemStatus, API_BASE } from '../../services/atcService'; // Add API_BASE to the import
import { AirspaceStatus } from './AirspaceStatus';
import { RunwayStatus } from './RunwayStatus';
import { LoadingStatus } from './LoadingStatus';
import { PlaneLog } from './PlaneLog';
import { Link } from 'react-router-dom';

export const Dashboard: React.FC = () => {
  const [status, setStatus] = useState<SystemStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [allMessages, setAllMessages] = useState<Array<{ // Moved inside the component
    timestamp: string;
    plane_id: string;
    message: string;
  }>>([]);

    const fetchStatus = async () => {
    try {
      const [status, messages] = await Promise.all([
        getSystemStatus(),
        axios.get(`${API_BASE}/messages`).then(res => res.data.messages)
      ]);
      setStatus(status);
      setAllMessages(messages);
    } catch (err) {
      setError('Failed to fetch system status');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  if (loading) return <CircularProgress />;
  if (error) return <Typography color="error">{error}</Typography>;
  if (!status) return <Typography>No data available</Typography>;

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" gutterBottom>
          Air Traffic Control Dashboard
        </Typography>
        <Button 
          component={Link}
          to="/create-plane"
          variant="contained"
          color="primary"
        >
          Create New Plane
        </Button>
      </Box>
      
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Box sx={{ flex: 1 }}>
            <AirspaceStatus 
              airspaces={status.airspaces} 
              airplanes={status.airplanes}
            />
          </Box>
          <Box sx={{ flex: 1 }}>
            <RunwayStatus 
              runways={status.runways} 
              airplanes={status.airplanes}
            />
          </Box>
        </Box>
        
        <LoadingStatus loading={status.loading} />
      </Box>

      <Box sx={{ mt: 2 }}>
        <Typography variant="h6" gutterBottom>
          Communication Logs
        </Typography>
        <Box sx={{ 
          display: 'flex', 
          gap: 2,
          flexWrap: 'wrap',
          alignItems: 'flex-start'
        }}>
          <PlaneLog planeId="SYSTEM" messages={allMessages} />
          {status && Object.keys(status.airplanes).map(planeId => (
            <PlaneLog 
              key={planeId} 
              planeId={planeId} 
              messages={allMessages.filter(msg => msg.plane_id === planeId)} 
            />
          ))}
        </Box>
      </Box>      
    </Box>
  );
};