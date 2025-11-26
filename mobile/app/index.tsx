// import { Redirect } from 'expo-router';

// export default function Index() {
//   return <Redirect href="/(auth)/login" />;
// }

import { Text, View, StyleSheet, Image, Animated, Easing, Dimensions } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { LinearGradient } from "expo-linear-gradient";
import { useEffect, useRef } from "react";
import { theme } from "../styles/theme";
import MainButton from "../components/ui/MainButton";
import { router } from "expo-router";
import { Ionicons } from '@expo/vector-icons';

const { width, height } = Dimensions.get('window');

export default function Index() {

    // Fade-in animation
    const fadeAnim = useRef(new Animated.Value(0)).current;
    const titleSlide = useRef(new Animated.Value(-50)).current;
    const logoScale = useRef(new Animated.Value(0)).current;
    const buttonSlide = useRef(new Animated.Value(50)).current;
    
    // Pulsing animation for logo background
    const pulseAnim = useRef(new Animated.Value(1)).current;
    const pulseOpacity = useRef(new Animated.Value(0.15)).current;
    
    // Floating birds animations
    const bird1Y = useRef(new Animated.Value(0)).current;
    const bird1X = useRef(new Animated.Value(0)).current;
    const bird2Y = useRef(new Animated.Value(0)).current;
    const bird2X = useRef(new Animated.Value(0)).current;
    const bird3Y = useRef(new Animated.Value(0)).current;
    const bird3X = useRef(new Animated.Value(0)).current;
    
    // Rotating feather
    const featherRotate = useRef(new Animated.Value(0)).current;
    const featherY = useRef(new Animated.Value(0)).current;

    useEffect(() => {
        // Entry animations
        Animated.parallel([
            Animated.timing(fadeAnim, {
                toValue: 1,
                duration: 1200,
                easing: Easing.out(Easing.ease),
                useNativeDriver: true,
            }),
            Animated.spring(titleSlide, {
                toValue: 0,
                tension: 50,
                friction: 7,
                useNativeDriver: true,
            }),
            Animated.spring(logoScale, {
                toValue: 1,
                delay: 300,
                tension: 40,
                friction: 6,
                useNativeDriver: true,
            }),
            Animated.spring(buttonSlide, {
                toValue: 0,
                delay: 600,
                tension: 50,
                friction: 7,
                useNativeDriver: true,
            }),
        ]).start();
        
        // Logo pulse
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
        
        // Floating birds
        Animated.loop(
            Animated.parallel([
                Animated.sequence([
                    Animated.timing(bird1Y, { toValue: -20, duration: 3000, easing: Easing.inOut(Easing.ease), useNativeDriver: true }),
                    Animated.timing(bird1Y, { toValue: 0, duration: 3000, easing: Easing.inOut(Easing.ease), useNativeDriver: true }),
                ]),
                Animated.sequence([
                    Animated.timing(bird1X, { toValue: 15, duration: 2500, easing: Easing.inOut(Easing.ease), useNativeDriver: true }),
                    Animated.timing(bird1X, { toValue: 0, duration: 2500, easing: Easing.inOut(Easing.ease), useNativeDriver: true }),
                ]),
            ])
        ).start();
        
        Animated.loop(
            Animated.parallel([
                Animated.sequence([
                    Animated.timing(bird2Y, { toValue: -30, duration: 4000, easing: Easing.inOut(Easing.ease), useNativeDriver: true }),
                    Animated.timing(bird2Y, { toValue: 0, duration: 4000, easing: Easing.inOut(Easing.ease), useNativeDriver: true }),
                ]),
                Animated.sequence([
                    Animated.timing(bird2X, { toValue: -20, duration: 3500, easing: Easing.inOut(Easing.ease), useNativeDriver: true }),
                    Animated.timing(bird2X, { toValue: 0, duration: 3500, easing: Easing.inOut(Easing.ease), useNativeDriver: true }),
                ]),
            ])
        ).start();
        
        Animated.loop(
            Animated.parallel([
                Animated.sequence([
                    Animated.timing(bird3Y, { toValue: -25, duration: 3500, easing: Easing.inOut(Easing.ease), useNativeDriver: true }),
                    Animated.timing(bird3Y, { toValue: 0, duration: 3500, easing: Easing.inOut(Easing.ease), useNativeDriver: true }),
                ]),
                Animated.sequence([
                    Animated.timing(bird3X, { toValue: 10, duration: 3000, easing: Easing.inOut(Easing.ease), useNativeDriver: true }),
                    Animated.timing(bird3X, { toValue: 0, duration: 3000, easing: Easing.inOut(Easing.ease), useNativeDriver: true }),
                ]),
            ])
        ).start();
        
        // Rotating feather
        Animated.loop(
            Animated.parallel([
                Animated.timing(featherRotate, {
                    toValue: 1,
                    duration: 8000,
                    easing: Easing.linear,
                    useNativeDriver: true,
                }),
                Animated.sequence([
                    Animated.timing(featherY, { toValue: -40, duration: 4000, easing: Easing.inOut(Easing.ease), useNativeDriver: true }),
                    Animated.timing(featherY, { toValue: 0, duration: 4000, easing: Easing.inOut(Easing.ease), useNativeDriver: true }),
                ]),
            ])
        ).start();
    }, []);

    const spin = featherRotate.interpolate({
        inputRange: [0, 1],
        outputRange: ['0deg', '360deg']
    });

    return (
        <LinearGradient
            colors={['#1a0a00', '#5d2f07ff', '#eb7310ff']}
            style={{ flex: 1 }}
            start={{ x: 0, y: 0 }}
            end={{ x: 0, y: 1 }}
        >
            <SafeAreaView style={styles.container}>
                {/* Floating decorative birds */}
                <Animated.View style={[styles.floatingBird, styles.bird1, { 
                    transform: [{ translateY: bird1Y }, { translateX: bird1X }],
                    opacity: fadeAnim 
                }]}>
                    <Ionicons name="airplane" size={24} color="rgba(255,154,0,0.3)" />
                </Animated.View>
                
                <Animated.View style={[styles.floatingBird, styles.bird2, { 
                    transform: [{ translateY: bird2Y }, { translateX: bird2X }],
                    opacity: fadeAnim 
                }]}>
                    <Ionicons name="airplane" size={32} color="rgba(255,154,0,0.4)" />
                </Animated.View>
                
                <Animated.View style={[styles.floatingBird, styles.bird3, { 
                    transform: [{ translateY: bird3Y }, { translateX: bird3X }],
                    opacity: fadeAnim 
                }]}>
                    <Ionicons name="airplane" size={20} color="rgba(255,154,0,0.25)" />
                </Animated.View>

                {/* Rotating feather */}
                <Animated.View style={[styles.featherContainer, { 
                    transform: [{ rotate: spin }, { translateY: featherY }],
                    opacity: fadeAnim 
                }]}>
                    <Ionicons name="leaf" size={60} color="rgba(235,115,16,0.15)" />
                </Animated.View>

                <Animated.View style={{ 
                    opacity: fadeAnim, 
                    alignItems: "center",
                    width: '100%',
                }}>
                    {/* Animated title */}
                    <Animated.View style={{ 
                        transform: [{ translateY: titleSlide }],
                        alignItems: 'center',
                    }}>
                        <View style={styles.titleContainer}>
                            
                            <Text style={styles.mainTitle}>WINGED</Text>
                            
                        </View>
                        <Text style={styles.tagline}>Tu guía de aves del Caribe</Text>
                    </Animated.View>

                    {/* Animated logo */}
                    <Animated.View style={{ transform: [{ scale: logoScale }] }}>
                        <View style={styles.logoContainer}>
                            <Animated.View style={[styles.pulseCircle, { 
                                transform: [{ scale: pulseAnim }], 
                                opacity: pulseOpacity 
                            }]} />
                            
                            {/* Multiple glow layers */}
                            <View style={styles.glowLayer1} />
                            <View style={styles.glowLayer2} />
                            
                            <View style={styles.logoWrapper}>
                                <LinearGradient
                                    colors={['rgba(255,154,0,0.2)', 'rgba(255,107,53,0.3)']}
                                    style={styles.logoBorder}
                                >
                                    <View style={styles.logoInner}>
                                        <Image 
                                            source={require('../assets/images/WingedLogo.png')} 
                                            style={styles.logo} 
                                            resizeMode="contain" 
                                        />
                                    </View>
                                </LinearGradient>
                            </View>
                        </View>
                    </Animated.View>

                    {/* Feature badges */}
                    <Animated.View style={[styles.featuresRow, { opacity: fadeAnim }]}>
                        <View style={styles.featureBadge}>
                            <LinearGradient colors={['rgba(255,154,0,0.15)', 'rgba(255,107,53,0.15)']} style={styles.badgeGradient}>
                                <Ionicons name="camera" size={20} color="#ff9a00" />
                                <Text style={styles.badgeText}>Identifica</Text>
                            </LinearGradient>
                        </View>
                        <View style={styles.featureBadge}>
                            <LinearGradient colors={['rgba(255,154,0,0.15)', 'rgba(255,107,53,0.15)']} style={styles.badgeGradient}>
                                <Ionicons name="map" size={20} color="#ff9a00" />
                                <Text style={styles.badgeText}>Explora</Text>
                            </LinearGradient>
                        </View>
                        <View style={styles.featureBadge}>
                            <LinearGradient colors={['rgba(255,154,0,0.15)', 'rgba(255,107,53,0.15)']} style={styles.badgeGradient}>
                                <Ionicons name="trophy" size={20} color="#ff9a00" />
                                <Text style={styles.badgeText}>Colecciona</Text>
                            </LinearGradient>
                        </View>
                    </Animated.View>

                    {/* Animated button */}
                    <Animated.View style={[styles.grid, { transform: [{ translateY: buttonSlide }] }]}>
                        <View style={styles.buttonWrapper}>
                            <LinearGradient
                                colors={['rgba(255,154,0,0.4)', 'rgba(255,107,53,0.5)']}
                                style={styles.buttonBorder}
                                start={{ x: 0, y: 0 }}
                                end={{ x: 1, y: 1 }}
                            >
                                <View style={styles.buttonInner}>
                                    <MainButton 
                                        title="COMENZAR AVENTURA"
                                        onPress={() => router.push("/login")}
                                    />
                                </View>
                            </LinearGradient>
                        </View>
                    </Animated.View>

                    <Animated.Text style={[styles.description, { opacity: fadeAnim }]}>
                        Descubre, registra y comparte
                    </Animated.Text>
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
    titleContainer: {
        marginBottom: 8,
    },

    mainTitle: {
        fontSize: 48,
        fontWeight: "900",
        letterSpacing: 8,
        color: "#fff",
        textShadowColor: "rgba(0, 0, 0, 0.5)",
        textShadowOffset: { width: 0, height: 2 },
        textShadowRadius: 8,
    },
    tagline: {
        fontSize: 13,
        color: "#ffd4ba",
        fontWeight: "600",
        letterSpacing: 1,
        textTransform: 'uppercase',
        marginBottom: 30,
    },
    logoContainer: {
        width: 280,
        height: 280,
        alignItems: 'center',
        justifyContent: 'center',
        marginBottom: 24,
    },
    logoWrapper: {
        width: 240,
        height: 240,
        borderRadius: 120,
    },
    logoBorder: {
        width: '100%',
        height: '100%',
        borderRadius: 120,
        padding: 4,
        shadowColor: '#ff9a00',
        shadowOffset: { width: 0, height: 8 },
        shadowOpacity: 0.6,
        shadowRadius: 20,
        elevation: 15,
    },
    logoInner: {
        width: '100%',
        height: '100%',
        borderRadius: 120,
        backgroundColor: 'rgba(0,0,0,0.3)',
        alignItems: 'center',
        justifyContent: 'center',
        overflow: 'hidden',
    },
    logo: {
        width: 200,
        height: 200,
    },
    pulseCircle: {
        position: 'absolute',
        width: 220,
        height: 220,
        borderRadius: 110,
        backgroundColor: 'rgba(255,154,0,0.2)',
    },
    glowLayer1: {
        position: 'absolute',
        width: 260,
        height: 260,
        borderRadius: 130,
        backgroundColor: 'rgba(255,154,0,0.08)',
    },
    glowLayer2: {
        position: 'absolute',
        width: 300,
        height: 300,
        borderRadius: 150,
        backgroundColor: 'rgba(255,107,53,0.05)',
    },
    featuresRow: {
        flexDirection: 'row',
        gap: 12,
        marginBottom: 32,

    },
    featureBadge: {
        borderRadius: 20,
        overflow: 'hidden',
        
    },
    badgeGradient: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 6,
        paddingHorizontal: 14,
        paddingVertical: 10,
    },
    badgeText: {
        color: '#ffd4ba',
        fontSize: 12,
        fontWeight: '700',
    },
    grid: {
        width: "100%",
        alignItems: "center",
        justifyContent: "center",
        marginBottom: 16,
    },
    buttonWrapper: {
        shadowColor: '#ff9a00',
        shadowOffset: { width: 0, height: 8 },
        shadowOpacity: 0.6,
        shadowRadius: 20,
        elevation: 15,
    },
    buttonBorder: {
        borderRadius: 50,
        padding: 3,
    },
    buttonInner: {
        borderRadius: 50,
        backgroundColor: 'rgba(0,0,0,0.15)',
        paddingVertical: 2,
        paddingHorizontal: 6,
    },
    description: {
        marginTop: 8,
        color: "#ffd4ba",
        fontSize: 15,
        fontWeight: "600",
        letterSpacing: 0.5,
    },
    ctaGradient: {
        borderRadius: 999,
        paddingVertical: 8,
        paddingHorizontal: 20,
        shadowColor: '#ff5e62',
        shadowOffset: { width: 0, height: 8 },
        shadowOpacity: 0.5,
        shadowRadius: 16,
        elevation: 12,
    },
    floatingBird: {
        position: 'absolute',
    },
    bird1: {
        top: height * 0.15,
        right: width * 0.1,
    },
    bird2: {
        top: height * 0.25,
        left: width * 0.08,
    },
    bird3: {
        top: height * 0.7,
        right: width * 0.15,
    },
    featherContainer: {
        position: 'absolute',
        top: height * 0.55,
        left: width * 0.12,
    },
});
