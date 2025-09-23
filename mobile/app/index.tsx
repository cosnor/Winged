import { Text, View, StyleSheet } from "react-native";
import { SafeAreaView } from 'react-native-safe-area-context';
import { theme } from "../styles/theme";
import InfoCard from "../components/cards/InfoCard";
import MainButton from "../components/ui/MainButton";
import { router } from "expo-router";


export default function Index() {
    return (
        <SafeAreaView style={styles.container}>
            <Text style={styles.mainTitle}>WINGED</Text>
            <Text style={styles.description}>Descubre y registra las aves del Caribe</Text>
            <View style={styles.grid}>
                <InfoCard title="Identifica aves por audio"/>
                <InfoCard title="Crea tu avedex personal"/>
                <InfoCard title="Haz de tu barrio una selva"/>
                <MainButton 
                    title="COMENZAR" 
                    onPress={() => router.push("/auth/login")}                
                />
            </View>
        </SafeAreaView>
    );

}

const styles = StyleSheet.create({
    container: {
        flex: 2,
        flexDirection: "column", 
        width: "100%",
        height: "100%",
        justifyContent: "center", 
        alignItems: "center",
        gap: 10,
        backgroundColor: theme.colors.background,
        padding: 10
        
    },
    mainTitle: {
        marginTop: 20,
        fontSize: 50,
        fontWeight: 900,
        color: theme.colors.primary
    },
    description:{
        color: theme.colors.foreground,
        fontSize: 16,
        fontWeight: 500,
        marginBottom: 20
    },
    grid : {
        flexDirection: "column",
        flex: 1,
        justifyContent: "center"
    }

});