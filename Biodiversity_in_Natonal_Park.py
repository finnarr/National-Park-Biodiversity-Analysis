
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr

# Load the datasets
species_info_path = 'species_info.csv'
observations_path = 'observations.csv'
species_info_df = pd.read_csv('species_info.csv', encoding='utf-8')
observations_df = pd.read_csv('observations.csv', encoding='utf-8')

# Data Cleaning
species_info_df['conservation_status'].fillna('Not Evaluated', inplace=True)
merged_df = pd.merge(observations_df, species_info_df, on='scientific_name', how='left')

# Analysis and Visualization

# 1. Distribution of Species Categories
category_distribution = merged_df['category'].value_counts()
plt.figure(figsize=(10, 6))
sns.barplot(x=category_distribution.index, y=category_distribution.values, palette="viridis")
plt.title('Distribution of Species Categories')
plt.xlabel('Category')
plt.ylabel('Number of Records')
plt.xticks(rotation=45)
plt.show()

# 2. Conservation Status Distribution
conservation_status_distribution = merged_df['conservation_status'].value_counts()
plt.figure(figsize=(10, 6))
sns.barplot(x=conservation_status_distribution.index, y=conservation_status_distribution.values, palette="muted")
plt.title('Distribution of Conservation Statuses')
plt.xlabel('Conservation Status')
plt.ylabel('Number of Records')
plt.xticks(rotation=45)
plt.show()

# 3. Observations in National Parks
park_observations_distribution = merged_df.groupby('park_name')['observations'].sum().sort_values(ascending=False)
plt.figure(figsize=(10, 6))
sns.barplot(x=park_observations_distribution.index, y=park_observations_distribution.values, palette="rocket")
plt.title('Total Observations in Each National Park')
plt.xlabel('National Park')
plt.ylabel('Total Observations')
plt.xticks(rotation=45)
plt.show()

# 4. Relationship Between Observations and Conservation Status
conservation_status_ranking = {
    'Not Evaluated': 0, 'Least Concern': 1, 'Near Threatened': 2, 'Vulnerable': 3,
    'Endangered': 4, 'Critically Endangered': 5, 'Extinct in the Wild': 6,
    'Extinct': 7, 'In Recovery': 8
}
merged_df['conservation_status_num'] = merged_df['conservation_status'].map(conservation_status_ranking)
correlation, p_value = spearmanr(merged_df['observations'], merged_df['conservation_status_num'])
print('Correlation Coefficient:', correlation)
print('P-value:', p_value)

# Endangered Species Analysis
endangered_statuses = ["Endangered", "Threatened", "Vulnerable", "In Recovery"]
endangered_species_df = merged_df[merged_df['conservation_status'].isin(endangered_statuses)]
endangered_species_category_distribution = endangered_species_df['category'].value_counts()
plt.figure(figsize=(10, 6))
sns.barplot(x=endangered_species_category_distribution.index, y=endangered_species_category_distribution.values, palette="colorblind")
plt.title('Distribution of Endangered Species Across Categories')
plt.xlabel('Category')
plt.ylabel('Number of Endangered Species')
plt.xticks(rotation=45)
plt.show()

# Park-Specific Biodiversity Analysis
unique_species_per_park = merged_df.groupby('park_name')['scientific_name'].nunique().sort_values(ascending=False)
endangered_species_per_park = endangered_species_df.groupby('park_name')['scientific_name'].nunique().sort_values(ascending=False)
park_biodiversity_df = pd.DataFrame({
    'Total Unique Species': unique_species_per_park,
    'Endangered Species': endangered_species_per_park
}).reset_index()
plt.figure(figsize=(12, 6))
sns.barplot(x='park_name', y='Total Unique Species', data=park_biodiversity_df, color='lightblue', label='Total Unique Species')
sns.barplot(x='park_name', y='Endangered Species', data=park_biodiversity_df, color='salmon', label='Endangered Species')
plt.title('Park-Specific Biodiversity: Total vs Endangered Species')
plt.xlabel('National Park')
plt.ylabel('Number of Species')
plt.legend()
plt.xticks(rotation=45)
plt.show()
