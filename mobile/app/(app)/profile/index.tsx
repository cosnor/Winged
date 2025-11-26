import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, Image, ActivityIndicator, Alert, ScrollView } from "react-native";
import Constants from "expo-constants";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { Ionicons, MaterialCommunityIcons } from "@expo/vector-icons";
import { theme } from "../../../styles/theme"; // Usa tu tema global si ya lo tienes
import { SafeAreaView } from 'react-native-safe-area-context';  
import { router } from "expo-router";
import { useAvedex } from "../../../context/avedex-context";
import { useBirdDetections } from "../../../context/bird-detection-context";
import { LinearGradient } from 'expo-linear-gradient';
import * as Animatable from 'react-native-animatable';  

export default function ProfileScreen() {
  const [user, setUser] = useState<any | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const { clearCollection } = useAvedex();
  const { clearDetections } = useBirdDetections();

  const handleLogout = () => {
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
              console.log('🚪 Starting logout process...');
              
              // Clear collection from Avedex context
              await clearCollection();
              console.log('🗑️ Avedex collection cleared');
              
              // Clear detections from bird-detection context
              clearDetections();
              console.log('🗑️ Bird detections cleared');
              
              // Clear auth tokens
              await AsyncStorage.removeItem('ACCESS_TOKEN');
              await AsyncStorage.removeItem('USER_INFO');
              console.log('🔑 Auth tokens cleared');
              
              console.log('✅ Logged out successfully');
              
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
    <LinearGradient
      colors={['#fffaf0', '#ffe4d6', '#ffd4ba']}
      style={styles.gradient}
    >
      <SafeAreaView style={styles.container} edges={['top']}>
        <ScrollView 
          contentContainerStyle={styles.scrollContent}
          showsVerticalScrollIndicator={false}
        >
          {/* 🪫 Avatar y nombre */}
          <Animatable.View animation="fadeInDown" duration={600} style={styles.header}>
            {loading ? (
              <View style={styles.loadingContainer}>
                <LinearGradient
                  colors={['#ff9a41', '#d2691e']}
                  style={styles.loadingCircle}
                >
                  <ActivityIndicator size="large" color="#fff" />
                </LinearGradient>
              </View>
            ) : user ? (
              <>
                <View style={styles.avatarContainer}>
                  <LinearGradient
                    colors={['#ff9a41', '#ff6b35']}
                    style={styles.avatarGradient}
                  >
                    <Image source={{ uri: user.avatar }} style={styles.avatar} />
                  </LinearGradient>
                  <View style={styles.badgeContainer}>
                    <LinearGradient
                      colors={['#4ade80', '#16a34a']}
                      style={styles.badge}
                    >
                      <Ionicons name="checkmark-circle" size={24} color="#fff" />
                    </LinearGradient>
                  </View>
                </View>
                <Text style={styles.name}>{user.name}</Text>
                <View style={styles.emailContainer}>
                  <Ionicons name="mail" size={16} color="#8b4513" />
                  <Text style={styles.email}>{user.email}</Text>
                </View>
              </>
            ) : (
              <>
                <View style={styles.avatarContainer}>
                  <LinearGradient
                    colors={['#9ca3af', '#6b7280']}
                    style={styles.avatarGradient}
                  >
                    <Ionicons name="person" size={60} color="#fff" />
                  </LinearGradient>
                </View>
                <Text style={styles.name}>No autenticado</Text>
                <Text style={styles.email}>Inicia sesión para ver tu perfil</Text>
              </>
            )}
          </Animatable.View>

          {/* 📊 Estadísticas */}
          <Animatable.View animation="fadeInUp" duration={600} delay={200}>
            <View style={styles.sectionHeader}>
              <Ionicons name="stats-chart" size={20} color="#d2691e" />
              <Text style={styles.sectionTitle}>Mis Estadísticas</Text>
            </View>
          </Animatable.View>

          <View style={styles.statsContainer}>
            <Animatable.View animation="zoomIn" duration={600} delay={300} style={styles.statCardWrapper}>
              <LinearGradient
                colors={['#ff9a41', '#d2691e']}
                style={styles.statCard}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 1 }}
              >
                <View style={styles.statIconCircle}>
                  <Ionicons name="egg" size={32} color="#fff" />
                </View>
                <Text style={styles.statNumber}>{user?.birdsCollected ?? 0}</Text>
                <Text style={styles.statLabel}>Aves</Text>
              </LinearGradient>
            </Animatable.View>

            <Animatable.View animation="zoomIn" duration={600} delay={400} style={styles.statCardWrapper}>
              <LinearGradient
                colors={['#60a5fa', '#2563eb']}
                style={styles.statCard}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 1 }}
              >
                <View style={styles.statIconCircle}>
                  <MaterialCommunityIcons name="binoculars" size={32} color="#fff" />
                </View>
                <Text style={styles.statNumber}>{user?.lastSighting ?? "-"}</Text>
                <Text style={styles.statLabel}>Avistamiento</Text>
              </LinearGradient>
            </Animatable.View>

            <Animatable.View animation="zoomIn" duration={600} delay={500} style={styles.statCardWrapper}>
              <LinearGradient
                colors={['#f59e0b', '#d97706']}
                style={styles.statCard}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 1 }}
              >
                <View style={styles.statIconCircle}>
                  <Ionicons name="flame" size={32} color="#fff" />
                </View>
                <Text style={styles.statNumber}>{user?.streakDays ?? 0}</Text>
                <Text style={styles.statLabel}>Días</Text>
              </LinearGradient>
            </Animatable.View>
          </View>

          {/* Información adicional */}
          <Animatable.View animation="fadeIn" duration={600} delay={600}>
            <View style={styles.infoSection}>
              <View style={styles.infoCard}>
                <LinearGradient
                  colors={['#fff', '#fffaf0']}
                  style={styles.infoGradient}
                >
                  <View style={styles.infoRow}>
                    <Ionicons name="calendar" size={20} color="#ff9a41" />
                    <View style={styles.infoTextContainer}>
                      <Text style={styles.infoLabel}>Miembro desde</Text>
                      <Text style={styles.infoValue}>Noviembre 2025</Text>
                    </View>
                  </View>
                  <View style={styles.divider} />
                  <View style={styles.infoRow}>
                    <Ionicons name="trophy" size={20} color="#f59e0b" />
                    <View style={styles.infoTextContainer}>
                      <Text style={styles.infoLabel}>Nivel</Text>
                      <Text style={styles.infoValue}>Observador Novato</Text>
                    </View>
                  </View>
                  <View style={styles.divider} />
                  <View style={styles.infoRow}>
                    <Ionicons name="star" size={20} color="#60a5fa" />
                    <View style={styles.infoTextContainer}>
                      <Text style={styles.infoLabel}>Puntos XP</Text>
                      <Text style={styles.infoValue}>{user?.streakDays ?? 0} pts</Text>
                    </View>
                  </View>
                </LinearGradient>
              </View>
            </View>
          </Animatable.View>
        </ScrollView>
      </SafeAreaView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  gradient: {
    flex: 1,
  },
  container: {
    flex: 1,
  },
  scrollContent: {
    paddingHorizontal: 20,
    paddingTop: 20,
    paddingBottom: 40,
  },
  header: {
    alignItems: "center",
    marginBottom: 32,
  },
  loadingContainer: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  loadingCircle: {
    width: 100,
    height: 100,
    borderRadius: 50,
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#d2691e',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 6,
  },
  avatarContainer: {
    position: 'relative',
    marginBottom: 16,
  },
  avatarGradient: {
    width: 130,
    height: 130,
    borderRadius: 65,
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#d2691e',
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.4,
    shadowRadius: 12,
    elevation: 8,
  },
  avatar: {
    width: 118,
    height: 118,
    borderRadius: 59,
    borderWidth: 4,
    borderColor: '#fff',
  },
  badgeContainer: {
    position: 'absolute',
    bottom: 0,
    right: 0,
  },
  badge: {
    width: 40,
    height: 40,
    borderRadius: 20,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 3,
    borderColor: '#fff',
    shadowColor: '#16a34a',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
    elevation: 4,
  },
  name: {
    fontSize: 28,
    fontWeight: "bold",
    color: '#d2691e',
    marginBottom: 8,
    textAlign: 'center',
  },
  emailContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    backgroundColor: 'rgba(255, 255, 255, 0.7)',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
  },
  email: {
    fontSize: 14,
    color: '#8b4513',
    fontWeight: '500',
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 16,
    paddingHorizontal: 4,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#d2691e',
  },
  statsContainer: {
    flexDirection: "row",
    gap: 12,
    marginBottom: 24,
  },
  statCardWrapper: {
    flex: 1,
  },
  statCard: {
    borderRadius: 20,
    padding: 16,
    alignItems: "center",
    shadowColor: "#000",
    shadowOpacity: 0.2,
    shadowRadius: 8,
    shadowOffset: { width: 0, height: 4 },
    elevation: 6,
    minHeight: 140,
    justifyContent: 'center',
  },
  statIconCircle: {
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: 'rgba(255, 255, 255, 0.25)',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 12,
  },
  statNumber: {
    fontSize: 24,
    fontWeight: "bold",
    color: '#fff',
    marginBottom: 4,
  },
  statLabel: {
    fontSize: 12,
    color: 'rgba(255, 255, 255, 0.9)',
    fontWeight: '600',
    textAlign: 'center',
  },
  infoSection: {
    marginTop: 8,
  },
  infoCard: {
    borderRadius: 20,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
  },
  infoGradient: {
    padding: 20,
  },
  infoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  infoTextContainer: {
    flex: 1,
  },
  infoLabel: {
    fontSize: 12,
    color: '#8b4513',
    fontWeight: '500',
    marginBottom: 2,
  },
  infoValue: {
    fontSize: 16,
    color: '#333',
    fontWeight: '700',
  },
  divider: {
    height: 1,
    backgroundColor: 'rgba(210, 105, 30, 0.1)',
    marginVertical: 16,
  },
  logoutButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#dc2626',
    paddingHorizontal: 30,
    paddingVertical: 15,
    borderRadius: 12,
    marginTop: 30,
    gap: 8,
  },
  logoutText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});
