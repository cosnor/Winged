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

    // Registrar en Avedex
    detections.forEach(detection => {
      // Usar el nombre de la especie como ID para evitar duplicados en Avedex
      const birdId = detection.species_name;
      
      // Solo agregar si no existe ya en el Avedex
      if (!hasBird(birdId)) {
        addBird({
          id: birdId,
          commonName: detection.common_name || detection.species_name,
          scientificName: detection.scientific_name || detection.species_name,
          imageUrl: 'https://via.placeholder.com/150', // Imagen por defecto
        });
        console.log(`✅ Ave registrada en Avedex: ${detection.common_name || detection.species_name}`);
      }
    });

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
