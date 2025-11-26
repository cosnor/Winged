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

export default function Register() {
  const [username, setUsername] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [passwordConfirm, setPasswordConfirm] = useState<string>("");
  const [status, setStatus] = useState<{
    type: 'success' | 'error';
    message: string;
    visible: boolean;
  }>({
    type: 'error',
    message: '',
    visible: false
  });

  const validatePasswords = () => {
    return password === passwordConfirm;
  }

  const handleRegister = async () => {
    try {
      // Reset any previous status message
      setStatus({ type: 'error', message: '', visible: false });

      if (!username || !email || !password) {
        setStatus({ type: 'error', message: 'Por favor completa todos los campos', visible: true });
        return;
      }

      if (!validatePasswords()) {
        setStatus({ type: 'error', message: 'Las contraseñas no coinciden', visible: true });
        return;
      }

      const API_BASE_URL = (Constants.expoConfig as any)?.extra?.API_BASE_URL;

      const resp = await fetch(`${API_BASE_URL}/users/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: username, email, password }),
      });

      if (!resp.ok) {
        let message = `Error ${resp.status}`;
        try {
          const json = await resp.json();
          if (json && (json.detail || json.message || json.error)) {
            message = json.detail || json.message || json.error;
          } else if (json && Object.keys(json).length) {
            message = JSON.stringify(json);
          }
        } catch (e) {
          const text = await resp.text();
          if (text) message = text;
        }
        setStatus({ type: 'error', message, visible: true });
        return;
      }

      const body = await resp.json();
      // The gateway performs login after signup and should return tokens
      const token = body.access_token || body.token || (body.data && body.data.access_token);
      if (!token) {
        setStatus({ type: 'error', message: 'Respuesta inválida del servidor', visible: true });
        return;
      }

      await AsyncStorage.setItem('ACCESS_TOKEN', token);
      setStatus({ type: 'success', message: 'Cuenta creada. Bienvenido!', visible: true });
      // Navigate to main app since backend auto-logged the user
      setTimeout(() => router.push('/(app)'), 400);
    } catch (error) {
      console.error('Signup error:', error);
      setStatus({ type: 'error', message: 'Error de red al registrarse', visible: true });
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
              colors={['#4ade80', '#16a34a']}
              style={styles.logoCircle}
            >
              <Ionicons name="person-add" size={48} color="#fff" />
            </LinearGradient>
            <Text style={styles.title}>Crear Cuenta</Text>
            <Text style={styles.subtitle}>¡Únete a la comunidad Winged!</Text>
          </Animatable.View>

          <Animatable.View animation="fadeInUp" delay={200} duration={800} style={styles.formContainer}>
            <View style={styles.inputContainer}>
              <View style={styles.inputIconWrapper}>
                <Ionicons name="person" size={20} color="#4ade80" />
              </View>
              <View style={styles.inputWrapper}>
                <Text style={styles.label}>Nombre de usuario</Text>
                <TextInput
                  style={styles.input}
                  placeholder="Tu nombre"
                  placeholderTextColor="#aaa"
                  autoCapitalize="words"
                  value={username}
                  onChangeText={(text: string) => setUsername(text)}
                />
              </View>
            </View>

            <View style={styles.inputContainer}>
              <View style={styles.inputIconWrapper}>
                <Ionicons name="mail" size={20} color="#4ade80" />
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
                <Ionicons name="lock-closed" size={20} color="#4ade80" />
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

            <View style={styles.inputContainer}>
              <View style={styles.inputIconWrapper}>
                <Ionicons name="checkmark-circle" size={20} color="#4ade80" />
              </View>
              <View style={styles.inputWrapper}>
                <Text style={styles.label}>Confirmar Contraseña</Text>
                <TextInput
                  style={styles.input}
                  placeholder="••••••"
                  placeholderTextColor="#aaa"
                  secureTextEntry
                  value={passwordConfirm}
                  onChangeText={(text: string) => setPasswordConfirm(text)}
                />
              </View>
            </View>

            <TouchableOpacity onPress={handleRegister}>
              <LinearGradient
                colors={['#4ade80', '#16a34a']}
                style={styles.button}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 0 }}
              >
                <Text style={styles.buttonText}>Crear Cuenta</Text>
                <Ionicons name="checkmark" size={22} color="#fff" />
              </LinearGradient>
            </TouchableOpacity>

            <TouchableOpacity onPress={() => router.push("/login")} style={styles.registerButton}>
              <Text style={styles.registerText}>
                ¿Ya tienes una cuenta?{" "}
                <Text style={styles.registerTextBold}>
                  Inicia Sesión
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
    paddingTop: 40,
  },
  headerContainer: {
    alignItems: 'center',
    marginBottom: 32,
  },
  logoCircle: {
    width: 100,
    height: 100,
    borderRadius: 50,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 24,
    shadowColor: '#16a34a',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.4,
    shadowRadius: 16,
    elevation: 10,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#16a34a',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 15,
    color: '#15803d',
    fontWeight: '500',
  },
  formContainer: {
    width: '100%',
  },
  inputContainer: {
    flexDirection: 'row',
    marginBottom: 16,
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
    backgroundColor: '#f0fdf4',
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
    shadowColor: '#16a34a',
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
    color: '#16a34a',
    fontWeight: 'bold',
  },
});