import React from "react";
import { View, Text, StyleSheet, Image } from "react-native";
import { Ionicons, MaterialCommunityIcons } from "@expo/vector-icons";
import { theme } from "../../../styles/theme"; // Usa tu tema global si ya lo tienes
import { SafeAreaView } from 'react-native-safe-area-context';  

export default function ProfileScreen() {
  // 🔹 Datos de ejemplo (luego los puedes reemplazar con datos reales del usuario)
  const user = {
    name: "Camila Osorno",
    email: "camila.osorno@example.com",
    birdsCollected: 7,
    lastSighting: "Tucán Amazónico",
    streakDays: 7,
    avatar: "https://ralfvanveen.com/wp-content/uploads/2021/06/Placeholder-_-Begrippenlijst.svg" // puedes usar cualquier imagen o avatar generado
  };

  return (
    <SafeAreaView style={styles.container}>
      {/* 🦜 Avatar y nombre */}
      <View style={styles.header}>
        <Image source={{ uri: user.avatar }} style={styles.avatar} />
        <Text style={styles.name}>{user.name}</Text>
        <Text style={styles.email}>{user.email}</Text>
      </View>

      {/* 📊 Estadísticas */}
      <View style={styles.statsContainer}>
        <View style={styles.statCard}>
          <Ionicons name="egg-outline" size={28} color={theme.colors.primary} />
          <Text style={styles.statNumber}>{user.birdsCollected}</Text>
          <Text style={styles.statLabel}>Aves Coleccionadas</Text>
        </View>

        <View style={styles.statCard}>
          <MaterialCommunityIcons
            name="binoculars"
            size={28}
            color={theme.colors.secondary}
          />
          <Text style={styles.statNumber}>{user.lastSighting}</Text>
          <Text style={styles.statLabel}>Último Avistamiento</Text>
        </View>

        <View style={styles.statCard}>
          <Ionicons name="flame-outline" size={28} color="#F97316" />
          <Text style={styles.statNumber}>{user.streakDays} días</Text>
          <Text style={styles.statLabel}>Racha Activa</Text>
        </View>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
    alignItems: "center",
    paddingTop: 50,
  },
  header: {
    alignItems: "center",
    marginBottom: 30,
  },
  avatar: {
    width: 120,
    height: 120,
    borderRadius: 60,
    borderWidth: 3,
    borderColor: theme.colors.primary,
  },
  name: {
    fontSize: 24,
    fontWeight: "700",
    color: theme.colors.foreground,
    marginTop: 10,
  },
  email: {
    fontSize: 14,
    color: theme.colors.mutedForeground,
    marginTop: 4,
  },
  statsContainer: {
    width: "90%",
    flexDirection: "column",
    gap: 15,
  },
  statCard: {
    backgroundColor: theme.colors.card,
    borderRadius: 20,
    padding: 20,
    alignItems: "center",
    elevation: 3,
    shadowColor: "#000",
    shadowOpacity: 0.1,
    shadowRadius: 5,
  },
  statNumber: {
    fontSize: 20,
    fontWeight: "600",
    color: theme.colors.foreground,
    marginTop: 5,
  },
  statLabel: {
    fontSize: 14,
    color: theme.colors.mutedForeground,
    marginTop: 3,
  },
});
