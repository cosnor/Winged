import { useState, useEffect, useRef } from 'react';
import { API_BASE_URL, WS_BASE_URL } from '../config/environment';
import { useBirdDetections } from '../context/bird-detection-context';

export interface BirdDetection {
  species_name: string;
  confidence: number;
  start_time: number;
  end_time: number;
  scientific_name?: string;
  common_name?: string;
}

export interface BirdAnalysis {
  detections: BirdDetection[];
  analysis_id?: string;
  total_detections?: number;
}

interface UseBirdAnalysisReturn {
  connected: boolean;
  analyzing: boolean;
  detections: BirdDetection[];
  analysisId: string | null;
  error: string | null;
  analyzeAudio: (base64Audio: string, filename: string) => Promise<void>;
  reset: () => void;
}

export function useBirdAnalysis(): UseBirdAnalysisReturn {
  const [connected, setConnected] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [detections, setDetections] = useState<BirdDetection[]>([]);
  const [analysisId, setAnalysisId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const { addDetections } = useBirdDetections();

  // Obtener la URL del WebSocket desde la configuración
  const getWebSocketUrl = () => {
    // Usar la URL del WebSocket configurada (ya incluye wss://)
    return `${WS_BASE_URL}/ws`;
  };

  // Conectar WebSocket
  const connect = () => {
    try {
      const wsUrl = getWebSocketUrl();
      console.log('🔌 Conectando a WebSocket:', wsUrl);
      
      const ws = new WebSocket(wsUrl);
      
      ws.onopen = () => {
        console.log('✅ WebSocket conectado');
        setConnected(true);
        setError(null);
      };

      ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          console.log('📨 Mensaje completo recibido:', JSON.stringify(message, null, 2));

          switch (message.type) {
            case 'connected':
              console.log('📋 Comandos disponibles:', message.available_commands);
              break;

            case 'analysis_accepted':
              setAnalysisId(message.analysis_id);
              console.log('✅ Análisis aceptado:', message.analysis_id);
              break;

            case 'analysis_completed':
              setAnalyzing(false);
              // Las detecciones están en message.result.detections
              const newDetections = message.result?.detections || message.detections || message.analysis?.detections || [];
              setDetections(newDetections);
              // Agregar las detecciones al contexto global
              if (newDetections.length > 0) {
                addDetections(newDetections);
              }
              console.log('✅ Análisis completado:', newDetections.length, 'detecciones');
              console.log('🐦 Detecciones:', JSON.stringify(newDetections, null, 2));
              break;

            case 'analysis_progress':
              console.log('⏳', message.message);
              break;

            case 'error':
              console.error('❌ Error del servidor:', message.message);
              setError(message.message);
              setAnalyzing(false);
              break;

            default:
              console.log('📨 Mensaje desconocido:', message);
          }
        } catch (err) {
          console.error('❌ Error parseando mensaje:', err);
          console.error('📨 Mensaje raw:', event.data);
        }
      };

      ws.onerror = (error) => {
        console.error('❌ Error de WebSocket:', error);
        setError('Error de conexión con el servidor');
      };

      ws.onclose = () => {
        console.log('🔌 WebSocket desconectado');
        setConnected(false);
        
        // Reconectar después de 5 segundos
        reconnectTimeoutRef.current = setTimeout(() => {
          console.log('🔄 Intentando reconectar...');
          connect();
        }, 5000);
      };

      wsRef.current = ws;
    } catch (err) {
      console.error('❌ Error creando WebSocket:', err);
      setError('No se pudo conectar al servidor');
    }
  };

  // Conectar al montar el componente
  useEffect(() => {
    connect();

    // Cleanup al desmontar
    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  // Función para analizar audio
  const analyzeAudio = async (base64Audio: string, filename: string): Promise<void> => {
    if (!connected || !wsRef.current) {
      setError('No hay conexión con el servidor');
      throw new Error('No hay conexión con el servidor');
    }

    if (analyzing) {
      console.warn('⚠️ Ya hay un análisis en progreso');
      return;
    }

    try {
      setAnalyzing(true);
      setDetections([]);
      setError(null);
      setAnalysisId(null);

      const message = {
        type: 'analyze_audio',
        audio: base64Audio,
        filename: filename
      };

      console.log('📤 Enviando audio para análisis:', filename);
      wsRef.current.send(JSON.stringify(message));
    } catch (err) {
      console.error('❌ Error enviando audio:', err);
      setError('Error al enviar el audio');
      setAnalyzing(false);
      throw err;
    }
  };

  // Función para resetear el estado
  const reset = () => {
    setDetections([]);
    setAnalysisId(null);
    setError(null);
    setAnalyzing(false);
  };

  return {
    connected,
    analyzing,
    detections,
    analysisId,
    error,
    analyzeAudio,
    reset
  };
}
