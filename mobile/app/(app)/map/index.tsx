import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Alert, Platform } from 'react-native';
import MapView, { Marker } from 'react-native-maps';
import * as Location from 'expo-location';
import { router } from 'expo-router';

const BARRANQUILLA_REGION = {
  latitude: 10.9685,
  longitude: -74.7813,
  latitudeDelta: 0.0922,
  longitudeDelta: 0.0421,
};

export default function MapScreen() {
  const [location, setLocation] = useState<Location.LocationObject | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

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

  const handleOptionPress = (option: 'nearby' | 'zones' | 'routes') => {
    switch (option) {
      case 'nearby':
        router.push('/map/nearby');
        break;
      case 'zones':
        router.push('/map/zones');
        break;
      case 'routes':
        router.push('/map/routes');
        break;
    }
  };

  if (errorMsg) {
    Alert.alert('Error', errorMsg);
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Mapa de Aves</Text>
      
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
        </MapView>
      </View>

      <View style={styles.optionsContainer}>
        <TouchableOpacity
          style={styles.optionButton}
          onPress={() => handleOptionPress('nearby')}
        >
          <Text style={styles.optionText}>Aves Cerca de ti</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.optionButton}
          onPress={() => handleOptionPress('zones')}
        >
          <Text style={styles.optionText}>Aves por Zona</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.optionButton}
          onPress={() => handleOptionPress('routes')}
        >
          <Text style={styles.optionText}>Rutas de Aves</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.constructionContainer}>
        <Text style={styles.constructionText}>🚧 Módulo en construcción — nuevas funciones pronto disponibles.</Text>
      </View>
      
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fffaf0',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#d2691e',
    textAlign: 'center',
    padding: 16,
    marginTop: 60,
  },
  mapContainer: {
    flex: 1,
    overflow: 'hidden',
    borderRadius: 20,
    margin: 16,
  },
  map: {
    flex: 1,
  },
  optionsContainer: {
    padding: 16,
    gap: 12,
  },
  optionButton: {
    backgroundColor: '#d2691e',
    padding: 16,
    borderRadius: 10,
    alignItems: 'center',
  },
  optionText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  constructionContainer: {
    alignItems: 'center',
    paddingVertical: 12,
    paddingHorizontal: 16,
    marginHorizontal: 16,
    marginBottom: 24,
    borderRadius: 10,
    backgroundColor: '#fff4e6',
    borderWidth: 1,
    borderColor: '#f0c7a3',
  },
  constructionText: {
    color: '#8a4b00',
    fontSize: 14,
    textAlign: 'center',
  },
});
