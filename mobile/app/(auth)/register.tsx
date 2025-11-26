import React, { useState } from "react";
import {
  StyleSheet,
  Text,
  View,
  TextInput,
  TouchableOpacity,
} from "react-native";
import Constants from "expo-constants";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { router } from "expo-router";
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
      
      console.log('✅ Registration successful, token saved');
      console.log('📦 Full response body:', JSON.stringify(body, null, 2));
      
      // Fetch user info after successful registration
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
        // Don't fail the registration if user info fetch fails
      }
      
      setStatus({ type: 'success', message: 'Cuenta creada. Bienvenido!', visible: true });
      // Navigate to main app since backend auto-logged the user
      setTimeout(() => router.push('/(app)'), 400);
    } catch (error) {
      console.error('Signup error:', error);
      setStatus({ type: 'error', message: 'Error de red al registrarse', visible: true });
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Crear Cuenta</Text>
      <Text style={styles.subtitle}>¡Únete a Winged!</Text>

      <Text style={styles.label}>Nombre de usuario</Text>
      <TextInput
        style={styles.input}
        placeholder="Tu nombre"
        autoCapitalize="words"
        value={username}
        onChangeText={(text: string) => setUsername(text)}
      />


      <Text style={styles.label}>Correo</Text>
      <TextInput
        style={styles.input}
        placeholder="tu@email.com"
        keyboardType="email-address"
        autoCapitalize="none"
        value={email}
        onChangeText={(text: string) => setEmail(text)}
      />

      <Text style={styles.label}>Contraseña</Text>
      <TextInput
        style={styles.input}
        placeholder="••••••"
        secureTextEntry
        value={password}
        onChangeText={(text: string) => setPassword(text)}
      />

      <Text style={styles.label}>Confirmar Contraseña</Text>
      <TextInput
        style={styles.input}
        placeholder="••••••"
        secureTextEntry
        value={passwordConfirm}
        onChangeText={(text: string) => setPasswordConfirm(text)}
      />

      <TouchableOpacity style={styles.button} onPress={handleRegister}>
        <Text style={styles.buttonText}>Crear Cuenta</Text>
      </TouchableOpacity>

      <TouchableOpacity onPress={() => router.push("/login")}>
        <Text style={styles.registerText}>
          ¿Ya tienes una cuenta?{" "}
          <Text style={{ color: "#d2691e", fontWeight: "bold" }}>
            Inicia Sesión
          </Text>
        </Text>
      </TouchableOpacity>

      <StatusMessage
        type={status.type}
        message={status.message}
        visible={status.visible}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fffaf0",
    alignItems: "center",
    justifyContent: "center",
    padding: 20,
  },
  title: {
    fontSize: 26,
    fontWeight: "bold",
    marginBottom: 5,
    color: "#d2691e",
  },
  subtitle: {
    fontSize: 14,
    color: "#555",
    marginBottom: 30,
  },
  label: {
    alignSelf: "flex-start",
    marginBottom: 5,
    fontSize: 14,
    color: "#333",
  },
  input: {
    width: "100%",
    padding: 12,
    borderWidth: 1,
    borderColor: "#ddd",
    borderRadius: 8,
    marginBottom: 15,
    backgroundColor: "#fff",
  },
  button: {
    width: "100%",
    backgroundColor: "#d2691e",
    padding: 15,
    borderRadius: 8,
    alignItems: "center",
    marginTop: 10,
  },
  buttonText: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "bold",
  },
  registerText: {
    marginTop: 20,
    color: "#333",
  },
});