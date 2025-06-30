export const API_URL = import.meta.env.VITE_API_URL || 'https://web-production-eab4a.up.railway.app';

export const apiCall = (endpoint) => {
  const url = `${API_URL}${endpoint}`;
  console.log('Making API call to:', url); // Debug logging
  return fetch(url);
};