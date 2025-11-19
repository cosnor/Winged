import { View, Text, StyleSheet, TouchableOpacity, ScrollView, Dimensions, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import MapView, { PROVIDER_GOOGLE, Polygon, LatLng, Region } from 'react-native-maps';
import * as Location from 'expo-location';
import { useEffect, useState, useRef } from 'react';
import { SpeciesDistribution } from '../../../../data/types';
import Ionicons from '@expo/vector-icons/Ionicons';
import zonas from '../../../../data/zonas.json';
import bird_zones from "../../../../data/bird_zones_test.json"; // Tu JSON con las aves
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
          {zonas.features.map((feature: Feature, i: number) => {
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
        <TouchableOpacity style={styles.optionButton} onPress={centerOnUser}>
            <Text style={styles.optionText}><Ionicons name="pin" size={20} color={"#ffffffff"} /></Text>
          </TouchableOpacity>
        </MapView>
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
    color: "#333",
  },
  selectedText: {
    marginTop: 20,
    fontSize: 16,
    color: "#ff7809ff",
    fontWeight: "400",
  },
});