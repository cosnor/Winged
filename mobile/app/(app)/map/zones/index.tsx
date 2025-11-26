import { View, Text, StyleSheet, TouchableOpacity, ScrollView, Dimensions, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import MapView, { PROVIDER_GOOGLE, Polygon, LatLng, Region } from 'react-native-maps';
import * as Location from 'expo-location';
import { useEffect, useState, useRef } from 'react';
import { SpeciesDistribution } from '../../../../data/types';
import Ionicons from '@expo/vector-icons/Ionicons';
import zonas from '../../../../data/zonas.json';
import bird_zones from "../../../../data/bird_zones_test.json"; // Tu JSON con las aves
import { getZones } from '../../../../services/mapsService';
import { ActivityIndicator } from 'react-native';
import DropDownPicker from "react-native-dropdown-picker";
import { LinearGradient } from 'expo-linear-gradient';
import * as Animatable from 'react-native-animatable';


// Centro exacto del polígono principal
const BARRANQUILLA_REGION: Region = {
  latitude: 11.008083495495494,
  longitude: -74.84013450450449,
  latitudeDelta: 0.5, // Zoom más cercano para ver mejor los polígonos
  longitudeDelta: 0.5,
};

interface Feature {
    type: string;
    properties: { name: string };
    geometry: { type: string; coordinates: number[][][] };
  }

type PolygonPoint = { lat: number; lon: number };

type Area = {
  polygon: PolygonPoint[];
  probability: number;
};


const zones = [
  { id: 0, nombre: "-"},
  { id: 1, nombre: "Villa Campestre"},
  { id: 2, nombre: "Mallorquín"},
  { id: 3, nombre: "Malecón del Río"},
  { id: 4, nombre: "Soledad"},
  { id: 5, nombre: "Sur Oriente"},
  { id: 6, nombre: "Sur"},
  { id: 7, nombre: "Oriente"},
  { id: 8, nombre: "Sur Occidente"},
  { id: 9, nombre: "Centro"},
  { id: 10, nombre: "Eduardo Santos"},
  { id: 11, nombre: "Norte-Centro Histórico"},
  { id: 12, nombre: "Riomar"},
  { id: 13, nombre: "Norte"},

];


export default function ZonesScreen() {
  const [location, setLocation] = useState<Location.LocationObject | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [selectedSpecies, setSelectedSpecies] = useState<SpeciesDistribution[]>([]);
  const [selectedZone, setSelectedZone] = useState<string | null>(null);
  const [selectedZoneId, setSelectedZoneId] = useState<number | null>(null);

  const [userRegion, setUserRegion] = useState<Region | null>(null);
  const [selectedArea, setSelectedArea] = useState<any | null >(null);
  const [outlineMode, setOutlineMode] = useState(false);

  // DropDownPicker state (required props) BORRAR esto por si acaso
  const [open, setOpen] = useState<boolean>(false);
  const [value, setValue] = useState<number | null>(0);
  const [items, setItems] = useState<Array<{label: string; value: number}>>(
    zones.map((z) => ({ label: z.nombre, value: z.id }))
  );

  
  const toggleOutlineMode = () => setOutlineMode(!outlineMode);

  

  const centerOnUser = () => {
    if (location && mapRef.current) {
      mapRef.current.animateToRegion({
        latitude: location.coords.latitude,
        longitude: location.coords.longitude,
        latitudeDelta: 0.01,
        longitudeDelta: 0.01,
      }, 1000);
    } else {
      Alert.alert('📍 Ubicación no disponible', 'Asegúrate de haber otorgado permisos de ubicación');
    }
  };

  const handleZoneSelect = (zoneName: string, zoneId: number) => {
    setSelectedZone(zoneName);
    setSelectedZoneId(zoneId);
    setValue(zoneId);
    
    // Encontrar el polígono de la zona seleccionada
    const feature = zonas.features.find((f: Feature) => f.properties.name === zoneName);
    if (feature && mapRef.current) {
      const coords = feature.geometry.coordinates[0];
      const lats = coords.map(([lon, lat]: number[]) => lat);
      const lons = coords.map(([lon, lat]: number[]) => lon);
      
      const centerLat = (Math.min(...lats) + Math.max(...lats)) / 2;
      const centerLon = (Math.min(...lons) + Math.max(...lons)) / 2;
      const deltaLat = Math.max(...lats) - Math.min(...lats);
      const deltaLon = Math.max(...lons) - Math.min(...lons);
      
      mapRef.current.animateToRegion({
        latitude: centerLat,
        longitude: centerLon,
        latitudeDelta: deltaLat * 1.5,
        longitudeDelta: deltaLon * 1.5,
      }, 1000);
    }
  };


  // Simulated species data - this should be fetched from your API
  const [speciesData, setSpeciesData] = useState<SpeciesDistribution[]>([
    
  ]);
    

  useEffect(() => {
    (async () => {
      const { status } = await Location.requestForegroundPermissionsAsync();
      if (status === "granted") {
        const location = await Location.getCurrentPositionAsync({});
        setUserRegion({
          latitude: location.coords.latitude,
          longitude: location.coords.longitude,
          latitudeDelta: 0.5,
          longitudeDelta: 0.5,
        });
      }
    })();
  }, []);


  // 🔹 Calcular color según probabilidad
  const getColorByProbability = (p: number) => {
    if (p >= 0.9) return "#1a9850";
    if (p >= 0.7) return "#66bd63";
    if (p >= 0.5) return "#fdae61";
    if (p >= 0.4) return "#d73027";
    return "#cccccc";
  };


  const mapRef = useRef<MapView>(null);
  const [zonesFeatures, setZonesFeatures] = useState<Feature[]>([]);
  const [loadingZones, setLoadingZones] = useState<boolean>(false);
  
  useEffect(() => {
    // Cargar zonas desde el backend al montar
    (async () => {
      try {
        setLoadingZones(true);
        const data = await getZones();
        // esperar GeoJSON { features: [...] } o un array directo
        const features = data?.features || data;
        if (Array.isArray(features)) {
          setZonesFeatures(features as Feature[]);
          console.log('🌐 Loaded zones features:', features.length);
        } else {
          console.warn('Zones response has no features array, using local zonas.json fallback');
        }
      } catch (error) {
        console.error('Failed to load zones from API, using local fallback', error);
      } finally {
        setLoadingZones(false);
      }
    })();
  }, []);

  

  

  return (
    <LinearGradient
      colors={['#fffaf0', '#ffe4d6', '#ffd4ba']}
      style={styles.gradient}
    >
      <SafeAreaView style={styles.container} edges={['top']}>
        <ScrollView>
        {/* Header */}
        <Animatable.View animation="fadeInDown" duration={600} style={styles.header}>
          <View style={styles.headerContent}>
            <LinearGradient
              colors={['#60a5fa', '#2563eb']}
              style={styles.iconCircle}
            >
              <Ionicons name="map" size={28} color="#fff" />
            </LinearGradient>
            <View style={styles.headerText}>
              <Text style={styles.title}>Zonas de Barranquilla</Text>
              <Text style={styles.headerSubtitle}>🗺️ Explora por ubicación</Text>
            </View>
          </View>
        </Animatable.View>

        {/* Map Card */}
        <Animatable.View animation="fadeIn" duration={600} delay={200} style={styles.mapWrapper}>
          <View style={styles.mapCard}>
            <View style={styles.mapHeader}>
              <Ionicons name="navigate-circle" size={20} color="#2563eb" />
              <Text style={styles.mapTitle}>Mapa Interactivo</Text>
              {selectedZone && (
                <View style={styles.selectedBadge}>
                  <Text style={styles.selectedBadgeText}>{selectedZone}</Text>
                </View>
              )}
            </View>
            <View style={styles.mapContainer}>
              <MapView
                style={styles.map}
                showsUserLocation={true}
                loadingEnabled={true}
                ref={mapRef}
                initialRegion={userRegion || BARRANQUILLA_REGION}
              >
          {/* {selectedSpecies.map((sp, sIndex) =>
            sp.areas
              .filter((a: any) => a.probability >= 0.4)
              .map((area: any, aIndex: number) => (
                <Polygon
                  key={`${sp.species}-${aIndex}`}
                  coordinates={area.polygon.map((p: any) => ({
                    latitude: p.lat,
                    longitude: p.lon,
                  }))}
                  fillColor={
                    outlineMode
                      ? "transparent"
                      : `${getColorByProbability(area.probability)}80`
                  }
                  strokeColor={getColorByProbability(area.probability)}
                  strokeWidth={2}
                  tappable
                  onPress={() => handlePolygonPress(sp, area)}
                />
              ))
          )} */}
                {zonas.features.map((feature: Feature, i: number) => {
                  const coords = feature.geometry.coordinates[0].map(([lon, lat]) => ({
                    latitude: lat,
                    longitude: lon,
                  }));

                  const isSelected = selectedZone === feature.properties.name;
                  const fillColor = isSelected ? 'rgba(96, 165, 250, 0.5)' : 'rgba(96, 165, 250, 0.15)';
                  const strokeColor = isSelected ? '#2563eb' : '#60a5fa';
                  const strokeWidth = isSelected ? 4 : 2;

                  return (
                    <Polygon
                      key={i}
                      coordinates={coords}
                      strokeColor={strokeColor}
                      fillColor={fillColor}
                      strokeWidth={strokeWidth}
                      tappable
                      onPress={() => handleZoneSelect(feature.properties.name, zones.find(z => z.nombre === feature.properties.name)?.id || 0)}
                    />
                  );
                })}

              </MapView>
            </View>
          </View>
        </Animatable.View>
        {/* Zone Selector */}
        <Animatable.View animation="fadeInUp" duration={600} delay={400} style={styles.selectorWrapper}>
          <View style={styles.selectorCard}>
            <View style={styles.selectorHeader}>
              <Ionicons name="location" size={20} color="#60a5fa" />
              <Text style={styles.selectorTitle}>Selecciona una Zona</Text>
            </View>
            <DropDownPicker
              open={open}
              value={value}
              items={items}
              setOpen={setOpen}
              setValue={(callback) => {
                const newValue = typeof callback === 'function' ? callback(value) : callback;
                setValue(newValue);
                const zone = zones.find(z => z.id === newValue);
                if (zone && zone.id !== 0) {
                  handleZoneSelect(zone.nombre, zone.id);
                } else {
                  setSelectedZone(null);
                  setSelectedZoneId(null);
                }
              }}
              setItems={setItems}
              placeholder="Elige una zona..."
              style={styles.dropdown}
              dropDownContainerStyle={styles.dropdownContainer}
              textStyle={styles.dropdownText}
              listMode="SCROLLVIEW"
              selectedItemContainerStyle={styles.selectedItemContainer}
              selectedItemLabelStyle={styles.selectedItemLabel}
            />
          </View>

          {/* Info Cards */}
          <View style={styles.infoCardsContainer}>
            <View style={styles.infoCardSmall}>
              <LinearGradient
                colors={['#fff', '#fffaf0']}
                style={styles.infoCardGradient}
              >
                <Ionicons name="grid" size={18} color="#60a5fa" />
                <Text style={styles.infoCardNumber}>{zonas.features.length}</Text>
                <Text style={styles.infoCardLabel}>Zonas</Text>
              </LinearGradient>
            </View>
            {selectedZone && (
              <Animatable.View animation="bounceIn" duration={600} style={styles.infoCardSmall}>
                <LinearGradient
                  colors={['#60a5fa', '#2563eb']}
                  style={styles.infoCardGradient}
                >
                  <Ionicons name="checkmark-circle" size={18} color="#fff" />
                  <Text style={[styles.infoCardNumber, { color: '#fff' }]}>✓</Text>
                  <Text style={[styles.infoCardLabel, { color: '#fff' }]}>Seleccionada</Text>
                </LinearGradient>
              </Animatable.View>
            )}
          </View>
        </Animatable.View>
        </ScrollView>
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
    paddingTop: 10,
    paddingBottom: 16,
  },
  headerContent: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  iconCircle: {
    width: 56,
    height: 56,
    borderRadius: 28,
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#2563eb',
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
    color: '#2563eb',
    marginBottom: 2,
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#60a5fa',
    fontWeight: '500',
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
    borderBottomColor: '#dbeafe',
  },
  mapTitle: {
    flex: 1,
    fontSize: 16,
    fontWeight: '700',
    color: '#2563eb',
  },
  selectedBadge: {
    backgroundColor: '#60a5fa',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
  },
  selectedBadgeText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '600',
  },
  mapContainer: {
    height: Dimensions.get('window').height * 0.4,
    overflow: 'hidden',
  },
  map: {
    width: '100%',
    height: '100%',
  },
  locationButton: {
    position: 'absolute',
    bottom: 16,
    right: 16,
    borderRadius: 28,
    overflow: 'hidden',
    shadowColor: '#16a34a',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 6,
  },
  locationButtonGradient: {
    width: 56,
    height: 56,
    alignItems: 'center',
    justifyContent: 'center',
  },
  selectorWrapper: {
    marginHorizontal: 20,
    marginBottom: 20,
  },
  selectorCard: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
    marginBottom: 16,
    zIndex: 1000,
  },
  selectorHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 12,
  },
  selectorTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: '#2563eb',
  },
  dropdown: {
    backgroundColor: '#fffaf0',
    borderColor: '#60a5fa',
    borderWidth: 2,
    borderRadius: 12,
    minHeight: 50,
  },
  dropdownContainer: {
    borderColor: '#60a5fa',
    borderWidth: 2,
    backgroundColor: '#fff',
    borderRadius: 12,
    marginTop: 4,
  },
  dropdownText: {
    fontSize: 15,
    color: '#333',
    fontWeight: '500',
  },
  selectedItemContainer: {
    backgroundColor: '#dbeafe',
  },
  selectedItemLabel: {
    fontWeight: '700',
    color: '#2563eb',
  },
  infoCardsContainer: {
    flexDirection: 'row',
    gap: 12,
  },
  infoCardSmall: {
    flex: 1,
    borderRadius: 16,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  infoCardGradient: {
    padding: 16,
    alignItems: 'center',
    gap: 4,
  },
  infoCardNumber: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2563eb',
  },
  infoCardLabel: {
    fontSize: 12,
    color: '#666',
    fontWeight: '600',
  },
});