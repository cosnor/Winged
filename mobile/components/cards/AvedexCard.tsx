import React from 'react';
import { View, Text, StyleSheet, Image, TouchableOpacity, Dimensions } from 'react-native';
import { router } from 'expo-router';
import * as Animatable from 'react-native-animatable';

export interface AvedexBird {
  id: string;
  commonName: string;
  scientificName: string;
  firstSeenDate: string;
  imageUrl: string;
  isNew?: boolean;
}

interface AvedexCardProps extends AvedexBird {
  onPress: () => void;
}

const CARD_WIDTH = (Dimensions.get('window').width - 48) / 2; // 2 cards por fila con padding

export default function AvedexCard({ 
  id, 
  commonName, 
  scientificName, 
  firstSeenDate, 
  imageUrl,
  isNew,
  onPress 
}: AvedexCardProps) {
  const CardWrapper = isNew ? Animatable.View : View;
  const wrapperProps = isNew ? {
    animation: "bounceIn",
    duration: 1500,
  } : {};

  return (
    <CardWrapper style={styles.card} {...wrapperProps}>
      <TouchableOpacity onPress={onPress} style={styles.touchable}>
        <Image 
          source={{ uri: imageUrl }}
          style={styles.image}
          resizeMode="cover"
        />
        <View style={styles.infoContainer}>
          <Text style={styles.commonName} numberOfLines={1}>
            {commonName}
          </Text>
          <Text style={styles.scientificName} numberOfLines={1}>
            {scientificName}
          </Text>
          <Text style={styles.date}>
            Primer avistamiento: {firstSeenDate}
          </Text>
          <TouchableOpacity style={styles.button}>
            <Text style={styles.buttonText}>Ver más</Text>
          </TouchableOpacity>
        </View>
      </TouchableOpacity>
    </CardWrapper>
  );
}

const styles = StyleSheet.create({
  card: {
    width: CARD_WIDTH,
    backgroundColor: '#fff',
    borderRadius: 10,
    margin: 8,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
    overflow: 'hidden',
  },
  touchable: {
    flex: 1,
  },
  image: {
    width: '100%',
    height: CARD_WIDTH, // Imagen cuadrada
    backgroundColor: '#f0f0f0', // Color placeholder
  },
  infoContainer: {
    padding: 10,
  },
  commonName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#d2691e',
  },
  scientificName: {
    fontSize: 12,
    fontStyle: 'italic',
    color: '#666',
    marginBottom: 4,
  },
  date: {
    fontSize: 11,
    color: '#888',
    marginBottom: 8,
  },
  button: {
    backgroundColor: '#d2691e',
    padding: 6,
    borderRadius: 5,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '500',
  },
});