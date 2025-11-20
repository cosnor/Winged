import { View, Text, StyleSheet } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

export default function RoutesScreen() {
  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>Rutas de Aves</Text>
      <View style={styles.constructionContainer}>
              <Text style={styles.constructionText}>🚧 Módulo en construcción — nuevas funciones próximamente.</Text>
            </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fffaf0',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#d2691e',
    textAlign: 'center',
    padding: 16,
  },
  constructionContainer: {
    marginHorizontal: 20,
    marginTop: 12,
    paddingVertical: 10,
    paddingHorizontal: 12,
    borderRadius: 8,
    backgroundColor: '#fff4e6',
    borderWidth: 1,
    borderColor: '#f0c7a3',
    alignItems: 'center',
  },
  constructionText: {
    color: '#8a4b00',
    fontSize: 13,
    textAlign: 'center',
  },
});