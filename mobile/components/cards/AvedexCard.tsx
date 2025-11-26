import React, { useState } from 'react';
import { View, Text, StyleSheet, Image, TouchableOpacity, Dimensions, Modal } from 'react-native';
import { router } from 'expo-router';
import * as Animatable from 'react-native-animatable';
import { LinearGradient } from 'expo-linear-gradient';
import Ionicons from '@expo/vector-icons/Ionicons';

const SCREEN_WIDTH = Dimensions.get('window').width;
const SCREEN_HEIGHT = Dimensions.get('window').height;

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
  const [showModal, setShowModal] = useState(false);
  const [wikiImage, setWikiImage] = useState<string | null>(null);
  const [loadingImage, setLoadingImage] = useState(false);

  // Fetch Wikipedia image
  React.useEffect(() => {
    const fetchWikipediaImage = async () => {
      try {
        setLoadingImage(true);
        // Normalizar el nombre: reemplazar espacios por guiones bajos
        const searchName = commonName.replace(/ /g, '_');
        const url = `https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(searchName)}`;
        
        const response = await fetch(url);
        if (response.ok) {
          const data = await response.json();
          // La imagen viene en data.thumbnail.source o data.originalimage.source
          if (data.thumbnail?.source) {
            setWikiImage(data.thumbnail.source);
          } else if (data.originalimage?.source) {
            setWikiImage(data.originalimage.source);
          }
        }
      } catch (error) {
        console.log('Error fetching Wikipedia image:', error);
      } finally {
        setLoadingImage(false);
      }
    };

    fetchWikipediaImage();
  }, [commonName]);

  const handleCardPress = () => {
    setShowModal(true);
  };

  const handleClose = () => {
    setShowModal(false);
  };

  // Usar imagen de Wikipedia si está disponible, sino usar la original
  const displayImage = wikiImage || imageUrl;


  return (
    <>
      <Animatable.View 
        style={styles.card}
        animation={isNew ? "tada" : "fadeInUp"}
        duration={isNew ? 1200 : 500}
        iterationCount={isNew ? 2 : 1}
      >
        <TouchableOpacity onPress={handleCardPress} style={styles.touchable} activeOpacity={0.9}>
        {/* Imagen con overlay gradiente */}
        <View style={styles.imageContainer}>
          <Image 
            source={{ uri: displayImage }}
            style={styles.image}
            resizeMode="cover"
          />
          {/* Overlay oscuro en la parte inferior */}
          <LinearGradient
            colors={['transparent', 'rgba(0,0,0,0.6)']}
            style={styles.imageOverlay}
          />
          
          {/* Badge NEW con animación */}
          {isNew && (
            <Animatable.View 
              animation="pulse"
              iterationCount="infinite"
              duration={1500}
              style={styles.newBadge}
            >
              <Ionicons name="sparkles" size={12} color="#fff" />
              <Text style={styles.newBadgeText}>NUEVO</Text>
            </Animatable.View>
          )}
          
          {/* Indicador de tap */}
          <View style={styles.tapIndicator}>
            <Ionicons name="hand-left-outline" size={18} color="#fff" />
          </View>
        </View>
        
        {/* Info Container */}
        <View style={styles.infoContainer}>
          <View style={styles.infoHeader}>
            <View style={styles.decorLine} />
            <Ionicons name="chevron-forward" size={16} color="#ff9a41" />
          </View>
          
          <Text style={styles.commonName} numberOfLines={1}>
            {commonName}
          </Text>
          <Text style={styles.scientificName} numberOfLines={1}>
            {scientificName}
          </Text>
          
          <View style={styles.dateContainer}>
            <Ionicons name="calendar-outline" size={11} color="#d2691e" />
            <Text style={styles.date}>
              {firstSeenDate}
            </Text>
          </View>
        </View>
      </TouchableOpacity>
    </Animatable.View>

    {/* Modal con la card en grande y movible */}
    <Modal
      visible={showModal}
      transparent={true}
      animationType="fade"
      onRequestClose={handleClose}
    >
      <View style={styles.modalOverlay}>
        <View style={styles.modalBackground}>
          <TouchableOpacity 
            style={styles.closeButton}
            onPress={handleClose}
          >
            <Ionicons name="close-circle" size={36} color="#fff" />
          </TouchableOpacity>
        </View>

        <Animatable.View
          animation="zoomIn"
          duration={400}
          style={styles.modalCard}
        >
          <View style={styles.imageContainer}>
            <Image 
              source={{ uri: displayImage }}
              style={styles.modalImage}
              resizeMode="cover"
            />
            <LinearGradient
              colors={['transparent', 'rgba(0,0,0,0.6)']}
              style={styles.imageOverlay}
            />
            
            {isNew && (
              <Animatable.View 
                animation="pulse"
                iterationCount="infinite"
                duration={1500}
                style={styles.newBadgeLarge}
              >
                <Ionicons name="sparkles" size={16} color="#fff" />
                <Text style={styles.newBadgeTextLarge}>NUEVO</Text>
              </Animatable.View>
            )}
          </View>
          
          <LinearGradient
            colors={['#fff', '#fffaf0']}
            style={styles.modalInfoContainer}
          >
            <View style={styles.infoHeader}>
              <View style={styles.decorLineLarge} />
              <Ionicons name="chevron-forward" size={20} color="#ff9a41" />
            </View>
            
            <Text style={styles.modalCommonName}>
              {commonName}
            </Text>
            <Text style={styles.modalScientificName}>
              {scientificName}
            </Text>
            
            <View style={styles.modalDateContainer}>
              <Ionicons name="calendar-outline" size={14} color="#d2691e" />
              <Text style={styles.modalDate}>
                Primer avistamiento: {firstSeenDate}
              </Text>
            </View>
          </LinearGradient>
        </Animatable.View>
      </View>
    </Modal>
    </>
  );
}

const styles = StyleSheet.create({
  card: {
    width: CARD_WIDTH,
    backgroundColor: '#fff',
    borderRadius: 16,
    margin: 8,
    shadowColor: '#ff6b35',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 6,
    overflow: 'hidden',
    borderWidth: 3,
    borderColor: '#ff9a41',
  },
  touchable: {
    flex: 1,
  },
  imageContainer: {
    position: 'relative',
  },
  image: {
    width: '100%',
    height: CARD_WIDTH,
    backgroundColor: '#f5f5f5',
  },
  imageOverlay: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    height: '40%',
  },
  newBadge: {
    position: 'absolute',
    top: 10,
    right: 10,
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#ff6b35',
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 20,
    gap: 4,
    shadowColor: '#ff6b35',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.5,
    shadowRadius: 4,
    elevation: 4,
  },
  newBadgeText: {
    color: '#fff',
    fontSize: 10,
    fontWeight: 'bold',
    letterSpacing: 0.5,
  },
  tapIndicator: {
    position: 'absolute',
    bottom: 10,
    right: 10,
    backgroundColor: 'rgba(210, 105, 30, 0.8)',
    borderRadius: 20,
    padding: 6,
    shadowColor: '#d2691e',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.4,
    shadowRadius: 3,
  },
  infoContainer: {
    padding: 12,
    backgroundColor: '#fff',
  },
  infoHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 6,
  },
  decorLine: {
    height: 3,
    width: 30,
    backgroundColor: '#ff9a41',
    borderRadius: 2,
  },
  commonName: {
    fontSize: 15,
    fontWeight: 'bold',
    color: '#d2691e',
    marginBottom: 3,
  },
  scientificName: {
    fontSize: 11,
    fontStyle: 'italic',
    color: '#888',
    marginBottom: 8,
  },
  dateContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 5,
  },
  date: {
    fontSize: 10,
    color: '#999',
    fontWeight: '500',
  },
  
  // Modal styles
  modalOverlay: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalBackground: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.85)',
  },
  closeButton: {
    position: 'absolute',
    top: 50,
    right: 20,
    zIndex: 1000,
    shadowColor: '#fff',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.5,
    shadowRadius: 4,
  },
  modalCard: {
    width: SCREEN_WIDTH * 0.85,
    backgroundColor: '#fff',
    borderRadius: 24,
    overflow: 'hidden',
    shadowColor: '#d2691e',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.5,
    shadowRadius: 16,
    elevation: 10,
    borderWidth: 3,
    borderColor: '#ff9a41',
  },
  modalImage: {
    width: '100%',
    height: SCREEN_WIDTH * 0.85,
  },
  newBadgeLarge: {
    position: 'absolute',
    top: 60,
    right: 16,
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#ff6b35',
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 24,
    gap: 6,
    shadowColor: '#ff6b35',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.6,
    shadowRadius: 5,
    elevation: 5,
  },
  newBadgeTextLarge: {
    color: '#fff',
    fontSize: 13,
    fontWeight: 'bold',
    letterSpacing: 0.8,
  },
  modalInfoContainer: {
    padding: 20,
  },
  decorLineLarge: {
    height: 4,
    width: 50,
    backgroundColor: '#ff9a41',
    borderRadius: 2,
  },
  modalCommonName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#d2691e',
    marginBottom: 6,
    marginTop: 12,
  },
  modalScientificName: {
    fontSize: 16,
    fontStyle: 'italic',
    color: '#888',
    marginBottom: 16,
  },
  modalDateContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 20,
  },
  modalDate: {
    fontSize: 14,
    color: '#666',
    fontWeight: '500',
  },
  viewDetailsHint: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 10,
    gap: 6,
    borderTopWidth: 1,
    borderTopColor: '#f0f0f0',
    marginTop: 12,
    paddingTop: 12,
  },
  viewDetailsText: {
    color: '#d2691e',
    fontSize: 13,
    fontWeight: '500',
  },
});