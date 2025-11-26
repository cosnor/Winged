import React, { useState } from "react";
import {
  StyleSheet,
  Text,
  View,
  TextInput,
  TouchableOpacity,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
} from "react-native";
import Constants from "expo-constants";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { router } from "expo-router";
import { LinearGradient } from 'expo-linear-gradient';
import * as Animatable from 'react-native-animatable';
import { Ionicons } from '@expo/vector-icons';
import StatusMessage from "../../components/ui/StatusMessage";

export default function Login() {
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [status, setStatus] = useState<{
    type: 'success' | 'error';
    message: string;
    visible: boolean;
  }>({
    type: 'error',
    message: '',
    visible: false
  });

  const handleLogin = async () => {
    try {
      setStatus({ type: 'error', message: '', visible: false });

      if (!email || !password) {
        setStatus({
          type: 'error',
          message: 'Por favor ingresa tu correo y contraseña',
          visible: true,
        });
        return;
      }

      const API_BASE_URL =
        (Constants.expoConfig as any)?.extra?.API_BASE_URL;

      const resp = await fetch(`${API_BASE_URL}/users/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (!resp.ok) {
        // Prefer the 'detail' field from gateway JSON responses so the UI
        // shows a concise, user-friendly message (already localized).
        let message = `Error ${resp.status}`;
        try {
          const json = await resp.json();
          if (json && (json.detail || json.message || json.error)) {
            message = json.detail || json.message || json.error;
          } else if (json && Object.keys(json).length) {
            message = JSON.stringify(json);
          }
        } catch (e) {
          // fallback to plain text
          const text = await resp.text();
          if (text) message = text;
        }

        setStatus({ type: 'error', message, visible: true });
        return;
      }

      const body = await resp.json();
      // Try common shapes for token
      const token = body.access_token || body.token || (body.data && body.data.access_token);
      if (!token) {
        setStatus({ type: 'error', message: 'Respuesta inválida del servidor', visible: true });
        return;
      }

      // Persist token
      await AsyncStorage.setItem('ACCESS_TOKEN', token);
      
      console.log('✅ Login successful, token saved');
      console.log('📦 Full response body:', JSON.stringify(body, null, 2));
      
      // Fetch user info after successful login
      try {
        console.log('👤 Fetching user info...');
        const userResp = await fetch(`${API_BASE_URL}/users/me`, {
          headers: { 
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        
        console.log('📥 User info response status:', userResp.status);
        
        if (userResp.ok) {
          const userData = await userResp.json();
          console.log('👤 User data received:', JSON.stringify(userData, null, 2));
          
          // Save user info
          await AsyncStorage.setItem('USER_INFO', JSON.stringify(userData));
          console.log('💾 User info saved to AsyncStorage');
        } else {
          console.warn('⚠️ Failed to fetch user info, status:', userResp.status);
          const errorText = await userResp.text();
          console.warn('⚠️ Error response:', errorText);
        }
      } catch (userError) {
        console.error('❌ Error fetching user info:', userError);
        // Don't fail the login if user info fetch fails
      }

      setStatus({ type: 'success', message: '¡Bienvenido!', visible: true });
      setTimeout(() => router.push('/(app)'), 400);
    } catch (error) {
      console.error('Login error:', error);
      setStatus({ type: 'error', message: 'Error de red al iniciar sesión', visible: true });
    }
  };

  return (
    <LinearGradient colors={['#fffaf0', '#ffe4d6', '#ffd4ba']} style={styles.gradient}>
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.keyboardView}
      >
        <ScrollView
          contentContainerStyle={styles.scrollContent}
          showsVerticalScrollIndicator={false}
          keyboardShouldPersistTaps="handled"
        >
          <Animatable.View animation="fadeInDown" duration={800} style={styles.headerContainer}>
            <LinearGradient
              colors={['#ff9a41', '#ff6b35']}
              style={styles.logoCircle}
            >
              <Ionicons name="people" size={48} color="#fff" />
            </LinearGradient>
            <Text style={styles.title}>Iniciar Sesión</Text>
            <Text style={styles.subtitle}>Bienvenido de vuelta a Winged</Text>
          </Animatable.View>

          <Animatable.View animation="fadeInUp" delay={200} duration={800} style={styles.formContainer}>
            <View style={styles.inputContainer}>
              <View style={styles.inputIconWrapper}>
                <Ionicons name="mail" size={20} color="#ff9a41" />
              </View>
              <View style={styles.inputWrapper}>
                <Text style={styles.label}>Correo</Text>
                <TextInput
                  style={styles.input}
                  placeholder="tu@email.com"
                  placeholderTextColor="#aaa"
                  keyboardType="email-address"
                  autoCapitalize="none"
                  value={email}
                  onChangeText={(text: string) => setEmail(text)}
                />
              </View>
            </View>

            <View style={styles.inputContainer}>
              <View style={styles.inputIconWrapper}>
                <Ionicons name="lock-closed" size={20} color="#ff9a41" />
              </View>
              <View style={styles.inputWrapper}>
                <Text style={styles.label}>Contraseña</Text>
                <TextInput
                  style={styles.input}
                  placeholder="••••••"
                  placeholderTextColor="#aaa"
                  secureTextEntry
                  value={password}
                  onChangeText={(text: string) => setPassword(text)}
                />
              </View>
            </View>

            <TouchableOpacity onPress={handleLogin}>
              <LinearGradient
                colors={['#ff9a41', '#ff6b35']}
                style={styles.button}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 0 }}
              >
                <Text style={styles.buttonText}>Iniciar Sesión</Text>
                <Ionicons name="arrow-forward" size={20} color="#fff" />
              </LinearGradient>
            </TouchableOpacity>

            <TouchableOpacity onPress={() => router.push("/(auth)/register")} style={styles.registerButton}>
              <Text style={styles.registerText}>
                ¿No tienes cuenta?{" "}
                <Text style={styles.registerTextBold}>
                  Regístrate aquí
                </Text>
              </Text>
            </TouchableOpacity>
          </Animatable.View>
        </ScrollView>
      </KeyboardAvoidingView>

      <StatusMessage
        type={status.type}
        message={status.message}
        visible={status.visible}
      />
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  gradient: {
    flex: 1,
  },
  keyboardView: {
    flex: 1,
  },
  scrollContent: {
    flexGrow: 1,
    justifyContent: 'center',
    padding: 24,
  },
  headerContainer: {
    alignItems: 'center',
    marginBottom: 40,
  },
  logoCircle: {
    width: 100,
    height: 100,
    borderRadius: 50,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 24,
    shadowColor: '#ff6b35',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.4,
    shadowRadius: 16,
    elevation: 10,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#d2691e',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 15,
    color: '#8b4513',
    fontWeight: '500',
  },
  formContainer: {
    width: '100%',
  },
  inputContainer: {
    flexDirection: 'row',
    marginBottom: 20,
    backgroundColor: '#fff',
    borderRadius: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
    overflow: 'hidden',
  },
  inputIconWrapper: {
    width: 56,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#fff4e6',
  },
  inputWrapper: {
    flex: 1,
    padding: 16,
  },
  label: {
    fontSize: 12,
    color: '#666',
    marginBottom: 4,
    fontWeight: '600',
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  input: {
    fontSize: 16,
    color: '#333',
    paddingVertical: 0,
  },
  button: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 18,
    paddingHorizontal: 24,
    borderRadius: 16,
    marginTop: 8,
    shadowColor: '#ff6b35',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 12,
    elevation: 6,
    gap: 8,
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  registerButton: {
    marginTop: 24,
    alignItems: 'center',
  },
  registerText: {
    fontSize: 15,
    color: '#666',
  },
  registerTextBold: {
    color: '#d2691e',
    fontWeight: 'bold',
  },
});