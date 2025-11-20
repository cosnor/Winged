// import { Redirect } from 'expo-router';

// export default function Index() {
//   return <Redirect href="/(auth)/login" />;
// }

import { Text, View, StyleSheet, Image, Animated, Easing } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { LinearGradient } from "expo-linear-gradient";
import { useEffect, useRef } from "react";
import { theme } from "../styles/theme";
import MainButton from "../components/ui/MainButton";
import { router } from "expo-router";

export default function Index() {

    // Fade-in animation
    const fadeAnim = useRef(new Animated.Value(0)).current;
    // Pulsing animation for logo background
    const pulseAnim = useRef(new Animated.Value(1)).current;
    const pulseOpacity = useRef(new Animated.Value(0.15)).current;

    useEffect(() => {
        Animated.timing(fadeAnim, {
            toValue: 1,
            duration: 1200,
            easing: Easing.out(Easing.ease),
            useNativeDriver: true,
        }).start();
        Animated.loop(
            Animated.parallel([
                Animated.sequence([
                    Animated.timing(pulseAnim, { toValue: 1.12, duration: 1000, useNativeDriver: true }),
                    Animated.timing(pulseAnim, { toValue: 1.0, duration: 1000, useNativeDriver: true }),
                ]),
                Animated.sequence([
                    Animated.timing(pulseOpacity, { toValue: 0.06, duration: 1000, useNativeDriver: true }),
                    Animated.timing(pulseOpacity, { toValue: 0.15, duration: 1000, useNativeDriver: true }),
                ])
            ])
        ).start();
    }, [fadeAnim, pulseAnim, pulseOpacity]);

    return (
        <LinearGradient
            colors={[theme.colors.background, "#5d2f07ff"]}
            style={{ flex: 1 }}

        >
            <SafeAreaView style={styles.container}>

                <Animated.View style={{ opacity: fadeAnim, alignItems: "center" }}>
                    <Text style={styles.mainTitle}>WINGED</Text>

                    <View style={styles.logoContainer}>
                        <Animated.View style={[styles.pulseCircle, { transform: [{ scale: pulseAnim }], opacity: pulseOpacity }]} />
                        <Image 
                            source={require('../assets/images/WingedLogo.png')} 
                            style={styles.logo} 
                            resizeMode="contain" 
                        />
                    </View>

                    <View style={styles.grid}>
                        <LinearGradient colors={["#ff9a00", "#ff5e62"]} style={styles.ctaGradient}>
                            <MainButton 
                                title="COMENZAR"
                                onPress={() => router.push("/login")}
                            />
                        </LinearGradient>
                    </View>

                    <Text style={styles.description}>
                        Descubre las aves del Caribe
                    </Text>
                </Animated.View>

            </SafeAreaView>
        </LinearGradient>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
        padding: 20,
    },
    mainTitle: {
        fontSize: 52,
        fontWeight: "900",
        letterSpacing: 4,
        color: "#eb7310ff",
        textShadowColor: "rgba(45, 37, 26, 0.43)",
        textShadowOffset: { width: 0, height: 0 },
        textShadowRadius: 4,
        marginBottom: 30,
    },
    logo: {
        width: 220,
        height: 220,
        marginBottom: 25,
        shadowColor: "#000",
        shadowOpacity: 0.25,
        shadowRadius: 10,
        elevation: 10,
    },
    grid: {
        width: "100%",
        alignItems: "center",
        justifyContent: "center",
        marginTop: 20,
        marginBottom: 20,
    },
    description: {
        marginTop: 5,
        color: "#fff",
        fontSize: 16,
        opacity: 0.8,
        fontWeight: "500",
    },
    logoContainer: {
        width: 240,
        height: 240,
        alignItems: 'center',
        justifyContent: 'center',
        marginBottom: 12,
    },
    pulseCircle: {
        position: 'absolute',
        width: 200,
        height: 200,
        borderRadius: 100,
        backgroundColor: 'rgba(255,255,255,0.12)',
    },
    ctaGradient: {
        borderRadius: 999,
        paddingVertical: 6,
        paddingHorizontal: 18,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 6 },
        shadowOpacity: 0.18,
        shadowRadius: 12,
        elevation: 8,
    },
});
