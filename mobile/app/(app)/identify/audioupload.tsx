import React from "react";
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  ScrollView,
} from "react-native";
import { LinearGradient } from 'expo-linear-gradient';
import Ionicons from '@expo/vector-icons/Ionicons';
import AudioSelector from "../../../components/ui/AudioSelector";
import BirdRegistry from "../../../components/ui/BirdRegistry";
import { router } from "expo-router";
import { SafeAreaView } from 'react-native-safe-area-context';
import { useBirdDetections } from "../../../context/bird-detection-context";

export default function AudioUploadScreen() {
  const { identifiedBirds } = useBirdDetections();

  return (
    <LinearGradient
      colors={['#fffaf0', '#ffe4d6', '#ffd4ba']}
      style={styles.gradient}
    >
      <SafeAreaView style={styles.container} edges={['top']}>
        <ScrollView 
          contentContainerStyle={styles.scrollContent}
          showsVerticalScrollIndicator={false}
        >
          <View style={styles.header}>
            <Text style={styles.title}>Identifica tu Ave</Text>
            <Text style={styles.subtitle}>🎵 Sube un archivo de audio</Text>
          </View>
          
          <View style={styles.selectorWrapper}>
            <AudioSelector />
          </View>
          
          <TouchableOpacity 
            style={styles.switchButton}
            onPress={() => router.push("/identify/record")}
          >
            <Ionicons name="mic-outline" size={16} color="#999" />
            <Text style={styles.switchText}>¿Prefieres grabar? Hazlo aquí</Text>
          </TouchableOpacity>

          <View style={styles.registryContainer}>
            <BirdRegistry birds={identifiedBirds} />
          </View>
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
  scrollContent: {
    paddingBottom: 20,
    backgroundColor: "transparent"
  },
  header: {
    alignItems: "center",
    paddingHorizontal: 20,
    paddingTop: 20,
    paddingBottom: 16,
  },
  title: {
    fontSize: 28,
    fontWeight: "900",
    marginBottom: 8,
    color: "#d2691e",
  },
  subtitle: {
    fontSize: 16,
    color: "#666",
    fontWeight: '600',
  },
  selectorWrapper: {
    paddingHorizontal: 20,
    marginTop: 10,
  },
  switchButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    paddingVertical: 12,
    paddingHorizontal: 20,
    marginTop: 16,
    marginHorizontal: 20,
  },
  switchText: {
    fontSize: 13,
    color: '#999',
    fontWeight: '500',
  },
  registryContainer: {
    marginTop: 20,
    flex: 1,
  },
});

