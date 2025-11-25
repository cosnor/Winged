import React, { useState } from 'react';
import { StyleSheet, View, Text, TouchableOpacity, Alert } from 'react-native';
import * as DocumentPicker from 'expo-document-picker';
import * as FileSystem from 'expo-file-system/legacy';
import { Audio } from 'expo-av';
import { Ionicons } from '@expo/vector-icons';
import { useBirdAnalysis } from '../../hooks/useBirdAnalysis';

interface AudioFile {
  uri: string;
  name: string;
  size: number;
  mimeType: string;
}

interface AudioSelectorProps {
  onDetectionsComplete?: (detections: any[]) => void;
}

export default function AudioSelector({ onDetectionsComplete }: AudioSelectorProps) {
  const [selectedFile, setSelectedFile] = useState<AudioFile | null>(null);
  const [sound, setSound] = useState<Audio.Sound | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const { connected, analyzing, analyzeAudio, error } = useBirdAnalysis();

  const selectFile = async () => {
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: 'audio/*',
        copyToCacheDirectory: true
      });

      if (result.assets && result.assets.length > 0) {
        const asset = result.assets[0];
        setSelectedFile({
          uri: asset.uri,
          name: asset.name ?? 'unknown',
          size: asset.size ?? 0,
          mimeType: asset.mimeType || 'audio/*'
        });
        // Detener la reproducción actual si existe
        if (sound) {
          await sound.unloadAsync();
          setSound(null);
        }
      }
    } catch (error) {
      console.error('Error al seleccionar el archivo:', error);
    }
  };

  const playSound = async () => {
    if (!selectedFile) return;

    try {
      if (sound) {
        if (isPlaying) {
          await sound.pauseAsync();
          setIsPlaying(false);
        } else {
          await sound.playAsync();
          setIsPlaying(true);
        }
      } else {
        const { sound: newSound } = await Audio.Sound.createAsync(
          { uri: selectedFile.uri },
          { shouldPlay: true }
        );
        setSound(newSound);
        setIsPlaying(true);

        // Cuando termine de reproducirse
        newSound.setOnPlaybackStatusUpdate(status => {
          if (status && 'didJustFinish' in status && status.didJustFinish) {
            setIsPlaying(false);
          }
        });
      }
    } catch (error) {
      console.error('Error al reproducir el audio:', error);
    }
  };

  const stopSound = async () => {
    if (sound) {
      await sound.stopAsync();
      await sound.unloadAsync();
      setSound(null);
      setIsPlaying(false);
    }
  };

  const analyzeSelectedFile = async () => {
    if (!selectedFile) {
      Alert.alert('Error', 'Primero selecciona un archivo de audio');
      return;
    }

    if (!connected) {
      Alert.alert(
        'Sin conexión',
        'No hay conexión con el servidor. Verifica que los servicios estén corriendo.'
      );
      return;
    }

    try {
      console.log('📁 Leyendo archivo:', selectedFile.name);
      
      // Convertir el archivo a base64
      const base64Audio = await FileSystem.readAsStringAsync(selectedFile.uri, {
        encoding: 'base64'
      });

      console.log('📤 Enviando archivo para análisis...');
      await analyzeAudio(base64Audio, selectedFile.name);
    } catch (err) {
      console.error('❌ Error al analizar archivo:', err);
      Alert.alert('Error', 'No se pudo procesar el archivo de audio');
    }
  };

  return (
    <View style={styles.container}>
      {!connected && (
        <Text style={styles.connectionStatus}>⚠️ Sin conexión al servidor</Text>
      )}

      <TouchableOpacity style={styles.fileButton} onPress={selectFile}>
        <Ionicons name="document-attach" size={24} color="#d2691e" />
        <Text style={styles.fileButtonText}>
          {selectedFile ? selectedFile.name : "Seleccionar archivo"}
        </Text>
      </TouchableOpacity>

      {selectedFile && (
        <View style={styles.controls}>
          <TouchableOpacity style={styles.controlButton} onPress={playSound}>
            <Ionicons 
              name={isPlaying ? "pause" : "play"} 
              size={24} 
              color="#d2691e" 
            />
          </TouchableOpacity>
          {isPlaying && (
            <TouchableOpacity style={styles.controlButton} onPress={stopSound}>
              <Ionicons name="stop" size={24} color="#d2691e" />
            </TouchableOpacity>
          )}
        </View>
      )}

      {selectedFile && (
        <TouchableOpacity 
          style={[styles.analyzeButton, analyzing && styles.analyzeButtonDisabled]} 
          onPress={analyzeSelectedFile}
          disabled={analyzing || !connected}
        >
          <Ionicons 
            name={analyzing ? "hourglass" : "search"} 
            size={20} 
            color="#fff" 
          />
          <Text style={styles.analyzeButtonText}>
            {analyzing ? 'Analizando...' : 'Analizar Audio'}
          </Text>
        </TouchableOpacity>
      )}

      {error && <Text style={styles.errorText}>❌ {error}</Text>}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    width: '80%',
    alignItems: 'center',
    marginVertical: 5,
  },
  fileButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#d2691e',
    width: '100%',
  },
  fileButtonText: {
    marginLeft: 10,
    color: '#d2691e',
    fontSize: 16,
  },
  controls: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginTop: 10,
    gap: 20,
  },
  controlButton: {
    padding: 10,
    borderRadius: 25,
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#d2691e',
  },
  analyzeButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#d2691e',
    padding: 15,
    borderRadius: 8,
    marginTop: 15,
    width: '100%',
    gap: 8,
  },
  analyzeButtonDisabled: {
    opacity: 0.6,
  },
  analyzeButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  connectionStatus: {
    fontSize: 12,
    color: '#ff6b6b',
    marginBottom: 10,
    textAlign: 'center',
  },
  errorText: {
    fontSize: 12,
    color: '#ff6b6b',
    marginTop: 10,
    textAlign: 'center',
  },
});