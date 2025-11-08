"""
Elevron: Space Exploration & Launch Data Analysis
Author: Michael Semera
Description: Analyzes global rocket launch trends, comparing private vs government
             sector performance across success rates, cost efficiency, and innovation.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configure visualization aesthetics
sns.set_style("darkgrid")
plt.rcParams['figure.facecolor'] = '#0a0e27'
plt.rcParams['axes.facecolor'] = '#0f1419'
plt.rcParams['text.color'] = 'white'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'
plt.rcParams['figure.dpi'] = 100


class SpaceLaunchAnalyzer:
    """
    Comprehensive analyzer for space launch data.
    Compares private vs government sector performance across multiple dimensions.
    """
    
    def __init__(self, data_path):
        """Initialize analyzer with space launch dataset."""
        self.df = pd.read_csv(data_path)
        self.private_companies = []
        self.government_agencies = []
        self.performance_metrics = {}
        
        print("="*80)
        print("🚀 ELEVRON: Space Launch Analysis System")
        print("Author: Michael Semera")
        print("="*80)
        
    def preprocess_data(self):
        """Clean and standardize space launch data."""
        print("\n[1/9] Preprocessing launch data...")
        
        # Standardize column names
        self.df.columns = self.df.columns.str.lower().str.strip().str.replace(' ', '_')
        
        # Parse dates
        date_cols = [col for col in self.df.columns if 'date' in col]
        for col in date_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
        
        # Extract year from launch date
        if 'date' in self.df.columns:
            self.df['launch_year'] = pd.to_datetime(self.df['date']).dt.year
        elif 'launch_date' in self.df.columns:
            self.df['launch_year'] = pd.to_datetime(self.df['launch_date']).dt.year
        
        # Standardize company/agency names
        if 'company_name' in self.df.columns:
            self.df['organization'] = self.df['company_name'].str.strip()
        elif 'organisation' in self.df.columns:
            self.df['organization'] = self.df['organisation'].str.strip()
        elif 'company' in self.df.columns:
            self.df['organization'] = self.df['company'].str.strip()
        
        # Standardize rocket names
        if 'rocket' in self.df.columns:
            self.df['rocket_name'] = self.df['rocket'].str.strip()
        elif 'rocket_name' in self.df.columns:
            self.df['rocket_name'] = self.df['rocket_name'].str.strip()
        
        # Standardize status/mission_status
        status_col = self._find_column(['status', 'mission_status', 'launch_status'])
        if status_col:
            self.df['launch_status'] = self.df[status_col].str.lower().str.strip()
            self.df['is_successful'] = self.df['launch_status'].isin(
                ['success', 'successful', 'partial failure']
            )
        
        # Classify organization type
        self.df['org_type'] = self.df['organization'].apply(self._classify_organization)
        
        # Parse cost data if available
        cost_cols = [col for col in self.df.columns if 'price' in col or 'cost' in col]
        if cost_cols:
            self.df['launch_cost'] = self._parse_currency(self.df[cost_cols[0]])
        
        # Extract location/country
        location_cols = [col for col in self.df.columns if 'location' in col or 'country' in col]
        if location_cols:
            self.df['launch_country'] = self._extract_country(self.df[location_cols[0]])
        
        print(f"✓ Preprocessed {len(self.df):,} launch records")
        print(f"✓ Date range: {self.df['launch_year'].min():.0f} - {self.df['launch_year'].max():.0f}")
        print(f"✓ Success rate: {self.df['is_successful'].mean()*100:.1f}%")
        
        return self
    
    def _find_column(self, possible_names):
        """Find first matching column from list of possibilities."""
        for name in possible_names:
            if name in self.df.columns:
                return name
        return None
    
    def _classify_organization(self, org_name):
        """Classify organization as private, government, or international."""
        if pd.isna(org_name):
            return 'Unknown'
        
        org_lower = str(org_name).lower()
        
        # Private companies
        private_indicators = [
            'spacex', 'space x', 'blue origin', 'rocket lab', 'virgin orbit',
            'virgin galactic', 'northrop grumman', 'united launch alliance',
            'ula', 'arianespace', 'sea launch', 'orbital atk', 'relativity',
            'astra', 'firefly', 'ispace', 'landspace', 'galactic energy',
            'expace', 'linkspace', 'oneweb'
        ]
        
        # Government agencies
        government_indicators = [
            'nasa', 'roscosmos', 'cnsa', 'isro', 'jaxa', 'esa', 
            'russian space forces', 'us air force', 'us navy', 'us space force',
            'iranian space agency', 'korean aerospace', 'france', 'soviet',
            'ministry of defence', 'armed forces', 'military'
        ]
        
        # International organizations
        international_indicators = [
            'international', 'multinational', 'esa', 'eumetsat'
        ]
        
        for indicator in private_indicators:
            if indicator in org_lower:
                return 'Private'
        
        for indicator in international_indicators:
            if indicator in org_lower:
                return 'International'
        
        for indicator in government_indicators:
            if indicator in org_lower:
                return 'Government'
        
        # Default heuristic: if contains "space" or specific tech company patterns
        if any(word in org_lower for word in ['space', 'aerospace', 'technologies', 'industries']):
            return 'Private'
        
        return 'Government'
    
    def _parse_currency(self, series):
        """Parse currency values from strings."""
        def clean_value(val):
            if pd.isna(val):
                return np.nan
            
            val_str = str(val).replace('$', '').replace(',', '').strip()
            
            try:
                if 'million' in val_str.lower() or 'm' in val_str.lower():
                    return float(val_str.split()[0]) * 1e6
                elif 'billion' in val_str.lower() or 'b' in val_str.lower():
                    return float(val_str.split()[0]) * 1e9
                else:
                    return float(val_str)
            except:
                return np.nan
        
        return series.apply(clean_value)
    
    def _extract_country(self, series):
        """Extract country from location string."""
        def get_country(location):
            if pd.isna(location):
                return 'Unknown'
            
            location_str = str(location)
            
            # Common patterns
            if ',' in location_str:
                return location_str.split(',')[-1].strip()
            
            # Known launch sites
            country_map = {
                'kennedy': 'USA', 'cape canaveral': 'USA', 'vandenberg': 'USA',
                'baikonur': 'Kazakhstan', 'plesetsk': 'Russia', 'vostochny': 'Russia',
                'kourou': 'French Guiana', 'jiuquan': 'China', 'xichang': 'China',
                'taiyuan': 'China', 'wenchang': 'China', 'tanegashima': 'Japan',
                'satish dhawan': 'India', 'sriharikota': 'India', 'wallops': 'USA',
                'mahia': 'New Zealand', 'palmachim': 'Israel'
            }
            
            location_lower = location_str.lower()
            for key, country in country_map.items():
                if key in location_lower:
                    return country
            
            return 'Other'
        
        return series.apply(get_country)
    
    def analyze_sector_performance(self):
        """Compare private vs government sector launch performance."""
        print("\n[2/9] Analyzing sector performance...")
        
        sector_metrics = self.df.groupby('org_type').agg({
            'organization': 'count',
            'is_successful': ['sum', 'mean'],
            'launch_year': ['min', 'max']
        })
        
        sector_metrics.columns = ['total_launches', 'successful_launches', 
                                  'success_rate', 'first_launch', 'last_launch']
        sector_metrics['success_rate'] = sector_metrics['success_rate'] * 100
        
        # Calculate failure rate
        sector_metrics['failure_rate'] = 100 - sector_metrics['success_rate']
        
        # Calculate years active
        sector_metrics['years_active'] = (
            sector_metrics['last_launch'] - sector_metrics['first_launch']
        )
        
        # Average launches per year
        sector_metrics['launches_per_year'] = (
            sector_metrics['total_launches'] / sector_metrics['years_active'].replace(0, 1)
        )
        
        self.performance_metrics['sector'] = sector_metrics
        
        print("\n🎯 Sector Performance Comparison:")
        print(sector_metrics[['total_launches', 'success_rate', 'launches_per_year']].to_string())
        
        return self
    
    def analyze_temporal_trends(self):
        """Analyze launch trends over time for each sector."""
        print("\n[3/9] Analyzing temporal trends...")
        
        # Filter to reasonable time range
        df_filtered = self.df[self.df['launch_year'].between(1957, 2023)]
        
        # Launches per year by sector
        yearly_sector = df_filtered.groupby(['launch_year', 'org_type']).agg({
            'organization': 'count',
            'is_successful': 'mean'
        }).reset_index()
        
        yearly_sector.columns = ['year', 'sector', 'launches', 'success_rate']
        yearly_sector['success_rate'] = yearly_sector['success_rate'] * 100
        
        self.performance_metrics['temporal'] = yearly_sector
        
        # Identify growth periods
        recent_years = df_filtered[df_filtered['launch_year'] >= 2010]
        growth_metrics = recent_years.groupby('org_type').agg({
            'organization': 'count'
        })
        
        print("\n📈 Launch Growth (2010-2023):")
        for sector, count in growth_metrics['organization'].items():
            print(f"  {sector}: {count:,} launches")
        
        return self
    
    def analyze_top_players(self, top_n=10):
        """Identify and analyze top organizations in each sector."""
        print(f"\n[4/9] Analyzing top {top_n} organizations...")
        
        # Overall top organizations
        org_metrics = self.df.groupby('organization').agg({
            'organization': 'count',
            'is_successful': ['sum', 'mean'],
            'org_type': 'first'
        })
        
        org_metrics.columns = ['total_launches', 'successful_launches', 
                              'success_rate', 'sector']
        org_metrics['success_rate'] = org_metrics['success_rate'] * 100
        
        # Filter organizations with at least 5 launches
        org_metrics = org_metrics[org_metrics['total_launches'] >= 5]
        org_metrics = org_metrics.sort_values('total_launches', ascending=False)
        
        self.performance_metrics['organizations'] = org_metrics
        
        print("\n🏆 Top 10 Organizations by Launch Count:")
        top_orgs = org_metrics.head(top_n)
        for idx, (org, row) in enumerate(top_orgs.iterrows(), 1):
            print(f"  {idx:2d}. {org:30s} | {int(row['total_launches']):4d} launches | "
                  f"{row['success_rate']:5.1f}% success | {row['sector']}")
        
        # Best success rates (minimum 10 launches)
        best_success = org_metrics[org_metrics['total_launches'] >= 10].sort_values(
            'success_rate', ascending=False
        ).head(5)
        
        print("\n⭐ Highest Success Rates (10+ launches):")
        for idx, (org, row) in enumerate(best_success.iterrows(), 1):
            print(f"  {idx}. {org}: {row['success_rate']:.1f}% ({int(row['total_launches'])} launches)")
        
        return self
    
    def analyze_rocket_families(self):
        """Analyze performance by rocket type/family."""
        print("\n[5/9] Analyzing rocket families...")
        
        if 'rocket_name' not in self.df.columns:
            print("⚠ Rocket name data not available")
            return self
        
        rocket_metrics = self.df.groupby('rocket_name').agg({
            'organization': ['count', 'first'],
            'is_successful': ['sum', 'mean'],
            'org_type': 'first'
        })
        
        rocket_metrics.columns = ['total_launches', 'primary_user', 
                                 'successful_launches', 'success_rate', 'sector']
        rocket_metrics['success_rate'] = rocket_metrics['success_rate'] * 100
        
        # Filter rockets with at least 3 launches
        rocket_metrics = rocket_metrics[rocket_metrics['total_launches'] >= 3]
        rocket_metrics = rocket_metrics.sort_values('total_launches', ascending=False)
        
        print("\n🚀 Top 10 Most-Launched Rockets:")
        for idx, (rocket, row) in enumerate(rocket_metrics.head(10).iterrows(), 1):
            print(f"  {idx:2d}. {rocket:25s} | {int(row['total_launches']):3d} launches | "
                  f"{row['success_rate']:5.1f}% success")
        
        return self
    
    def compare_launch_sites(self):
        """Compare launch site performance and utilization."""
        print("\n[6/9] Comparing launch sites...")
        
        if 'launch_country' not in self.df.columns:
            print("⚠ Launch location data not available")
            return self
        
        country_metrics = self.df.groupby('launch_country').agg({
            'organization': 'count',
            'is_successful': ['sum', 'mean']
        })
        
        country_metrics.columns = ['total_launches', 'successful_launches', 'success_rate']
        country_metrics['success_rate'] = country_metrics['success_rate'] * 100
        country_metrics = country_metrics.sort_values('total_launches', ascending=False)
        
        print("\n🌍 Top 10 Launch Countries:")
        for idx, (country, row) in enumerate(country_metrics.head(10).iterrows(), 1):
            print(f"  {idx:2d}. {country:20s} | {int(row['total_launches']):5d} launches | "
                  f"{row['success_rate']:5.1f}% success")
        
        return self
    
    def calculate_innovation_metrics(self):
        """Calculate innovation metrics: reusability adoption, new entrants."""
        print("\n[7/9] Calculating innovation metrics...")
        
        # Analyze new market entrants over time
        if 'launch_year' in self.df.columns:
            first_launches = self.df.groupby('organization')['launch_year'].min().reset_index()
            first_launches.columns = ['organization', 'first_launch_year']
            
            new_entrants = first_launches.groupby('first_launch_year').size()
            
            print("\n🆕 New Space Organizations by Decade:")
            for decade in range(1960, 2030, 10):
                count = new_entrants[(new_entrants.index >= decade) & 
                                    (new_entrants.index < decade + 10)].sum()
                if count > 0:
                    print(f"  {decade}s: {count} new organizations")
        
        # Analyze SpaceX reusability impact (if data available)
        spacex_data = self.df[self.df['organization'].str.contains('SpaceX', case=False, na=False)]
        if len(spacex_data) > 0:
            print(f"\n🔄 SpaceX Launch Statistics:")
            print(f"  Total Launches: {len(spacex_data)}")
            print(f"  Success Rate: {spacex_data['is_successful'].mean()*100:.1f}%")
            
            # Launches by year
            if 'launch_year' in spacex_data.columns:
                recent_spacex = spacex_data[spacex_data['launch_year'] >= 2015]
                print(f"  Launches since 2015: {len(recent_spacex)}")
        
        return self
    
    def analyze_cost_efficiency(self):
        """Analyze launch cost trends if data available."""
        print("\n[8/9] Analyzing cost efficiency...")
        
        if 'launch_cost' not in self.df.columns:
            print("⚠ Cost data not available in dataset")
            return self
        
        # Remove NaN costs
        df_with_cost = self.df.dropna(subset=['launch_cost'])
        
        if len(df_with_cost) == 0:
            print("⚠ No cost data available")
            return self
        
        cost_by_sector = df_with_cost.groupby('org_type')['launch_cost'].agg([
            'count', 'mean', 'median'
        ])
        
        print("\n💰 Launch Cost by Sector:")
        for sector, row in cost_by_sector.iterrows():
            print(f"  {sector:15s} | Avg: ${row['mean']/1e6:.1f}M | "
                  f"Median: ${row['median']/1e6:.1f}M | "
                  f"({int(row['count'])} launches with data)")
        
        return self
    
    def visualize_sector_comparison(self, save_path=None):
        """Create comprehensive sector comparison visualizations."""
        print("\n[9/9] Creating visualizations...")
        
        fig = plt.figure(figsize=(18, 12))
        fig.patch.set_facecolor('#0a0e27')
        
        # Create 2x3 grid
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # 1. Launch count by sector (pie chart)
        ax1 = fig.add_subplot(gs[0, 0])
        sector_counts = self.df['org_type'].value_counts()
        colors_pie = ['#00d9ff', '#ff6b6b', '#4ecdc4', '#95e1d3']
        wedges, texts, autotexts = ax1.pie(sector_counts.values, labels=sector_counts.index,
                                           autopct='%1.1f%%', startangle=90, colors=colors_pie,
                                           textprops={'color': 'white', 'fontsize': 10, 'weight': 'bold'})
        ax1.set_title('Launch Distribution by Sector', color='white', fontsize=12, weight='bold', pad=15)
        
        # 2. Success rate comparison (bar chart)
        ax2 = fig.add_subplot(gs[0, 1])
        if 'sector' in self.performance_metrics:
            sector_data = self.performance_metrics['sector']['success_rate'].sort_values(ascending=False)
            bars = ax2.barh(range(len(sector_data)), sector_data.values, color='#00d9ff', alpha=0.8)
            ax2.set_yticks(range(len(sector_data)))
            ax2.set_yticklabels(sector_data.index, color='white', fontsize=10)
            ax2.set_xlabel('Success Rate (%)', color='white', fontsize=10, weight='bold')
            ax2.set_title('Success Rate by Sector', color='white', fontsize=12, weight='bold', pad=15)
            ax2.grid(axis='x', alpha=0.2, color='white')
            ax2.invert_yaxis()
            
            # Add value labels
            for i, bar in enumerate(bars):
                width = bar.get_width()
                ax2.text(width, bar.get_y() + bar.get_height()/2,
                        f'{width:.1f}%', ha='left', va='center',
                        color='white', fontsize=9, weight='bold')
        
        # 3. Temporal trends (line chart)
        ax3 = fig.add_subplot(gs[0, 2])
        if 'temporal' in self.performance_metrics:
            temporal_data = self.performance_metrics['temporal']
            
            for sector in temporal_data['sector'].unique():
                sector_data = temporal_data[temporal_data['sector'] == sector]
                # Rolling average for smoother lines
                if len(sector_data) > 3:
                    sector_data = sector_data.sort_values('year')
                    ax3.plot(sector_data['year'], 
                            sector_data['launches'].rolling(window=3, min_periods=1).mean(),
                            label=sector, linewidth=2, marker='o', markersize=3, alpha=0.8)
            
            ax3.set_xlabel('Year', color='white', fontsize=10, weight='bold')
            ax3.set_ylabel('Launches per Year (3yr avg)', color='white', fontsize=10, weight='bold')
            ax3.set_title('Launch Frequency Over Time', color='white', fontsize=12, weight='bold', pad=15)
            ax3.legend(facecolor='#1a1f3a', edgecolor='white', labelcolor='white', fontsize=9)
            ax3.grid(alpha=0.2, color='white')
        
        # 4. Top organizations (horizontal bar)
        ax4 = fig.add_subplot(gs[1, :])
        if 'organizations' in self.performance_metrics:
            top_10 = self.performance_metrics['organizations'].head(10)
            y_pos = np.arange(len(top_10))
            
            # Color by sector
            colors_map = {'Private': '#00d9ff', 'Government': '#ff6b6b', 
                         'International': '#4ecdc4', 'Unknown': '#95e1d3'}
            bar_colors = [colors_map.get(sector, '#95e1d3') for sector in top_10['sector']]
            
            bars = ax4.barh(y_pos, top_10['total_launches'], color=bar_colors, alpha=0.8)
            ax4.set_yticks(y_pos)
            ax4.set_yticklabels(top_10.index, color='white', fontsize=10)
            ax4.set_xlabel('Total Launches', color='white', fontsize=11, weight='bold')
            ax4.set_title('Top 10 Organizations by Launch Count', color='white', 
                         fontsize=13, weight='bold', pad=15)
            ax4.grid(axis='x', alpha=0.2, color='white')
            ax4.invert_yaxis()
            
            # Add success rate as text
            for i, (idx, row) in enumerate(top_10.iterrows()):
                ax4.text(row['total_launches'], i,
                        f" {row['success_rate']:.0f}%",
                        va='center', ha='left', color='white', fontsize=9, weight='bold')
        
        # 5. Success rate distribution (violin plot)
        ax5 = fig.add_subplot(gs[2, 0])
        if 'organizations' in self.performance_metrics:
            org_data = self.performance_metrics['organizations']
            org_data_filtered = org_data[org_data['total_launches'] >= 5]
            
            sectors = org_data_filtered['sector'].unique()
            violin_data = [org_data_filtered[org_data_filtered['sector'] == s]['success_rate'].values 
                          for s in sectors]
            
            parts = ax5.violinplot(violin_data, positions=range(len(sectors)),
                                  widths=0.7, showmeans=True, showmedians=True)
            
            # Color the violins
            colors_violin = ['#00d9ff', '#ff6b6b', '#4ecdc4', '#95e1d3']
            for i, pc in enumerate(parts['bodies']):
                pc.set_facecolor(colors_violin[i % len(colors_violin)])
                pc.set_alpha(0.6)
            
            ax5.set_xticks(range(len(sectors)))
            ax5.set_xticklabels(sectors, color='white', fontsize=9, rotation=45, ha='right')
            ax5.set_ylabel('Success Rate (%)', color='white', fontsize=10, weight='bold')
            ax5.set_title('Success Rate Distribution\n(5+ launches)', color='white', 
                         fontsize=11, weight='bold', pad=15)
            ax5.grid(axis='y', alpha=0.2, color='white')
        
        # 6. Launch count by country (top 10)
        ax6 = fig.add_subplot(gs[2, 1:])
        if 'launch_country' in self.df.columns:
            country_counts = self.df['launch_country'].value_counts().head(10)
            
            bars = ax6.bar(range(len(country_counts)), country_counts.values,
                          color='#00d9ff', alpha=0.8, edgecolor='white', linewidth=0.5)
            ax6.set_xticks(range(len(country_counts)))
            ax6.set_xticklabels(country_counts.index, color='white', fontsize=10, 
                               rotation=45, ha='right')
            ax6.set_ylabel('Number of Launches', color='white', fontsize=11, weight='bold')
            ax6.set_title('Top 10 Launch Countries', color='white', fontsize=13, weight='bold', pad=15)
            ax6.grid(axis='y', alpha=0.2, color='white')
            
            # Add value labels
            for i, bar in enumerate(bars):
                height = bar.get_height()
                ax6.text(bar.get_x() + bar.get_width()/2, height,
                        f'{int(height)}', ha='center', va='bottom',
                        color='white', fontsize=9, weight='bold')
        
        plt.suptitle('🚀 ELEVRON: Space Launch Analysis Dashboard', 
                    color='white', fontsize=16, weight='bold', y=0.995)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='#0a0e27')
            print(f"✓ Visualization saved to {save_path}")
        
        plt.show()
    
    def generate_comprehensive_report(self):
        """Generate executive summary report."""
        print("\n" + "="*80)
        print("🚀 ELEVRON: COMPREHENSIVE SPACE LAUNCH ANALYSIS REPORT")
        print("="*80)
        print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d')}")
        print(f"Author: Michael Semera")
        print("="*80)
        
        print(f"\n📊 DATASET OVERVIEW")
        print(f"  Total Launches Analyzed: {len(self.df):,}")
        print(f"  Date Range: {self.df['launch_year'].min():.0f} - {self.df['launch_year'].max():.0f}")
        print(f"  Overall Success Rate: {self.df['is_successful'].mean()*100:.1f}%")
        print(f"  Unique Organizations: {self.df['organization'].nunique():,}")
        print(f"  Unique Rockets: {self.df.get('rocket_name', pd.Series()).nunique():,}")
        
        # Sector breakdown
        if 'sector' in self.performance_metrics:
            print(f"\n🎯 SECTOR PERFORMANCE")
            print("-" * 80)
            for sector, row in self.performance_metrics['sector'].iterrows():
                print(f"\n  {sector}:")
                print(f"    Total Launches: {int(row['total_launches']):,}")
                print(f"    Success Rate: {row['success_rate']:.1f}%")
                print(f"    Launches/Year: {row['launches_per_year']:.1f}")
                print(f"    Years Active: {int(row['years_active'])}")
        
        # Top performers
        if 'organizations' in self.performance_metrics:
            print(f"\n🏆 TOP PERFORMERS")
            print("-" * 80)
            top_5 = self.performance_metrics['organizations'].head(5)
            for idx, (org, row) in enumerate(top_5.iterrows(), 1):
                print(f"  {idx}. {org}")
                print(f"     Launches: {int(row['total_launches'])} | "
                      f"Success: {row['success_rate']:.1f}% | "
                      f"Sector: {row['sector']}")
        
        print("\n" + "="*80)
        print("✓ Analysis Complete!")
        print("="*80)
        
        return self
    
    def export_results(self, output_dir='output'):
        """Export analysis results to CSV files."""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        if 'sector' in self.performance_metrics:
            self.performance_metrics['sector'].to_csv(f'{output_dir}/sector_performance.csv')
            print(f"✓ Sector performance exported to {output_dir}/sector_performance.csv")
        
        if 'organizations' in self.performance_metrics:
            self.performance_metrics['organizations'].to_csv(f'{output_dir}/organization_rankings.csv')
            print(f"✓ Organization rankings exported to {output_dir}/organization_rankings.csv")
        
        if 'temporal' in self.performance_metrics:
            self.performance_metrics['temporal'].to_csv(f'{output_dir}/temporal_trends.csv', index=False)
            print(f"✓ Temporal trends exported to {output_dir}/temporal_trends.csv")
        
        return self


def main():
    """Main execution pipeline."""
    print("\n🚀 Initializing Elevron Space Launch Analysis...")
    print("Author: Michael Semera\n")
    
    # Initialize analyzer
    analyzer = SpaceLaunchAnalyzer('data/space_launches.csv')
    
    # Run analysis pipeline
    analyzer.preprocess_data()
    analyzer.analyze_sector_performance()
    analyzer.analyze_temporal_trends()
    analyzer.analyze_top_players(top_n=10)
    analyzer.analyze_rocket_families()
    analyzer.compare_launch_sites()
    analyzer.calculate_innovation_metrics()
    analyzer.analyze_cost_efficiency()
    
    # Generate visualizations
    analyzer.visualize_sector_comparison(save_path='output/sector_comparison_dashboard.png')
    
    # Generate report
    analyzer.generate_comprehensive_report()
    
    # Export results
    analyzer.export_results()
    
    print("\n✅ Elevron analysis complete!")
    print("📁 Check the 'output' folder for results and visualizations.")


if __name__ == "__main__":
    main()