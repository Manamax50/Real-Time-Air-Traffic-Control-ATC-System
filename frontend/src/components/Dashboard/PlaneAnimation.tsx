// dashboard/PlaneAnimation.tsx
import React from 'react';
import { Box, keyframes } from '@mui/material';
import AirplanemodeActiveIcon from '@mui/icons-material/AirplanemodeActive';

const fly = keyframes`
  0% { transform: translateX(0) translateY(0) rotate(0deg); opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { transform: translateX(0) translateY(-100px) rotate(0deg); opacity: 0; }
`;

const land = keyframes`
  0% { transform: translateY(-100px) rotate(180deg); opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { transform: translateY(0) rotate(180deg); opacity: 0; }
`;

const takeoff = keyframes`
  0% { transform: translateY(0) rotate(0deg); opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { transform: translateY(-100px) rotate(0deg); opacity: 0; }
`;

interface PlaneAnimationProps {
  status: 'flying' | 'landing' | 'taking-off';
  color?: 'primary' | 'secondary' | 'error';
}

export const PlaneAnimation: React.FC<PlaneAnimationProps> = ({ status, color = 'primary' }) => {
  const animation = status === 'flying' ? fly : 
                    status === 'landing' ? land : 
                    takeoff;
  
  return (
    <Box
      sx={{
        position: 'absolute',
        animation: `${animation} 2s infinite`,
        color: `${color}.main`,
        transformOrigin: 'center', 
      }}
    >
      <AirplanemodeActiveIcon fontSize="large" />
    </Box>
  );
};