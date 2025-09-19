import React from "react";
import { StyleSheet, Text, Pressable } from "react-native";
import {theme} from "../../styles/theme"


type MyButton = {
  title: string;            // Título principal
  onPress?: () => void;     // Acción al presionar
};

export default function MainButton({ title , onPress}: MyButton) {
    return (
        <Pressable style={styles.bttn} onPress={onPress}>
            <Text style={styles.bttnText}>{title}</Text>
        </Pressable>
    );
}

const styles = StyleSheet.create({
    bttn: {
        margin: 20,
        paddingVertical:15,
        paddingHorizontal: 50,
        backgroundColor: theme.colors.primary,
        borderWidth: 2,
        borderColor: theme.colors.primary, // amber
        shadowColor: theme.colors.secondary,
        shadowOpacity: 1,
        shadowRadius: 0, 
        shadowOffset: { width: 5, height: 4 },
    },
    bttnText:{
        fontSize: 16,
        fontWeight: 800,
        color: theme.colors.muted,
        textAlign: "center"
    }
    
});