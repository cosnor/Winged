import { Platform } from 'react-native';

/**
 * Obtener la URL base para el servicio de mapas
 * - Emulador Android: 10.0.2.2 (IP especial que apunta a localhost)
 * - iOS Simulator: localhost
 * - Producción: URL del servidor
 */
const getMapsApiUrl = () => {
  // Si hay variable de entorno, usarla
  const envUrl = process.env.EXPO_PUBLIC_MAPS_URL;
  if (envUrl) {
    return envUrl;
  }

  // En desarrollo
  if (__DEV__) {
    if (Platform.OS === 'android') {
      return 'http://10.0.2.2:8004';
    }
    if (Platform.OS === 'ios') {
      return 'http://localhost:8004';
    }
    return 'http://localhost:8004';
  }
  
  // En producción
  return 'https://tu-api-produccion.azurewebsites.net';
};

export const MAPS_API_URL = getMapsApiUrl();

console.log('🗺️ Maps API URL:', MAPS_API_URL);

// Types
export interface PolygonPoint {
  lat: number;
  lon: number;
}

export interface Area {
  polygon: PolygonPoint[];
  probability: number;
}

export interface SpeciesDistribution {
  species: string;
  max_probability: number;
  areas: Area[];
}

export interface DistributionRequest {
  lat: number;
  lon: number;
  datetime: string; // ISO format
  radius: number;
  grid_size: number;
}

export interface DistributionResponse {
  zone: string;
  location: {
    lat: number;
    lon: number;
  };
  datetime: string;
  species_distributions: SpeciesDistribution[];
}

/**
 * Obtiene la distribución de especies en un radio determinado
 * @param lat Latitud del punto central
 * @param lon Longitud del punto central
 * @param radius Radio en metros (default: 500)
 * @param grid_size Tamaño de la cuadrícula (default: 0.002)
 */
export const getDistribution = async (
  lat: number,
  lon: number,
  radius: number = 500,
  grid_size: number = 0.002
): Promise<DistributionResponse> => {
  try {
    const datetime = new Date().toISOString();
    
    const requestBody: DistributionRequest = {
      lat,
      lon,
      datetime,
      radius,
      grid_size
    };

    console.log('🗺️ Requesting distribution from:', MAPS_API_URL);
    console.log('📍 Request:', requestBody);

    const response = await fetch(`${MAPS_API_URL}/distribution`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('❌ Maps API error:', response.status, errorText);
      throw new Error(`Maps API error: ${response.status} - ${errorText}`);
    }

    const data = await response.json();
    console.log(`✅ Distribution loaded: ${data.species_distributions?.length || 0} species`);
    
    return data;
  } catch (error) {
    console.error('❌ Error fetching distribution:', error);
    throw error;
  }
};

/**
 * Obtiene las zonas de Barranquilla como GeoJSON
 */
export const getZones = async () => {
  try {
    const response = await fetch(`${MAPS_API_URL}/zones`);
    
    if (!response.ok) {
      throw new Error(`Zones API error: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Zones loaded');
    return data;
  } catch (error) {
    console.error('❌ Error fetching zones:', error);
    throw error;
  }
};
