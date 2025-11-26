import { createContext, useContext, useState, ReactNode } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { BirdDetection } from "../hooks/useBirdAnalysis";
import { API_BASE_URL } from "../config/environment";

// Tipo de ave identificada para el registro
export interface IdentifiedBird {
  id: string;
  commonName: string;
  scientificName: string;
  imageUrl?: string;
  confidence?: number;
  detectedAt?: Date;
}

// Contexto para manejar las detecciones de aves
type BirdDetectionContextType = {
  identifiedBirds: IdentifiedBird[];
  addDetections: (detections: BirdDetection[]) => void;
  clearDetections: () => void;
};

const BirdDetectionContext = createContext<BirdDetectionContextType>({
  identifiedBirds: [],
  addDetections: () => {},
  clearDetections: () => {}
});

export function BirdDetectionProvider({ children }: { children: ReactNode }) {
  const [identifiedBirds, setIdentifiedBirds] = useState<IdentifiedBird[]>([]);

  const addDetections = async (detections: BirdDetection[]) => {
    // Convertir detecciones a aves identificadas
    const newBirds: IdentifiedBird[] = detections.map((detection, index) => ({
      id: `${Date.now()}_${index}`,
      commonName: detection.common_name || detection.species_name,
      scientificName: detection.scientific_name || detection.species_name,
      confidence: detection.confidence,
      detectedAt: new Date(),
      // Por ahora sin imagen, se podría agregar una búsqueda de imagen después
      imageUrl: undefined
    }));

    // Agregar las nuevas aves al principio de la lista
    setIdentifiedBirds(prev => [...newBirds, ...prev]);

    console.log('✅ Agregadas', newBirds.length, 'nuevas detecciones al registro');

    // Register with backend (Avedex)
    try {
      const userInfoStr = await AsyncStorage.getItem('USER_INFO');
      const token = await AsyncStorage.getItem('ACCESS_TOKEN');
      
      if (userInfoStr && token) {
        const userInfo = JSON.parse(userInfoStr);
        const userId = userInfo.user_id || userInfo.id;

        for (const detection of detections) {
           const payload = {
             user_id: userId,
             species_name: detection.species_name,
             common_name: detection.common_name || detection.species_name,
             confidence_score: detection.confidence,
             lat: 0, // TODO: Get real location
             lon: 0,
             timestamp: new Date().toISOString()
           };

           console.log('📤 Registering sighting:', payload);
           
           // Fire and forget registration
           fetch(`${API_BASE_URL}/sightings/`, {
             method: 'POST',
             headers: {
               'Content-Type': 'application/json',
               'Authorization': `Bearer ${token}`
             },
             body: JSON.stringify(payload)
           }).then(async res => {
             if (res.ok) {
                console.log('✅ Sighting registered successfully');
                // Optionally trigger Avedex refresh if we had a context for it
             } else {
                const text = await res.text();
                console.error('❌ Failed to register sighting:', res.status, text);
             }
           }).catch(err => console.error('❌ Error registering sighting:', err));
        }
      } else {
        console.warn('⚠️ No user info or token found, skipping backend registration');
      }
    } catch (error) {
      console.error('❌ Error processing detections for backend:', error);
    }
  };

  const clearDetections = () => {
    setIdentifiedBirds([]);
  };

  return (
    <BirdDetectionContext.Provider value={{ identifiedBirds, addDetections, clearDetections }}>
      {children}
    </BirdDetectionContext.Provider>
  );
}

export function useBirdDetections() {
  return useContext(BirdDetectionContext);
}
