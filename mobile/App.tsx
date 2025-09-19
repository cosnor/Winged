import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Alert,
  ScrollView,
  ActivityIndicator,
  SafeAreaView
} from 'react-native';
import { Audio } from 'expo-av';
import * as DocumentPicker from 'expo-document-picker';
import * as FileSystem from 'expo-file-system';

const BirdNetAnalyzer = () => {
  const [ws, setWs] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [recording, setRecording] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [results, setResults] = useState([]);
  const [statusMessage, setStatusMessage] = useState('');

  // Conectar WebSocket
  const connectWebSocket = () => {
    try {
      // Cambia esta IP por tu IP real (no localhost desde móvil)
      const websocket = new WebSocket('ws://127.0.0.1:8000/ws');
      
      websocket.onopen = () => {
        setIsConnected(true);
        setStatusMessage('✅ Conectado al servidor');
      };

      websocket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        if (data.type === 'status') {
          setStatusMessage(`📊 ${data.message}`);
        } else if (data.type === 'results') {
          setResults(data.detections);
          setIsAnalyzing(false);
          setStatusMessage(`🎯 ${data.total_detections} aves detectadas`);
        }
      };

      websocket.onclose = () => {
        setIsConnected(false);
        setStatusMessage('❌ Desconectado');
      };

      websocket.onerror = () => {
        Alert.alert('Error', 'No se pudo conectar al servidor');
      };

      setWs(websocket);
    } catch (error) {
      Alert.alert('Error', 'Error al conectar');
    }
  };

  // Grabar audio
  const startRecording = async () => {
    try {
      const permission = await Audio.requestPermissionsAsync();
      if (permission.status !== 'granted') {
        Alert.alert('Error', 'Se necesitan permisos de micrófono');
        return;
      }

      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
      });

      const { recording } = await Audio.Recording.createAsync(
        Audio.RecordingOptionsPresets.HIGH_QUALITY
      );
      
      setRecording(recording);
      setIsRecording(true);
      setStatusMessage('🎤 Grabando...');
    } catch (err) {
      Alert.alert('Error', 'No se pudo grabar');
    }
  };

  const stopRecording = async () => {
    if (!recording) return;

    try {
      setIsRecording(false);
      await recording.stopAndUnloadAsync();
      const uri = recording.getURI();
      
      if (uri) {
        await sendAudioFile(uri, 'grabacion.m4a');
      }
      
      setRecording(null);
    } catch (error) {
      Alert.alert('Error', 'Error al parar grabación');
    }
  };

  // Seleccionar archivo
  const pickAudioFile = async () => {
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: 'audio/*',
        copyToCacheDirectory: true,
      });

      if (result.type === 'success') {
        await sendAudioFile(result.uri, result.name);
      }
    } catch (error) {
      Alert.alert('Error', 'Error al seleccionar archivo');
    }
  };

  // Enviar audio
  const sendAudioFile = async (uri, filename) => {
    if (!isConnected || !ws) {
      Alert.alert('Error', 'No hay conexión');
      return;
    }

    try {
      setIsAnalyzing(true);
      setResults([]);
      setStatusMessage('📤 Enviando audio...');

      const base64 = await FileSystem.readAsStringAsync(uri, {
        encoding: FileSystem.EncodingType.Base64,
      });

      const message = {
        type: 'audio',
        audio: base64,
        filename: filename
      };

      ws.send(JSON.stringify(message));
    } catch (error) {
      setIsAnalyzing(false);
      Alert.alert('Error', 'Error al enviar audio');
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.content}>
        
        <Text style={styles.title}>🐦 BirdNet Analyzer</Text>
        
        {/* Estado de conexión */}
        <View style={styles.section}>
          <View style={[styles.statusBadge, { 
            backgroundColor: isConnected ? '#28a745' : '#dc3545' 
          }]}>
            <Text style={styles.statusText}>
              {isConnected ? 'Conectado' : 'Desconectado'}
            </Text>
          </View>
          
          <TouchableOpacity 
            style={[styles.button, styles.connectBtn]}
            onPress={connectWebSocket}
            disabled={isConnected}
          >
            <Text style={styles.buttonText}>
              {isConnected ? 'Conectado' : 'Conectar'}
            </Text>
          </TouchableOpacity>
        </View>

        {/* Controles de audio */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>🎤 Audio</Text>
          
          <View style={styles.buttonRow}>
            <TouchableOpacity 
              style={[styles.button, styles.recordBtn]}
              onPress={isRecording ? stopRecording : startRecording}
              disabled={!isConnected || isAnalyzing}
            >
              <Text style={styles.buttonText}>
                {isRecording ? '⏹️ Parar' : '🎤 Grabar'}
              </Text>
            </TouchableOpacity>
            
            <TouchableOpacity 
              style={[styles.button, styles.fileBtn]}
              onPress={pickAudioFile}
              disabled={!isConnected || isAnalyzing}
            >
              <Text style={styles.buttonText}>📁 Archivo</Text>
            </TouchableOpacity>
          </View>
        </View>

        {/* Estado */}
        {statusMessage && (
          <View style={styles.section}>
            <View style={styles.statusRow}>
              {isAnalyzing && <ActivityIndicator color="#007bff" />}
              <Text style={styles.statusMessage}>{statusMessage}</Text>
            </View>
          </View>
        )}

        {/* Resultados */}
        {results.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>
              🎯 Resultados ({results.length})
            </Text>
            
            {results.map((bird, index) => (
              <View key={index} style={styles.birdCard}>
                <Text style={styles.birdName}>{bird.common_name}</Text>
                <Text style={styles.birdDetails}>
                  Código: {bird.species_code}
                </Text>
                <Text style={styles.birdDetails}>
                  Tiempo: {bird.begin_time.toFixed(1)}s - {bird.end_time.toFixed(1)}s
                </Text>
                <Text style={styles.confidence}>
                  Confianza: {(bird.confidence * 100).toFixed(1)}%
                </Text>
              </View>
            ))}
          </View>
        )}

      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  content: {
    flex: 1,
    padding: 20,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 30,
    color: '#333',
  },
  section: {
    backgroundColor: 'white',
    borderRadius: 10,
    padding: 15,
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 15,
    color: '#333',
  },
  statusBadge: {
    alignSelf: 'center',
    paddingHorizontal: 15,
    paddingVertical: 8,
    borderRadius: 20,
    marginBottom: 15,
  },
  statusText: {
    color: 'white',
    fontWeight: 'bold',
  },
  buttonRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  button: {
    paddingVertical: 12,
    paddingHorizontal: 25,
    borderRadius: 8,
    alignItems: 'center',
    minWidth: 120,
  },
  connectBtn: {
    backgroundColor: '#007bff',
    alignSelf: 'center',
  },
  recordBtn: {
    backgroundColor: '#fd7e14',
  },
  fileBtn: {
    backgroundColor: '#6f42c1',
  },
  buttonText: {
    color: 'white',
    fontWeight: 'bold',
    fontSize: 16,
  },
  statusRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 10,
  },
  statusMessage: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
  },
  birdCard: {
    backgroundColor: '#f8f9fa',
    padding: 15,
    borderRadius: 8,
    marginBottom: 10,
    borderLeftWidth: 4,
    borderLeftColor: '#28a745',
  },
  birdName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 5,
  },
  birdDetails: {
    fontSize: 14,
    color: '#666',
    marginBottom: 3,
  },
  confidence: {
    fontSize: 14,
    color: '#28a745',
    fontWeight: 'bold',
  },
});

export default BirdNetAnalyzer;
