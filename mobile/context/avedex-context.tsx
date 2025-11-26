import React, { createContext, useContext, useReducer, useEffect } from 'react';
import AsyncStorage from "@react-native-async-storage/async-storage";
import { API_BASE_URL } from "../config/environment";
import type { AvedexBird } from '../components/cards/AvedexCard';

interface AvedexState {
  birds: AvedexBird[];
  loading: boolean;
  error: string | null;
  newBirdIds: Set<string>;
}

type AvedexAction = 
  | { type: 'ADD_BIRD'; payload: AvedexBird }
  | { type: 'SET_BIRDS'; payload: AvedexBird[] }
  | { type: 'UPDATE_BIRD'; payload: AvedexBird }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'MARK_BIRDS_AS_SEEN'; payload: string[] };

interface AvedexContextType extends AvedexState {
  addBird: (bird: Omit<AvedexBird, 'firstSeenDate'>) => Promise<void>;
  hasBird: (id: string) => boolean;
  markBirdsAsSeen: (birdIds: string[]) => void;
  refresh: () => Promise<void>;
  clearCollection: () => Promise<void>;
}

const AvedexContext = createContext<AvedexContextType | undefined>(undefined);

const initialState: AvedexState = {
  birds: [],
  loading: false,
  error: null,
  newBirdIds: new Set()
};

function avedexReducer(state: AvedexState, action: AvedexAction): AvedexState {
  switch (action.type) {
    case 'ADD_BIRD':
      const newBirdIds = new Set(state.newBirdIds);
      newBirdIds.add(action.payload.id);
      return {
        ...state,
        birds: [action.payload, ...state.birds],
        newBirdIds
      };
    case 'SET_BIRDS':
      return {
        ...state,
        birds: action.payload
      };
    case 'UPDATE_BIRD':
      return {
        ...state,
        birds: state.birds.map(bird => 
          bird.id === action.payload.id ? action.payload : bird
        )
      };
    case 'SET_LOADING':
      return {
        ...state,
        loading: action.payload
      };
    case 'SET_ERROR':
      return {
        ...state,
        error: action.payload
      };
    case 'MARK_BIRDS_AS_SEEN':
      const updatedNewBirdIds = new Set(state.newBirdIds);
      action.payload.forEach(id => updatedNewBirdIds.delete(id));
      return {
        ...state,
        newBirdIds: updatedNewBirdIds
      };
    default:
      return state;
  }
}

export function AvedexProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(avedexReducer, initialState);
  const [currentUserId, setCurrentUserId] = React.useState<string | null>(null);

  // Helper to get the storage key for current user
  const getStorageKey = async () => {
    const userInfoStr = await AsyncStorage.getItem('USER_INFO');
    if (userInfoStr) {
      const userInfo = JSON.parse(userInfoStr);
      const userId = userInfo.user_id || userInfo.id;
      return `AVEDEX_COLLECTION_${userId}`;
    }
    return null;
  };

  // Save birds to AsyncStorage whenever they change
  const saveBirdsToStorage = async (birds: AvedexBird[]) => {
    try {
      const storageKey = await getStorageKey();
      if (storageKey) {
        await AsyncStorage.setItem(storageKey, JSON.stringify(birds));
        console.log(`💾 Saved ${birds.length} birds to storage`);
      }
    } catch (err) {
      console.error('Error saving birds to storage:', err);
    }
  };

  // Load birds from AsyncStorage
  const loadBirdsFromStorage = async () => {
    try {
      const storageKey = await getStorageKey();
      if (storageKey) {
        const storedBirds = await AsyncStorage.getItem(storageKey);
        if (storedBirds) {
          const birds = JSON.parse(storedBirds);
          console.log(`💾 Loaded ${birds.length} birds from storage`);
          return birds;
        }
      }
    } catch (err) {
      console.error('Error loading birds from storage:', err);
    }
    return null;
  };

  // Auto-save birds to storage whenever state.birds changes
  useEffect(() => {
    if (state.birds.length > 0) {
      saveBirdsToStorage(state.birds);
    }
  }, [state.birds]);

  const fetchCollection = async () => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      const userInfoStr = await AsyncStorage.getItem('USER_INFO');
      const token = await AsyncStorage.getItem('ACCESS_TOKEN');
      
      if (userInfoStr && token) {
        const userInfo = JSON.parse(userInfoStr);
        const userId = userInfo.user_id || userInfo.id;
        
        console.log(`🔄 Fetching collection for user ${userId}`);
        const response = await fetch(`${API_BASE_URL}/achievements/users/${userId}/collection`, {
             headers: {
               'Authorization': `Bearer ${token}`
             }
        });
        
        console.log(`📥 Collection fetch response status: ${response.status}`);
        
        if (response.ok) {
            const data = await response.json();
            console.log(`📦 Received collection data:`, JSON.stringify(data, null, 2));
            console.log(`🐦 Birds in response: ${data.birds ? data.birds.length : 0}`);
            
            // data.birds is the list
            // Use a Map to deduplicate by species_name (keep first occurrence)
            const birdsMap = new Map();
            (data.birds || []).forEach((b: any) => {
                const speciesName = b.species_name;
                console.log(`🔍 Processing bird from backend:`, {
                  species_name: b.species_name,
                  common_name: b.common_name,
                  first_sighted_at: b.first_sighted_at
                });
                if (!birdsMap.has(speciesName)) {
                    birdsMap.set(speciesName, {
                        id: speciesName, 
                        commonName: b.common_name || speciesName,
                        scientificName: speciesName,
                        imageUrl: b.image_url || 'https://via.placeholder.com/150',
                        firstSeenDate: b.first_sighted_at 
                          ? new Date(b.first_sighted_at).toLocaleDateString('es-ES', { day: '2-digit', month: 'short', year: 'numeric' })
                          : new Date().toLocaleDateString('es-ES', { day: '2-digit', month: 'short', year: 'numeric' }),
                        isNew: false 
                    });
                }
            });
            
            const birds = Array.from(birdsMap.values());
            console.log(`✅ Processed ${birds.length} unique birds`);
            console.log(`🐦 Sample bird data:`, birds.length > 0 ? birds[0] : 'none');
            dispatch({ type: 'SET_BIRDS', payload: birds });
            await saveBirdsToStorage(birds);
        } else {
            const errorText = await response.text();
            console.error(`❌ Failed to fetch collection: ${response.status}`, errorText);
            // If API fails, try to load from storage as fallback
            const storedBirds = await loadBirdsFromStorage();
            if (storedBirds) {
              console.log(`💾 Loaded ${storedBirds.length} birds from local storage`);
              dispatch({ type: 'SET_BIRDS', payload: storedBirds });
            }
        }
      } else {
        console.log('⚠️ No user logged in, loading from storage');
        const storedBirds = await loadBirdsFromStorage();
        if (storedBirds) {
          console.log(`💾 Loaded ${storedBirds.length} birds from storage (no auth)`);
          dispatch({ type: 'SET_BIRDS', payload: storedBirds });
        }
      }
    } catch (err) {
      console.error('❌ Error fetching collection:', err);
      dispatch({ type: 'SET_ERROR', payload: err instanceof Error ? err.message : 'Error al cargar colección' });
      const storedBirds = await loadBirdsFromStorage();
      if (storedBirds) {
        console.log(`💾 Loaded ${storedBirds.length} birds from storage (error fallback)`);
        dispatch({ type: 'SET_BIRDS', payload: storedBirds });
      }
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  useEffect(() => {
    fetchCollection();
  }, []);

  // Monitor user changes and reload collection when user logs in
  useEffect(() => {
    const checkUserChange = async () => {
      const userInfoStr = await AsyncStorage.getItem('USER_INFO');
      if (userInfoStr) {
        const userInfo = JSON.parse(userInfoStr);
        const userId = userInfo.user_id || userInfo.id;
        
        if (userId && userId !== currentUserId) {
          console.log(`👤 User changed from ${currentUserId} to ${userId}, reloading collection...`);
          setCurrentUserId(userId);
          await fetchCollection();
        }
      } else if (currentUserId !== null) {
        console.log('👤 User logged out, clearing collection...');
        setCurrentUserId(null);
        dispatch({ type: 'SET_BIRDS', payload: [] });
      }
    };

    checkUserChange();
    const interval = setInterval(checkUserChange, 1000);
    
    return () => clearInterval(interval);
  }, [currentUserId]);

  const addBird = async (bird: Omit<AvedexBird, 'firstSeenDate'>) => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      dispatch({ type: 'SET_ERROR', payload: null });

      console.log(`🔍 Attempting to add bird: ${bird.id} (${bird.commonName})`);
      console.log(`📊 Current collection size: ${state.birds.length}`);

      // Check if bird already exists to prevent duplicates
      if (state.birds.some(b => b.id === bird.id)) {
        console.log(`⚠️ Bird ${bird.id} already exists in collection, skipping`);
        return;
      }

      // Get user info and token for backend call
      const userInfoStr = await AsyncStorage.getItem('USER_INFO');
      const token = await AsyncStorage.getItem('ACCESS_TOKEN');
      
      console.log(`🔑 Auth status - Token: ${token ? 'present' : 'missing'}, UserInfo: ${userInfoStr ? 'present' : 'missing'}`);

      if (userInfoStr && token) {
        const userInfo = JSON.parse(userInfoStr);
        const userId = userInfo.user_id || userInfo.id;

        // Create a sighting with only scientific name and common name
        try {
          const sightingPayload = {
            user_id: userId,
            species_name: bird.scientificName,  // Scientific name
            common_name: bird.commonName,       // Common name
            timestamp: new Date().toISOString(),
          };

          console.log(`📤 Creating sighting:`, JSON.stringify(sightingPayload, null, 2));
          const response = await fetch(`${API_BASE_URL}/sightings/`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify(sightingPayload),
          });

          console.log(`📥 Response status: ${response.status}`);

          if (response.ok) {
            const responseData = await response.json();
            console.log(`✅ Sighting created successfully for ${bird.commonName}`, responseData);
            
            console.log('🔄 Refreshing collection from backend...');
            await fetchCollection();
            return;
          } else {
            const errorText = await response.text();
            console.error(`❌ Failed to create sighting: ${response.status}`, errorText);
          }
        } catch (apiError) {
          console.error('❌ Error calling sightings API:', apiError);
        }
      }

      // Fallback: Add locally if backend call failed or no auth
      console.log('💾 Adding bird locally as fallback...');
      const newBird: AvedexBird = {
        ...bird,
        firstSeenDate: new Date().toLocaleDateString('es-ES', { day: '2-digit', month: 'short', year: 'numeric' }),
        isNew: true
      };

      dispatch({ type: 'ADD_BIRD', payload: newBird });
      
      const updatedBirds = [newBird, ...state.birds];
      await saveBirdsToStorage(updatedBirds);
      console.log(`✅ Bird added locally. Collection size: ${updatedBirds.length}`);
    } catch (err) {
      console.error('❌ Error in addBird:', err);
      dispatch({ type: 'SET_ERROR', payload: err instanceof Error ? err.message : 'Error al añadir el ave' });
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const hasBird = (id: string) => {
    return state.birds.some((bird: AvedexBird) => bird.id === id);
  };

  const markBirdsAsSeen = (birdIds: string[]) => {
    dispatch({ type: 'MARK_BIRDS_AS_SEEN', payload: birdIds });
  };

  const clearCollection = async () => {
    try {
      const storageKey = await getStorageKey();
      if (storageKey) {
        await AsyncStorage.removeItem(storageKey);
        console.log('🗑️ Cleared collection from storage');
      }
      dispatch({ type: 'SET_BIRDS', payload: [] });
      dispatch({ type: 'MARK_BIRDS_AS_SEEN', payload: Array.from(state.newBirdIds) });
    } catch (err) {
      console.error('Error clearing collection:', err);
    }
  };

  return (
    <AvedexContext.Provider value={{
      birds: state.birds,
      loading: state.loading,
      error: state.error,
      newBirdIds: state.newBirdIds,
      addBird,
      hasBird,
      markBirdsAsSeen,
      refresh: fetchCollection,
      clearCollection
    }}>
      {children}
    </AvedexContext.Provider>
  );
}

export function useAvedex() {
  const context = useContext(AvedexContext);
  if (context === undefined) {
    throw new Error('useAvedex must be used within an AvedexProvider');
  }
  return context;
}