// app.config.js - Configuración dinámica de Expo con variables de entorno
require('dotenv').config();

module.exports = {
  expo: {
    name: "mobile",
    slug: "mobile",
    version: "1.0.0",
    orientation: "portrait",
    icon: "./assets/icon.png",
    userInterfaceStyle: "light",
    newArchEnabled: true,
    plugins: [
      "expo-router",
      "expo-audio",
      "expo-font",
      "expo-asset"
    ],
    extra: {
      // Variables de entorno expuestas a la app
      API_BASE_URL: process.env.API_BASE_URL || "http://localhost:8007",
      // Puedes acceder a estas usando: Constants.expoConfig.extra.API_BASE_URL
    },
    splash: {
      image: "./assets/splash-icon.png",
      resizeMode: "contain",
      backgroundColor: "#ffffff"
    },
    ios: {
      supportsTablet: true,
      infoPlist: {
        NSMicrophoneUsageDescription: "Esta app necesita acceso al micrófono para grabar sonidos de aves"
      }
    },
    android: {
      permissions: [
        "RECORD_AUDIO",
        "ACCESS_COARSE_LOCATION",
        "ACCESS_FINE_LOCATION"
      ],
      config: {
        googleMaps: {
          apiKey: process.env.GOOGLE_MAPS_API_KEY || "TU_API_KEY_DE_GOOGLE_MAPS"
        }
      },
      adaptiveIcon: {
        foregroundImage: "./assets/adaptive-icon.png",
        backgroundColor: "#ffffff"
      },
      edgeToEdgeEnabled: true,
      predictiveBackGestureEnabled: false
    },
    web: {
      favicon: "./assets/favicon.png"
    }
  }
};
