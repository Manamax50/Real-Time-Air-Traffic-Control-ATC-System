import React, { useEffect } from 'react';
import { Paper, Typography, List, ListItem, ListItemText, Box, Chip } from '@mui/material';

interface PlaneLogProps {
  planeId: string;
  messages: Array<{
    timestamp: string;
    plane_id: string;
    message: string;
  }>;
}

export const PlaneLog: React.FC<PlaneLogProps> = ({ planeId, messages }) => {
  // Filter messages for the current plane
  const filteredMessages = messages.filter(msg => msg.plane_id === planeId);

  // Cleanup effect to remove messages when component unmounts
  useEffect(() => {
    return () => {
      // Implement logic to remove messages for the plane when it exits
      // This can be done by updating the parent state to remove the plane's messages
      console.log(`Cleaning up messages for plane ${planeId}`);
    };
  }, [planeId]);

  // Only render if there are messages for the plane
  if (filteredMessages.length === 0) {
    return null;
  }

  return (
    <Paper elevation={3} sx={{ p: 2, mb: 2, flex: 1, minWidth: 300 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
        <Chip 
          label={planeId} 
          color="primary" 
          size="small" 
          sx={{ mr: 1 }} 
        />
        <Typography variant="subtitle2">
          {filteredMessages.length} messages
        </Typography>
      </Box>
      <List sx={{ maxHeight: 200, overflow: 'auto' }}>
        {filteredMessages.map((msg, index) => (
          <ListItem key={index} sx={{ py: 0.5 }}>
            <ListItemText
              primary={msg.message}
              secondary={msg.timestamp}
              primaryTypographyProps={{ variant: 'body2' }}
              secondaryTypographyProps={{ variant: 'caption' }}
            />
          </ListItem>
        ))}
      </List>
    </Paper>
  );
};