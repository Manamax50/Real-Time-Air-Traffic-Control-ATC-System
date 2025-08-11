import React, { useEffect, useState } from 'react';
import { Paper, Typography, List, ListItem, ListItemText } from '@mui/material';
import { getMessages } from '../../services/atcService';

export const MessageLog: React.FC = () => {
  const [messages, setMessages] = useState<string[]>([]);

  const fetchMessages = async () => {
    try {
      const data = await getMessages();
      setMessages(data.reverse()); // Show newest first
    } catch (err) {
      console.error('Failed to fetch messages', err);
    }
  };

  useEffect(() => {
    fetchMessages();
    const interval = setInterval(fetchMessages, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <Paper elevation={3} sx={{ p: 2, mt: 2 }}>
      <Typography variant="h6" gutterBottom>
        ATC Activity Log
      </Typography>
      <List sx={{ maxHeight: 200, overflow: 'auto' }}>
        {messages.length > 0 ? (
          messages.map((msg, index) => (
            <ListItem key={index} sx={{ py: 0.5 }}>
              <ListItemText 
                primary={msg} 
                primaryTypographyProps={{ variant: 'body2' }}
              />
            </ListItem>
          ))
        ) : (
          <Typography variant="body2" color="textSecondary">
            No activity to display
          </Typography>
        )}
      </List>
    </Paper>
  );
};