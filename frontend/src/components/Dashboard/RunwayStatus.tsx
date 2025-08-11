// dashboard/RunwayStatus.tsx
import React from 'react';
import { Paper, Typography, List, ListItem, ListItemText, Box } from '@mui/material';
import DirectionsRunIcon from '@mui/icons-material/DirectionsRun';
import { PlaneAnimation } from './PlaneAnimation';

interface RunwayStatusProps {
  runways: Record<string, string | null>;
  airplanes: Record<string, any>; // Add airplanes prop
}

export const RunwayStatus: React.FC<RunwayStatusProps> = ({ runways, airplanes }) => {
  const getPlaneStatus = (planeId: string | null) => {
    if (!planeId) return 'idle';
    const plane = airplanes[planeId];
    if (!plane) return 'idle';
    
    if (plane.plane_state === 'landing') {
      return 'landing';
    }
    if (plane.plane_state === 'taxiing') {
      return 'taxiing';
    }
    return 'idle';
  };

  return (
    <Paper elevation={3} sx={{ p: 2, mb: 2, position: 'relative' }}>
      <Typography variant="h6" gutterBottom>
        Runway Status
      </Typography>
      <List>
        {Object.entries(runways).map(([name, planeId]) => (
          <ListItem key={name} sx={{ position: 'relative', height: 60 }}>
            {planeId && (
              <PlaneAnimation 
                status={getPlaneStatus(planeId) as any}
                color={getPlaneStatus(planeId) === 'landing' ? 'error' : 'secondary'}
              />
            )}
            <DirectionsRunIcon sx={{ mr: 2 }} />
            <ListItemText
              primary={name}
              secondary={planeId || 'Empty'}
              secondaryTypographyProps={{
                color: planeId ? 'secondary' : 'textSecondary'
              }}
            />
          </ListItem>
        ))}
      </List>
    </Paper>
  );
};