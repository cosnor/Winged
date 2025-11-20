import { Text, View, StyleSheet, ScrollView, Pressable, Dimensions } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { useState, useEffect } from "react";
import { theme } from "../../styles/theme";

export default function HomeScreen({ userName = "Camila" }) {

    const [streak, setStreak] = useState(7);
    const [dailyFact, setDailyFact] = useState("");
    const [dailyChallenge, setDailyChallenge] = useState("");
    const [challengeDone, setChallengeDone] = useState(false);

    const goal = 30;
    const progress = Math.min(1, streak / goal);
    const dateStr = new Date().toLocaleDateString("es-ES", { weekday: "long", day: "numeric", month: "long" });

    useEffect(() => {
        setDailyFact("Las aves migratorias pueden viajar hasta 20,000 km al año.");
        setDailyChallenge("Observa y registra 2 especies nuevas hoy.");
    }, []);

    return (
        <SafeAreaView style={styles.container}>
            <ScrollView contentContainerStyle={styles.scroll}>

                <View style={styles.header}>
                    <View style={styles.avatar}>
                        <Text style={styles.avatarText}>{userName?.charAt(0).toUpperCase()}</Text>
                    </View>
                    <View style={styles.headerTexts}>
                        <Text style={styles.welcome}>Bienvenida, {userName}</Text>
                        <Text style={styles.date}>{dateStr}</Text>
                    </View>
                </View>

                <View style={styles.card}>
                    <View style={styles.cardAccent} />
                    <Text style={styles.cardTitle}>Racha</Text>
                    <Text style={styles.cardNumber}>{streak} días</Text>
                    <Text style={styles.cardSubtitle}>¡Sigue así!</Text>

                    <View style={styles.progressWrap}>
                        <View style={styles.progressBar}>
                            <View style={[styles.progressFill, { width: `${progress * 100}%` }]} />
                        </View>
                        <Text style={styles.progressLabel}>{Math.round(progress * 100)}% de {goal}</Text>
                    </View>

                    
                </View>

                <View style={styles.card}>
                    <View style={styles.cardAccent} />
                    <Text style={styles.cardTitle}>Dato Curioso</Text>
                    <Text style={styles.cardText}>{dailyFact}</Text>
                </View>

                <View style={styles.card}>
                    <View style={styles.cardAccent} />
                    <Text style={styles.cardTitle}>Reto del Día</Text>
                    <Text style={styles.cardText}>{dailyChallenge}</Text>
                    <Pressable
                        style={[styles.completeBtn, challengeDone && styles.completeBtnDone]}
                        onPress={() => setChallengeDone(!challengeDone)}
                    >
                        <Text style={[styles.completeBtnText, challengeDone && styles.completeBtnTextDone]}>
                            {challengeDone ? "Completado ✓" : "Marcar como completado"}
                        </Text>
                    </Pressable>
                </View>

                <Text style={styles.footerNote}>Consejo: Registra observaciones diarias para mantener la racha activa</Text>

            </ScrollView>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: theme.colors.background,
        padding: 25,
    },
    scroll: {
        alignItems: "center",
        paddingBottom: 40,
        width: "100%",
    },
    header: {
        width: "100%",
        flexDirection: "row",
        alignItems: "center",
        marginBottom: 12,
    },
    avatar: {
        width: 56,
        height: 56,
        borderRadius: 28,
        backgroundColor: theme.colors.primary,
        alignItems: "center",
        justifyContent: "center",
        marginRight: 12,
        elevation: 3,
    },
    avatarText: {
        color: "#fff",
        fontWeight: "800",
        fontSize: 20,
    },
    headerTexts: {
        justifyContent: "center",
        gap: 2,
        marginBottom: 2,

    },
    welcome: {
        fontSize: 28,
        fontWeight: "700",
        color: theme.colors.primary,
        marginBottom: 5,
        width: "100%",
    },
    date: {
        color: theme.colors.foreground,
        opacity: 0.8,
        marginTop: 2,
        fontSize: 13,
    },
    card: {
        width: "100%",
        padding: 16,
        borderRadius: 16,
        backgroundColor: theme.colors.card || "#14222F",
        marginBottom: 16,
        elevation: 3,
        shadowColor: "#000",
        shadowOpacity: 0.12,
        shadowRadius: 8,
        overflow: "hidden",
    },
    cardAccent: {
        position: "absolute",
        left: 0,
        right: 0,
        top: 0,
        height: 8,
        backgroundColor: theme.colors.primary,
        opacity: 0.12,
    },
    cardTitle: {
        fontSize: 20,
        fontWeight: "700",
        marginBottom: 10,
        color: theme.colors.primary,
    },
    cardNumber: {
        fontSize: 40,
        fontWeight: "900",
        color: theme.colors.foreground,
    },
    cardSubtitle: {
        fontSize: 16,
        color: theme.colors.foreground,
        opacity: 0.8,
        marginTop: 4,
    },
    cardText: {
        color: theme.colors.foreground,
        fontSize: 16,
        lineHeight: 22,
    },
    progressWrap: {
        marginTop: 14,
    },
    progressBar: {
        width: "100%",
        height: 10,
        backgroundColor: theme.colors.background === "#fff" ? "#eee" : "#0F2730",
        borderRadius: 6,
        overflow: "hidden",
    },
    progressFill: {
        height: "100%",
        backgroundColor: theme.colors.primary,
    },
    progressLabel: {
        marginTop: 8,
        color: theme.colors.foreground,
        opacity: 0.85,
        fontSize: 12,
    },
    actionsRow: {
        flexDirection: "row",
        marginTop: 14,
    },
    actionBtn: {
        flex: 1,
        backgroundColor: theme.colors.primary,
        paddingVertical: 10,
        paddingHorizontal: 12,
        borderRadius: 12,
        marginRight: 8,
        alignItems: "center",
    },
    outlineBtn: {
        backgroundColor: "transparent",
        borderWidth: 1,
        borderColor: theme.colors.primary,
        marginRight: 0,
        marginLeft: 8,
    },
    actionBtnText: {
        color: "#fff",
        fontWeight: "700",
        fontSize: 13,
    },
    outlineText: {
        color: theme.colors.primary,
    },
    completeBtn: {
        marginTop: 12,
        paddingVertical: 10,
        paddingHorizontal: 12,
        borderRadius: 10,
        backgroundColor: "transparent",
        borderWidth: 1,
        borderColor: theme.colors.foreground,
        alignItems: "center",
    },
    completeBtnDone: {
        backgroundColor: theme.colors.primary,
        borderColor: "transparent",
    },
    completeBtnText: {
        color: theme.colors.foreground,
        fontWeight: "700",
    },
    completeBtnTextDone: {
        color: "#fff",
    },
    footerNote: {
        marginTop: 6,
        color: theme.colors.foreground,
        opacity: 0.7,
        fontSize: 12,
        textAlign: "center",
        width: "100%",
    },
});