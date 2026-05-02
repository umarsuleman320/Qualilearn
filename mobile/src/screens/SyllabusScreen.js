import React, { useState, useEffect } from 'react';
import {
  StyleSheet,
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  SafeAreaView,
  ActivityIndicator,
  FlatList,
} from 'react-native';
import { ChevronLeft, CheckCircle, Circle, ExternalLink } from 'lucide-react-native';
import { COLORS, SPACING, SIZES } from '../theme/theme';
import apiClient from '../api/client';

const SyllabusScreen = ({ authToken, onBack }) => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchSyllabus = async () => {
    try {
      const response = await apiClient.get('/syllabus/', {
        headers: { Authorization: `Token ${authToken}` }
      });
      setCategories(response.data);
    } catch (error) {
      console.error('Error fetching syllabus:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSyllabus();
  }, []);

  const toggleTopic = async (topicId) => {
    try {
      await apiClient.post(`/syllabus/toggle/${topicId}/`, {}, {
        headers: { Authorization: `Token ${authToken}` }
      });
      // Optimized: just re-fetch to show updated state
      fetchSyllabus();
    } catch (error) {
      console.error('Error toggling topic:', error);
    }
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={COLORS.primary} />
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={onBack} style={styles.backButton}>
          <ChevronLeft size={24} color={COLORS.secondary} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Syllabus Browser</Text>
        <View style={{ width: 24 }} />
      </View>

      <ScrollView style={styles.content}>
        {categories.map((category) => (
          <View key={category.id} style={styles.categoryCard}>
            <View style={styles.categoryHeader}>
              <Text style={styles.categoryName}>{category.name}</Text>
              <View style={styles.progressBar}>
                <View style={[styles.progressFill, { width: `${category.percentage}%` }]} />
              </View>
              <Text style={styles.progressText}>{category.percentage}% Complete</Text>
            </View>

            <View style={styles.topicsList}>
              {category.topics.map((topic) => (
                <View key={topic.id} style={styles.topicItem}>
                  <TouchableOpacity 
                    style={styles.topicCheck} 
                    onPress={() => toggleTopic(topic.id)}
                  >
                    {topic.is_completed ? (
                      <CheckCircle size={24} color={COLORS.success} />
                    ) : (
                      <Circle size={24} color={COLORS.textSecondary} />
                    )}
                  </TouchableOpacity>
                  <View style={styles.topicInfo}>
                    <Text style={[
                      styles.topicName,
                      topic.is_completed && styles.topicNameCompleted
                    ]}>
                      {topic.name}
                    </Text>
                  </View>
                  <TouchableOpacity style={styles.youtubeLink}>
                    <ExternalLink size={18} color={COLORS.primary} />
                  </TouchableOpacity>
                </View>
              ))}
            </View>
          </View>
        ))}
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: SPACING.md,
    backgroundColor: COLORS.surface,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: COLORS.secondary,
  },
  backButton: {
    padding: 4,
  },
  content: {
    padding: SPACING.md,
  },
  categoryCard: {
    backgroundColor: COLORS.surface,
    borderRadius: SIZES.radius,
    marginBottom: SPACING.md,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
  },
  categoryHeader: {
    padding: SPACING.md,
    backgroundColor: COLORS.secondary + '05',
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
  },
  categoryName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: COLORS.secondary,
    marginBottom: SPACING.sm,
  },
  progressBar: {
    height: 6,
    backgroundColor: COLORS.border,
    borderRadius: 3,
    marginBottom: 4,
  },
  progressFill: {
    height: '100%',
    backgroundColor: COLORS.primary,
    borderRadius: 3,
  },
  progressText: {
    fontSize: 11,
    color: COLORS.textSecondary,
    fontWeight: '600',
  },
  topicsList: {
    paddingVertical: SPACING.sm,
  },
  topicItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.md,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border + '50',
  },
  topicCheck: {
    marginRight: SPACING.md,
  },
  topicInfo: {
    flex: 1,
  },
  topicName: {
    fontSize: 15,
    color: COLORS.text,
  },
  topicNameCompleted: {
    color: COLORS.textSecondary,
    textDecorationLine: 'line-through',
  },
  youtubeLink: {
    padding: 8,
  },
});

export default SyllabusScreen;
