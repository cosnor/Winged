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
  addBird: (bird: Omit<AvedexBird, 'firstSeenDate'>) => void;
  hasBird: (id: string) => boolean;
  markBirdsAsSeen: (birdIds: string[]) => void;
  refresh: () => Promise<void>;
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

  const fetchCollection = async () => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      const userInfoStr = await AsyncStorage.getItem('USER_INFO');
      const token = await AsyncStorage.getItem('ACCESS_TOKEN');
      
      if (userInfoStr && token) {
        const userInfo = JSON.parse(userInfoStr);
        const userId = userInfo.user_id || userInfo.id;
        
        console.log(`Fetching collection for user ${userId}`);
        const response = await fetch(`${API_BASE_URL}/achievements/users/${userId}/collection`, {
             headers: {
               'Authorization': `Bearer ${token}`
             }
        });
        
        if (response.ok) {
            const data = await response.json();
            // data.birds is the list
            const birds = (data.birds || []).map((b: any) => ({
                id: b.species_name, 
                commonName: b.common_name || b.species_name,
                scientificName: b.species_name,
                imageUrl: b.image_url || 'https://via.placeholder.com/150', // Fallback image
                firstSeenDate: b.first_seen_at || new Date().toLocaleDateString(),
                isNew: false 
            }));
            
            dispatch({ type: 'SET_BIRDS', payload: birds });
        } else {
            console.error('Failed to fetch collection:', response.status);
        }
      }
    } catch (err) {
      console.error('Error fetching collection:', err);
      dispatch({ type: 'SET_ERROR', payload: err instanceof Error ? err.message : 'Error al cargar colección' });
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  useEffect(() => {
    fetchCollection();
  }, []);

  const addBird = (bird: Omit<AvedexBird, 'firstSeenDate'>) => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      dispatch({ type: 'SET_ERROR', payload: null });

      const newBird: AvedexBird = {
        ...bird,
        firstSeenDate: new Date().toLocaleDateString(),
        isNew: true
      };

      dispatch({ type: 'ADD_BIRD', payload: newBird });
    } catch (err) {
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

  return (
    <AvedexContext.Provider value={{ ...state, addBird, hasBird, markBirdsAsSeen, refresh: fetchCollection }}>
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