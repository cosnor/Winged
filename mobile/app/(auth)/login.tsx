import React, { useState } from "react";
import {
  StyleSheet,
  Text,
  View,
  TextInput,
  TouchableOpacity,
} from "react-native";
import { router } from "expo-router";
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
          visible: true
        });
        return;
      }

      // Aquí iría la lógica de autenticación (Firebase, API, etc.)
      // Simularemos una operación asíncrona
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setStatus({
        type: 'success',
        message: '¡Bienvenido de vuelta!',
        visible: true
      });

      // Redirigir después de un pequeño delay
      setTimeout(() => {
         router.push("/(app)");
      }, 1000);    } catch (error) {
      setStatus({
        type: 'error',
        message: 'Error al iniciar sesión. Verifica tus credenciales.',
        visible: true
      });
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Iniciar Sesión</Text>
      <Text style={styles.subtitle}>Bienvenido de vuelta</Text>

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

      <TouchableOpacity style={styles.button} onPress={handleLogin}>
        <Text style={styles.buttonText}>Iniciar Sesión</Text>
      </TouchableOpacity>

      <TouchableOpacity onPress={() => router.push("/(auth)/register")}>
        <Text style={styles.registerText}>
          ¿No tienes cuenta?{" "}
          <Text style={{ color: "#d2691e", fontWeight: "bold" }}>
            Regístrate
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