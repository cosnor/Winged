import { Platform } from 'react-native';
import Constants from 'expo-constants';

/**
 * Configuración de URLs del API según el entorno
 * 
 * DESARROLLO:
 * - NGROK_URL: Si está definida, usa ngrok (funciona en emulador Y teléfono físico)
 * - Emulador Android: usa 10.0.2.2 (apunta a localhost de tu PC)
 * - Simulador iOS: usa localhost directamente
 * 
 * PRODUCCIÓN:
 * - Usa la URL de tu API en Azure/servidor
 */

// Leer variables de entorno desde .env
const NGROK_URL = process.env.EXPO_PUBLIC_NGROK_URL || ''; // API Gateway en local (no expuesto)
const WEBSOCKET_URL = process.env.EXPO_PUBLIC_WEBSOCKET_URL || 'wss://virgilio-octamerous-darnell.ngrok-free.dev';

// eBird API Token
export const EBIRD_API_TOKEN = process.env.EXPO_PUBLIC_EBIRD_API_TOKEN || '';

const getApiUrl = () => {
  // Si hay URL de ngrok, úsala (funciona para todo: emulador y teléfono físico)
  if (NGROK_URL) {
    return NGROK_URL;
  }

  // En desarrollo sin ngrok
  if (__DEV__) {
    // Emulador Android - IP especial que apunta a localhost de tu PC
    if (Platform.OS === 'android') {
      return 'http://10.0.2.2:8000';
    }
    
    // Simulador iOS - puede usar localhost directamente
    if (Platform.OS === 'ios') {
      return 'http://localhost:8000';
    }
    
    // Web (si usas Expo web)
    return 'http://localhost:8000';
  }
  
  // En producción (cuando hagas el build de la app)
  return 'https://tu-api-produccion.azurewebsites.net';
};

export const API_BASE_URL = getApiUrl();
export const WS_BASE_URL = WEBSOCKET_URL || API_BASE_URL.replace('http://', 'ws://').replace('https://', 'wss://');

// Para debugging - ver qué URL se está usando
console.log('🌐 API URL:', API_BASE_URL);
console.log('📱 Platform:', Platform.OS);
console.log('🔧 DEV mode:', __DEV__);
