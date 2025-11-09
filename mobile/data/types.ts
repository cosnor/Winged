export interface SpeciesDistribution {
  species: string;
  max_probability: number;
  areas: {
    polygon: {
      lat: number;
      lon: number;
    }[];
    probability: number;
  }[];
}