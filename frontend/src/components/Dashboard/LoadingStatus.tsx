import React from 'react';
import { Paper, Typography, List, ListItem, ListItemText } from '@mui/material';
import AirportShuttleIcon from '@mui/icons-material/AirportShuttle';

interface LoadingStatusProps {
  loading: string[];
}

export const LoadingStatus: React.FC<LoadingStatusProps> = ({ loading }) => (
  <Paper elevation={3} sx={{ p: 2, mb: 2 }}>
    <Typography variant="h6" gutterBottom>
      Planes at Gates
    </Typography>
    {loading.length > 0 ? (
      <List>
        {loading.map(planeId => (
          <ListItem key={planeId}>
            <AirportShuttleIcon sx={{ mr: 2 }} />
            <ListItemText primary={planeId} />
          </ListItem>
        ))}
      </List>
    ) : (
      <Typography variant="body2" color="textSecondary">
        No planes currently at gates
      </Typography>
    )}
  </Paper>
);