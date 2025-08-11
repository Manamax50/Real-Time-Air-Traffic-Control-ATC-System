import React, { useState } from 'react';
import { 
  Box, 
  Typography, 
  TextField, 
  Button, 
  Select, 
  MenuItem, 
  FormControl, 
  InputLabel, 
  Paper 
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { createPlane } from '../../services/atcService';

export const CreatePlaneForm: React.FC = () => {
  const [planeId, setPlaneId] = useState('');
  const [state, setState] = useState<'air' | 'ground'>('air');
  const [position, setPosition] = useState('outer_airspace');
  const [target, setTarget] = useState('runway_1');
  const [originCountry, setOriginCountry] = useState('');
  const [destinationCountry, setDestinationCountry] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      await createPlane({
        plane_id: planeId,
        state,
        position,
        target,
        origin_country: state === 'air' ? originCountry : undefined,
        destination_country: destinationCountry,
        plane_model: 'Unknown', // These can be made into form fields if needed
        plane_size: 0,
        plane_pascount: 0
      });
      navigate('/');
    } catch (err) {
      setError('Failed to create plane. Please check your inputs.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleStateChange = (newState: 'air' | 'ground') => {
    setState(newState);
    setPosition(newState === 'air' ? 'outer_airspace' : 'loading');
    setTarget('runway_1'); // Reset to default
    if (newState === 'ground') {
      setOriginCountry(''); // Clear origin country if switching to ground
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 3, maxWidth: 500, mx: 'auto' }}>
      <Typography variant="h5" gutterBottom>
        Create New Plane
      </Typography>
      
      {error && (
        <Typography color="error" sx={{ mb: 2 }}>
          {error}
        </Typography>
      )}
      
      <Box component="form" onSubmit={handleSubmit}>
        <TextField
          label="Plane ID"
          value={planeId}
          onChange={(e) => setPlaneId(e.target.value)}
          fullWidth
          required
          margin="normal"
        />
        
        <FormControl fullWidth margin="normal">
          <InputLabel>State</InputLabel>
          <Select
            value={state}
            onChange={(e) => handleStateChange(e.target.value as 'air' | 'ground')}
            label="State"
            required
          >
            <MenuItem value="air">Air</MenuItem>
            <MenuItem value="ground">Ground</MenuItem>
          </Select>
        </FormControl>
        
        {state === 'air' && (
          <TextField
            label="Origin Country"
            value={originCountry}
            onChange={(e) => setOriginCountry(e.target.value)}
            fullWidth
            required={state === 'air'}
            margin="normal"
          />
        )}
        
        <TextField
          label="Destination Country"
          value={destinationCountry}
          onChange={(e) => setDestinationCountry(e.target.value)}
          fullWidth
          required
          margin="normal"
        />
        
        <TextField
          label="Position"
          value={position}
          disabled
          fullWidth
          margin="normal"
        />
        
        <TextField
          label="Default Runway"
          value={target}
          disabled
          fullWidth
          margin="normal"
        />
        
        <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end' }}>
          <Button 
            type="submit" 
            variant="contained" 
            disabled={loading}
          >
            {loading ? 'Creating...' : 'Create Plane'}
          </Button>
        </Box>
      </Box>
    </Paper>
  );
};