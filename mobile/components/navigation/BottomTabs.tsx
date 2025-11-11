import { Tabs } from "expo-router";
import Ionicons from '@expo/vector-icons/Ionicons';
import { useAuth } from "../../context/auth-context";

export default function BottomTabs() {
  // const { user } = useAuth();

  // if (!user) return null; // No mostrar tabs si no hay auth

  return (
    <Tabs screenOptions={{headerShown: false}}>
      <Tabs.Screen
        name="index"
        options={{
          title: "Inicio",
          tabBarIcon: ({ color, size }) => <Ionicons name="home" size={size} color={color} />
        }}
      />
      <Tabs.Screen
        name="identify/record"
        options={{
          title: "Grabar",
          tabBarIcon: ({ color, size }) => <Ionicons name="mic" size={size} color={color} />
        }}
      />
      <Tabs.Screen
        name="identify/audioupload"
        options={{
          title: "Identificar",
          tabBarIcon: ({ color, size }) => <Ionicons name="cloud-upload" size={size} color={color} />
        }}
      />
      <Tabs.Screen
        name="avedex/index"
        options={{
          title: "Avedex",
          tabBarIcon: ({ color, size }) => <Ionicons name="albums" size={size} color={color} />
        }}
      />
      <Tabs.Screen
        name="map"
        options={{
          title: "Mapa",
          tabBarIcon: ({ color, size }) => <Ionicons name="map" size={size} color={color} />
        }}
      />
      <Tabs.Screen
        name="profile/index"
        options={{
          title: "Perfil",
          tabBarIcon: ({ color, size }) => <Ionicons name="person" size={size} color={color} />
        }}
      />
    </Tabs>
  );
}