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
import AudioRecorder from "../../../components/ui/AudioRecorder";
import { router } from "expo-router";
import BirdRegistry from "../../../components/ui/BirdRegistry";
import { SafeAreaView } from 'react-native-safe-area-context';
import { useBirdDetections } from "../../../context/bird-detection-context";


export default function IdentifyScreen() {
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
            <Text style={styles.subtitle}>🎤 Graba el canto en vivo</Text>
          </View>
          
          <View style={styles.recorderWrapper}>
            <AudioRecorder />
          </View>
          
          <TouchableOpacity 
            style={styles.switchButton}
            onPress={() => router.push("/identify/audioupload")}
          >
            <Ionicons name="cloud-upload-outline" size={16} color="#999" />
            <Text style={styles.switchText}>¿Tienes un audio guardado? Súbelo aquí</Text>
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
  recorderWrapper: {
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

