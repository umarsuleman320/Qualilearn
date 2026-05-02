import React, { useState } from 'react';
import { StatusBar } from 'expo-status-bar';
import { StyleSheet, View } from 'react-native';
import LoginScreen from './src/screens/LoginScreen';
import DashboardScreen from './src/screens/DashboardScreen';
import SyllabusScreen from './src/screens/SyllabusScreen';
import { COLORS } from './src/theme/theme';

export default function App() {
  const [authToken, setAuthToken] = useState(null);
  const [user, setUser] = useState(null);
  const [currentScreen, setCurrentScreen] = useState('LOGIN'); // LOGIN, DASHBOARD, SYLLABUS

  const handleLoginSuccess = (token, userData) => {
    setAuthToken(token);
    setUser(userData);
    setCurrentScreen('DASHBOARD');
  };

  const handleLogout = () => {
    setAuthToken(null);
    setUser(null);
    setCurrentScreen('LOGIN');
  };

  const renderScreen = () => {
    switch (currentScreen) {
      case 'LOGIN':
        return <LoginScreen onLoginSuccess={handleLoginSuccess} />;
      case 'DASHBOARD':
        return (
          <DashboardScreen 
            user={user} 
            authToken={authToken} 
            onLogout={handleLogout} 
            onNavigate={() => setCurrentScreen('SYLLABUS')}
          />
        );
      case 'SYLLABUS':
        return (
          <SyllabusScreen 
            authToken={authToken} 
            onBack={() => setCurrentScreen('DASHBOARD')} 
          />
        );
      default:
        return <LoginScreen onLoginSuccess={handleLoginSuccess} />;
    }
  };

  return (
    <View style={styles.container}>
      <StatusBar style="dark" />
      {renderScreen()}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
});
