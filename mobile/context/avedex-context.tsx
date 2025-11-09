import React, { createContext, useContext, useReducer } from 'react';
import type { AvedexBird } from '../components/cards/AvedexCard';

interface AvedexState {
  birds: AvedexBird[];
  loading: boolean;
  error: string | null;
  newBirdIds: Set<string>;
}

type AvedexAction = 
  | { type: 'ADD_BIRD'; payload: AvedexBird }
  | { type: 'UPDATE_BIRD'; payload: AvedexBird }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'MARK_BIRDS_AS_SEEN'; payload: string[] };

interface AvedexContextType extends AvedexState {
  addBird: (bird: Omit<AvedexBird, 'firstSeenDate'>) => void;
  hasBird: (id: string) => boolean;
  markBirdsAsSeen: (birdIds: string[]) => void;
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
    <AvedexContext.Provider value={{
      birds: state.birds,
      loading: state.loading,
      error: state.error,
      newBirdIds: state.newBirdIds,
      addBird,
      hasBird,
      markBirdsAsSeen
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