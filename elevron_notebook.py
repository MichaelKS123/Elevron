# Elevron: Space Launch Exploratory Analysis
# Author: Michael Semera
# Interactive notebook for exploring space launch data

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Visualization settings - Space theme
plt.rcParams['figure.facecolor'] = '#0a0e27'
plt.rcParams['axes.facecolor'] = '#0f1419'
plt.rcParams['text.color'] = 'white'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'
plt.rcParams['figure.figsize'] = (14, 6)
plt.rcParams['font.size'] = 11

print("="*80)
print("🚀 ELEVRON: Space Launch Exploratory Analysis")
print("Author: Michael Semera")
print("="*80)

# ============================================================================
# SECTION 1: DATA LOADING AND INITIAL EXPLORATION
# ============================================================================

print("\n[SECTION 1] Loading and Exploring Data\n")

# Load dataset
df = pd.read_csv('data/space_launches.csv', low_memory=False)

print(f"Dataset loaded: {df.shape[0]:,} rows × {df.shape[1]} columns\n")

# Display first few rows
print("First 5 records:")
display(df.head())

# Basic information
print("\n" + "="*80)
print("DATASET INFORMATION")
print("="*80)
df.info()

# Column names
print("\nAvailable Columns:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i:2d}. {col}")

# ============================================================================
# SECTION 2: DATA QUALITY ASSESSMENT
# ============================================================================

print("\n" + "="*80)
print("[SECTION 2] Data Quality Assessment")
print("="*80)

# Missing values analysis
missing_data = pd.DataFrame({
    'Column': df.columns,
    'Missing_Count': df.isnull().sum(),
    'Missing_Percentage': (df.isnull().sum() / len(df) * 100).round(2)
})
missing_data = missing_data[missing_data['Missing_Count'] > 0].sort_values(
    'Missing_Count', ascending=False
)

print("\nColumns with Missing Values:")
display(missing_data)

# Visualize missing data
if len(missing_data) > 0:
    fig, ax = plt.subplots(figsize=(12, 6), facecolor='#0a0e27')
    ax.set_facecolor('#0f1419')
    ax.barh(missing_data['Column'], missing_data['Missing_Percentage'], color='#00d9ff')
    ax.set_xlabel('Percentage Missing (%)', color='white', fontweight='bold')
    ax.set_ylabel('Column', color='white', fontweight='bold')
    ax.set_title('Missing Data by Column', color='white', fontweight='bold', fontsize=14)
    plt.tight_layout()
    plt.show()

# ============================================================================
# SECTION 3: TEMPORAL ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("[SECTION 3] Temporal Analysis")
print("="*80)

# Find date column
date_cols = [col for col in df.columns if 'date' in col.lower()]
print(f"\nDate-related columns found: {date_cols}")

if date_cols:
    date_col = date_cols[0]
    df['launch_date_parsed'] = pd.to_datetime(df[date_col], errors='coerce')
    df['launch_year'] = df['launch_date_parsed'].dt.year
    
    # Filter reasonable years
    df_years = df[(df['launch_year'] >= 1957) & (df['launch_year'] <= 2023)]
    
    print(f"\nLaunch Statistics:")
    print(f"  First Launch: {df_years['launch_year'].min():.0f}")
    print(f"  Last Launch: {df_years['launch_year'].max():.0f}")
    print(f"  Total Years: {df_years['launch_year'].max() - df_years['launch_year'].min():.0f}")
    
    # Launches per year
    yearly_counts = df_years['launch_year'].value_counts().sort_index()
    
    fig, axes = plt.subplots(2, 1, figsize=(16, 10), facecolor='#0a0e27')
    
    # Line chart
    ax1 = axes[0]
    ax1.set_facecolor('#0f1419')
    ax1.plot(yearly_counts.index, yearly_counts.values, color='#00d9ff', 
            linewidth=2, marker='o', markersize=4)
    ax1.fill_between(yearly_counts.index, yearly_counts.values, alpha=0.3, color='#00d9ff')
    ax1.set_xlabel('Year', color='white', fontweight='bold')
    ax1.set_ylabel('Number of Launches', color='white', fontweight='bold')
    ax1.set_title('Annual Launch Frequency (1957-2023)', color='white', 
                 fontweight='bold', fontsize=14, pad=15)
    ax1.grid(alpha=0.2, color='white')
    
    # Add era annotations
    ax1.axvspan(1957, 1975, alpha=0.1, color='red', label='Space Race')
    ax1.axvspan(1976, 2010, alpha=0.1, color='yellow', label='Shuttle Era')
    ax1.axvspan(2011, 2023, alpha=0.1, color='green', label='New Space')
    ax1.legend(facecolor='#1a1f3a', edgecolor='white', labelcolor='white')
    
    # Bar chart by decade
    ax2 = axes[1]
    ax2.set_facecolor('#0f1419')
    decades = df_years.groupby(df_years['launch_year'] // 10 * 10).size()
    colors = plt.cm.plasma(np.linspace(0, 1, len(decades)))
    bars = ax2.bar(decades.index, decades.values, width=8, color=colors, 
                  edgecolor='white', linewidth=0.5)
    ax2.set_xlabel('Decade', color='white', fontweight='bold')
    ax2.set_ylabel('Total Launches', color='white', fontweight='bold')
    ax2.set_title('Launches by Decade', color='white', fontweight='bold', 
                 fontsize=14, pad=15)
    ax2.grid(alpha=0.2, color='white', axis='y')
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, height,
                f'{int(height)}', ha='center', va='bottom',
                color='white', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.show()
    
    print("\nTop 5 Years by Launch Count:")
    print(yearly_counts.sort_values(ascending=False).head())

# ============================================================================
# SECTION 4: ORGANIZATION ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("[SECTION 4] Organization Analysis")
print("="*80)

# Find organization column
org_cols = [col for col in df.columns if any(
    keyword in col.lower() for keyword in ['company', 'organisation', 'organization']
)]
print(f"\nOrganization-related columns: {org_cols}")

if org_cols:
    org_col = org_cols[0]
    
    print(f"\nTop 15 Organizations by Launch Count:")
    top_orgs = df[org_col].value_counts().head(15)
    print(top_orgs)
    
    fig, ax = plt.subplots(figsize=(14, 8), facecolor='#0a0e27')
    ax.set_facecolor('#0f1419')
    
    y_pos = np.arange(len(top_orgs))
    colors = plt.cm.viridis(np.linspace(0, 1, len(top_orgs)))
    bars = ax.barh(y_pos, top_orgs.values, color=colors, edgecolor='white', linewidth=0.5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(top_orgs.index, color='white', fontsize=10)
    ax.set_xlabel('Number of Launches', color='white', fontweight='bold')
    ax.set_title('Top 15 Organizations by Launch Count', color='white', 
                fontweight='bold', fontsize=14, pad=15)
    ax.invert_yaxis()
    ax.grid(alpha=0.2, color='white', axis='x')
    
    # Add value labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2,
               f' {int(width)}', ha='left', va='center',
               color='white', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.show()
    
    # Organization growth over time
    if 'launch_year' in df.columns:
        print("\n📈 Organization Activity by Era:")
        
        eras = {
            'Space Race (1957-1975)': (1957, 1975),
            'Shuttle Era (1976-2010)': (1976, 2010),
            'New Space (2011-2023)': (2011, 2023)
        }
        
        for era_name, (start, end) in eras.items():
            era_data = df[(df['launch_year'] >= start) & (df['launch_year'] <= end)]
            top_3 = era_data[org_col].value_counts().head(3)
            print(f"\n  {era_name}:")
            for i, (org, count) in enumerate(top_3.items(), 1):
                print(f"    {i}. {org}: {count} launches")

# ============================================================================
# SECTION 5: MISSION STATUS ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("[SECTION 5] Mission Status Analysis")
print("="*80)

# Find status column
status_cols = [col for col in df.columns if 'status' in col.lower()]
print(f"Status-related columns: {status_cols}")

if status_cols:
    status_col = status_cols[0]
    
    print(f"\nMission Status Distribution:")
    status_counts = df[status_col].value_counts()
    print(status_counts)
    
    # Calculate overall success rate
    success_keywords = ['success', 'successful']
    total_launches = len(df[df[status_col].notna()])
    successful = df[status_col].str.lower().str.contains('|'.join(success_keywords), na=False).sum()
    success_rate = (successful / total_launches * 100) if total_launches > 0 else 0
    
    print(f"\n🎯 Overall Success Rate: {success_rate:.1f}%")
    print(f"   Successful: {successful:,}")
    print(f"   Total: {total_launches:,}")
    
    # Pie chart
    fig, axes = plt.subplots(1, 2, figsize=(16, 7), facecolor='#0a0e27')
    
    # Status distribution
    ax1 = axes[0]
    ax1.set_facecolor('#0f1419')
    colors_pie = ['#00d9ff', '#ff6b6b', '#4ecdc4', '#95e1d3']
    wedges, texts, autotexts = ax1.pie(status_counts.values, labels=status_counts.index,
                                       autopct='%1.1f%%', startangle=90, colors=colors_pie,
                                       textprops={'color': 'white', 'fontsize': 10, 'weight': 'bold'})
    ax1.set_title('Launch Outcome Distribution', color='white', fontweight='bold', 
                 fontsize=13, pad=15)
    
    # Success rate over time
    if 'launch_year' in df.columns:
        ax2 = axes[1]
        ax2.set_facecolor('#0f1419')
        
        yearly_success = df.groupby('launch_year').apply(
            lambda x: (x[status_col].str.lower().str.contains('success', na=False).sum() / 
                      len(x) * 100) if len(x) > 0 else 0
        )
        
        ax2.plot(yearly_success.index, yearly_success.values, color='#00d9ff',
                linewidth=2, marker='o', markersize=4)
        ax2.axhline(y=success_rate, color='#ff6b6b', linestyle='--', linewidth=2,
                   label=f'Overall Average: {success_rate:.1f}%')
        ax2.set_xlabel('Year', color='white', fontweight='bold')
        ax2.set_ylabel('Success Rate (%)', color='white', fontweight='bold')
        ax2.set_title('Success Rate Trend Over Time', color='white', fontweight='bold',
                     fontsize=13, pad=15)
        ax2.legend(facecolor='#1a1f3a', edgecolor='white', labelcolor='white')
        ax2.grid(alpha=0.2, color='white')
        ax2.set_ylim([0, 105])
    
    plt.tight_layout()
    plt.show()

# ============================================================================
# SECTION 6: ROCKET ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("[SECTION 6] Rocket Analysis")
print("="*80)

# Find rocket column
rocket_cols = [col for col in df.columns if 'rocket' in col.lower()]
print(f"Rocket-related columns: {rocket_cols}")

if rocket_cols:
    rocket_col = rocket_cols[0]
    
    print(f"\nTop 15 Most-Launched Rockets:")
    top_rockets = df[rocket_col].value_counts().head(15)
    print(top_rockets)
    
    fig, ax = plt.subplots(figsize=(14, 8), facecolor='#0a0e27')
    ax.set_facecolor('#0f1419')
    
    colors_rocket = plt.cm.plasma(np.linspace(0, 1, len(top_rockets)))
    bars = ax.bar(range(len(top_rockets)), top_rockets.values, color=colors_rocket,
                 edgecolor='white', linewidth=0.5)
    ax.set_xticks(range(len(top_rockets)))
    ax.set_xticklabels(top_rockets.index, rotation=45, ha='right', color='white', fontsize=9)
    ax.set_ylabel('Number of Launches', color='white', fontweight='bold')
    ax.set_title('Top 15 Most-Launched Rockets', color='white', fontweight='bold',
                fontsize=14, pad=15)
    ax.grid(alpha=0.2, color='white', axis='y')
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height,
               f'{int(height)}', ha='center', va='bottom',
               color='white', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.show()
    
    # Rocket success rates (for rockets with 10+ launches)
    if status_col in df.columns:
        print(f"\n⭐ Most Reliable Rockets (10+ launches):")
        
        rocket_success = df.groupby(rocket_col).agg({
            rocket_col: 'count',
            status_col: lambda x: (x.str.lower().str.contains('success', na=False).sum() / 
                                  len(x) * 100) if len(x) > 0 else 0
        })
        rocket_success.columns = ['launches', 'success_rate']
        rocket_success = rocket_success[rocket_success['launches'] >= 10]
        rocket_success = rocket_success.sort_values('success_rate', ascending=False).head(10)
        
        for i, (rocket, row) in enumerate(rocket_success.iterrows(), 1):
            print(f"  {i:2d}. {rocket:30s} | {row['success_rate']:5.1f}% | {int(row['launches'])} launches")

# ============================================================================
# SECTION 7: GEOGRAPHIC ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("[SECTION 7] Geographic Analysis")
print("="*80)

# Find location column
location_cols = [col for col in df.columns if any(
    keyword in col.lower() for keyword in ['location', 'country', 'site']
)]
print(f"Location-related columns: {location_cols}")

if location_cols:
    location_col = location_cols[0]
    
    print(f"\nTop 15 Launch Locations:")
    top_locations = df[location_col].value_counts().head(15)
    print(top_locations)
    
    fig, ax = plt.subplots(figsize=(14, 8), facecolor='#0a0e27')
    ax.set_facecolor('#0f1419')
    
    y_pos = np.arange(len(top_locations))
    colors_loc = plt.cm.coolwarm(np.linspace(0, 1, len(top_locations)))
    bars = ax.barh(y_pos, top_locations.values, color=colors_loc, 
                  edgecolor='white', linewidth=0.5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(top_locations.index, color='white', fontsize=10)
    ax.set_xlabel('Number of Launches', color='white', fontweight='bold')
    ax.set_title('Top 15 Launch Locations', color='white', fontweight='bold',
                fontsize=14, pad=15)
    ax.invert_yaxis()
    ax.grid(alpha=0.2, color='white', axis='x')
    
    plt.tight_layout()
    plt.show()

# ============================================================================
# SECTION 8: PRIVATE VS GOVERNMENT CLASSIFICATION
# ============================================================================

print("\n" + "="*80)
print("[SECTION 8] Private vs Government Classification")
print("="*80)

def classify_organization(org_name):
    """Classify organization as private or government."""
    if pd.isna(org_name):
        return 'Unknown'
    
    org_lower = str(org_name).lower()
    
    private_indicators = ['spacex', 'blue origin', 'rocket lab', 'virgin', 
                         'arianespace', 'united launch alliance', 'ula']
    government_indicators = ['nasa', 'roscosmos', 'cnsa', 'isro', 'jaxa', 
                            'air force', 'navy', 'military', 'space forces']
    
    for indicator in private_indicators:
        if indicator in org_lower:
            return 'Private'
    
    for indicator in government_indicators:
        if indicator in org_lower:
            return 'Government'
    
    return 'Unknown'

if org_col in df.columns:
    df['sector'] = df[org_col].apply(classify_organization)
    
    print("\nSector Distribution:")
    sector_counts = df['sector'].value_counts()
    print(sector_counts)
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 7), facecolor='#0a0e27')
    
    # Pie chart
    ax1 = axes[0]
    ax1.set_facecolor('#0f1419')
    colors_sector = ['#00d9ff', '#ff6b6b', '#95e1d3']
    wedges, texts, autotexts = ax1.pie(sector_counts.values, labels=sector_counts.index,
                                       autopct='%1.1f%%', startangle=90, colors=colors_sector,
                                       textprops={'color': 'white', 'fontsize': 11, 'weight': 'bold'})
    ax1.set_title('Launch Distribution by Sector', color='white', fontweight='bold',
                 fontsize=13, pad=15)
    
    # Success rate comparison
    if status_col in df.columns:
        ax2 = axes[1]
        ax2.set_facecolor('#0f1419')
        
        sector_success = df.groupby('sector').apply(
            lambda x: (x[status_col].str.lower().str.contains('success', na=False).sum() / 
                      len(x) * 100) if len(x) > 0 else 0
        ).sort_values(ascending=False)
        
        bars = ax2.bar(range(len(sector_success)), sector_success.values,
                      color=colors_sector, edgecolor='white', linewidth=1)
        ax2.set_xticks(range(len(sector_success)))
        ax2.set_xticklabels(sector_success.index, color='white', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Success Rate (%)', color='white', fontweight='bold')
        ax2.set_title('Success Rate by Sector', color='white', fontweight='bold',
                     fontsize=13, pad=15)
        ax2.grid(alpha=0.2, color='white', axis='y')
        ax2.set_ylim([0, 105])
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2, height,
                    f'{height:.1f}%', ha='center', va='bottom',
                    color='white', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.show()

# ============================================================================
# SECTION 9: EXPORT CLEANED DATA
# ============================================================================

print("\n" + "="*80)
print("[SECTION 9] Exporting Cleaned Data")
print("="*80)

# Save cleaned dataset
output_file = 'data/space_launches_cleaned.csv'
df.to_csv(output_file, index=False)
print(f"\n✓ Cleaned dataset exported to: {output_file}")
print(f"  Rows: {len(df):,}")
print(f"  Columns: {len(df.columns)}")

print("\n" + "="*80)
print("✅ EXPLORATORY ANALYSIS COMPLETE!")
print("="*80)
print("\nKey Insights:")
print("1. Review the temporal trends to understand space industry evolution")
print("2. Note the shift from government to private sector launches")
print("3. Observe success rate improvements over time")
print("4. Identify leading organizations and rocket families")
print("\nNext Steps:")
print("- Run the main elevron_analysis.py script")
print("- Create Tableau dashboard with cleaned data")
print("- Document findings for portfolio")
print("="*80)