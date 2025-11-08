# Elevron: Data Dictionary & Space Industry Guide

**Author:** Michael Semera  
**Project:** Elevron - Space Launch Analysis  
**Last Updated:** November 2025

---

## 📊 Dataset Overview

**Primary Source:** Space Launch Dataset (Kaggle)  
**Coverage:** Global orbital launch attempts (1957-2023)  
**Record Type:** Individual launch missions  
**Typical Size:** 4,000-5,000 records

---

## 📋 Core Variables

### Launch Identification

| Variable | Type | Description | Example Values |
|----------|------|-------------|----------------|
| `mission_name` | String | Name/designation of mission | "Starlink 4-15", "Soyuz MS-21" |
| `launch_id` | String/Integer | Unique launch identifier | "12345", "SL-0047" |
| `mission_type` | Categorical | Purpose of mission | "Communications", "ISS Resupply" |

### Temporal Information

| Variable | Type | Description | Format |
|----------|------|-------------|--------|
| `date` | DateTime | Launch date and time (UTC) | YYYY-MM-DD HH:MM:SS |
| `launch_date` | DateTime | Alternative date field | YYYY-MM-DD |
| `launch_year` | Integer (Computed) | Year of launch | 1957-2023 |
| `launch_month` | Integer | Month of launch | 1-12 |
| `time_utc` | Time | Launch time in UTC | HH:MM:SS |

### Organization Information

| Variable | Type | Description | Example Values |
|----------|------|-------------|----------------|
| `company_name` | String | Launch service provider | "SpaceX", "NASA", "Roscosmos" |
| `organisation` | String | Alternative spelling | Same as above |
| `organization` | String (Standardized) | Cleaned organization name | Standardized version |
| `org_type` | Categorical (Computed) | Sector classification | "Private", "Government", "International" |

### Vehicle Information

| Variable | Type | Description | Example Values |
|----------|------|-------------|----------------|
| `rocket` | String | Rocket model/variant | "Falcon 9 Block 5", "Soyuz 2.1a" |
| `rocket_name` | String | Standardized rocket name | "Falcon 9", "Delta IV Heavy" |
| `rocket_family` | String | Vehicle family/series | "Falcon", "Soyuz", "Long March" |
| `vehicle_type` | Categorical | Launch vehicle category | "Medium-lift", "Heavy-lift" |

### Launch Site Information

| Variable | Type | Description | Example Values |
|----------|------|-------------|----------------|
| `location` | String | Launch site name/location | "Kennedy Space Center, USA" |
| `launch_site` | String | Specific launch pad | "LC-39A", "SLC-4E" |
| `launch_country` | String (Computed) | Country of launch | "USA", "Russia", "China" |
| `latitude` | Float | Launch site latitude | 28.5721 (Cape Canaveral) |
| `longitude` | Float | Launch site longitude | -80.6480 (Cape Canaveral) |

### Mission Status

| Variable | Type | Description | Possible Values |
|----------|------|-------------|-----------------|
| `status` | Categorical | Launch outcome | "Success", "Failure", "Partial Failure" |
| `mission_status` | Categorical | Alternative status field | Same as above |
| `launch_status` | Categorical (Standardized) | Cleaned status | Lowercase, standardized |
| `is_successful` | Boolean (Computed) | Binary success indicator | True, False |
| `failure_reason` | String | Cause of failure (if applicable) | "Engine failure", "Guidance issue" |

### Cost Information

| Variable | Type | Description | Typical Range |
|----------|------|-------------|---------------|
| `price` | Float/String | Launch cost in USD | $5M - $500M |
| `cost` | Float/String | Alternative cost field | Same as above |
| `launch_cost` | Float (Computed) | Standardized cost in USD | Numeric only |

### Payload Information

| Variable | Type | Description | Example Values |
|----------|------|-------------|----------------|
| `payload` | String | Satellite(s) launched | "Starlink satellites", "ISS Crew" |
| `payload_mass_kg` | Float | Total payload mass | 0 - 100,000 kg |
| `orbit` | Categorical | Target orbit | "LEO", "GEO", "Interplanetary" |
| `customer` | String | Payload owner/operator | "NASA", "US Air Force", "Iridium" |

---

## 🔧 Computed Variables

### Organization Classification

| Variable | Formula | Values |
|----------|---------|--------|
| `org_type` | Classification algorithm | "Private", "Government", "International", "Unknown" |

**Classification Logic:**

**Private Companies:**
- Contains: SpaceX, Blue Origin, Rocket Lab, Arianespace, Virgin Orbit, ULA, etc.
- Indicators: "Technologies", "Industries", "Space", "Aerospace"
- Characteristics: Commercial ownership, profit-driven

**Government Agencies:**
- Contains: NASA, Roscosmos, CNSA, ISRO, JAXA, ESA, military branches
- Indicators: "Air Force", "Navy", "Ministry", "Armed Forces", "Space Agency"
- Characteristics: State-owned, public funding

**International Organizations:**
- Contains: ESA, Eumetsat, International Launch Services
- Indicators: "International", "Multinational"
- Characteristics: Multi-nation consortiums

### Success Determination

| Variable | Logic | Interpretation |
|----------|-------|----------------|
| `is_successful` | Status in ["Success", "Partial Failure"] | Binary outcome |

**Success Criteria:**
- Status = "Success" → TRUE
- Status = "Partial Failure" → TRUE (partial credit for reaching orbit)
- Status = "Failure" → FALSE
- Status = "Prelaunch Failure" → FALSE

**Rationale:** "Partial Failure" often means primary mission succeeded but secondary objectives failed (e.g., satellite deployed but booster landing failed).

### Temporal Features

| Variable | Computation | Purpose |
|----------|-------------|---------|
| `launch_year` | Extract year from date | Temporal analysis |
| `launch_decade` | Round down to decade | Era-based grouping |
| `days_since_first` | Days from 1957-10-04 (Sputnik) | Launch frequency analysis |

---

## 📈 Space Industry Context

### Launch Vehicle Classification

**Small-Lift (< 2,000 kg to LEO)**
- Examples: Electron, LauncherOne, Vega C
- Use: Small satellites, tech demos
- Cost: $5-15M

**Medium-Lift (2,000 - 20,000 kg to LEO)**
- Examples: Falcon 9, Soyuz, Long March 2D
- Use: Most commercial satellites, crew missions
- Cost: $50-100M

**Heavy-Lift (20,000 - 50,000 kg to LEO)**
- Examples: Falcon Heavy, Delta IV Heavy, Ariane 5
- Use: Large satellites, interplanetary probes
- Cost: $150-350M

**Super Heavy-Lift (> 50,000 kg to LEO)**
- Examples: Space Launch System, Starship (in development)
- Use: Moon/Mars missions, space stations
- Cost: $500M - $2B

### Orbit Types

**LEO (Low Earth Orbit):** 200-2,000 km altitude
- Uses: ISS, Starlink, Earth observation
- Access difficulty: Easiest
- Energy required: Lowest

**MEO (Medium Earth Orbit):** 2,000-35,786 km
- Uses: GPS, navigation constellations
- Access difficulty: Moderate
- Energy required: Moderate

**GEO (Geostationary Orbit):** 35,786 km
- Uses: Communications, weather satellites
- Access difficulty: High
- Energy required: High

**HEO (Highly Elliptical Orbit):** Varies greatly
- Uses: Communications (high latitudes), science
- Access difficulty: High
- Energy required: High

**Interplanetary:** Beyond Earth orbit
- Uses: Moon, Mars, deep space missions
- Access difficulty: Highest
- Energy required: Highest

### Space Era Definitions

**Era 1: Space Race (1957-1975)**
- First satellites and humans in space
- USSR vs USA competition
- Rapid technological advancement
- Government monopoly
- 100% government launches

**Era 2: Shuttle Era (1976-2010)**
- Routine space access
- Commercial satellites emerge
- International cooperation (ISS)
- Government still dominant
- 95% government, 5% commercial

**Era 3: New Space (2011-present)**
- Private companies lead growth
- Reusable rockets proven
- Dramatic cost reduction
- Small satellite revolution
- 70% commercial, 30% government (by 2022)

---

## 🔍 Data Quality Considerations

### Missing Data Patterns

| Field | Typical Missing % | Handling Strategy |
|-------|------------------|-------------------|
| Cost/Price | 60-80% | Analyze subset with data |
| Payload Mass | 30-50% | Use median for estimates |
| Failure Reason | 90% | Only analyze failures |
| Customer | 40-60% | Infer from organization |
| Exact Time | 10-20% | Date sufficient for most analysis |

### Data Anomalies

**Historical Data Issues:**
- Pre-1970 launches may lack detailed info
- Soviet/Russian data often incomplete
- Military launches may be redacted
- Some failures unreported

**Cost Data Issues:**
- Contract prices vs actual costs differ
- Adjusted for inflation inconsistently
- Government accounting opaque
- Multi-launch contracts complicate per-launch cost

**Status Classification Challenges:**
- "Partial Failure" subjective
- Some failures initially reported as successes
- Mission success vs vehicle success differ
- Long-term payload failures not captured

### Validation Rules

```python
# Remove invalid records
df = df[
    (df['launch_year'] >= 1957) &  # First orbital launch
    (df['launch_year'] <= 2024) &  # Current year
    (df['organization'].notna()) &  # Must have organization
    (df['status'].notna())  # Must have status
]
```

---

## 📊 Benchmark Statistics

### Global Averages (All Time)

| Metric | Value |
|--------|-------|
| Overall Success Rate | 92.7% |
| Average Launches per Year (1957-2023) | 68 |
| Peak Year (2021) | 144 launches |
| Most Launches (USSR/Russia) | 3,200+ |
| Most Reliable Rocket (Soyuz) | 1,900+ launches, 97.5% success |

### Sector Benchmarks (2015-2023)

| Sector | Launches | Success Rate | Avg Cost |
|--------|----------|--------------|----------|
| Private | 850+ | 94.2% | $62M |
| Government | 650+ | 95.3% | $152M |
| International | 100+ | 96.1% | $185M |

### Organization Benchmarks (Active, 2020-2023)

| Organization | Annual Launches | Success Rate | Primary Rocket |
|--------------|----------------|--------------|----------------|
| SpaceX | 50+ | 95.7% | Falcon 9 |
| CNSA (China) | 40+ | 96.2% | Long March series |
| Roscosmos | 20+ | 93.8% | Soyuz |
| Rocket Lab | 10+ | 92.5% | Electron |
| Arianespace | 5+ | 97.1% | Ariane 5/6 |

---

## 🌍 Launch Site Reference

### Major Active Launch Sites

**United States:**
- Kennedy Space Center (KSC), Florida - LC-39A/B
- Cape Canaveral Space Force Station, Florida - Multiple pads
- Vandenberg Space Force Base, California - SLC-4E, SLC-6
- Wallops Flight Facility, Virginia - Pad 0A

**Russia/Kazakhstan:**
- Baikonur Cosmodrome, Kazakhstan - Multiple pads
- Plesetsk Cosmodrome, Russia - Multiple pads
- Vostochny Cosmodrome, Russia - Limited operations

**China:**
- Jiuquan Satellite Launch Center - Multiple pads
- Xichang Satellite Launch Center - Multiple pads
- Taiyuan Satellite Launch Center - Multiple pads
- Wenchang Satellite Launch Center - Newest facility

**Europe:**
- Guiana Space Centre, French Guiana - Multiple pads

**Other:**
- Satish Dhawan Space Centre, India - Two pads
- Tanegashima Space Center, Japan - Two pads
- Rocket Lab Launch Complex 1, New Zealand - One pad

---

## 🔄 Data Preprocessing Pipeline

### Step 1: Load and Inspect
```python
df = pd.read_csv('space_launches.csv', low_memory=False)
print(df.info())
print(df.head())
```

### Step 2: Standardize Columns
```python
df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
```

### Step 3: Parse Dates
```python
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['launch_year'] = df['date'].dt.year
```

### Step 4: Clean Status
```python
df['launch_status'] = df['status'].str.lower().str.strip()
df['is_successful'] = df['launch_status'].isin(['success', 'partial failure'])
```

### Step 5: Classify Organizations
```python
df['org_type'] = df['organization'].apply(classify_organization)
```

### Step 6: Extract Country
```python
df['launch_country'] = df['location'].apply(extract_country)
```

### Step 7: Parse Costs
```python
df['launch_cost'] = df['price'].apply(parse_currency)
```

### Step 8: Validate and Filter
```python
df = df[(df['launch_year'] >= 1957) & (df['launch_year'] <= 2024)]
```

---

## 📚 Space Industry Terminology

**Apogee:** Highest point in an elliptical orbit  
**Booster:** First stage of a rocket  
**Constellation:** Group of satellites working together  
**Downrange:** Direction of rocket flight from launch site  
**Fairing:** Protective shell around payload  
**GTO:** Geostationary Transfer Orbit  
**Inclination:** Angle of orbit relative to equator  
**Kick Stage:** Small upper stage for final orbital insertion  
**LEO:** Low Earth Orbit  
**Manifest:** Schedule of upcoming launches  
**Orbital Velocity:** Speed needed to maintain orbit (~7.8 km/s for LEO)  
**Payload:** Satellite(s) being launched  
**Scrub:** Launch cancellation/postponement  
**Stage:** Separate section of rocket that detaches  
**Thrust:** Force produced by rocket engines  
**Trajectory:** Path of rocket through space  
**Upper Stage:** Final rocket stage that reaches orbit  

---

## ⚠️ Analysis Limitations

### Data Completeness
- Cost data available for < 30% of launches
- Payload details often classified for military missions
- Historical data (pre-1990) less detailed
- Some countries don't report all launches

### Classification Challenges
- Public-private partnerships blur sector lines
- International organizations hard to categorize
- Organization name changes over time
- Some launches use multiple providers

### Success Definition
- "Partial failure" interpretation varies
- Long-term satellite failures not captured
- Mission success vs vehicle success differ
- Experimental flights complicate statistics

### Temporal Bias
- Recent years over-represented in data
- Historical launches under-documented
- Soviet era data gaps
- Reporting standards changed over time

---

## 🔄 Version History

**v1.0 (November 2025)**
- Initial data dictionary
- Core variable definitions
- Space industry context
- Preprocessing guidelines

---

**Document Maintained By:** Michael Semera  
**For Project:** Elevron  
**Version:** 1.0.0