import React, { useState, useEffect } from 'react';
import {
  StyleSheet,
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  SafeAreaView,
  RefreshControl,
  ActivityIndicator,
} from 'react-native';
import { BookOpen, Award, Flame, LogOut, ChevronRight } from 'lucide-react-native';
import { COLORS, SPACING, SIZES } from '../theme/theme';
import apiClient from '../api/client';

const DashboardScreen = ({ user, authToken, onLogout }) => {
  const [stats, setStats] = useState({
    streak: 0,
    study_minutes: 0,
    categories_completed: 0
  });
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const fetchStats = async () => {
    try {
      const response = await apiClient.get('/profile/', {
        headers: { Authorization: `Token ${authToken}` }
      });
      setStats({
        streak: response.data.streak_count,
        study_minutes: response.data.total_study_minutes,
        categories_completed: 0 // We'll add this logic later
      });
    } catch (error) {
      console.error('Error fetching stats:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    fetchStats();
  };

  const StatCard = ({ icon: Icon, label, value, color }) => (
    <View style={styles.statCard}>
      <View style={[styles.statIcon, { backgroundColor: color + '15' }]}>
        <Icon size={24} color={color} />
      </View>
      <View>
        <Text style={styles.statValue}>{value}</Text>
        <Text style={styles.statLabel}>{label}</Text>
      </View>
    </View>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <View>
          <Text style={styles.welcomeText}>Welcome back,</Text>
          <Text style={styles.userName}>{user.first_name || user.username}!</Text>
        </View>
        <TouchableOpacity style={styles.logoutButton} onPress={onLogout}>
          <LogOut size={20} color={COLORS.error} />
        </TouchableOpacity>
      </View>

      <ScrollView 
        style={styles.content}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
      >
        <View style={styles.statsGrid}>
          <StatCard 
            icon={Flame} 
            label="Day Streak" 
            value={stats.streak} 
            color="#ff5400" 
          />
          <StatCard 
            icon={BookOpen} 
            label="Study Mins" 
            value={stats.study_minutes} 
            color={COLORS.primary} 
          />
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Continue Learning</Text>
          <TouchableOpacity style={styles.mainAction} activeOpacity={0.8}>
            <View style={styles.actionIconContainer}>
              <BookOpen size={28} color={COLORS.white} />
            </View>
            <View style={styles.actionTextContainer}>
              <Text style={styles.actionTitle}>Syllabus Browser</Text>
              <Text style={styles.actionSubtitle}>Mathematics, Physics, Chemistry & more</Text>
            </View>
            <ChevronRight size={24} color={COLORS.textSecondary} />
          </TouchableOpacity>
        </View>

        <View style={styles.infoBox}>
          <Award size={24} color={COLORS.primary} />
          <Text style={styles.infoText}>
            You're doing great! Complete your daily goal to increase your streak.
          </Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: SPACING.xl,
    paddingVertical: SPACING.lg,
    backgroundColor: COLORS.surface,
  },
  welcomeText: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
  userName: {
    fontSize: 22,
    fontWeight: 'bold',
    color: COLORS.secondary,
  },
  logoutButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: COLORS.error + '10',
    justifyContent: 'center',
    alignItems: 'center',
  },
  content: {
    flex: 1,
    padding: SPACING.lg,
  },
  statsGrid: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: SPACING.lg,
  },
  statCard: {
    flex: 0.48,
    backgroundColor: COLORS.surface,
    borderRadius: SIZES.radius,
    padding: SPACING.md,
    flexDirection: 'row',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
  },
  statIcon: {
    width: 44,
    height: 44,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: SPACING.sm,
  },
  statValue: {
    fontSize: 18,
    fontWeight: 'bold',
    color: COLORS.text,
  },
  statLabel: {
    fontSize: 12,
    color: COLORS.textSecondary,
  },
  section: {
    marginTop: SPACING.md,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: COLORS.secondary,
    marginBottom: SPACING.md,
  },
  mainAction: {
    backgroundColor: COLORS.surface,
    borderRadius: SIZES.radius,
    padding: SPACING.lg,
    flexDirection: 'row',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
  },
  actionIconContainer: {
    width: 56,
    height: 56,
    borderRadius: 16,
    backgroundColor: COLORS.primary,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: SPACING.md,
  },
  actionTextContainer: {
    flex: 1,
  },
  actionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: COLORS.text,
  },
  actionSubtitle: {
    fontSize: 12,
    color: COLORS.textSecondary,
    marginTop: 2,
  },
  infoBox: {
    backgroundColor: COLORS.primary + '10',
    borderRadius: SIZES.radius,
    padding: SPACING.md,
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: SPACING.xl,
    borderWidth: 1,
    borderColor: COLORS.primary + '20',
  },
  infoText: {
    flex: 1,
    fontSize: 13,
    color: COLORS.secondary,
    marginLeft: SPACING.sm,
    lineHeight: 18,
  },
});

export default DashboardScreen;
