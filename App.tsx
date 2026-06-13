import { StatusBar } from 'expo-status-bar';
import React from 'react';
import { ScrollView, StyleSheet, Text, View } from 'react-native';

export default function App() {
  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Fitu Mobile Preview</Text>
      <Text style={styles.subtitle}>Expo React Native setup is now initialized.</Text>
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Quick Start</Text>
        <Text style={styles.cardText}>Press `a` in the Expo CLI to open the Android emulator.</Text>
      </View>
      <View style={styles.card}>
        <Text style={styles.cardTitle}>App Status</Text>
        <Text style={styles.cardText}>This is the mobile shell for the Fitu app.</Text>
      </View>
      <StatusBar style="auto" />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    padding: 24,
    backgroundColor: '#f8fafc',
    alignItems: 'center',
    justifyContent: 'flex-start',
  },
  title: {
    fontSize: 32,
    fontWeight: '800',
    marginBottom: 12,
    color: '#0f172a',
  },
  subtitle: {
    fontSize: 18,
    color: '#475569',
    marginBottom: 20,
    textAlign: 'center',
  },
  card: {
    width: '100%',
    backgroundColor: '#ffffff',
    borderRadius: 16,
    padding: 18,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
  },
  cardTitle: {
    fontSize: 20,
    fontWeight: '700',
    color: '#0f172a',
    marginBottom: 8,
  },
  cardText: {
    fontSize: 16,
    color: '#475569',
    lineHeight: 24,
  },
});
