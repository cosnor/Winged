import { Text, View, StyleSheet, ScrollView, Pressable, Dimensions, ImageBackground } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { useState, useEffect } from "react";
import { LinearGradient } from "expo-linear-gradient";
import Ionicons from '@expo/vector-icons/Ionicons';
import * as Animatable from 'react-native-animatable';
import AsyncStorage from "@react-native-async-storage/async-storage";
import { theme } from "../../styles/theme";

export default function HomeScreen() {
    const [userName, setUserName] = useState("Usuario");
    const [streak, setStreak] = useState(0);
    const [dailyFact, setDailyFact] = useState("");
    const [dailyChallenge, setDailyChallenge] = useState("");
    const [challengeDone, setChallengeDone] = useState(false);
    const [birdOfTheDay, setBirdOfTheDay] = useState({
        name: "Colibrí Rutilante",
        scientificName: "Colibri coruscans",
        fact: "Puede batir sus alas hasta 80 veces por segundo",
        imageUrl: "https://images.unsplash.com/photo-1570997447151-0bfb3e9c2d94?w=400"
    });

    const dateStr = new Date().toLocaleDateString("es-ES", { weekday: "long", day: "numeric", month: "long" });

    // Load user info from AsyncStorage
    useEffect(() => {
        const loadUserInfo = async () => {
            try {
                const userInfoStr = await AsyncStorage.getItem('USER_INFO');
                if (userInfoStr) {
                    const userInfo = JSON.parse(userInfoStr);
                    // Try different possible field names for the username
                    const name = userInfo.name || userInfo.username || userInfo.email?.split('@')[0] || "Usuario";
                    setUserName(name);
                    console.log('👤 Loaded user name:', name);
                }
            } catch (error) {
                console.error('❌ Error loading user info:', error);
            }
        };

        loadUserInfo();
    }, []);

    useEffect(() => {
        setDailyFact("Las aves migratorias pueden viajar hasta 20,000 km al año.");
        setDailyChallenge("Observa y registra 2 especies nuevas hoy.");
    }, []);

    return (
        <LinearGradient
            colors={['#fffaf0', '#ffe4d6', '#ffd4ba']}
            style={{ flex: 1 }}
        >
            {/* Decoraciones de fondo */}
            <View style={styles.backgroundDecor}>
                <Ionicons name="leaf" size={140} color="rgba(210, 105, 30, 0.04)" style={styles.decorLeaf1} />
                <Ionicons name="sunny" size={100} color="rgba(255, 154, 65, 0.06)" style={styles.decorSun} />
                <Ionicons name="sparkles" size={70} color="rgba(255, 107, 53, 0.05)" style={styles.decorSparkle} />
            </View>
            
            <SafeAreaView style={styles.container}>
                <ScrollView contentContainerStyle={styles.scroll}>

                <View style={styles.header}>
                    <LinearGradient
                        colors={['#ff9a41', '#d2691e']}
                        style={styles.avatar}
                    >
                        <Text style={styles.avatarText}>{userName?.charAt(0).toUpperCase()}</Text>
                    </LinearGradient>
                    <View style={styles.headerTexts}>
                        <Text style={styles.welcome}>Hola, {userName} 👋</Text>
                        <View style={styles.dateRow}>
                            <Ionicons name="calendar-outline" size={14} color="#d2691e" />
                            <Text style={styles.date}>{dateStr}</Text>
                        </View>
                    </View>
                </View>

                <Animatable.View animation="fadeInUp" duration={600} delay={100}>
                    <LinearGradient
                        colors={['#fff', '#fffaf0']}
                        style={styles.card}
                    >
                        <View style={styles.cardHeader}>
                            <View style={styles.cardIconContainer}>
                                <Ionicons name="flame" size={28} color="#ff6b35" />
                            </View>
                            <View style={styles.cardHeaderText}>
                                <Text style={styles.cardTitle}>Racha Activa</Text>
                                <Text style={styles.cardSubtitle}>¡Sigue así!</Text>
                            </View>
                        </View>
                        <View style={styles.streakNumberContainer}>
                            <Text style={styles.cardNumber}>{streak}</Text>
                            <Text style={styles.cardNumberLabel}>días consecutivos</Text>
                        </View>
                    </LinearGradient>
                </Animatable.View>

                {/* Ave del Día */}
                <Animatable.View animation="fadeInUp" duration={600} delay={200}>
                    <View style={styles.cardBird}>
                        <ImageBackground
                            source={{ uri: birdOfTheDay.imageUrl }}
                            style={styles.birdImage}
                            imageStyle={{ borderRadius: 16 }}
                        >
                            <LinearGradient
                                colors={['transparent', 'rgba(0,0,0,0.8)']}
                                style={styles.birdOverlay}
                            >
                                <View style={styles.birdBadge}>
                                    <Ionicons name="star" size={16} color="#fff" />
                                    <Text style={styles.birdBadgeText}>Ave del Día</Text>
                                </View>
                                <Text style={styles.birdName}>{birdOfTheDay.name}</Text>
                                <Text style={styles.birdScientific}>{birdOfTheDay.scientificName}</Text>
                                <View style={styles.birdFactContainer}>
                                    <Ionicons name="information-circle" size={16} color="#ff9a41" />
                                    <Text style={styles.birdFact}>{birdOfTheDay.fact}</Text>
                                </View>
                            </LinearGradient>
                        </ImageBackground>
                    </View>
                </Animatable.View>

                <Animatable.View animation="fadeInUp" duration={600} delay={300}>
                    <LinearGradient
                        colors={['#fff', '#fffaf0']}
                        style={styles.card}
                    >
                        <View style={styles.cardHeader}>
                            <View style={styles.cardIconContainer}>
                                <Ionicons name="bulb" size={28} color="#fbbf24" />
                            </View>
                            <View style={styles.cardHeaderText}>
                                <Text style={styles.cardTitle}>Dato Curioso</Text>
                            </View>
                        </View>
                        <Text style={styles.cardText}>{dailyFact}</Text>
                    </LinearGradient>
                </Animatable.View>

                <Animatable.View animation="fadeInUp" duration={600} delay={400}>
                    <LinearGradient
                        colors={['#fff', '#fffaf0']}
                        style={styles.card}
                    >
                        <View style={styles.cardHeader}>
                            <View style={styles.cardIconContainer}>
                                <Ionicons name="trophy" size={28} color="#d2691e" />
                            </View>
                            <View style={styles.cardHeaderText}>
                                <Text style={styles.cardTitle}>Reto del Día</Text>
                            </View>
                        </View>
                        <Text style={styles.cardText}>{dailyChallenge}</Text>
                        <Pressable
                            style={[styles.completeBtn, challengeDone && styles.completeBtnDone]}
                            onPress={() => setChallengeDone(!challengeDone)}
                        >
                            <Ionicons 
                                name={challengeDone ? "checkmark-circle" : "checkmark-circle-outline"} 
                                size={20} 
                                color={challengeDone ? "#fff" : "#d2691e"} 
                            />
                            <Text style={[styles.completeBtnText, challengeDone && styles.completeBtnTextDone]}>
                                {challengeDone ? "Completado" : "Marcar como completado"}
                            </Text>
                        </Pressable>
                    </LinearGradient>
                </Animatable.View>

                <View style={styles.footerContainer}>
                    <Ionicons name="information-circle-outline" size={16} color="#d2691e" />
                    <Text style={styles.footerNote}>Registra observaciones diarias para mantener tu racha</Text>
                </View>

            </ScrollView>
        </SafeAreaView>
        </LinearGradient>
    );
}

const styles = StyleSheet.create({
    backgroundDecor: {
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        overflow: 'hidden',
    },
    decorLeaf1: {
        position: 'absolute',
        top: -20,
        right: -30,
        transform: [{ rotate: '45deg' }],
    },
    decorSun: {
        position: 'absolute',
        top: 80,
        left: -20,
        opacity: 0.8,
    },
    decorSparkle: {
        position: 'absolute',
        bottom: 150,
        right: 30,
    },
    container: {
        flex: 1,
        backgroundColor: 'transparent',
    },
    scroll: {
        padding: 16,
        paddingBottom: 40,
    },
    header: {
        flexDirection: "row",
        alignItems: "center",
        marginBottom: 20,
    },
    avatar: {
        width: 64,
        height: 64,
        borderRadius: 32,
        alignItems: "center",
        justifyContent: "center",
        marginRight: 16,
        shadowColor: '#d2691e',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        shadowRadius: 8,
        elevation: 6,
        borderWidth: 3,
        borderColor: '#fff',
    },
    avatarText: {
        color: "#fff",
        fontWeight: "900",
        fontSize: 28,
    },
    headerTexts: {
        flex: 1,
        justifyContent: "center",
    },
    welcome: {
        fontSize: 26,
        fontWeight: "800",
        color: '#d2691e',
        marginBottom: 6,
    },
    dateRow: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 6,
    },
    date: {
        color: '#666',
        fontSize: 14,
        fontWeight: '500',
    },
    card: {
        width: "100%",
        padding: 20,
        borderRadius: 20,
        marginBottom: 16,
        shadowColor: '#ff6b35',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.2,
        shadowRadius: 8,
        elevation: 5,
        borderWidth: 2,
        borderColor: '#ff9a41',
    },
    cardHeader: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: 16,
    },
    cardIconContainer: {
        width: 50,
        height: 50,
        borderRadius: 25,
        backgroundColor: 'rgba(255, 154, 65, 0.15)',
        alignItems: 'center',
        justifyContent: 'center',
        marginRight: 12,
    },
    cardHeaderText: {
        flex: 1,
    },
    cardTitle: {
        fontSize: 20,
        fontWeight: "800",
        color: '#d2691e',
    },
    cardSubtitle: {
        fontSize: 14,
        color: '#666',
        fontWeight: '600',
        marginTop: 2,
    },
    streakNumberContainer: {
        alignItems: 'center',
        paddingVertical: 12,
        backgroundColor: 'rgba(255, 154, 65, 0.08)',
        borderRadius: 16,
        borderWidth: 2,
        borderColor: 'rgba(255, 107, 53, 0.2)',
        borderStyle: 'dashed',
    },
    cardNumber: {
        fontSize: 56,
        fontWeight: "900",
        color: '#ff6b35',
        lineHeight: 60,
    },
    cardNumberLabel: {
        fontSize: 15,
        color: '#d2691e',
        fontWeight: '600',
        marginTop: 4,
    },
    cardText: {
        color: '#555',
        fontSize: 15,
        lineHeight: 24,
        fontWeight: '500',
    },
    
    // Bird of the day styles
    cardBird: {
        width: "100%",
        marginBottom: 16,
        borderRadius: 20,
        overflow: 'hidden',
        shadowColor: '#ff6b35',
        shadowOffset: { width: 0, height: 6 },
        shadowOpacity: 0.3,
        shadowRadius: 12,
        elevation: 8,
        borderWidth: 3,
        borderColor: '#ff9a41',
    },
    birdImage: {
        width: '100%',
        height: 240,
    },
    birdOverlay: {
        flex: 1,
        justifyContent: 'flex-end',
        padding: 20,
    },
    birdBadge: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: '#d2691e',
        paddingHorizontal: 12,
        paddingVertical: 6,
        borderRadius: 20,
        alignSelf: 'flex-start',
        marginBottom: 12,
        gap: 6,
    },
    birdBadgeText: {
        color: '#fff',
        fontSize: 12,
        fontWeight: '700',
        letterSpacing: 0.5,
    },
    birdName: {
        fontSize: 24,
        fontWeight: '900',
        color: '#fff',
        marginBottom: 4,
    },
    birdScientific: {
        fontSize: 14,
        fontStyle: 'italic',
        color: '#f0f0f0',
        marginBottom: 12,
    },
    birdFactContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: 'rgba(255, 255, 255, 0.15)',
        paddingHorizontal: 12,
        paddingVertical: 8,
        borderRadius: 12,
        gap: 8,
    },
    birdFact: {
        flex: 1,
        fontSize: 13,
        color: '#fff',
        fontWeight: '600',
    },
    
    completeBtn: {
        marginTop: 16,
        paddingVertical: 14,
        paddingHorizontal: 16,
        borderRadius: 14,
        backgroundColor: "#fff",
        borderWidth: 2,
        borderColor: '#d2691e',
        alignItems: "center",
        flexDirection: 'row',
        justifyContent: 'center',
        gap: 8,
    },
    completeBtnDone: {
        backgroundColor: '#d2691e',
        borderColor: '#ff6b35',
    },
    completeBtnText: {
        color: '#d2691e',
        fontWeight: "700",
        fontSize: 15,
    },
    completeBtnTextDone: {
        color: "#fff",
    },
    footerContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
        marginTop: 8,
        paddingHorizontal: 16,
        gap: 8,
    },
    footerNote: {
        color: '#666',
        fontSize: 13,
        textAlign: "center",
        fontWeight: '500',
        flex: 1,
    },
});