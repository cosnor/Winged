import { Tabs, Stack } from 'expo-router';

export default function MapLayout() {
  return (
    <Stack
      screenOptions={{
        headerStyle: {
          backgroundColor: '#d2691e',
        },
        headerTintColor: '#fff',
        headerTitleStyle: {
          fontWeight: 'bold',
        },
        headerBackTitle: 'Atrás',
      }}
    >
      <Stack.Screen 
        name="index"
        options={{
          headerShown: false,
          // Esto asegura que esta pantalla aparezca en los tabs
          presentation: 'modal',
        }}
      />
      <Stack.Screen 
        name="nearby/index"
        options={{
          title: 'Aves Cerca de ti',
          presentation: 'card',
        }}
      />
      <Stack.Screen 
        name="zones/index"
        options={{
          title: 'Aves por Zona',
          presentation: 'card',
        }}
      />
      <Stack.Screen 
        name="routes/index"
        options={{
          title: 'Rutas de Aves',
          presentation: 'card',
        }}
      />
    </Stack>
  );
}