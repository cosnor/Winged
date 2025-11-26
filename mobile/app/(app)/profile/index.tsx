import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, Image, ActivityIndicator, TouchableOpacity, Alert } from "react-native";
import Constants from "expo-constants";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { Ionicons, MaterialCommunityIcons } from "@expo/vector-icons";
import { theme } from "../../../styles/theme"; // Usa tu tema global si ya lo tienes
import { SafeAreaView } from 'react-native-safe-area-context';
import { router } from "expo-router";
import { useAvedex } from "../../../context/avedex-context";  

export default function ProfileScreen() {
  const [user, setUser] = useState<any | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const { clearCollection } = useAvedex();

  const handleLogout = async () => {
    Alert.alert(
      "Cerrar Sesión",
      "¿Estás seguro que deseas cerrar sesión?",
      [
        {
          text: "Cancelar",
          style: "cancel"
        },
        {
          text: "Cerrar Sesión",
          style: "destructive",
          onPress: async () => {
            try {
              // Clear AsyncStorage
              await AsyncStorage.removeItem('ACCESS_TOKEN');
              await AsyncStorage.removeItem('USER_INFO');
              
              // Clear Avedex collection for this user
              await clearCollection();
              
              // Navigate to login
              router.replace('/(auth)/login');
            } catch (error) {
              console.error('Error during logout:', error);
              Alert.alert('Error', 'Hubo un problema al cerrar sesión');
            }
          }
        }
      ]
    );
  };

  useEffect(() => {
    let mounted = true;
    const loadProfile = async () => {
      setLoading(true);
      try {
        const API_BASE_URL = (Constants.expoConfig as any)?.extra?.API_BASE_URL;
        const token = await AsyncStorage.getItem("ACCESS_TOKEN");
        if (!token) {
          if (mounted) {
            setUser(null);
            setLoading(false);
          }
          return;
        }

        const resp = await fetch(`${API_BASE_URL}/users/me`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        });

        if (!resp.ok) {
          // Could show a message or handle 401 -> logout. For now just log and clear user
          console.warn("Failed to fetch profile", resp.status);
          if (mounted) setUser(null);
          return;
        }

        const body = await resp.json();
        // The gateway returns either { data: {...} } or the object itself
        const data = (body && body.data) ? body.data : body;

        if (mounted) {
          setUser({
            name: data.name || data.full_name || "Usuario",
            email: data.email || "",
            birdsCollected: 0,
            lastSighting: "-",
            streakDays: data.xp || 0,
            avatar: "https://ralfvanveen.com/wp-content/uploads/2021/06/Placeholder-_-Begrippenlijst.svg",
          });
        }
      } catch (e) {
        console.error("Error loading profile:", e);
        if (mounted) setUser(null);
      } finally {
        if (mounted) setLoading(false);
      }
    };

    loadProfile();
    return () => { mounted = false; };
  }, []);

  return (
    <SafeAreaView style={styles.container}>
      {/* 🦜 Avatar y nombre */}
      <View style={styles.header}>
        {loading ? (
          <ActivityIndicator size="large" color={theme.colors.primary} />
        ) : user ? (
          <>
            <Image source={{ uri: user.avatar }} style={styles.avatar} />
            <Text style={styles.name}>{user.name}</Text>
            <Text style={styles.email}>{user.email}</Text>
          </>
        ) : (
          <>
            <Text style={styles.name}>No autenticado</Text>
            <Text style={styles.email}>Inicia sesión para ver tu perfil</Text>
          </>
        )}
      </View>

      {/* 📊 Estadísticas */}
      <View style={styles.statsContainer}>
        <View style={styles.statCard}>
          <Ionicons name="egg-outline" size={28} color={theme.colors.primary} />
          <Text style={styles.statNumber}>{user?.birdsCollected ?? 0}</Text>
          <Text style={styles.statLabel}>Aves Coleccionadas</Text>
        </View>

        <View style={styles.statCard}>
          <MaterialCommunityIcons
            name="binoculars"
            size={28}
            color={theme.colors.secondary}
          />
          <Text style={styles.statNumber}>{user?.lastSighting ?? "-"}</Text>
          <Text style={styles.statLabel}>Último Avistamiento</Text>
        </View>

        <View style={styles.statCard}>
          <Ionicons name="flame-outline" size={28} color="#F97316" />
          <Text style={styles.statNumber}>{user?.streakDays ?? 0} días</Text>
          <Text style={styles.statLabel}>Racha Activa</Text>
        </View>
      </View>

      {/* Botón de Cerrar Sesión */}
      {user && (
        <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
          <Ionicons name="log-out-outline" size={24} color="#fff" />
          <Text style={styles.logoutText}>Cerrar Sesión</Text>
        </TouchableOpacity>
      )}
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
  logoutButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#dc2626',
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 10,
    marginTop: 30,
    gap: 8,
  },
  logoutText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});
