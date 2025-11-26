import { View, Text, StyleSheet, TouchableOpacity, ScrollView, Dimensions, Alert, ActivityIndicator } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import MapView, { Marker, Polygon } from 'react-native-maps';
import * as Location from 'expo-location';
import React, { useEffect, useState } from 'react';
import { SpeciesDistribution } from '../../../../data/types';
import { getDistribution } from '../../../../services/mapsService';
import Ionicons from '@expo/vector-icons/Ionicons';
import { LinearGradient } from 'expo-linear-gradient';
import * as Animatable from 'react-native-animatable';

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
    fillColor: 'rgba(255, 107, 53, 0.25)',
    strokeColor: '#ff6b35',
    strokeWidth: 3,
  },
  medium: {
    fillColor: 'rgba(255, 154, 65, 0.2)',
    strokeColor: '#ff9a41',
    strokeWidth: 3,
  },
  low: {
    fillColor: 'rgba(76, 222, 128, 0.2)',
    strokeColor: '#4ade80',
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
    <LinearGradient
      colors={['#fffaf0', '#ffe4d6', '#ffd4ba']}
      style={styles.gradient}
    >
      <SafeAreaView style={styles.container} edges={['top']}>
        <Animatable.View animation="fadeInDown" duration={600} style={styles.header}>
          <View style={styles.headerContent}>
            <LinearGradient
              colors={['#ff9a41', '#d2691e']}
              style={styles.iconCircle}
            >
              <Ionicons name="location" size={28} color="#fff" />
            </LinearGradient>
            <View style={styles.headerText}>
              <Text style={styles.title}>Aves Cerca de Ti</Text>
              <Text style={styles.headerSubtitle}>Descubre especies en tu zona</Text>
            </View>
          </View>
        </Animatable.View>
      
        {isLoading && (
          <View style={styles.loadingOverlay}>
            <LinearGradient
              colors={['rgba(255, 250, 240, 0.98)', 'rgba(255, 228, 214, 0.98)']}
              style={styles.loadingContent}
            >
              <Animatable.View animation="pulse" iterationCount="infinite" duration={1500}>
                <LinearGradient
                  colors={['#ff9a41', '#d2691e']}
                  style={styles.loadingIconCircle}
                >
                  <Ionicons name="search" size={40} color="#fff" />
                </LinearGradient>
              </Animatable.View>
              <Text style={styles.loadingText}>Buscando especies cercanas...</Text>
              <Text style={styles.loadingSubtext}>Analizando {radius}m a tu alrededor</Text>
            </LinearGradient>
          </View>
        )}
      
        {/* Mapa fijo en la parte superior */}
        <Animatable.View animation="fadeIn" duration={600} delay={200} style={styles.mapWrapper}>
          <View style={styles.mapCard}>
            <View style={styles.mapHeader}>
              <Ionicons name="map-outline" size={20} color="#d2691e" />
              <Text style={styles.mapTitle}>Mapa de Distribución</Text>
            </View>
            <View style={styles.mapContainer}>
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
                  {/* Ajustar para que quede con los colores */}
                  <LinearGradient 
                    colors={area.probability >= 0.7 ? ['#ff6b35', '#d2691e'] : area.probability >= 0.3 ? ['#ff9a41', '#d2691e'] : ['#4ade80', '#16a34a']}
                    style={styles.probabilityBox}
                  >
                    <Text style={styles.probabilityText}>
                      {(area.probability * 100).toFixed(0)}%
                    </Text>
                  </LinearGradient>
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
            {selectedSpecies && (
              <Animatable.View animation="fadeIn" duration={400} style={styles.selectedSpeciesBar}>
                <LinearGradient
                  colors={['#ff9a41', '#d2691e']}
                  style={styles.selectedSpeciesGradient}
                  start={{ x: 0, y: 0 }}
                  end={{ x: 1, y: 0 }}
                >
                  <Ionicons name="checkmark-circle" size={20} color="#fff" />
                  <Text style={styles.selectedSpeciesText}>{selectedSpecies.species}</Text>
                  <Text style={styles.selectedSpeciesProbability}>
                    {Math.round(selectedSpecies.max_probability * 100)}%
                  </Text>
                </LinearGradient>
              </Animatable.View>
            )}
          </View>
        </Animatable.View>

        {/* Lista de especies con scroll independiente */}
        <Animatable.View animation="fadeInUp" duration={600} delay={400} style={styles.listWrapper}>
          <View style={styles.listHeader}>
            <Ionicons name="list" size={20} color="#d2691e" />
            <Text style={styles.listTitle}>Especies en {radius}m</Text>
            <View style={styles.speciesCount}>
              <Text style={styles.speciesCountText}>{speciesData.length}</Text>
            </View>
          </View>
          <ScrollView 
            style={styles.speciesList} 
            showsVerticalScrollIndicator={false}
            nestedScrollEnabled={true}
          >
            {speciesData.map((species, index) => (
              <Animatable.View
                key={species.species}
                animation="fadeInUp"
                duration={400}
                delay={index * 50}
              >
                <TouchableOpacity
                  style={[
                    styles.speciesItem,
                    selectedSpecies?.species === species.species && styles.selectedSpecies
                  ]}
                  onPress={() => { 
                    setSelectedSpecies(selectedSpecies?.species === species.species ? null : species);
                    handleSelectSpecies(species) 
                  }}
                  activeOpacity={0.7}
                >
                  <View style={styles.speciesContent}>
                    <View style={styles.speciesHeader}>
                      <View style={[
                        styles.probabilityBadge,
                        { backgroundColor: species.max_probability >= 0.7 ? '#ff6b35' : species.max_probability >= 0.3 ? '#ff9a41' : '#4ade80' }
                      ]}>
                        <Text style={styles.probabilityBadgeText}>
                          {Math.round(species.max_probability * 100)}%
                        </Text>
                      </View>
                      <Text style={styles.speciesName} numberOfLines={1}>{species.species}</Text>
                      {selectedSpecies?.species === species.species && (
                        <Ionicons name="checkmark-circle" size={24} color="#ff9a41" />
                      )}
                    </View>
                    {selectedSpecies?.species === species.species && (
                      <Animatable.View animation="fadeIn" duration={300} style={styles.legendContainer}>
                        <View style={styles.legendRow}>
                          <View style={styles.legendItem}>
                            <LinearGradient colors={['#ff6b35', '#d2691e']} style={styles.legendColor} />
                            <Text style={styles.legendText}>Alta</Text>
                          </View>
                          <View style={styles.legendItem}>
                            <LinearGradient colors={['#ff9a41', '#d2691e']} style={styles.legendColor} />
                            <Text style={styles.legendText}>Media</Text>
                          </View>
                          <View style={styles.legendItem}>
                            <LinearGradient colors={['#4ade80', '#16a34a']} style={styles.legendColor} />
                            <Text style={styles.legendText}>Baja</Text>
                          </View>
                        </View>
                      </Animatable.View>
                    )}
                  </View>
                </TouchableOpacity>
              </Animatable.View>
            ))}
          </ScrollView>
        </Animatable.View>
      </SafeAreaView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  gradient: {
    flex: 1,
  },
  container: {
    flex: 1,
  },
  header: {
    paddingHorizontal: 20,
    paddingBottom: 16,
  },
  headerContent: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    marginBottom: 8,
  },
  iconCircle: {
    width: 56,
    height: 56,
    borderRadius: 28,
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#d2691e',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 6,
  },
  headerText: {
    flex: 1,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#d2691e',
    marginBottom: 2,
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#8b4513',
    fontWeight: '500',
  },
  reloadButton: {
    borderRadius: 28,
    overflow: 'hidden',
    shadowColor: '#16a34a',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
    elevation: 4,
  },
  reloadGradient: {
    width: 56,
    height: 56,
    alignItems: 'center',
    justifyContent: 'center',
  },
  loadingOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    zIndex: 1000,
  },
  loadingContent: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingIconCircle: {
    width: 100,
    height: 100,
    borderRadius: 50,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 20,
    shadowColor: '#d2691e',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.4,
    shadowRadius: 12,
    elevation: 8,
  },
  loadingText: {
    fontSize: 18,
    color: '#d2691e',
    fontWeight: '700',
    marginTop: 12,
  },
  loadingSubtext: {
    fontSize: 14,
    color: '#8b4513',
    marginTop: 4,
  },
  mapWrapper: {
    marginHorizontal: 20,
    marginBottom: 16,
  },
  mapCard: {
    backgroundColor: '#fff',
    borderRadius: 20,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 12,
    elevation: 6,
  },
  mapHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    paddingHorizontal: 16,
    paddingVertical: 12,
    backgroundColor: '#fffaf0',
    borderBottomWidth: 2,
    borderBottomColor: '#ffd4ba',
  },
  mapTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: '#d2691e',
  },
  mapContainer: {
    height: Dimensions.get('window').height * 0.28,
    overflow: 'hidden',
  },
  map: {
    width: '100%',
    height: '100%',
  },
  selectedSpeciesBar: {
    overflow: 'hidden',
  },
  selectedSpeciesGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 12,
    gap: 10,
  },
  selectedSpeciesText: {
    flex: 1,
    fontSize: 15,
    fontWeight: '700',
    color: '#fff',
  },
  selectedSpeciesProbability: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#fff',
    backgroundColor: 'rgba(255, 255, 255, 0.25)',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
  },
  probabilityBox: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 4,
    elevation: 4,
  },
  probabilityText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 13,
  },
  listWrapper: {
    flex: 1,
    marginHorizontal: 20,
    marginBottom: 20,
  },
  listHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    paddingVertical: 12,
    paddingHorizontal: 16,
    backgroundColor: '#fff',
    borderRadius: 16,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  listTitle: {
    flex: 1,
    fontSize: 16,
    fontWeight: '700',
    color: '#d2691e',
  },
  speciesCount: {
    backgroundColor: '#ff9a41',
    width: 32,
    height: 32,
    borderRadius: 16,
    alignItems: 'center',
    justifyContent: 'center',
  },
  speciesCountText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: 'bold',
  },
  speciesList: {
    flex: 1,
    backgroundColor: '#fff',
    borderRadius: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
  },
  speciesItem: {
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  selectedSpecies: {
    backgroundColor: '#fff8f0',
    borderLeftWidth: 4,
    borderLeftColor: '#ff9a41',
  },
  speciesContent: {
    padding: 16,
  },
  speciesHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
    marginBottom: 8,
  },
  probabilityBadge: {
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.2,
    shadowRadius: 2,
    elevation: 2,
  },
  probabilityBadgeText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: 'bold',
  },
  speciesName: {
    flex: 1,
    fontSize: 15,
    fontWeight: '600',
    color: '#333',
  },
  legendContainer: {
    marginTop: 12,
    padding: 12,
    backgroundColor: '#fffaf0',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#ffd4ba',
  },
  legendRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    gap: 8,
  },
  legendItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  legendColor: {
    width: 24,
    height: 16,
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.2,
    shadowRadius: 2,
    elevation: 2,
  },
  legendText: {
    fontSize: 12,
    color: '#666',
    fontWeight: '600',
  },
});