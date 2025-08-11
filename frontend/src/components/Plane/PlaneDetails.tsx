import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { 
  Box, 
  Typography, 
  Paper, 
  Chip,
  CircularProgress 
} from '@mui/material';
import { getPlaneDetails } from '../../services/atcService';
import AirplanemodeActiveIcon from '@mui/icons-material/AirplanemodeActive';

export const PlaneDetails: React.FC = () => {
  const { planeId } = useParams<{ planeId: string }>();
  const [plane, setPlane] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPlane = async () => {
      try {
        if (!planeId) return;
        const data = await getPlaneDetails(planeId);
        setPlane(data);
        setError(null);
      } catch (err) {
        setError('Failed to fetch plane details');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchPlane();
  }, [planeId]);

  if (loading) return <CircularProgress />;
  if (error) return <Typography color="error">{error}</Typography>;
  if (!plane) return <Typography>Plane not found</Typography>;

  return (
    <Paper elevation={3} sx={{ p: 3, maxWidth: 600, mx: 'auto' }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <AirplanemodeActiveIcon sx={{ fontSize: 40, mr: 2 }} />
        <Typography variant="h4">{planeId}</Typography>
      </Box>
      
      <Box sx={{ mb: 3 }}>
        <Typography variant="subtitle1" gutterBottom>
          Current Status
        </Typography>
        <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
          <Chip label={`State: ${plane.plane_state}`} color="primary" />
          <Chip label={`Position: ${plane.plane_position}`} />
          <Chip label={`Target: ${plane.plane_target}`} />
        </Box>
      </Box>
      
      <Box>
        <Typography variant="subtitle1" gutterBottom>
          Plane Information
        </Typography>
        <Typography>Model: {plane.plane_model || 'Unknown'}</Typography>
        <Typography>Size: {plane.plane_size || 'Unknown'} meters</Typography>
        <Typography>Passengers: {plane.plane_pascount || 'Unknown'}</Typography>
      </Box>
    </Paper>
  );
};