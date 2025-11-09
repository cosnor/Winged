import React, { useState } from 'react';
import { StyleSheet, View, Text, TouchableOpacity } from 'react-native';
import * as DocumentPicker from 'expo-document-picker';
import { Audio } from 'expo-av';
import { Ionicons } from '@expo/vector-icons';

interface AudioFile {
  uri: string;
  name: string;
  size: number;
  mimeType: string;
}

export default function AudioSelector() {
  const [selectedFile, setSelectedFile] = useState<AudioFile | null>(null);
  const [sound, setSound] = useState<Audio.Sound | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);

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

  return (
    <View style={styles.container}>
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
});