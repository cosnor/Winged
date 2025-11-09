import { View, Text, StyleSheet, TouchableOpacity, ScrollView, Dimensions, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import MapView, { Marker, Polygon } from 'react-native-maps';
import * as Location from 'expo-location';
import { useEffect, useState } from 'react';
import { SpeciesDistribution } from '../../../../data/types';

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
    console.log("Selected Species:", selectedSpecies);
    console.log("Species Data:", speciesData);
  }, [selectedSpecies, speciesData]);

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



  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>¡Encuentra aves cerca de ti!</Text>
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
            return (
              <>
                <Marker flat  coordinate={{
                  latitude: area.polygon[0].lat , 
                  longitude: area.polygon[0].lon
                  }}
                >
                  {/* Ajustar para que quede con los colores */}
                  <View style={styles.probabilityBox}>
                    <Text style={{ color: '#000', fontWeight: 'bold' }}>
                      {(area.probability * 100).toFixed(1)}%
                    </Text>
                  </View>
                </Marker>

                <Polygon
                  key={`${selectedSpecies.species}-${areaIndex}`}
                  coordinates={area.polygon.map(point => ({
                    latitude: point.lat,
                    longitude: point.lon,
                  }))}
                  {...getAreaStyle(area.probability)}
                  zIndex={1000}
                  
                />
              </>
            );
          })}
        </MapView>
      </View>
    <Text style={styles.subtitle}>Especies en un radio de 500 metros de ti</Text>
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
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#d2691e',
    textAlign: 'center',
    padding: 16,
    paddingBottom: 4,
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