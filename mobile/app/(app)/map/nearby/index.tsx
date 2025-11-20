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
      "max_probability": 0.8520902615359469,
      "areas": [
        {
          "polygon": [
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            }
          ],
          "probability": 0.1
        },
        {
          "polygon": [
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            }
          ],
          "probability": 0.3
        },
        {
          "polygon": [
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            }
          ],
          "probability": 0.5
        },
        {
          "polygon": [
            {
              "lat": 11.014995495495496,
              "lon": -74.85119838205551
            },
            {
              "lat": 11.020505699577125,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.84991266776979
            },
            {
              "lat": 11.023444475087327,
              "lon": -74.84881062695345
            },
            {
              "lat": 11.02326080161794,
              "lon": -74.84844328001468
            },
            {
              "lat": 11.023077128148552,
              "lon": -74.8480759330759
            },
            {
              "lat": 11.022893454679165,
              "lon": -74.84789225960651
            },
            {
              "lat": 11.022158760801615,
              "lon": -74.84789225960651
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.8497289943004
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.85119838205551
            }
          ],
          "probability": 0.7
        }
      ]
    },
    {
      "species": "Coragyps atratus",
      "max_probability": 0.6911085097790898,
      "areas": [
        {
          "polygon": [
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            }
          ],
          "probability": 0.1
        },
        {
          "polygon": [
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            }
          ],
          "probability": 0.3
        },
        {
          "polygon": [
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.02326080161794,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.84954532083101
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            }
          ],
          "probability": 0.5
        }
      ]
    },
    {
      "species": "Eupsittula pertinax",
      "max_probability": 0.7244091493315742,
      "areas": [
        {
          "polygon": [
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            }
          ],
          "probability": 0.1
        },
        {
          "polygon": [
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            }
          ],
          "probability": 0.3
        },
        {
          "polygon": [
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023444475087327,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023628148556716,
              "lon": -74.85413715756573
            },
            {
              "lat": 11.023811822026103,
              "lon": -74.85340246368817
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.85230042287183
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            }
          ],
          "probability": 0.5
        },
        {
          "polygon": [
            {
              "lat": 11.022893454679165,
              "lon": -74.84991266776979
            },
            {
              "lat": 11.023077128148552,
              "lon": -74.84991266776979
            },
            {
              "lat": 11.023077128148552,
              "lon": -74.84844328001468
            },
            {
              "lat": 11.022893454679165,
              "lon": -74.84844328001468
            },
            {
              "lat": 11.022893454679165,
              "lon": -74.84991266776979
            }
          ],
          "probability": 0.7
        }
      ]
    },
    {
      "species": "Cathartes aura",
      "max_probability": 0.5093539849836454,
      "areas": [
        {
          "polygon": [
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            }
          ],
          "probability": 0.1
        },
        {
          "polygon": [
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.8466065453208
            },
            {
              "lat": 11.023811822026103,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            }
          ],
          "probability": 0.3
        },
        {
          "polygon": [
            {
              "lat": 11.014995495495496,
              "lon": -74.85266776981062
            },
            {
              "lat": 11.01554651590366,
              "lon": -74.85248409634123
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.85046368817795
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.85266776981062
            }
          ],
          "probability": 0.5
        }
      ]
    },
    {
      "species": "Campylorhynchus griseus",
      "max_probability": 0.5871710038049661,
      "areas": [
        {
          "polygon": [
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            }
          ],
          "probability": 0.1
        },
        {
          "polygon": [
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            }
          ],
          "probability": 0.3
        },
        {
          "polygon": [
            {
              "lat": 11.021056719985289,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.85285144328
            },
            {
              "lat": 11.023444475087327,
              "lon": -74.85046368817795
            },
            {
              "lat": 11.023077128148552,
              "lon": -74.85028001470856
            },
            {
              "lat": 11.022893454679165,
              "lon": -74.85046368817795
            },
            {
              "lat": 11.021056719985289,
              "lon": -74.85432083103511
            },
            {
              "lat": 11.021056719985289,
              "lon": -74.8545045045045
            }
          ],
          "probability": 0.5
        }
      ]
    },
    {
      "species": "Tyrannus melancholicus",
      "max_probability": 0.6690896935137991,
      "areas": [
        {
          "polygon": [
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            }
          ],
          "probability": 0.1
        },
        {
          "polygon": [
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            }
          ],
          "probability": 0.3
        },
        {
          "polygon": [
            {
              "lat": 11.018852638352637,
              "lon": -74.85101470858612
            },
            {
              "lat": 11.019036311822024,
              "lon": -74.85358613715756
            },
            {
              "lat": 11.019219985291413,
              "lon": -74.85413715756573
            },
            {
              "lat": 11.0194036587608,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.020322026107738,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.02013835263835,
              "lon": -74.84587185144323
            },
            {
              "lat": 11.019036311822024,
              "lon": -74.84825960654528
            },
            {
              "lat": 11.018852638352637,
              "lon": -74.8497289943004
            },
            {
              "lat": 11.018852638352637,
              "lon": -74.85101470858612
            }
          ],
          "probability": 0.5
        }
      ]
    },
    {
      "species": "Ortalis garrula",
      "max_probability": 0.7970137221312686,
      "areas": [
        {
          "polygon": [
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            }
          ],
          "probability": 0.1
        },
        {
          "polygon": [
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            }
          ],
          "probability": 0.3
        },
        {
          "polygon": [
            {
              "lat": 11.015362842434271,
              "lon": -74.85046368817795
            },
            {
              "lat": 11.01554651590366,
              "lon": -74.85064736164735
            },
            {
              "lat": 11.021240393454676,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023444475087327,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023811822026103,
              "lon": -74.85395348409634
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.85358613715756
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.84770858613713
            },
            {
              "lat": 11.023811822026103,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.016832230189372,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.015730189373047,
              "lon": -74.84752491266774
            },
            {
              "lat": 11.01554651590366,
              "lon": -74.8480759330759
            },
            {
              "lat": 11.015362842434271,
              "lon": -74.85046368817795
            }
          ],
          "probability": 0.5
        },
        {
          "polygon": [
            {
              "lat": 11.021424066924064,
              "lon": -74.85064736164735
            },
            {
              "lat": 11.021607740393451,
              "lon": -74.85119838205551
            },
            {
              "lat": 11.021975087332226,
              "lon": -74.85211674940246
            },
            {
              "lat": 11.022709781209777,
              "lon": -74.85174940246368
            },
            {
              "lat": 11.022893454679165,
              "lon": -74.85156572899429
            },
            {
              "lat": 11.023077128148552,
              "lon": -74.8513820555249
            },
            {
              "lat": 11.02326080161794,
              "lon": -74.85101470858612
            },
            {
              "lat": 11.023444475087327,
              "lon": -74.85064736164735
            },
            {
              "lat": 11.023444475087327,
              "lon": -74.85046368817795
            },
            {
              "lat": 11.02326080161794,
              "lon": -74.85028001470856
            },
            {
              "lat": 11.023077128148552,
              "lon": -74.85009634123918
            },
            {
              "lat": 11.022709781209777,
              "lon": -74.84991266776979
            },
            {
              "lat": 11.022158760801615,
              "lon": -74.8497289943004
            },
            {
              "lat": 11.021975087332226,
              "lon": -74.8497289943004
            },
            {
              "lat": 11.021607740393451,
              "lon": -74.84991266776979
            },
            {
              "lat": 11.021424066924064,
              "lon": -74.85028001470856
            },
            {
              "lat": 11.021424066924064,
              "lon": -74.85064736164735
            }
          ],
          "probability": 0.7
        }
      ]
    },
    {
      "species": "Columbina talpacoti",
      "max_probability": 0.4961258140680064,
      "areas": [
        {
          "polygon": [
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            }
          ],
          "probability": 0.1
        },
        {
          "polygon": [
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.02326080161794,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023628148556716,
              "lon": -74.84936164736162
            },
            {
              "lat": 11.023628148556716,
              "lon": -74.84679021879018
            },
            {
              "lat": 11.023444475087327,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            }
          ],
          "probability": 0.3
        }
      ]
    },
    {
      "species": "Quiscalus mexicanus",
      "max_probability": 0.4108161896921655,
      "areas": [
        {
          "polygon": [
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            }
          ],
          "probability": 0.1
        },
        {
          "polygon": [
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023811822026103,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.85266776981062
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.85230042287183
            },
            {
              "lat": 11.023811822026103,
              "lon": -74.85028001470856
            },
            {
              "lat": 11.023077128148552,
              "lon": -74.8480759330759
            },
            {
              "lat": 11.02179141386284,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            }
          ],
          "probability": 0.3
        }
      ]
    },
    {
      "species": "Saltator olivascens",
      "max_probability": 0.6235054867277563,
      "areas": [
        {
          "polygon": [
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            }
          ],
          "probability": 0.1
        },
        {
          "polygon": [
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023811822026103,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.8530351167494
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            }
          ],
          "probability": 0.3
        },
        {
          "polygon": [
            {
              "lat": 11.021056719985289,
              "lon": -74.85064736164735
            },
            {
              "lat": 11.021424066924064,
              "lon": -74.85413715756573
            },
            {
              "lat": 11.021607740393451,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023077128148552,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.02326080161794,
              "lon": -74.85285144328
            },
            {
              "lat": 11.023444475087327,
              "lon": -74.85046368817795
            },
            {
              "lat": 11.023444475087327,
              "lon": -74.85028001470856
            },
            {
              "lat": 11.02326080161794,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.021056719985289,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.021056719985289,
              "lon": -74.85064736164735
            }
          ],
          "probability": 0.5
        }
      ]
    },
    {
      "species": "Troglodytes musculus",
      "max_probability": 0.5212272421745348,
      "areas": [
        {
          "polygon": [
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            }
          ],
          "probability": 0.1
        },
        {
          "polygon": [
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            }
          ],
          "probability": 0.3
        },
        {
          "polygon": [
            {
              "lat": 11.02179141386284,
              "lon": -74.84954532083101
            },
            {
              "lat": 11.021975087332226,
              "lon": -74.85028001470856
            },
            {
              "lat": 11.022158760801615,
              "lon": -74.85028001470856
            },
            {
              "lat": 11.022342434271001,
              "lon": -74.85009634123918
            },
            {
              "lat": 11.022709781209777,
              "lon": -74.84954532083101
            },
            {
              "lat": 11.02252610774039,
              "lon": -74.84936164736162
            },
            {
              "lat": 11.022342434271001,
              "lon": -74.84917797389224
            },
            {
              "lat": 11.021975087332226,
              "lon": -74.84917797389224
            },
            {
              "lat": 11.02179141386284,
              "lon": -74.84954532083101
            }
          ],
          "probability": 0.5
        }
      ]
    },
    {
      "species": "Icterus nigrogularis",
      "max_probability": 0.5051371104427056,
      "areas": [
        {
          "polygon": [
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            }
          ],
          "probability": 0.1
        },
        {
          "polygon": [
            {
              "lat": 11.014995495495496,
              "lon": -74.85064736164735
            },
            {
              "lat": 11.01628120978121,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.85064736164735
            }
          ],
          "probability": 0.3
        },
        {
          "polygon": [
            {
              "lat": 11.019954679168963,
              "lon": -74.8466065453208
            },
            {
              "lat": 11.02013835263835,
              "lon": -74.8466065453208
            },
            {
              "lat": 11.020322026107738,
              "lon": -74.8464228718514
            },
            {
              "lat": 11.020322026107738,
              "lon": -74.84587185144323
            },
            {
              "lat": 11.02013835263835,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.019954679168963,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.019954679168963,
              "lon": -74.8466065453208
            }
          ],
          "probability": 0.5
        }
      ]
    },
    {
      "species": "Ardea alba",
      "max_probability": 0.245,
      "areas": [
        {
          "polygon": [
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            }
          ],
          "probability": 0.1
        }
      ]
    },
    {
      "species": "Melanerpes rubricapillus",
      "max_probability": 0.2678404259771073,
      "areas": [
        {
          "polygon": [
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            }
          ],
          "probability": 0.1
        }
      ]
    },
    {
      "species": "Quiscalus lugubris",
      "max_probability": 0.29285650465072643,
      "areas": [
        {
          "polygon": [
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.8545045045045
            },
            {
              "lat": 11.023995495495491,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.84550450450446
            },
            {
              "lat": 11.014995495495496,
              "lon": -74.8545045045045
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