import { View, Text, StyleSheet } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

export default function RoutesScreen() {
  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>Rutas de Aves</Text>
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
});