import { createContext, useContext, useState, ReactNode } from "react";
import { BirdDetection } from "../hooks/useBirdAnalysis";

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

  const addDetections = (detections: BirdDetection[]) => {
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
