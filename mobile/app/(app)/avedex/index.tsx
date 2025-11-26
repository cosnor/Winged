import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, ActivityIndicator, Dimensions, TouchableOpacity } from 'react-native';
import { useAvedex } from '../../../context/avedex-context';
import AvedexCard from '../../../components/cards/AvedexCard';
import { router, useNavigation } from 'expo-router';
import * as Animatable from 'react-native-animatable';
import { SafeAreaView } from 'react-native-safe-area-context';
import { LinearGradient } from 'expo-linear-gradient';
import Ionicons from '@expo/vector-icons/Ionicons';

const CARD_WIDTH = (Dimensions.get('window').width - 48) / 2;

export default function AvedexScreen() {
  const { birds, loading, error, newBirdIds, markBirdsAsSeen } = useAvedex();
  const [shouldAnimate, setShouldAnimate] = useState(false);
  const [sortBy, setSortBy] = useState<'alphabetical' | 'date'>('date');
  const navigation = useNavigation();

  // Ordenar aves según criterio seleccionado y eliminar duplicados
  const sortedBirds = React.useMemo(() => {
    if (!birds) return [];
    
    // Primero, eliminar duplicados usando Map con species_name como key
    const uniqueBirdsMap = new Map();
    birds.forEach((bird) => {
      // Use scientificName (species_name) as unique identifier
      if (!uniqueBirdsMap.has(bird.scientificName)) {
        uniqueBirdsMap.set(bird.scientificName, bird);
      } else {
        console.log(`🗑️ Duplicate found and removed: ${bird.scientificName} (${bird.commonName})`);
      }
    });
    
    const uniqueBirds = Array.from(uniqueBirdsMap.values());
    console.log(`🔍 Filtering duplicates: ${birds.length} → ${uniqueBirds.length} unique birds`);
    
    // Luego ordenar según el criterio
    if (sortBy === 'alphabetical') {
      return uniqueBirds.sort((a, b) => a.commonName.localeCompare(b.commonName));
    } else {
      return uniqueBirds.sort((a, b) => 
        new Date(b.firstSeenDate).getTime() - new Date(a.firstSeenDate).getTime()
      );
    }
  }, [birds, sortBy]);

  useEffect(() => {
    const unsubscribe = navigation.addListener('focus', () => {
      setShouldAnimate(true);
      // Reiniciar la animación después de un tiempo
      const timer = setTimeout(() => {
        if (newBirdIds.size > 0) {
          markBirdsAsSeen(Array.from(newBirdIds));
        }
        setShouldAnimate(false);
      }, 2000);
      return () => clearTimeout(timer);
    });

    return unsubscribe;
  }, [navigation, newBirdIds]);

  if (loading) {
    return (
      <LinearGradient
        colors={['#fffaf0', '#ffe4d6', '#ffd4ba']}
        style={{ flex: 1 }}
      >
        <View style={styles.centerContainer}>
          <ActivityIndicator size="large" color="#d2691e" />
        </View>
      </LinearGradient>
    );
  }

  if (error) {
    return (
      <LinearGradient
        colors={['#fffaf0', '#ffe4d6', '#ffd4ba']}
        style={{ flex: 1 }}
      >
        <View style={styles.centerContainer}>
          <Text style={styles.errorText}>{error}</Text>
        </View>
      </LinearGradient>
    );
  }

  if (birds.length === 0) {
    return (
      <LinearGradient
        colors={['#fffaf0', '#ffe4d6', '#ffd4ba']}
        style={{ flex: 1 }}
      >
        {/* Decoraciones de fondo */}
        <View style={styles.backgroundDecor}>
          <Ionicons name="leaf" size={120} color="rgba(210, 105, 30, 0.05)" style={styles.decorLeaf1} />
          <Ionicons name="leaf" size={100} color="rgba(255, 154, 65, 0.06)" style={styles.decorLeaf2} />
          <Ionicons name="leaf" size={80} color="rgba(210, 105, 30, 0.04)" style={styles.decorLeaf3} />
        </View>
        
        <SafeAreaView style={styles.containerTransparent}>
          <Text style={styles.title}>Mi Avedex</Text>
        
        {/* Mensaje principal estilizado */}
        <Animatable.View 
          animation="fadeInDown" 
          duration={800}
          style={styles.emptyMessageContainer}
        >
          <Ionicons name="leaf-outline" size={80} color="#d2691e" />
          <Text style={styles.emptyTitle}>¡Tu Avedex está esperando!</Text>
          <Text style={styles.emptySubtitle}>
            Comienza a explorar y descubrir aves increíbles
          </Text>
          <View style={styles.emptyStepsContainer}>
            <View style={styles.emptyStep}>
              <Ionicons name="camera-outline" size={24} color="#ff9a41" />
              <Text style={styles.emptyStepText}>Identifica aves</Text>
            </View>
            <View style={styles.emptyStep}>
              <Ionicons name="add-circle-outline" size={24} color="#ff9a41" />
              <Text style={styles.emptyStepText}>Colecciónalas aquí</Text>
            </View>
            <View style={styles.emptyStep}>
              <Ionicons name="trophy-outline" size={24} color="#ff9a41" />
              <Text style={styles.emptyStepText}>Amplía tu álbum</Text>
            </View>
          </View>
        </Animatable.View>

        {/* Placeholders de cards */}
        <ScrollView contentContainerStyle={styles.grid}>
          {[1, 2, 3, 4, 5, 6].map((index) => (
            <Animatable.View
              key={`placeholder-${index}`}
              animation="fadeIn"
              delay={index * 100}
              duration={600}
              style={styles.placeholderCard}
            >
              <View style={styles.placeholderImage}>
                <Ionicons name="image-outline" size={40} color="#ccc" />
              </View>
              <View style={styles.placeholderInfo}>
                <View style={styles.placeholderLine} />
                <View style={[styles.placeholderLine, styles.placeholderLineShort]} />
                <View style={[styles.placeholderLine, styles.placeholderLineTiny]} />
              </View>
            </Animatable.View>
          ))}
        </ScrollView>
      </SafeAreaView>
      </LinearGradient>
    );
  }

  return (
    <LinearGradient
      colors={['#fffaf0', '#ffe4d6', '#ffd4ba']}
      style={{ flex: 1 }}
    >
      {/* Decoraciones de fondo */}
      <View style={styles.backgroundDecor}>
        <Ionicons name="leaf" size={140} color="rgba(210, 105, 30, 0.04)" style={styles.decorLeaf1} />
        <Ionicons name="leaf" size={110} color="rgba(255, 154, 65, 0.05)" style={styles.decorLeaf2} />
        <Ionicons name="leaf" size={90} color="rgba(210, 105, 30, 0.03)" style={styles.decorLeaf3} />
        <Ionicons name="sparkles" size={60} color="rgba(255, 107, 53, 0.08)" style={styles.decorSparkle} />
      </View>
      
      <SafeAreaView style={styles.containerTransparent}>
        <View style={styles.headerContainer}>
          <View style={styles.titleRow}>
            <Text style={styles.title}>Mi Avedex</Text>
            <View style={styles.statsContainer}>
              <Ionicons name="egg" size={18} color="#ff6b35" />
              <Text style={styles.statsText}>{birds.length} especies</Text>
            </View>
          </View>
          
          <View style={styles.sortContainer}>
            <Text style={styles.sortLabel}>Ordenar por:</Text>
            <View style={styles.sortButtons}>
              <TouchableOpacity 
                style={[styles.sortButton, sortBy === 'alphabetical' && styles.sortButtonActive]}
                onPress={() => setSortBy('alphabetical')}
              >
                <Ionicons name="text" size={16} color={sortBy === 'alphabetical' ? '#fff' : '#d2691e'} />
                <Text style={[styles.sortButtonText, sortBy === 'alphabetical' && styles.sortButtonTextActive]}>
                  A-Z
                </Text>
              </TouchableOpacity>
              
              <TouchableOpacity 
                style={[styles.sortButton, sortBy === 'date' && styles.sortButtonActive]}
                onPress={() => setSortBy('date')}
              >
                <Ionicons name="calendar" size={16} color={sortBy === 'date' ? '#fff' : '#d2691e'} />
                <Text style={[styles.sortButtonText, sortBy === 'date' && styles.sortButtonTextActive]}>
                  Fecha
                </Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      <ScrollView contentContainerStyle={styles.grid}>
        {sortedBirds.map((bird, index) => (
          <Animatable.View
            key={bird.id}
            animation={shouldAnimate && newBirdIds.has(bird.id) ? "slideInUp" : undefined}
            delay={shouldAnimate ? index * 100 : 0} // Retraso escalonado solo cuando se debe animar
            duration={500}
            useNativeDriver
          >
            <AvedexCard
              {...bird}
              onPress={() => router.push(`/avedex/${bird.id}`)}
            />
          </Animatable.View>
        ))}
      </ScrollView>
    </SafeAreaView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fffaf0',
  },
  containerTransparent: {
    flex: 1,
    backgroundColor: 'transparent',
  },
  backgroundDecor: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    overflow: 'hidden',
  },
  decorLeaf1: {
    position: 'absolute',
    top: -20,
    right: -30,
    transform: [{ rotate: '45deg' }],
  },
  decorLeaf2: {
    position: 'absolute',
    bottom: 100,
    left: -20,
    transform: [{ rotate: '-30deg' }],
  },
  decorLeaf3: {
    position: 'absolute',
    top: '40%',
    right: 20,
    transform: [{ rotate: '120deg' }],
  },
  decorSparkle: {
    position: 'absolute',
    top: '20%',
    left: 30,
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'transparent',
    padding: 20,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#d2691e',
    padding: 15,
  },
  headerContainer: {
    paddingHorizontal: 16,
    paddingTop: 12,
    paddingBottom: 8,
  },
  titleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 12,
    padding: 10,
  },
  statsContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
    gap: 6,
    shadowColor: '#d2691e',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.15,
    shadowRadius: 4,
    elevation: 3,
  },
  statsText: {
    fontSize: 14,
    fontWeight: '700',
    color: '#d2691e',
  },
  sortContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: 'rgba(255, 255, 255, 0.85)',
    paddingHorizontal: 14,
    paddingVertical: 10,
    borderRadius: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 2,
  },
  sortLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: '#666',
  },
  sortButtons: {
    flexDirection: 'row',
    gap: 8,
  },
  sortButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: '#d2691e',
    backgroundColor: '#fff',
    gap: 6,
  },
  sortButtonActive: {
    backgroundColor: '#d2691e',
    borderColor: '#ff6b35',
    shadowColor: '#d2691e',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
    elevation: 3,
  },
  sortButtonText: {
    fontSize: 13,
    fontWeight: '600',
    color: '#d2691e',
  },
  sortButtonTextActive: {
    color: '#fff',
  },
  grid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'center',
    padding: 8,
  },
  errorText: {
    fontSize: 16,
    color: 'red',
    textAlign: 'center',
  },
  
  // Empty state styles
  emptyMessageContainer: {
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 24,
    marginHorizontal: 16,
    marginBottom: 16,
    backgroundColor: '#fff',
    borderRadius: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  emptyTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#d2691e',
    marginTop: 16,
    marginBottom: 8,
    textAlign: 'center',
  },
  emptySubtitle: {
    fontSize: 15,
    color: '#666',
    textAlign: 'center',
    marginBottom: 20,
    lineHeight: 22,
  },
  emptyStepsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    width: '100%',
    marginTop: 8,
  },
  emptyStep: {
    alignItems: 'center',
    flex: 1,
    paddingHorizontal: 4,
  },
  emptyStepText: {
    fontSize: 12,
    color: '#666',
    marginTop: 8,
    textAlign: 'center',
    fontWeight: '500',
  },
  
  // Placeholder card styles
  placeholderCard: {
    width: CARD_WIDTH,
    backgroundColor: '#fff',
    borderRadius: 10,
    margin: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.08,
    shadowRadius: 3.84,
    elevation: 2,
    overflow: 'hidden',
    opacity: 0.6,
  },
  placeholderImage: {
    width: '100%',
    height: CARD_WIDTH,
    backgroundColor: '#f5f5f5',
    justifyContent: 'center',
    alignItems: 'center',
  },
  placeholderInfo: {
    padding: 10,
  },
  placeholderLine: {
    height: 12,
    backgroundColor: '#e0e0e0',
    borderRadius: 6,
    marginBottom: 8,
  },
  placeholderLineShort: {
    width: '70%',
  },
  placeholderLineTiny: {
    width: '50%',
    marginBottom: 12,
  },
});
