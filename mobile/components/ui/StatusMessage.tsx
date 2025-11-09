import React from 'react';
import { StyleSheet, Text, View, Animated } from 'react-native';

interface StatusMessageProps {
  type: 'success' | 'error';
  message: string;
  visible: boolean;
}

export default function StatusMessage({ type, message, visible }: StatusMessageProps) {
  if (!visible) return null;

  return (
    <View style={[
      styles.container,
      type === 'success' ? styles.successContainer : styles.errorContainer
    ]}>
      <Text style={[
        styles.text,
        type === 'success' ? styles.successText : styles.errorText
      ]}>
        {message}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 12,
    borderRadius: 8,
    marginVertical: 10,
    marginHorizontal: 20,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  successContainer: {
    backgroundColor: '#e6ffe6',
    borderColor: '#00b300',
    borderWidth: 1,
  },
  errorContainer: {
    backgroundColor: '#ffe6e6',
    borderColor: '#ff0000',
    borderWidth: 1,
  },
  text: {
    fontSize: 14,
    textAlign: 'center',
  },
  successText: {
    color: '#006600',
  },
  errorText: {
    color: '#cc0000',
  },
});