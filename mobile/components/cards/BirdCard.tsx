import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { useAvedex } from '../../context/avedex-context';
import { useBirdDetections } from '../../context/bird-detection-context';
import { router } from 'expo-router';
import * as Animatable from 'react-native-animatable';

interface BirdCardProps {
  id: string;
  commonName: string;
  scientificName: string;
  imageUrl: string;
}

export default function BirdCard({ id, commonName, scientificName, imageUrl }: BirdCardProps) {
  const { hasBird, addBird, birds } = useAvedex();
  const { removeBird } = useBirdDetections();
  const [isInAvedex, setIsInAvedex] = useState(hasBird(id));

  // Update isInAvedex when birds collection changes
  useEffect(() => {
    setIsInAvedex(hasBird(id));
  }, [birds, id]);

  const handleAvedexPress = () => {
    if (!isInAvedex) {
      addBird({
        id,
        commonName,
        scientificName,
        imageUrl,
      });
    } else {
      router.push(`/avedex/${id}`);
    }
  };

  const [isAdding, setIsAdding] = useState(false);

  const handleAddBird = async () => {
    if (isInAvedex) {
      console.log(`⚠️ Bird ${id} already in Avedex, skipping`);
      return;
    }
    
    setIsAdding(true);
    try {
      await addBird({id, commonName, scientificName, imageUrl});
      // Update local state immediately
      setIsInAvedex(true);
      console.log(`✅ Bird ${id} added to Avedex, button hidden`);
      
      // Remove from detections list after successful add
      setTimeout(() => {
        removeBird(id);
        console.log(`🗑️ Bird ${id} removed from detections list`);
      }, 1000); // Wait 1 second to show the success state
      
      // La animación durará 500ms
      await new Promise(resolve => setTimeout(resolve, 500));
    } catch (error) {
      console.error(`❌ Error adding bird ${id}:`, error);
    } finally {
      setIsAdding(false);
    }
  };

  return (
    <Animatable.View 
      animation={isAdding ? "pulse" : undefined}
      style={styles.card}
    >
      <View style={styles.nameContainer}>
        <Text style={styles.commonName}>{commonName}</Text>
        <Text style={styles.scientificName}>{scientificName}</Text>
        {!isInAvedex && <Text style={styles.newBadge}>Nueva</Text>}
      </View>
      {!isInAvedex ? (
        <TouchableOpacity 
          style={[styles.avedexButton, isAdding && styles.avedexButtonDisabled]}
          onPress={handleAddBird}
          disabled={isAdding}
        >
          <Text style={styles.avedexButtonText}>
            {isAdding ? 'Agregando...' : 'Agregar a avedex'}
          </Text>
        </TouchableOpacity>
      ) : (
        <View style={styles.inAvedexContainer}>
          <Text style={styles.inAvedexText}>✓ Ya en Avedex</Text>
        </View>
      )}
    </Animatable.View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#fff',
    borderRadius: 10,
    padding: 15,
    marginVertical: 8,
    marginHorizontal: 16,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  nameContainer: {
    marginBottom: 10,
  },
  commonName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#d2691e',
  },
  scientificName: {
    fontSize: 14,
    fontStyle: 'italic',
    color: '#666',
    marginTop: 2,
  },
  newBadge: {
    position: 'absolute',
    right: 0,
    top: 0,
    backgroundColor: '#90EE90',
    padding: 4,
    borderRadius: 4,
    fontSize: 12,
    fontWeight: 'bold',
    color: '#006400',
  },
  avedexButton: {
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#d2691e',
    padding: 8,
    borderRadius: 5,
    alignItems: 'center',
  },
  avedexButtonText: {
    color: '#d2691e',
    fontSize: 14,
    fontWeight: '500',
  },
  avedexButtonDisabled: {
    backgroundColor: '#f0f0f0',
    borderColor: '#ccc',
  },
  inAvedexContainer: {
    backgroundColor: '#e8f5e9',
    padding: 8,
    borderRadius: 5,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#4caf50',
  },
  inAvedexText: {
    color: '#2e7d32',
    fontSize: 14,
    fontWeight: '500',
  },
});