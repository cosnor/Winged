import React, { useState, useEffect, useRef } from "react";
import { View, TouchableOpacity, Text, StyleSheet, ActivityIndicator, Animated, Easing, Alert } from "react-native";
import {
  useAudioRecorder,
  AudioModule,
  RecordingPresets,
  setAudioModeAsync,
  useAudioRecorderState,
} from "expo-audio";
import * as FileSystem from "expo-file-system/legacy";
import { Ionicons } from "@expo/vector-icons";
import { theme } from "../../styles/theme";
import { useBirdAnalysis } from "../../hooks/useBirdAnalysis";

interface AudioRecorderProps {
  onDetectionsComplete?: (detections: any[]) => void;
}

export default function AudioRecorder({ onDetectionsComplete }: AudioRecorderProps) {
  const [loading, setLoading] = useState(false);

  const audioRecorder = useAudioRecorder(RecordingPresets.HIGH_QUALITY);
  const recorderState = useAudioRecorderState(audioRecorder);
  const { connected, analyzing, analyzeAudio, error } = useBirdAnalysis();
  
  // 🔹 animación del pulso con Animated API
  const scaleAnim = useRef(new Animated.Value(1)).current;


  // 🔊 Pedir permisos y configurar modo de audio
  useEffect(() => {
  (async () => {
    const { granted } = await AudioModule.requestRecordingPermissionsAsync();
    if (!granted) {
      Alert.alert("Permiso requerido", "Se necesita acceso al micrófono 🎤");
      return;
    }

    await setAudioModeAsync({
      allowsRecording: true,
      playsInSilentMode: true,
    });
  })();
}, []);


  // 🎞️ Animación de pulso mientras graba
  useEffect(() => {
    if (recorderState.isRecording) {
      Animated.loop(
        Animated.sequence([
          Animated.timing(scaleAnim, { toValue: 1.1, duration: 1000, easing: Easing.ease, useNativeDriver: true }),
          Animated.timing(scaleAnim, { toValue: 1, duration: 1000, easing: Easing.ease, useNativeDriver: true }),
        ])
      ).start();
    } else {
      scaleAnim.stopAnimation();
      scaleAnim.setValue(1);
    }
  }, [recorderState.isRecording]);

  // 🧹 Limpiar grabaciones previas
  // const clearOldRecordings = async () => {
  //   try {
  //     const cacheDir = (FileSystem as any).cacheDirectory;
  //     if (!cacheDir) {
  //       console.warn("⚠️ No se pudo acceder al directorio de caché.");
  //       return;
  //     }

  //     const files = await FileSystem.readDirectoryAsync(cacheDir);
  //     if (files.includes("Audio")) {
  //       const audioDir = cacheDir + "Audio/";
  //       const audioFiles = await FileSystem.readDirectoryAsync(audioDir);

  //       for (const file of audioFiles) {
  //         await FileSystem.deleteAsync(audioDir + file, { idempotent: true });
  //       }

  //       console.log("🧹 Caché de audio limpiado correctamente.");
  //     }
  //   } catch (error) {
  //     console.error("Error limpiando caché de audio:", error);
  //   }
  // };

 // 🎙️ Iniciar grabación
  const startRecording = async () => {
    try {
      setLoading(true);
      // await clearOldRecordings();

      const status = await AudioModule.requestRecordingPermissionsAsync();
      if (!status.granted) {
        Alert.alert("Permiso denegado", "Se necesita acceso al micrófono 🎤");
        return;
      }

      await setAudioModeAsync({
        playsInSilentMode: true,
        allowsRecording: true,
      });

      await audioRecorder.prepareToRecordAsync();
      audioRecorder.record();
    } catch (error) {
      console.error("Error al grabar:", error);
    } finally {
      setLoading(false);
    }
  };


  // ⏹️ Detener grabación y analizar
  const stopRecording = async () => {
    setLoading(true);
    try {
      await audioRecorder.stop();
      const audioUrl = recorderState.url;
      console.log("Grabación guardada en:", audioUrl);

      if (audioUrl && connected) {
        // Convertir el audio a base64 para enviarlo
        const base64Audio = await FileSystem.readAsStringAsync(audioUrl, {
          encoding: 'base64'
        });

        const filename = `recording_${Date.now()}.wav`;
        console.log("📤 Enviando audio para análisis:", filename);

        await analyzeAudio(base64Audio, filename);
      } else if (!connected) {
        Alert.alert(
          "Sin conexión",
          "No hay conexión con el servidor. Verifica que los servicios estén corriendo."
        );
      }
    } catch (error) {
      console.error("Error al detener la grabación:", error);
      Alert.alert("Error", "No se pudo procesar el audio");
    } finally {
      setLoading(false);
    }
  };


  return (
    <View style={styles.container}>
      {/* Estado de conexión */}
      {!connected && (
        <Text style={styles.connectionStatus}>⚠️ Sin conexión al servidor</Text>
      )}

      <View style={styles.micContainer}>
        {recorderState.isRecording && (
          <Animated.View
            style={[styles.pulse, { transform: [{ scale: scaleAnim }] }]}
          />
        )}

        <TouchableOpacity
          style={[
            styles.micButton,
            recorderState.isRecording && styles.recording,
          ]}
          onPress={recorderState.isRecording ? stopRecording : startRecording}
          disabled={loading || analyzing}
        >
          {loading || analyzing ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Ionicons name="mic" size={40} color="#fff" />
          )}
        </TouchableOpacity>
      </View>

      <Text style={styles.statusText}>
        {analyzing
          ? "🔍 Analizando..."
          : recorderState.isRecording
          ? "🎙️ Grabando..."
          : "Presiona para grabar"}
      </Text>

      {error && <Text style={styles.errorText}>❌ {error}</Text>}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: "center",
    justifyContent: "center",
  },

  // 🔹 El contenedor que agrupa la animación y el botón
  micContainer: {
    alignItems: "center",
    justifyContent: "center",
    width: 140,
    height: 100,
  },

  pulse: {
    position: "absolute",
    width: 100,
    height: 100,
    borderRadius: 60,
    backgroundColor: theme.colors.accent,
    zIndex: 1,
  },

  micButton: {
    backgroundColor: theme.colors.primary,
    borderRadius: 100,
    padding: 25,
    elevation: 6,
    zIndex: 2,
  },
  recording: {
    backgroundColor: theme.colors.secondary,
  },
  statusText: {
    marginTop: 5,
    fontSize: 16,
    color: "#333",
  },
  connectionStatus: {
    fontSize: 12,
    color: "#ff6b6b",
    marginBottom: 10,
  },
  errorText: {
    fontSize: 12,
    color: "#ff6b6b",
    marginTop: 10,
    textAlign: "center",
  },
  playButton: {
    marginTop: 30,
    alignItems: "center",
  },
  playDisabled: {
    opacity: 0.5,
  },
  playText: {
    marginTop: 5,
    color: theme.colors.mutedForeground,
    fontSize: 14,
  },
});
