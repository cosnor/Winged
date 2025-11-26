import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView, Dimensions } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import Ionicons from '@expo/vector-icons/Ionicons';
import * as Animatable from 'react-native-animatable';
import * as Location from 'expo-location';
import { router } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';

export default function MapScreen() {
  const [location, setLocation] = useState<Location.LocationObject | null>(null);
  const [hasPermission, setHasPermission] = useState<boolean>(false);

  useEffect(() => {
    (async () => {
      const { status } = await Location.requestForegroundPermissionsAsync();
      if (status === 'granted') {
        setHasPermission(true);
        try {
          const userLocation = await Location.getCurrentPositionAsync({});
          setLocation(userLocation);
        } catch (error) {
          console.log('Error obteniendo ubicación:', error);
        }
      }
    })();
  }, []);

  const mapFeatures = [
    {
      id: 'nearby',
      title: 'Aves Cerca de Ti',
      description: 'Descubre qué especies están en tu área',
      icon: 'location',
      color: '#ff9a41',
      gradient: ['#ff9a41', '#d2691e'] as const,
      route: '/map/nearby',
    },
    {
      id: 'zones',
      title: 'Aves por Zona',
      description: 'Explora especies por ubicación geográfica',
      icon: 'map',
      color: '#4ade80',
      gradient: ['#4ade80', '#16a34a'] as const,
      route: '/map/zones',
    },
    {
      id: 'routes',
      title: 'Rutas de Observación',
      description: 'Descubre las mejores rutas para avistar aves',
      icon: 'trail-sign',
      color: '#60a5fa',
      gradient: ['#60a5fa', '#2563eb'] as const,
      route: '/map/routes',
    },
  ];

  return (
    <LinearGradient
      colors={['#fffaf0', '#ffe4d6', '#ffd4ba']}
      style={styles.gradient}
    >
      {/* Decoraciones de fondo */}
      <View style={styles.backgroundDecor}>
        <Ionicons name="navigate" size={140} color="rgba(210, 105, 30, 0.04)" style={styles.decorNav} />
        <Ionicons name="compass" size={100} color="rgba(255, 154, 65, 0.05)" style={styles.decorCompass} />
        <Ionicons name="location" size={80} color="rgba(255, 107, 53, 0.04)" style={styles.decorLocation} />
      </View>

      <SafeAreaView style={styles.container} edges={['top']}>
        <ScrollView 
          contentContainerStyle={styles.scrollContent}
          showsVerticalScrollIndicator={false}
        >
          {/* Header */}
          <Animatable.View animation="fadeInDown" duration={600} style={styles.header}>
            <View style={styles.iconHeader}>
              <LinearGradient
                colors={['#ff9a41', '#d2691e']}
                style={styles.headerIconCircle}
              >
                <Ionicons name="map" size={36} color="#fff" />
              </LinearGradient>
            </View>
            <Text style={styles.title}>Explorador de Aves</Text>
            <Text style={styles.subtitle}>🗺️ Descubre especies en tu región</Text>
          </Animatable.View>

          {/* Location Info */}
          {hasPermission && location && (
            <Animatable.View animation="fadeIn" duration={600} delay={200}>
              <View style={styles.locationCard}>
                <LinearGradient
                  colors={['#fff', '#fffaf0']}
                  style={styles.locationGradient}
                >
                  <Ionicons name="location-sharp" size={24} color="#d2691e" />
                  <View style={styles.locationTextContainer}>
                    <Text style={styles.locationTitle}>Tu ubicación actual</Text>
                    <Text style={styles.locationCoords}>
                      {location.coords.latitude.toFixed(4)}, {location.coords.longitude.toFixed(4)}
                    </Text>
                  </View>
                  <Ionicons name="checkmark-circle" size={24} color="#4ade80" />
                </LinearGradient>
              </View>
            </Animatable.View>
          )}

          {/* Feature Cards */}
          <View style={styles.featuresContainer}>
            {mapFeatures.map((feature, index) => (
              <Animatable.View
                key={feature.id}
                animation="fadeInUp"
                duration={600}
                delay={300 + index * 100}
              >
                <TouchableOpacity
                  style={styles.featureCard}
                  onPress={() => router.push(feature.route as any)}
                  activeOpacity={0.8}
                >
                  <LinearGradient
                    colors={feature.gradient}
                    style={styles.featureGradient}
                    start={{ x: 0, y: 0 }}
                    end={{ x: 1, y: 1 }}
                  >
                    <View style={styles.featureIconContainer}>
                      <Ionicons name={feature.icon as any} size={32} color="#fff" />
                    </View>
                    <View style={styles.featureTextContainer}>
                      <Text style={styles.featureTitle}>{feature.title}</Text>
                      <Text style={styles.featureDescription}>{feature.description}</Text>
                    </View>
                    <Ionicons name="chevron-forward" size={24} color="#fff" />
                  </LinearGradient>
                </TouchableOpacity>
              </Animatable.View>
            ))}
          </View>

          {/* Info Section */}
          <Animatable.View animation="fadeIn" duration={600} delay={800}>
            <View style={styles.infoSection}>
              <Text style={styles.infoTitle}>💡 ¿Sabías qué?</Text>
              <View style={styles.infoCard}>
                <LinearGradient
                  colors={['#fff', '#fffaf0']}
                  style={styles.infoGradient}
                >
                  <View style={styles.infoItem}>
                    <Ionicons name="analytics" size={20} color="#ff9a41" />
                    <Text style={styles.infoText}>
                      Nuestros datos dependen de la hora a la que nos consultes
                    </Text>
                  </View>
                  <View style={styles.divider} />
                  <View style={styles.infoItem}>
                    <Ionicons name="earth" size={20} color="#4ade80" />
                    <Text style={styles.infoText}>
                      Explora zonas de alta biodiversidad para aumentar tus avistamientos
                    </Text>
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
  backgroundDecor: {
    position: 'absolute',
    width: '100%',
    height: '100%',
  },
  decorNav: {
    position: 'absolute',
    top: -20,
    right: -30,
    transform: [{ rotate: '15deg' }],
  },
  decorCompass: {
    position: 'absolute',
    top: '35%',
    left: -20,
    transform: [{ rotate: '-20deg' }],
  },
  decorLocation: {
    position: 'absolute',
    bottom: '20%',
    right: 20,
    transform: [{ rotate: '25deg' }],
  },
  container: {
    flex: 1,
  },
  scrollContent: {
    paddingHorizontal: 20,
    paddingBottom: 40,
  },
  header: {
    alignItems: 'center',
    marginTop: 10,
    marginBottom: 20,
  },
  iconHeader: {
    marginBottom: 12,
  },
  headerIconCircle: {
    width: 70,
    height: 70,
    borderRadius: 35,
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#d2691e',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 6,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#d2691e',
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 16,
    color: '#8b4513',
    fontWeight: '500',
  },
  locationCard: {
    marginBottom: 24,
    borderRadius: 16,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  locationGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    gap: 12,
  },
  locationTextContainer: {
    flex: 1,
  },
  locationTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#8b4513',
    marginBottom: 2,
  },
  locationCoords: {
    fontSize: 12,
    color: '#666',
  },
  featuresContainer: {
    gap: 16,
    marginBottom: 24,
  },
  featureCard: {
    borderRadius: 20,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 8,
    elevation: 5,
  },
  featureGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 20,
    gap: 16,
  },
  featureIconContainer: {
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: 'rgba(255, 255, 255, 0.3)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  featureTextContainer: {
    flex: 1,
  },
  featureTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 4,
  },
  featureDescription: {
    fontSize: 13,
    color: 'rgba(255, 255, 255, 0.9)',
    lineHeight: 18,
  },
  infoSection: {
    marginTop: 8,
  },
  infoTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#d2691e',
    marginBottom: 12,
    textAlign: 'center',
  },
  infoCard: {
    borderRadius: 16,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  infoGradient: {
    padding: 20,
  },
  infoItem: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 12,
  },
  infoText: {
    flex: 1,
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
  },
  divider: {
    height: 1,
    backgroundColor: 'rgba(210, 105, 30, 0.1)',
    marginVertical: 16,
  },
});
