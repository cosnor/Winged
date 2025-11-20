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
        paddingVertical:15,
        paddingHorizontal: 50,

    },
    bttnText:{
        fontSize: 16,
        fontWeight: 800,
        color: theme.colors.muted,
        textAlign: "center"
    }
    
});