import React, { useEffect, useState } from "react";
import { View, Text, Button, FlatList, StyleSheet } from "react-native";
import MapView, { Marker, Polygon } from "react-native-maps";
import * as Location from "expo-location";
import axios from "axios";

type SpeciesProb = {
  species: string;
  probability: number;
};

type PolygonArea = {
  polygon: { lat: number; lon: number }[];
  probability: number;
};

type SpeciesDistribution = {
  species: string;
  max_probability: number;
  areas: PolygonArea[];
};

export default function BirdMapScreen() {
  const [location, setLocation] = useState<{ latitude: number; longitude: number } | null>(null);
  const [speciesList, setSpeciesList] = useState<SpeciesProb[]>([]);
  const [distributions, setDistributions] = useState<SpeciesDistribution[]>([]);
  const [zone, setZone] = useState<string>("");

  // 1️⃣ obtener ubicación usuario
  useEffect(() => {
    (async () => {
      let { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== "granted") {
        console.log("Permiso ubicación denegado");
        return;
      }
      let loc = await Location.getCurrentPositionAsync({});
      setLocation({ latitude: loc.coords.latitude, longitude: loc.coords.longitude });
    })();
  }, []);

  const datetimeNow = new Date().toISOString();
  const API_BASE = " http://127.0.0.1:8000"; 

  // 2️⃣ consumir endpoint `/predict`
  const fetchPredict = async () => {
    if (!location) return;
    const res = await axios.post(`${API_BASE}/predict`, {
      lat: location.latitude,
      lon: location.longitude,
      datetime: datetimeNow,
    });
    setZone(res.data.zone);
    setSpeciesList(res.data.species_probabilities);
    setDistributions([]); // limpiar distribuciones
  };

  // 3️⃣ consumir endpoint `/distribution`
  const fetchDistribution = async () => {
    if (!location) return;
    const res = await axios.post(`${API_BASE}/distribution`, {
      lat: location.latitude,
      lon: location.longitude,
      datetime: datetimeNow,
      radius: 1000,
      grid_size: 0.001,
    });
    setZone(res.data.zone);
    setDistributions(res.data.species_distributions);
    setSpeciesList([]);
  };

  // 4️⃣ consumir endpoint `/distribution-zone`
  const fetchDistributionZone = async () => {
    if (!location) return;
    const res = await axios.post(`${API_BASE}/distribution-zone`, {
      lat: location.latitude,
      lon: location.longitude,
      datetime: datetimeNow,
      grid_size: 0.001,
    });
    setZone(res.data.zone);
    setDistributions(res.data.species_distributions);
    setSpeciesList([]);
  };

  return (
    <View style={{ flex: 1 }}>
      {/* 🗺️ MAPA */}
      <MapView
        style={{ flex: 1 }}
        initialRegion={{
          latitude: location ? location.latitude : 11.0196,
          longitude: location ? location.longitude : -74.85,
          latitudeDelta: 0.05,
          longitudeDelta: 0.05,
        }}
      >
        {/* 🧍 ubicacion */}
        {location && (
          <Marker
            coordinate={location}
            title="Tu ubicación"
            pinColor="blue"
          />
        )}

        {/* 🎨 Polígonos especie */}
        {distributions.map((dist) =>
          dist.areas.map((a, idx) => (
            <Polygon
              key={`${dist.species}-${idx}`}
              coordinates={a.polygon.map(pt => ({
                latitude: pt.lat,
                longitude: pt.lon,
              }))}
              strokeColor="rgba(0,0,255,0.3)"
              fillColor={`rgba(0,0,255,${a.probability})`}
            />
          ))
        )}
      </MapView>

      {/* 🔘 BOTONES */}
      <View style={{ flexDirection: "row", justifyContent: "space-around", padding: 6 }}>
        <Button title="Predict" onPress={fetchPredict} />
        <Button title="Distribution" onPress={fetchDistribution} />
        <Button title="Distribution Zone" onPress={fetchDistributionZone} />
      </View>

      {/* 🐦 LISTA especies */}
      {speciesList.length > 0 && (
        <FlatList
          data={speciesList}
          keyExtractor={(item) => item.species}
          renderItem={({ item }) => (
            <View style={styles.card}>
              <Text style={{ fontWeight: "bold" }}>{item.species}</Text>
              <Text>Prob: {(item.probability * 100).toFixed(1)}%</Text>
            </View>
          )}
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    flexDirection: "row",
    justifyContent: "space-between",
    padding: 10,
    borderBottomWidth: 1,
    borderBottomColor: "#ddd"
  }
});

