import React from "react";
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
} from "react-native";
import AudioSelector from "../../../components/ui/AudioSelector";
import BirdRegistry from "../../../components/ui/BirdRegistry";
import { router } from "expo-router";
import { SafeAreaView } from 'react-native-safe-area-context';
import { useBirdDetections } from "../../../context/bird-detection-context";

export default function AudioUploadScreen() {
  const { identifiedBirds } = useBirdDetections();

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Identifica tu Ave</Text>
        <Text style={styles.subtitle}>Sube un audio</Text>
        <AudioSelector />
        <TouchableOpacity onPress={() => router.push("/identify/record")}>
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
    </SafeAreaView>
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
    paddingTop: 20
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

