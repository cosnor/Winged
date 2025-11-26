import { createContext, useContext, useState, ReactNode, useEffect } from "react";
import { BirdDetection } from "../hooks/useBirdAnalysis";
import { useAvedex } from "./avedex-context";
import AsyncStorage from "@react-native-async-storage/async-storage";
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
  addDetections: (detections: BirdDetection[]) => Promise<void>;
  clearDetections: () => void;
  removeBird: (birdId: string) => void;
};

const BirdDetectionContext = createContext<BirdDetectionContextType>({
  identifiedBirds: [],
  addDetections: async () => {},
  clearDetections: () => {},
  removeBird: () => {}
});

export function BirdDetectionProvider({ children }: { children: ReactNode }) {
  const [identifiedBirds, setIdentifiedBirds] = useState<IdentifiedBird[]>([]);
  const [currentUserId, setCurrentUserId] = useState<string | null>(null);
  const { refresh, birds: avedexBirds } = useAvedex();

  // Auto-clean detections that are already in Avedex
  useEffect(() => {
    if (avedexBirds.length > 0 && identifiedBirds.length > 0) {
      const avedexIds = new Set(avedexBirds.map(b => b.id));
      const filtered = identifiedBirds.filter(bird => !avedexIds.has(bird.id));
      
      if (filtered.length < identifiedBirds.length) {
        const removedCount = identifiedBirds.length - filtered.length;
        console.log(`🧹 Auto-cleaned ${removedCount} birds already in Avedex from detections`);
        setIdentifiedBirds(filtered);
      }
    }
  }, [avedexBirds]);

  // Monitor user changes and clear detections when user logs out or changes
  useEffect(() => {
    const checkUserChange = async () => {
      const userInfoStr = await AsyncStorage.getItem('USER_INFO');
      
      if (userInfoStr) {
        const userInfo = JSON.parse(userInfoStr);
        const userId = userInfo.user_id || userInfo.id;
        
        // Si el usuario cambió, limpiar las detecciones
        if (userId && userId !== currentUserId) {
          if (currentUserId !== null) {
            console.log(`🔄 User changed from ${currentUserId} to ${userId}, clearing detections...`);
            setIdentifiedBirds([]);
          }
          setCurrentUserId(userId);
        }
      } else if (currentUserId !== null) {
        // Usuario cerró sesión, limpiar detecciones
        console.log('🚪 User logged out, clearing detections...');
        setIdentifiedBirds([]);
        setCurrentUserId(null);
      }
    };

    checkUserChange();
    const interval = setInterval(checkUserChange, 1000); // Check every second
    
    return () => clearInterval(interval);
  }, [currentUserId]);

  const addDetections = async (detections: BirdDetection[]) => {
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log(`🎯 addDetections called with ${detections.length} detections`);
    console.log('📋 Detections data:', JSON.stringify(detections, null, 2));
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    
    // Convertir detecciones a aves identificadas
    const newBirds: IdentifiedBird[] = detections.map((detection) => ({
      id: detection.species_name, // Use species_name as ID to avoid duplicates
      commonName: detection.common_name || detection.species_name,
      scientificName: detection.scientific_name || detection.species_name,
      confidence: detection.confidence,
      detectedAt: new Date(),
      imageUrl: undefined
    }));

    console.log(`🐦 Converted to ${newBirds.length} identified birds:`, newBirds.map(b => b.commonName).join(', '));

    // Deduplicate: only add birds that aren't already in the list
    setIdentifiedBirds(prev => {
      const existingIds = new Set(prev.map(b => b.id));
      const uniqueNewBirds = newBirds.filter(b => !existingIds.has(b.id));
      console.log(`📋 Adding ${uniqueNewBirds.length} new birds to identifiedBirds list (${existingIds.size} already existed)`);
      return [...uniqueNewBirds, ...prev];
    });

    // Obtener user_id y token
    try {
      console.log('🔐 Attempting to get user credentials from AsyncStorage...');
      const userInfoStr = await AsyncStorage.getItem('USER_INFO');
      const token = await AsyncStorage.getItem('ACCESS_TOKEN');
      
      console.log('📦 UserInfo exists:', !!userInfoStr);
      console.log('🔑 Token exists:', !!token);
      
      if (!userInfoStr || !token) {
        console.log('⚠️ No user logged in, skipping sighting creation');
        console.log('   UserInfo:', userInfoStr ? 'present' : 'MISSING');
        console.log('   Token:', token ? 'present' : 'MISSING');
        return;
      }

      const userInfo = JSON.parse(userInfoStr);
      const userId = userInfo.user_id || userInfo.id;
      
      console.log('👤 User ID:', userId);
      console.log('📧 User Email:', userInfo.email || 'N/A');

      console.log(`📝 Creating sightings for ${detections.length} birds (user_id: ${userId})...`);
      
      // Crear un sighting por cada detección
      for (let i = 0; i < detections.length; i++) {
        const detection = detections[i];
        
        try {
          const sightingPayload = {
            user_id: userId,
            species_name: detection.scientific_name,      // Nombre científico
            common_name: detection.common_name,
            timestamp: new Date().toISOString(),
          };

          console.log(`[${i + 1}/${detections.length}] 📤 Creating sighting for ${detection.common_name}:`, sightingPayload);
          console.log(`[${i + 1}/${detections.length}] 🌐 API URL: ${API_BASE_URL}/sightings/`);
          console.log(`[${i + 1}/${detections.length}] 🔑 Token (first 20 chars): ${token.substring(0, 20)}...`);

          const response = await fetch(`${API_BASE_URL}/sightings/`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify(sightingPayload),
          });

          console.log(`[${i + 1}/${detections.length}] 📥 Response status: ${response.status}`);
          console.log(`[${i + 1}/${detections.length}] 📥 Response headers:`, JSON.stringify([...response.headers.entries()]));

          if (response.ok) {
            const responseData = await response.json();
            console.log(`[${i + 1}/${detections.length}] ✅ Sighting created successfully:`, responseData);
            
            // Mostrar achievements desbloqueados si hay
            if (responseData.achievements_unlocked && responseData.achievements_unlocked.length > 0) {
              console.log(`[${i + 1}/${detections.length}] 🏆 Achievements unlocked:`, responseData.achievements_unlocked);
            }
          } else {
            const errorText = await response.text();
            console.error(`[${i + 1}/${detections.length}] ❌ Failed to create sighting: ${response.status}`, errorText);
          }
        } catch (error) {
          console.error(`[${i + 1}/${detections.length}] ❌ Error creating sighting for ${detection.common_name}:`, error);
        }
      }

      // Refrescar la colección de Avedex después de crear todos los sightings
      console.log('🔄 Refreshing Avedex collection...');
      await refresh();
      console.log('✅ Avedex collection refreshed');

    } catch (error) {
      console.error('❌ Error in addDetections:', error);
    }

    console.log(`✅ Finished processing detections`);
  };

  const clearDetections = () => {
    setIdentifiedBirds([]);
  };

  const removeBird = (birdId: string) => {
    console.log(`🗑️ Removing bird ${birdId} from detections list`);
    setIdentifiedBirds(prev => prev.filter(bird => bird.id !== birdId));
  };

  return (
    <BirdDetectionContext.Provider value={{ identifiedBirds, addDetections, clearDetections, removeBird }}>
      {children}
    </BirdDetectionContext.Provider>
  );
}

export function useBirdDetections() {
  return useContext(BirdDetectionContext);
}
