import React from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { router } from 'expo-router';
import Ionicons from '@expo/vector-icons/Ionicons';
import * as Animatable from 'react-native-animatable';
import BirdCard from '../cards/BirdCard';

export interface Bird {
  id: string;
  commonName: string;
  scientificName: string;
  imageUrl: string;
}

interface BirdRegistryProps {
  birds: Bird[];
  title?: string;
}

export default function BirdRegistry({ birds, title = "Registro de Identificaciones" }: BirdRegistryProps) {
  if (birds.length === 0) {
    return (
      <View style={styles.container}>
        <Text style={styles.title}>{title}</Text>
        <Animatable.View 
          animation="fadeIn" 
          duration={800}
          style={styles.emptyState}
        >
          <Animatable.View
            animation="pulse"
            iterationCount="infinite"
            duration={2000}
            style={styles.emptyIconContainer}
          >
            <Ionicons name="musical-notes-outline" size={60} color="#d2691e" />
          </Animatable.View>
          <Text style={styles.emptyTitle}>Aún no hay identificaciones</Text>
          <Text style={styles.emptySubtext}>
            Sube o graba el canto de un ave para comenzar
          </Text>
          <View style={styles.emptyStepsContainer}>
            <View style={styles.emptyStep}>
              <Ionicons name="cloud-upload" size={24} color="#ff9a41" />
              <Text style={styles.emptyStepText}>Sube audio</Text>
            </View>
            <View style={styles.emptyStep}>
              <Ionicons name="scan" size={24} color="#ff9a41" />
              <Text style={styles.emptyStepText}>Analiza</Text>
            </View>
            <View style={styles.emptyStep}>
              <Ionicons name="checkmark-circle" size={24} color="#ff9a41" />
              <Text style={styles.emptyStepText}>Identifica</Text>
            </View>
          </View>
        </Animatable.View>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{title}</Text>
      <ScrollView 
        style={styles.scrollView}
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={true}
        nestedScrollEnabled={true}
      >
        {birds.map((bird) => (
          <BirdCard
            key={bird.id}
            id={bird.id}
            commonName={bird.commonName}
            scientificName={bird.scientificName}
            imageUrl={bird.imageUrl}
          />
        ))}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    width: '100%',
    backgroundColor: 'transparent',
    paddingHorizontal: 20,
  },
  title: {
    fontSize: 22,
    fontWeight: '800',
    color: '#d2691e',
    textAlign: 'center',
    marginVertical: 16,
  },
  scrollView: {
    flex: 1,
    width: '100%',
    borderTopWidth: 2,
    borderTopColor: '#ff9a41',
    paddingTop: 16,
  },
  scrollContent: {
    paddingBottom: 20,
  },
  emptyState: {
    alignItems: 'center',
    paddingVertical: 40,
    paddingHorizontal: 20,
  },
  emptyIconContainer: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: 'rgba(255, 154, 65, 0.1)',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 24,
    borderWidth: 3,
    borderColor: 'rgba(255, 154, 65, 0.3)',
    borderStyle: 'dashed',
  },
  emptyTitle: {
    fontSize: 20,
    fontWeight: '700',
    color: '#d2691e',
    marginBottom: 8,
    textAlign: 'center',
  },
  emptySubtext: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
    marginBottom: 28,
    lineHeight: 20,
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
    paddingHorizontal: 8,
  },
  emptyStepText: {
    fontSize: 12,
    color: '#666',
    marginTop: 8,
    textAlign: 'center',
    fontWeight: '600',
  },
});
