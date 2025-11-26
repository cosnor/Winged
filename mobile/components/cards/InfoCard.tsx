import React from "react";
import { Text, StyleSheet, Pressable } from "react-native";
import {theme} from "../../styles/theme"

type TextCardProps = {
  title: string;            // Título principal
  description?: string;     // Texto o detalle adicional
  onPress?: () => void;     // Acción al presionar
};

export default function InfoCard({ title, description }: TextCardProps) {
  return (
    <Pressable style={styles.card}>
      <Text style={styles.title}>{title}</Text>
      {description && <Text style={styles.description}>{description}</Text>}
    </Pressable>
  );
}

const styles = StyleSheet.create({
  card: {
    height: "10%",
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: theme.colors.card, // Cream (paleta Winged)
    padding: 12,
    marginVertical: 8,
    marginHorizontal: 12,

    // Sombra GAMING-RETRO
    borderWidth: 2,
    borderColor: theme.colors.primary, // amber
    shadowColor: theme.colors.primary,
    shadowOpacity: 1,
    shadowRadius: 0,
    shadowOffset: { width: 5, height: 5 },
    elevation: 3,
  },
  title: {
    fontSize: 18,
    fontWeight: "bold",
    color: "#d97706", // Amber
  },
  description: {
    fontSize: 14,
    color: "#444",
  },
});