import { Tabs } from "expo-router";
import Ionicons from '@expo/vector-icons/Ionicons';
import { useAuth } from "../../context/auth-context";
import { Platform } from 'react-native';

export default function BottomTabs() {
  // const { user } = useAuth();

  // if (!user) return null; // No mostrar tabs si no hay auth

  return (
    <Tabs 
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: '#ff9a41',
        tabBarInactiveTintColor: '#8b4513',
        tabBarStyle: {
          backgroundColor: '#fffaf0',
          borderTopWidth: 0,
          elevation: 20,
          shadowColor: '#d2691e',
          shadowOffset: { width: 0, height: -4 },
          shadowOpacity: 0.15,
          shadowRadius: 12,
          height: Platform.OS === 'ios' ? 88 : 65,
          paddingBottom: Platform.OS === 'ios' ? 24 : 8,
          paddingTop: 8,
          paddingHorizontal: 10,
        },
        tabBarLabelStyle: {
          fontSize: 11,
          fontWeight: '600',
          marginTop: -2,
        },
        tabBarIconStyle: {
          marginTop: 4,
        },
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: "Inicio",
          tabBarIcon: ({ color, size, focused }) => (
            <Ionicons 
              name={focused ? "home" : "home-outline"} 
              size={focused ? size + 2 : size} 
              color={color} 
            />
          )
        }}
      />
      <Tabs.Screen
        name="identify/record"
        options={{
          title: "Grabar",
          tabBarIcon: ({ color, size, focused }) => (
            <Ionicons 
              name={focused ? "mic" : "mic-outline"} 
              size={focused ? size + 2 : size} 
              color={color} 
            />
          )
        }}
      />
      <Tabs.Screen
        name="identify/audioupload"
        options={{
          title: "Identificar",
          tabBarIcon: ({ color, size, focused }) => (
            <Ionicons 
              name={focused ? "cloud-upload" : "cloud-upload-outline"} 
              size={focused ? size + 2 : size} 
              color={color} 
            />
          )
        }}
      />
      <Tabs.Screen
        name="avedex/index"
        options={{
          title: "Avedex",
          tabBarIcon: ({ color, size, focused }) => (
            <Ionicons 
              name={focused ? "albums" : "albums-outline"} 
              size={focused ? size + 2 : size} 
              color={color} 
            />
          )
        }}
      />
      <Tabs.Screen
        name="map"
        options={{
          title: "Mapa",
          tabBarIcon: ({ color, size, focused }) => (
            <Ionicons 
              name={focused ? "map" : "map-outline"} 
              size={focused ? size + 2 : size} 
              color={color} 
            />
          )
        }}
      />
      <Tabs.Screen
        name="profile/index"
        options={{
          title: "Perfil",
          tabBarIcon: ({ color, size, focused }) => (
            <Ionicons 
              name={focused ? "person" : "person-outline"} 
              size={focused ? size + 2 : size} 
              color={color} 
            />
          )
        }}
      />
    </Tabs>
  );
}