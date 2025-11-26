import { View, Text, StyleSheet, TouchableOpacity, ScrollView, Dimensions, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import MapView, { PROVIDER_GOOGLE, Polygon, LatLng, Region } from 'react-native-maps';
import * as Location from 'expo-location';
import { useEffect, useState, useRef } from 'react';
import { SpeciesDistribution } from '../../../../data/types';
import Ionicons from '@expo/vector-icons/Ionicons';
import zonas from '../../../../data/zonas.json';
import bird_zones from "../../../../data/bird_zones_test.json"; // Tu JSON con las aves
import { getZones, getZonesForPoint } from '../../../../services/mapsService';
import { ActivityIndicator } from 'react-native';
import DropDownPicker from "react-native-dropdown-picker";


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
      }, 1000); // 1 segundo de animación
    } else {
      Alert.alert('Ubicación no disponible', 'Asegúrate de haber otorgado permisos de ubicación. Si tiene permiso, espere unos momentos');
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

  useEffect(() => {
    // Cargar distribución de especies para la ubicación del usuario
    (async () => {
      if (userRegion?.latitude && userRegion?.longitude) {
        try {
          const data = await getZonesForPoint(
            userRegion.latitude,
            userRegion.longitude,
            500,
            0.002
          );
          if (data?.species_distributions) {
            setSpeciesData(data.species_distributions);
            console.log('📍 Loaded species distribution for location:', data.species_distributions.length, 'species');
          }
        } catch (error) {
          console.error('Failed to load species distribution:', error);
        }
      }
    })();
  }, [userRegion]);

  

  

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.mapContainer}>
        <Text style={styles.subtitle}>Selecciona una especie para ver su distribución a 500 metros de ti</Text>
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
          {(zonesFeatures.length ? zonesFeatures : zonas.features).map((feature: Feature, i: number) => {
            const coords = feature.geometry.coordinates[0].map(([lon, lat]) => ({
              latitude: lat,
              longitude: lon,
            }));

            const fillColor = "#2196F380";

            return (
              <Polygon
                key={i}
                coordinates={coords}
                strokeColor="#2E7D32"
                fillColor={fillColor}
                strokeWidth={2}
                tappable
                onPress={() => setSelectedZone(feature.properties.name)}
              />
            );
          })}
        </MapView>
        {loadingZones && (
          <View style={{ position: 'absolute', top: 16, left: 16, zIndex: 1000 }} pointerEvents="none">
            <ActivityIndicator size="small" color="#2E7D32" />
          </View>
        )}
        <TouchableOpacity style={styles.optionButton} onPress={centerOnUser}>
          <Text style={styles.optionText}><Ionicons name="pin" size={20} color={"#ffffffff"} /></Text>
        </TouchableOpacity>
        {selectedZone && (
        <View style={styles.infoBox}>
          <Text style={styles.infoText}>📍 {selectedZone}</Text>
          <TouchableOpacity onPress={() => setSelectedZone(null)}>
            <Text style={styles.closeBtn}>Cerrar</Text>
          </TouchableOpacity>
        </View>
      )}
      </View>
      <View style={styles.speciesList}>
        <Text style={{ marginBottom: 10 }}>Selecciona una zona:</Text>

      <DropDownPicker
        open={open}
        value={value}
        items={items}
        setOpen={setOpen}
        setValue={setValue}
        setItems={setItems}
        placeholder="Elige una zona"
        style={styles.dropdown}
        dropDownContainerStyle={styles.dropdownContainer}
        textStyle={styles.dropdownText}
        listMode="SCROLLVIEW"
      />
      
      <View style={styles.constructionContainer}>
        <Text style={styles.constructionText}>🚧 Módulo en construcción — nuevas funciones próximamente.</Text>
      </View>
      
      </View>
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
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#d2691e',
    textAlign: 'center',
    padding: 10,
    paddingBottom: 4,
  },
  subtitle: {
    fontSize: 14,
    fontStyle: 'italic',
    color: '#666',
    textAlign: 'justify',
    paddingTop: 0,
    paddingBottom: 10,
    paddingHorizontal: 20,



  },
  mapContainer: {
    height: Dimensions.get('window').height * 0.4, // Reducido para dejar más espacio a la lista
    overflow: 'hidden',
    margin: 0,
    marginBottom: 8, // Reducido para acercar la lista
    elevation: 3,
    shadowRadius: 3.84,
  },
  map: {
    flex: 1,
  },
  infoBox: {
    position: "absolute",
    bottom: 30,
    left: 20,
    right: 20,
    backgroundColor: "rgba(255,255,255,0.95)",
    borderRadius: 10,
    padding: 10,
    shadowColor: "#000",
    shadowOpacity: 0.2,
    shadowRadius: 4,
    elevation: 5,
  },
  infoText: { fontSize: 16, fontWeight: "600", color: "#333" },
  closeBtn: { color: "#2196F3", marginTop: 5, textAlign: "right" },
  speciesList: {
    flex: 1,
    paddingHorizontal: 20,
    paddingTop: 5,
    
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
  optionButton: {
    position: 'absolute',
    bottom: 50,
    right: 10,
    backgroundColor: '#d2691edc',
    padding: 10,
    borderRadius: 10,
    alignItems: 'center',
  },
  optionText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  legendContainer: {
        
    paddingHorizontal: 20,
    borderRadius: 12,
    elevation: 5,
  },
  legendTitle: { fontWeight: 'bold', fontSize: 12, marginBottom: 5 },
  legendBar: {
    flexDirection: 'row',
    borderRadius: 8,
    overflow: 'hidden',
  },
  legendLabels: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 3,
    paddingHorizontal: 5,
  },
  legendText: { fontSize: 8, color: '#333' },
  toggleButton: {
    position: 'absolute',
    bottom: 100,
    right: 10,
    backgroundColor: '#d2691edc',
    padding: 10,
    borderRadius: 8,
    elevation: 5,
  },
  toggleButtonText: { fontWeight: 'bold', color: '#333', fontSize: 12 },
  label: {
    fontSize: 16,
    fontWeight: "500",
    marginBottom: 10,
    color: "#333",
  },
  dropdown: {
    backgroundColor: "transparent",
    borderColor: "transparent",
    borderBottomColor: "#ff9a41ff",
  },
  dropdownContainer: {
    borderColor: "#ff9a41ff",
    backgroundColor: "#fffaf0",
  },
  dropdownText: {
    fontSize: 15,
    color: '#333',
  },
  selectedText: {
    marginTop: 20,
    fontSize: 16,
    color: "#ff7809ff",
    fontWeight: "400",
  },
  constructionContainer: {
    marginHorizontal: 20,
    marginTop: 12,
    paddingVertical: 10,
    paddingHorizontal: 12,
    borderRadius: 8,
    backgroundColor: '#fff4e6',
    borderWidth: 1,
    borderColor: '#f0c7a3',
    alignItems: 'center',
  },
  constructionText: {
    color: '#8a4b00',
    fontSize: 13,
    textAlign: 'center',
  },
});