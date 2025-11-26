import { View, Text, StyleSheet, TouchableOpacity, ScrollView, Dimensions, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import MapView, { PROVIDER_GOOGLE, Polygon, LatLng, Region } from 'react-native-maps';
import * as Location from 'expo-location';
import { useEffect, useState, useRef } from 'react';
import { SpeciesDistribution } from '../../../../data/types';
import Ionicons from '@expo/vector-icons/Ionicons';
import zonas from '../../../../data/zonas.json';
import bird_zones from "../../../../data/bird_zones_test.json";
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
    {
    "species": "Pitangus sulphuratus",
      "max_probability": 0.7193924648228038,
      "areas": [
        {
          "polygon": [
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            }
          ],
          "probability": 0.1
        },
        {
          "polygon": [
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            }
          ],
          "probability": 0.3
        },
        {
          "polygon": [
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            }
          ],
          "probability": 0.5
        },
        {
          "polygon": [
            {
              "lat": 11.00413451590366,
              "lon": -74.84353246368818
            },
            {
              "lat": 11.004318189373047,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.005420230189372,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.005603903658761,
              "lon": -74.84445083103512
            },
            {
              "lat": 11.005603903658761,
              "lon": -74.84243042287184
            },
            {
              "lat": 11.005420230189372,
              "lon": -74.84224674940246
            },
            {
              "lat": 11.005052883250597,
              "lon": -74.84206307593307
            },
            {
              "lat": 11.004501862842435,
              "lon": -74.84206307593307
            },
            {
              "lat": 11.004318189373047,
              "lon": -74.84243042287184
            },
            {
              "lat": 11.00413451590366,
              "lon": -74.84279776981063
            },
            {
              "lat": 11.00413451590366,
              "lon": -74.84353246368818
            }
          ],
          "probability": 0.7
        }
      ]
    },
    {
      "species": "Eupsittula pertinax",
      "max_probability": 0.7275209917775228,
      "areas": [
        {
          "polygon": [
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            }
          ],
          "probability": 0.1
        },
        {
          "polygon": [
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.01258349,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.8356347
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            }
          ],
          "probability": 0.3
        },
        {
          "polygon": [
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            }
          ],
          "probability": 0.5
        },
        {
          "polygon": [
            {
              "lat": 11.003950842434271,
              "lon": -74.83747123919835
            },
            {
              "lat": 11.00413451590366,
              "lon": -74.84389981062695
            },
            {
              "lat": 11.004318189373047,
              "lon": -74.84426715756574
            },
            {
              "lat": 11.004685536311822,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.00872635263835,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.008910026107738,
              "lon": -74.84445083103512
            },
            {
              "lat": 11.009277373046514,
              "lon": -74.84371613715757
            },
            {
              "lat": 11.009277373046514,
              "lon": -74.84041001470857
            },
            {
              "lat": 11.008910026107738,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003950842434271,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003950842434271,
              "lon": -74.83747123919835
            }
          ],
          "probability": 0.7
        }
      ]
    },
    {
      "species": "Troglodytes musculus",
      "max_probability": 0.6869101504128007,
      "areas": [
        {
          "polygon": [
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            }
          ],
          "probability": 0.1
        },
        {
          "polygon": [
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            }
          ],
          "probability": 0.3
        },
        {
          "polygon": [
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.83857328001469
            },
            {
              "lat": 11.012216148556716,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            }
          ],
          "probability": 0.5
        }
      ]
    },
    {
      "species": "Columbina talpacoti",
      "max_probability": 0.6344262865941791,
      "areas": [
        {
          "polygon": [
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            }
          ],
          "probability": 0.1
        },
        {
          "polygon": [
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            }
          ],
          "probability": 0.3
        },
        {
          "polygon": [
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            }
          ],
          "probability": 0.5
        }
      ]
    },
    {
      "species": "Ortalis garrula",
      "max_probability": 0.6151326933334732,
      "areas": [
        {
          "polygon": [
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            }
          ],
          "probability": 0.1
        },
        {
          "polygon": [
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.83930797389225
            },
            {
              "lat": 11.009828393454676,
              "lon": -74.83655287185141
            },
            {
              "lat": 11.0094610465159,
              "lon": -74.83636919838203
            },
            {
              "lat": 11.007807985291413,
              "lon": -74.83636919838203
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.83655287185141
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            }
          ],
          "probability": 0.3
        },
        {
          "polygon": [
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84187940246369
            },
            {
              "lat": 11.00872635263835,
              "lon": -74.84114470858613
            },
            {
              "lat": 11.008542679168963,
              "lon": -74.84114470858613
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.8415120555249
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            }
          ],
          "probability": 0.5
        }
      ]
    },
    {
      "species": "Saltator olivascens",
      "max_probability": 0.5216329142995201,
      "areas": [
        {
          "polygon": [
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            }
          ],
          "probability": 0.1
        },
        {
          "polygon": [
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            }
          ],
          "probability": 0.3
        },
        {
          "polygon": [
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.005787577128148,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.005787577128148,
              "lon": -74.8433487902188
            },
            {
              "lat": 11.005603903658761,
              "lon": -74.84261409634124
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84224674940246
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            }
          ],
          "probability": 0.5
        }
      ]
    },
    {
      "species": "Icterus nigrogularis",
      "max_probability": 0.462643356040526,
      "areas": [
        {
          "polygon": [
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            }
          ],
          "probability": 0.1
        },
        {
          "polygon": [
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            }
          ],
          "probability": 0.3
        }
      ]
    },
    {
      "species": "Cathartes aura",
      "max_probability": 0.4547689164480209,
      "areas": [
        {
          "polygon": [
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            }
          ],
          "probability": 0.1
        },
        {
          "polygon": [
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            }
          ],
          "probability": 0.3
        }
      ]
    },
    {
      "species": "Coragyps atratus",
      "max_probability": 0.49163585443351693,
      "areas": [
        {
          "polygon": [
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            }
          ],
          "probability": 0.1
        },
        {
          "polygon": [
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            }
          ],
          "probability": 0.3
        }
      ]
    },
    {
      "species": "Tyrannus melancholicus",
      "max_probability": 0.5110163455595941,
      "areas": [
        {
          "polygon": [
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            }
          ],
          "probability": 0.1
        },
        {
          "polygon": [
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            }
          ],
          "probability": 0.3
        },
        {
          "polygon": [
            {
              "lat": 11.004501862842435,
              "lon": -74.8415120555249
            },
            {
              "lat": 11.004685536311822,
              "lon": -74.84224674940246
            },
            {
              "lat": 11.00486920978121,
              "lon": -74.84132838205552
            },
            {
              "lat": 11.00486920978121,
              "lon": -74.83949164736163
            },
            {
              "lat": 11.004501862842435,
              "lon": -74.83949164736163
            },
            {
              "lat": 11.004501862842435,
              "lon": -74.8415120555249
            }
          ],
          "probability": 0.5
        }
      ]
    },
    {
      "species": "Melanerpes rubricapillus",
      "max_probability": 0.4482163499678894,
      "areas": [
        {
          "polygon": [
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            }
          ],
          "probability": 0.1
        },
        {
          "polygon": [
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            }
          ],
          "probability": 0.3
        }
      ]
    },
    {
      "species": "Campylorhynchus griseus",
      "max_probability": 0.43360289284578585,
      "areas": [
        {
          "polygon": [
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            }
          ],
          "probability": 0.1
        },
        {
          "polygon": [
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            }
          ],
          "probability": 0.3
        }
      ]
    },
    {
      "species": "Quiscalus mexicanus",
      "max_probability": 0.5353834344775447,
      "areas": [
        {
          "polygon": [
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            }
          ],
          "probability": 0.1
        },
        {
          "polygon": [
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            }
          ],
          "probability": 0.3
        },
        {
          "polygon": [
            {
              "lat": 11.010563087332226,
              "lon": -74.83581817797386
            },
            {
              "lat": 11.010746760801615,
              "lon": -74.83600185144324
            },
            {
              "lat": 11.01111410774039,
              "lon": -74.83618552491264
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.83618552491264
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.010563087332226,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.010563087332226,
              "lon": -74.83581817797386
            }
          ],
          "probability": 0.5
        }
      ]
    },
    {
      "species": "Quiscalus lugubris",
      "max_probability": 0.31022888182042935,
      "areas": [
        {
          "polygon": [
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            }
          ],
          "probability": 0.1
        },
        {
          "polygon": [
            {
              "lat": 11.012216148556716,
              "lon": -74.84279776981063
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.8431651167494
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.83563450450447
            },
            {
              "lat": 11.012216148556716,
              "lon": -74.84261409634124
            },
            {
              "lat": 11.012216148556716,
              "lon": -74.84279776981063
            }
          ],
          "probability": 0.3
        }
      ]
    },
    {
      "species": "Ardea alba",
      "max_probability": 0.13743707702836286,
      "areas": [
        {
          "polygon": [
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84463450450451
            },
            {
              "lat": 11.012583495495491,
              "lon": -74.84041001470857
            },
            {
              "lat": 11.006705944475087,
              "lon": -74.84022634123919
            },
            {
              "lat": 11.006522271005698,
              "lon": -74.84022634123919
            },
            {
              "lat": 11.006154924066923,
              "lon": -74.84041001470857
            },
            {
              "lat": 11.005971250597536,
              "lon": -74.84059368817796
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.8431651167494
            },
            {
              "lat": 11.003583495495496,
              "lon": -74.84463450450451
            }
          ],
          "probability": 0.1
        }
        ]
    }
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