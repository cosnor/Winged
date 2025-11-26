import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { LinearGradient } from 'expo-linear-gradient';
import * as Animatable from 'react-native-animatable';
import Ionicons from '@expo/vector-icons/Ionicons';

export default function RoutesScreen() {
  return (
    <LinearGradient
      colors={['#fffaf0', '#ffe4d6', '#ffd4ba']}
      style={styles.gradient}
    >
      <SafeAreaView style={styles.container} edges={['top']}>
        <ScrollView>
        {/* Header */}
        <Animatable.View animation="fadeInDown" duration={600} style={styles.header}>
         
        </Animatable.View>

        {/* Coming Soon Content */}
        <View style={styles.content}>
          <Animatable.View animation="bounceIn" duration={1000} delay={300}>
            <LinearGradient
              colors={['#ff9a41', '#d2691e']}
              style={styles.comingSoonCircle}
            >
              <Ionicons name="construct" size={80} color="#fff" />
            </LinearGradient>
          </Animatable.View>

          <Animatable.View animation="fadeInUp" duration={600} delay={600} style={styles.textContainer}>
            <Text style={styles.comingSoonTitle}>Próximamente</Text>
            <Text style={styles.comingSoonSubtitle}>
              Estamos trabajando en esta funcionalidad
            </Text>
          </Animatable.View>

          <Animatable.View animation="fadeIn" duration={600} delay={900} style={styles.featuresContainer}>
            <View style={styles.featureCard}>
              <LinearGradient
                colors={['#fff', '#fffaf0']}
                style={styles.featureGradient}
              >
                <Ionicons name="map-outline" size={24} color="#60a5fa" />
                <Text style={styles.featureTitle}>Rutas Guiadas</Text>
                <Text style={styles.featureDescription}>
                  Explora senderos optimizados para el avistamiento de aves
                </Text>
              </LinearGradient>
            </View>

            <View style={styles.featureCard}>
              <LinearGradient
                colors={['#fff', '#fffaf0']}
                style={styles.featureGradient}
              >
                <Ionicons name="location-outline" size={24} color="#4ade80" />
                <Text style={styles.featureTitle}>Puntos de Interés</Text>
                <Text style={styles.featureDescription}>
                  Descubre los mejores lugares para observar cada especie
                </Text>
              </LinearGradient>
            </View>

            <View style={styles.featureCard}>
              <LinearGradient
                colors={['#fff', '#fffaf0']}
                style={styles.featureGradient}
              >
                <Ionicons name="time-outline" size={24} color="#ff9a41" />
                <Text style={styles.featureTitle}>Mejores Horarios</Text>
                <Text style={styles.featureDescription}>
                  Recomendaciones de horarios ideales para cada ruta
                </Text>
              </LinearGradient>
            </View>
          </Animatable.View>

          <Animatable.View animation="pulse" iterationCount="infinite" duration={2000} style={styles.notificationCard}>
            <LinearGradient
              colors={['#dbeafe', '#bfdbfe']}
              style={styles.notificationGradient}
            >
              <Ionicons name="notifications" size={20} color="#2563eb" />
              <Text style={styles.notificationText}>
                Te notificaremos cuando esta función esté disponible
              </Text>
            </LinearGradient>
          </Animatable.View>
        </View>
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
    marginBottom: 5,
  },
  header: {
    paddingHorizontal: 20,
    paddingTop: 10,
    paddingBottom: 16,
  },
  headerContent: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  iconCircle: {
    width: 56,
    height: 56,
    borderRadius: 28,
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#2563eb',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 6,
  },
  headerText: {
    flex: 1,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2563eb',
    marginBottom: 2,
  },
  subtitle: {
    fontSize: 14,
    color: '#60a5fa',
    fontWeight: '500',
  },
  content: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 20,
  },
  comingSoonCircle: {
    width: 160,
    height: 160,
    borderRadius: 80,
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#d2691e',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.4,
    shadowRadius: 16,
    elevation: 10,
    marginBottom: 32,
  },
  textContainer: {
    alignItems: 'center',
    marginBottom: 32,
  },
  comingSoonTitle: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#d2691e',
    marginBottom: 8,
  },
  comingSoonSubtitle: {
    fontSize: 16,
    color: '#8b4513',
    textAlign: 'center',
    fontWeight: '500',
  },
  featuresContainer: {
    width: '100%',
    gap: 16,
    marginBottom: 24,
  },
  featureCard: {
    borderRadius: 16,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
  },
  featureGradient: {
    padding: 20,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 16,
  },
  featureTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: '#333',
    marginBottom: 4,
    flex: 1,
  },
  featureDescription: {
    fontSize: 13,
    color: '#666',
    lineHeight: 18,
    flex: 2,
  },
  notificationCard: {
    borderRadius: 12,
    overflow: 'hidden',
    width: '100%',
  },
  notificationGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    gap: 12,
  },
  notificationText: {
    flex: 1,
    fontSize: 13,
    color: '#2563eb',
    fontWeight: '600',
    lineHeight: 18,
  },
});