import { View, Text, StyleSheet, TouchableOpacity, ScrollView, Dimensions, Alert, ActivityIndicator } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import MapView, { Marker, Polygon } from 'react-native-maps';
import * as Location from 'expo-location';
import React, { useEffect, useState } from 'react';
import { SpeciesDistribution } from '../../../../data/types';
import { getDistribution } from '../../../../services/mapsService';
import Ionicons from '@expo/vector-icons/Ionicons';

// Centro exacto del polígono principal
const BARRANQUILLA_REGION = {
  latitude: 11.008083495495494,
  longitude: -74.84013450450449,
  latitudeDelta: 0.01, // Zoom más cercano para ver mejor los polígonos
  longitudeDelta: 0.01,
};

// Colores para distinguir las diferentes áreas de probabilidad
const AREA_STYLES = {
  high: {
    fillColor: 'rgba(255, 0, 0, 0.2)',
    strokeColor: '#ff0000',
    strokeWidth: 2,
  },
  medium: {
    fillColor: 'rgba(255, 165, 0, 0.2)',
    strokeColor: '#ffa500',
    strokeWidth: 2,
  },
  low: {
    fillColor: 'rgba(255, 255, 0, 0.2)',
    strokeColor: '#ffff00',
    strokeWidth: 2,
  },
} as const;

const getAreaStyle = (probability: number) => {
  if (probability >= 0.7) return AREA_STYLES.high;
  if (probability >= 0.3) return AREA_STYLES.medium;
  return AREA_STYLES.low;
};


export default function NearbyScreen() {
  const [location, setLocation] = useState<Location.LocationObject | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [selectedSpecies, setSelectedSpecies] = useState<SpeciesDistribution | null>(null);
  const [probabilityText, setProbabilityText] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [radius, setRadius] = useState<number>(500); // Radio en metros


  // Real species data from API
  const [speciesData, setSpeciesData] = useState<SpeciesDistribution[]>([
    
  ]);
    
  useEffect(() => {
    console.log("Selected Species:", selectedSpecies);
    console.log("Species Data:", speciesData);
  }, [selectedSpecies, speciesData]);

  // Cargar distribución de especies desde el API
  const loadDistribution = async (lat: number, lon: number) => {
    try {
      setIsLoading(true);
      console.log(`🔍 Cargando distribución para: ${lat}, ${lon}`);
      
      const data = await getDistribution(lat, lon, radius, 0.002);
      
      if (data.species_distributions && data.species_distributions.length > 0) {
        setSpeciesData(data.species_distributions);
        Alert.alert(
          '✅ Especies cargadas', 
          `Se encontraron ${data.species_distributions.length} especies en un radio de ${radius}m`,
          [{ text: 'OK' }]
        );
      } else {
        Alert.alert(
          '⚠️ Sin resultados',
          'No se encontraron especies en esta ubicación. Mostrando datos de ejemplo.',
          [{ text: 'OK' }]
        );
      }
    } catch (error) {
      console.error('❌ Error loading distribution:', error);
      Alert.alert(
        '❌ Error de conexión',
        'No se pudo conectar con el servidor. Verifica que el servicio de mapas esté corriendo en el puerto 8004.',
        [{ text: 'OK' }]
      );
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    (async () => {
      const { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        setErrorMsg('Se necesita permiso para acceder a la ubicación');
        return;
      }

      try {
        const userLocation = await Location.getCurrentPositionAsync({});
        setLocation(userLocation);
        
        // Cargar distribución automáticamente
        await loadDistribution(
          userLocation.coords.latitude,
          userLocation.coords.longitude
        );
      } catch (error) {
        setErrorMsg('No se pudo obtener la ubicación');
      }
    })();
  }, []);

  const handleSelectSpecies = (species: SpeciesDistribution) => {
    setSelectedSpecies(species);
    const avg = species.areas.reduce((sum, a) => sum + a.probability, 0) / species.areas.length;
    const sensitivity = 0.1; // ±10%
    const nearby = species.areas.filter(
      (a) => Math.abs(a.probability - avg) <= sensitivity
    );
    const avgNearby =
      nearby.reduce((sum, a) => sum + a.probability, 0) / nearby.length || avg;
    setProbabilityText(`Probabilidad en zona: ${(avgNearby * 100).toFixed(1)}%`);
  };



  const handleReloadDistribution = () => {
    if (location) {
      loadDistribution(location.coords.latitude, location.coords.longitude);
    } else {
      Alert.alert('⚠️ Ubicación no disponible', 'Espera a que se obtenga tu ubicación');
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>¡Encuentra aves cerca de ti!</Text>
        {location && (
          <TouchableOpacity 
            style={styles.reloadButton} 
            onPress={handleReloadDistribution}
            disabled={isLoading}
          >
            <Ionicons name="reload" size={20} color="#fff" />
            <Text style={styles.reloadButtonText}>Recargar</Text>
          </TouchableOpacity>
        )}
      </View>
      
      {isLoading && (
        <View style={styles.loadingOverlay}>
          <ActivityIndicator size="large" color="#d2691e" />
          <Text style={styles.loadingText}>Cargando especies cercanas...</Text>
        </View>
      )}
      
      <View style={styles.mapContainer}>
        <Text style={styles.subtitle}>Selecciona una especie para ver su distribución</Text>
        <MapView
          style={styles.map}
          initialRegion={BARRANQUILLA_REGION}>
          {location && (
            <Marker
              coordinate={{
                latitude: location.coords.latitude,
                longitude: location.coords.longitude,
              }}
              title="Tú estás aquí"
              pinColor="#d2691e"
            />
          )}
          {selectedSpecies && selectedSpecies.areas.map((area, areaIndex) => {
            const fragmentKey = `${selectedSpecies.species}-${areaIndex}`;
            return (
              <React.Fragment key={fragmentKey}>
                <Marker
                  key={`${fragmentKey}-marker`}
                  flat
                  coordinate={{
                    latitude: area.polygon[0].lat,
                    longitude: area.polygon[0].lon,
                  }}
                >
                  <View style={styles.probabilityBox}>
                    <Text style={{ color: '#000', fontWeight: 'bold' }}>
                      {(area.probability * 100).toFixed(1)}%
                    </Text>
                  </View>
                </Marker>

                <Polygon
                  key={`${fragmentKey}-polygon`}
                  coordinates={area.polygon.map(point => ({
                    latitude: point.lat,
                    longitude: point.lon,
                  }))}
                  {...getAreaStyle(area.probability)}
                  zIndex={1000}
                />
              </React.Fragment>
            );
          })}
        </MapView>
      </View>
    <Text style={styles.subtitle}>Especies en un radio de {radius} metros de ti</Text>
      <ScrollView style={styles.speciesList}>
        {speciesData.map((species) => (
          <TouchableOpacity
            key={species.species}
            style={[
              styles.speciesItem,
              selectedSpecies?.species === species.species && styles.selectedSpecies
            ]}
            onPress={() => { setSelectedSpecies(selectedSpecies?.species === species.species ? null : species);
                          handleSelectSpecies(species) }}
                          
          >
            <View style={styles.speciesContent}>
              <Text style={styles.speciesName}>{species.species}</Text>
              <Text style={styles.probabilityText}>
                Probabilidad máxima: {Math.round(species.max_probability * 100)}%
              </Text>
              {selectedSpecies?.species === species.species && (
                <Text style={styles.helpText}>
                  Toca los polígonos en el mapa para ver la probabilidad en cada área
                </Text>
              )}
              <View style={styles.legendContainer}>
                <View style={styles.legendItem}>
                  <View style={[styles.legendColor, { backgroundColor: AREA_STYLES.high.strokeColor }]} />
                  <Text style={styles.legendText}>Alta (≥70%)</Text>
                </View>
                <View style={styles.legendItem}>
                  <View style={[styles.legendColor, { backgroundColor: AREA_STYLES.medium.strokeColor }]} />
                  <Text style={styles.legendText}>Media (30-69%)</Text>
                </View>
                <View style={styles.legendItem}>
                  <View style={[styles.legendColor, { backgroundColor: AREA_STYLES.low.strokeColor }]} />
                  <Text style={styles.legendText}>Baja (≤29%)</Text>
                </View>
              </View>
            </View>
          </TouchableOpacity>
        ))}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fffaf0',
    justifyContent: 'flex-start',
    alignContent: 'flex-start'
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingTop: 16,
    paddingBottom: 4,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#d2691e',
    flex: 1,
  },
  reloadButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#d2691e',
    paddingVertical: 8,
    paddingHorizontal: 12,
    borderRadius: 8,
    gap: 4,
  },
  reloadButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
  },
  loadingOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(255, 250, 240, 0.95)',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 1000,
  },
  loadingText: {
    marginTop: 12,
    fontSize: 16,
    color: '#666',
    fontWeight: '500',
  },
  subtitle: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
    paddingVertical: 10,

  },
  mapContainer: {
    height: Dimensions.get('window').height * 0.4, // Reducido para dejar más espacio a la lista
    overflow: 'hidden',
    borderRadius: 20,
    margin: 16,
    marginBottom: 8, // Reducido para acercar la lista
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
  },
  map: {
    width: '100%',
    height: '100%',
  },
  speciesList: {
    flexGrow: 1,
    margin: 16,
    backgroundColor: '#fff',
    borderRadius: 10,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.2,
    shadowRadius: 2.62,
  },
  speciesItem: {
    padding: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  selectedSpecies: {
    backgroundColor: '#fff3e6',
  },
  speciesName: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#333',
  },
  probabilityText: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
  },
  speciesContent: {
    padding: 8,
  },
  helpText: {
    fontSize: 12,
    color: '#666',
    fontStyle: 'italic',
    marginTop: 4,
  },
  legendContainer: {
    marginTop: 8,
    flexDirection: 'row',
    justifyContent: 'space-around',
    flexWrap: 'wrap',
    gap: 8,
  },
  legendItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginRight: 8,
  },
  legendColor: {
    width: 12,
    height: 12,
    borderRadius: 6,
    marginRight: 4,
  },
  legendText: {
    fontSize: 10,
    color: '#666',
  },
  probabilityBox: {
    position: 'absolute',
    bottom: 30,
    alignSelf: 'center',
    backgroundColor: 'rgba(255, 255, 228, 1)',
    padding: 10,
    borderRadius: 8,
    borderColor: '#d2691e',
  },  

});