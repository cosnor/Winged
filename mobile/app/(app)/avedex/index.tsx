import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, ActivityIndicator } from 'react-native';
import { useAvedex } from '../../../context/avedex-context';
import AvedexCard from '../../../components/cards/AvedexCard';
import { router, useNavigation } from 'expo-router';
import * as Animatable from 'react-native-animatable';

export default function AvedexScreen() {
  const { birds, loading, error, newBirdIds, markBirdsAsSeen } = useAvedex();
  const [shouldAnimate, setShouldAnimate] = useState(false);
  const navigation = useNavigation();

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
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#d2691e" />
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.centerContainer}>
        <Text style={styles.errorText}>{error}</Text>
      </View>
    );
  }

  if (birds.length === 0) {
    return (
      <View style={styles.centerContainer}>
        <Text style={styles.emptyText}>
          Tu avedex está vacío. ¡Comienza a identificar aves!
        </Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Avedex de Carlos</Text>
      <ScrollView contentContainerStyle={styles.grid}>
        {birds.map((bird, index) => (
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
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fffaf0',
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fffaf0',
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#d2691e',
    textAlign: 'center',
    padding: 16,
  },
  grid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'center',
    padding: 8,
  },
  emptyText: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
  },
  errorText: {
    fontSize: 16,
    color: 'red',
    textAlign: 'center',
  },
});
