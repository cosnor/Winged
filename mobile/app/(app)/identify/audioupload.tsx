import React, { useState } from "react";
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
} from "react-native";
import AudioSelector from "../../../components/ui/AudioSelector";
import BirdRegistry from "../../../components/ui/BirdRegistry";
import { router } from "expo-router";

export default function AudioUploadScreen() {
  // Datos de ejemplo - En una implementación real, esto vendría de una API o estado global
  const identifiedBirds = [
    {
      id: '3',
      commonName: 'Tucán Pico Iris',
      scientificName: 'Ramphastos sulfuratus',
      imageUrl: 'https://static.inaturalist.org/photos/75880847/large.jpg',
    },
    {
      id: '4',
      commonName: 'Guacamaya Roja',
      scientificName: 'Ara macao',
      imageUrl: 'https://static.inaturalist.org/photos/75880846/large.jpg',
    },
    {
      id: '5',
      commonName: 'Guacamaya Verde',
      scientificName: 'Ara militaris',
      imageUrl: 'https://static.inaturalist.org/photos/75880845/large.jpg',
    },
    {
      id: '6',
      commonName: 'Colibrí Ruby',
      scientificName: 'Chrysolampis mosquitus',
      imageUrl: 'https://static.inaturalist.org/photos/75880844/large.jpg',
    },
    {
      id: '7',
      commonName: 'Colibrí Ruby',
      scientificName: 'Chrysolampis mosquitus',
      imageUrl: 'https://static.inaturalist.org/photos/75880844/large.jpg',
    }
  ];

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Identifica tu Ave</Text>
        <Text style={styles.subtitle}>Sube un audio</Text>
        <AudioSelector />
        <TouchableOpacity onPress={() => router.push("/identify")}>
            <Text style={styles.registerText}>
              ¿Prefieres grabar?{" "}
              <Text style={{ color: "#d2691e", fontWeight: "bold" }}>
                Hazlo aquí
              </Text>
            </Text>
        </TouchableOpacity>
      </View>
      <View style={styles.registryContainer}>
        <BirdRegistry birds={identifiedBirds} />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fffaf0",
  },
  header: {
    alignItems: "center",
    justifyContent: "center",
    padding: 20,
    paddingTop: 80
  },
  title: {
    fontSize: 26,
    fontWeight: "bold",
    marginBottom: 5,
    color: "#d2691e",
  },
  subtitle: {
    fontSize: 14,
    color: "#555",
    marginBottom: 30,
  },
  registryContainer: {
    flex: 1,
    width: '100%',
  },
  label: {
    alignSelf: "flex-start",
    marginBottom: 5,
    fontSize: 14,
    color: "#333",
  },
  input: {
    width: "100%",
    padding: 12,
    borderWidth: 1,
    borderColor: "#ddd",
    borderRadius: 8,
    marginBottom: 15,
    backgroundColor: "#fff",
  },
  button: {
    width: "100%",
    backgroundColor: "#d2691e",
    padding: 15,
    borderRadius: 8,
    alignItems: "center",
    marginTop: 10,
  },
  buttonText: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "bold",
  },
  registerText: {
    marginTop: 20,
    color: "#333",
  },
});

