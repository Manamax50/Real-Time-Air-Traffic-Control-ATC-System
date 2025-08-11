import axios from 'axios';

export const API_BASE = 'https://atc-system-app.azurewebsites.net';

export interface Plane {
  plane_id: string;
  plane_state: string;
  plane_position: string;
  plane_target: string;
  plane_model?: string;
  plane_size?: string;
  plane_pascount?: string;
}

export interface PlaneCreateData {
  plane_id: string;
  state: string;
  position: string;
  target: string;
  origin_country?: string;
  destination_country: string;
  plane_model?: string;
  plane_size?: number;
  plane_pascount?: number;
}

export interface SystemStatus {
  airplanes: Record<string, Plane>;
  airspaces: Record<string, string | null>;
  runways: Record<string, string | null>;
  loading: string[];
}

export const getSystemStatus = async (): Promise<SystemStatus> => {
  const response = await axios.get(`${API_BASE}/system-status`);
  return response.data;
};

export const getPlaneDetails = async (planeId: string): Promise<Plane> => {
  const response = await axios.get(`${API_BASE}/plane/${planeId}`);
  return response.data;
};

export const getMessages = async (): Promise<string[]> => {
  const response = await axios.get(`${API_BASE}/messages`);
  return response.data;
};

export const createPlane = async (data: PlaneCreateData): Promise<void> => {
  await axios.post(`${API_BASE}/planes`, data);
};
