import { createContext, useContext, useState, ReactNode } from "react";
import { BirdDetection } from "../hooks/useBirdAnalysis";
import { useAvedex } from "./avedex-context";

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
  const { addBird, hasBird } = useAvedex();

  const addDetections = (detections: BirdDetection[]) => {
    console.log(`🎯 addDetections called with ${detections.length} detections`);
    
    // Convertir detecciones a aves identificadas
    const newBirds: IdentifiedBird[] = detections.map((detection, index) => ({
      id: detection.species_name, // Use species_name as ID to avoid duplicates
      commonName: detection.common_name || detection.species_name,
      scientificName: detection.scientific_name || detection.species_name,
      confidence: detection.confidence,
      detectedAt: new Date(),
      // Por ahora sin imagen, se podría agregar una búsqueda de imagen después
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

    // Registrar en Avedex
    console.log(`📝 Registering ${detections.length} birds in Avedex...`);
    detections.forEach((detection, index) => {
      // Usar el nombre de la especie como ID para evitar duplicados en Avedex
      const birdId = detection.species_name;
      const alreadyInAvedex = hasBird(birdId);
      
      console.log(`[${index + 1}/${detections.length}] ${detection.common_name || detection.species_name} - Already in Avedex: ${alreadyInAvedex}`);
      
      // Solo agregar si no existe ya en el Avedex
      if (!alreadyInAvedex) {
        console.log(`  ➕ Adding to Avedex...`);
        addBird({
          id: birdId,
          commonName: detection.common_name || detection.species_name,
          scientificName: detection.scientific_name || detection.species_name,
          imageUrl: 'https://via.placeholder.com/150', // Imagen por defecto
        });
      } else {
        console.log(`  ⏭️ Skipping (already in collection)`);
      }
    });

    console.log(`✅ Finished processing detections`);
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
