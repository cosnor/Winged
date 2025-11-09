import React from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { router } from 'expo-router';
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
        <View style={styles.emptyState}>
          <Text style={styles.emptyText}>No hay aves identificadas aún</Text>
        </View>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{title}</Text>
      <ScrollView style={styles.scrollView}>
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
    backgroundColor: '#fffaf0',
    padding: 0
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#d2691e',
    textAlign: 'center',
    marginVertical: 5,
  },
  scrollView: {
    flex: 1,
    width: '100%',
    marginTop: 20,
    borderWidth: 2,
    borderColor: 'transparent',
    borderTopColor: '#d2691e',
    padding: 10
  },
  emptyState: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 20,
  },
  emptyText: {
    color: '#666',
    fontSize: 16,
  },
});
