import { View, Text, StyleSheet, TouchableOpacity, ScrollView, Dimensions, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import MapView, { Marker, Polygon } from 'react-native-maps';
import * as Location from 'expo-location';
import { useEffect, useState, useRef } from 'react';
import { SpeciesDistribution } from '../../../../data/types';
import Ionicons from '@expo/vector-icons/Ionicons';


// Centro exacto del polígono principal
const BARRANQUILLA_REGION = {
  latitude: 11.008083495495494,
  longitude: -74.84013450450449,
  latitudeDelta: 0.01, // Zoom más cercano para ver mejor los polígonos
  longitudeDelta: 0.01,
};





export default function ZonesScreen() {
  const [location, setLocation] = useState<Location.LocationObject | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [selectedSpecies, setSelectedSpecies] = useState<SpeciesDistribution | null>(null);
  const [probabilityText, setProbabilityText] = useState<string | null>(null);
  const mapRef = useRef<MapView | null>(null);
  const [outlineMode, setOutlineMode] = useState(false);

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

    if (status !== 'granted') {
      setErrorMsg('Permiso de ubicación denegado');
      return;
    }

    const currentLocation = await Location.getCurrentPositionAsync({
      accuracy: Location.Accuracy.High,
    });

    setLocation(currentLocation);
  })();
}, []);

  const handleSelectSpecies = (species: SpeciesDistribution) => {
    setSelectedSpecies(species);
    const avg = species.areas.reduce((sum, a) => sum + a.probability, 0) / species.areas.length;
    const nearby = species.areas.filter(
      (a) => Math.abs(a.probability - avg) 
    );
    const avgNearby =
      nearby.reduce((sum, a) => sum + a.probability, 0) / nearby.length || avg;
    setProbabilityText(`Probabilidad en zona: ${(avgNearby * 100).toFixed(1)}%`);
  };

 

  const getAreaStyle = ( probability: number , outlineMode: boolean ) => {
    const p = probability * 100; // pasa a porcentaje (0–100)
    const fillColor = getColorForRange(p); // color por defecto (gris semi-transparente)

    if (outlineMode){
      return {
        strokeColor: fillColor,
        strokeWidth: 4,
        fillColor: 'transparent',
      };
    } else {
      return { 
      strokeColor: '#00000055',
      strokeWidth: 1,
      fillColor: fillColor + '88',
    };
  };
                 

    
  };

  const getColorForRange = (p: number) => {
    if (p < 10) return "#ffd057ff";       
    else if (p < 20) return "#FAA307";
    else if (p < 30) return "#F48C06";
    else if (p < 40) return "#E85D04";
    else if (p < 50) return"#DC2F02";
    else if (p < 60) return"#D00000";  
    else if (p < 70) return"#9D0208";
    else if (p < 80) return "#6A040F";
    else if (p < 90) return "#370617";  
    else return "#03071E";
  };


  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.mapContainer}>
        <Text style={styles.subtitle}>Selecciona una especie para ver su distribución a 500 metros de ti</Text>
        <MapView
          style={styles.map}
          initialRegion={BARRANQUILLA_REGION}
          showsUserLocation={true}
          loadingEnabled={true}
          ref={mapRef}
            >
          {selectedSpecies && selectedSpecies.areas.map((area, areaIndex) => {
            return (
              <>
                <Polygon
                  key={`${selectedSpecies.species}-${areaIndex}`}
                  coordinates={area.polygon.map(point => ({
                    latitude: point.lat,
                    longitude: point.lon,
                  }))}
                  {...getAreaStyle(area.probability, outlineMode)}
                  zIndex={1000 + areaIndex}
                  
                />
              </>
            );
          })}
          <TouchableOpacity style={styles.optionButton} onPress={centerOnUser}>
            <Text style={styles.optionText}><Ionicons name="pin" size={20} color={"#ffffffff"} /></Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.toggleButton} onPress={toggleOutlineMode}>
            <Text style={styles.toggleButtonText}>
              {outlineMode 
              ? <Ionicons name="radio-button-off" size={20} color={"#ffffffff"} /> 
              : <Ionicons name="radio-button-on" size={20} color={"#ffffffff"} /> }
            </Text>
          </TouchableOpacity>
          

        </MapView>
        
      </View>
    <Text style={styles.subtitle}>Especies en un radio de 500 metros de ti</Text>
    <View style={styles.legendContainer}>
            <Text style={styles.legendTitle}>Probabilidad</Text>
            <View style={styles.legendBar}>
            {Array.from({ length: 10 }).map((_, i) => (
              <View
                key={i}
                style={{
                  flex: 1,
                  height: 15,
                  backgroundColor: getColorForRange(i * 10),
                }}
              />
            ))}
          </View>
          <View style={styles.legendLabels}>
            <Text style={styles.legendText}>0%</Text>
            <Text style={styles.legendText}>10%</Text>
            <Text style={styles.legendText}>20%</Text>
            <Text style={styles.legendText}>30%</Text>
            <Text style={styles.legendText}>40%</Text>
            <Text style={styles.legendText}>50%</Text>
            <Text style={styles.legendText}>60%</Text>
            <Text style={styles.legendText}>70%</Text>
            <Text style={styles.legendText}>80%</Text>
            <Text style={styles.legendText}>90%</Text>
            <Text style={styles.legendText}>100%</Text>
          </View>
          </View>
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

});