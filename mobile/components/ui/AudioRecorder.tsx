import React, { useState, useEffect } from "react";
import { View, TouchableOpacity, Text, StyleSheet, ActivityIndicator } from "react-native";
import { Audio } from "expo-av";
import * as FileSystem from "expo-file-system";
import { Ionicons } from "@expo/vector-icons";
import { MotiView } from "moti";
import { theme } from "../../styles/theme";

export default function AudioRecorder() {
  const [recording, setRecording] = useState<Audio.Recording | null>(null);
  const [isRecording, setIsRecording] = useState(false);
  const [uri, setUri] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    (async () => {
      const { status } = await Audio.requestPermissionsAsync();
      if (status !== "granted") {
        alert("Se necesita permiso para usar el micrófono 🎤");
      }
    })();
  }, []);

  // 🧹 Limpiar el caché de grabaciones anteriores

const clearOldRecordings = async () => {
  try {
    const cacheDir = (FileSystem as any).cacheDirectory;

    if (!cacheDir) {
      console.warn("⚠️ No se pudo acceder al directorio de caché.");
      return;
    }

    const files = await FileSystem.readDirectoryAsync(cacheDir);

    if (files.includes("Audio")) {
      const audioDir = cacheDir + "Audio/";
      const audioFiles = await FileSystem.readDirectoryAsync(audioDir);

      for (const file of audioFiles) {
        await FileSystem.deleteAsync(audioDir + file, { idempotent: true });
      }

      console.log("🧹 Caché de audio limpiado correctamente.");
    } else {
      console.log("No hay carpeta de audio en caché.");
    }
  } catch (error) {
    console.error("Error limpiando caché de audio:", error);
  }
};



  const startRecording = async () => {
    try {
      setLoading(true);

      // 🧹 Limpia grabaciones anteriores antes de empezar una nueva
      await clearOldRecordings();

      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
      });

      const { recording } = await Audio.Recording.createAsync(
        Audio.RecordingOptionsPresets.HIGH_QUALITY
      );

      setRecording(recording);
      setIsRecording(true);
    } catch (err) {
      console.error("Error al grabar:", err);
    } finally {
      setLoading(false);
    }
  };

  const stopRecording = async () => {
    setLoading(true);
    if (!recording) return;

    await recording.stopAndUnloadAsync();
    const uri = recording.getURI();
    setUri(uri);
    setRecording(null);
    setIsRecording(false);
    setLoading(false);
  };

  const playRecording = async () => {
    if (!uri) return;
    const { sound } = await Audio.Sound.createAsync({ uri });
    await sound.playAsync();
  };

  return (
    <View style={styles.container}>
      <View style={styles.micContainer}>
        {isRecording && (
          <MotiView
            from={{ scale: 1, opacity: 0.8 }}
            animate={{ scale: 1.8, opacity: 0 }}
            transition={{
              type: "timing",
              duration: 1200,
              loop: true,
            }}
            style={styles.pulse}
          />
        )}

        <TouchableOpacity
          style={[styles.micButton, isRecording && styles.recording]}
          onPress={isRecording ? stopRecording : startRecording}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Ionicons name="mic" size={40} color="#fff" />
          )}
        </TouchableOpacity>
      </View>

      <Text style={styles.statusText}>
        {isRecording ? "Grabando..." : "Presiona para grabar"}
      </Text>

      {/* <TouchableOpacity
        style={[styles.playButton, !uri && styles.playDisabled]}
        onPress={playRecording}
        disabled={!uri}
      >
        <Ionicons
          name="play-circle"
          size={36}
          color={uri ? "#4CAF50" : "rgba(76,175,80,0.4)"}
        />
        <Text
          style={[styles.playText, !uri && { color: "rgba(76,175,80,0.4)" }]}
        >
          Reproducir
        </Text>
      </TouchableOpacity> */}
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
    width: 120,
    height: 120,
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
