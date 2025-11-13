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
        setStatus({
          type: 'error',
          message: 'Por favor completa todos los campos',
          visible: true
        });
        return;
      }

      if (!validatePasswords()) {
        setStatus({
          type: 'error',
          message: 'Las contraseñas no coinciden',
          visible: true
        });
        return;
      }

      // Aquí iría la lógica de creación de cuenta (Firebase, API, etc.)
      // Simularemos una operación asíncrona
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setStatus({
        type: 'success',
        message: 'Tu cuenta ha sido creada exitosamente',
        visible: true
      });

      // Redirigir después de un pequeño delay para que el usuario vea el mensaje
      setTimeout(() => {
        router.push("/login");
      }, 2000);
      
    } catch (error) {
      setStatus({
        type: 'error',
        message: 'No se pudo crear la cuenta. Por favor intenta de nuevo.',
        visible: true
      });
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