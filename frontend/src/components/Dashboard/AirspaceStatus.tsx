// dashboard/AirspaceStatus.tsx
import React from 'react';
import { Paper, Typography, List, ListItem, ListItemText, Box } from '@mui/material';
import AirplanemodeActiveIcon from '@mui/icons-material/AirplanemodeActive';
import { PlaneAnimation } from './PlaneAnimation';

interface AirspaceStatusProps {
  airspaces: Record<string, string | null>;
  airplanes: Record<string, any>; // Add airplanes prop
}

export const AirspaceStatus: React.FC<AirspaceStatusProps> = ({ airspaces, airplanes }) => {
  const getPlaneStatus = (planeId: string | null) => {
    if (!planeId) return 'idle';
    const plane = airplanes[planeId];
    if (!plane) return 'idle';
    
    if (plane.plane_state === 'air' && plane.plane_target.includes('runway')) {
      return 'landing';
    }
    if (plane.plane_state === 'takeoff') {
      return 'taking-off';
    }
    return 'flying';
  };

  return (
    <Paper elevation={3} sx={{ p: 2, mb: 2, position: 'relative' }}>
      <Typography variant="h6" gutterBottom>
        Airspace Status
      </Typography>
      <List>
        {Object.entries(airspaces).map(([name, planeId]) => (
          <ListItem key={name} sx={{ position: 'relative', height: 60 }}>
            {planeId && (
              <PlaneAnimation 
                status={getPlaneStatus(planeId) as any} 
                color={getPlaneStatus(planeId) === 'landing' ? 'error' : 'primary'}
              />
            )}
            <AirplanemodeActiveIcon sx={{ mr: 2 }} />
            <ListItemText
              primary={name}
              secondary={planeId || 'Empty'}
              secondaryTypographyProps={{
                color: planeId ? 'primary' : 'textSecondary'
              }}
            />
          </ListItem>
        ))}
      </List>
    </Paper>
  );
};