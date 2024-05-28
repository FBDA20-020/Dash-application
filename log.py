import pandas as pd
import random
from datetime import datetime, timedelta

# Mock function to map IP to country for demonstration purposes
def get_country_from_ip(ip):
    # Example IP to Country mapping
    country_mapping = {
        "228.10.0.1": "USA",
        "155.55.0.24": "Canada",
        "157.20.30.10": "UK",
        "172.16.0.1": "Australia",
        "201.24.35.67": "Brazil",
        "89.23.45.67": "Germany",
        "120.25.45.67": "Japan",
        "203.0.113.0": "India",
        "54.240.196.186": "Netherlands",
        "203.0.113.195": "South Africa",
        # Add more mappings here
    }
    return country_mapping.get(ip, "Unknown")

# Function to map country to continent
def get_continent_from_country(country):
    continent_mapping = {
        "USA": "North America",
        "Canada": "North America",
        "UK": "Europe",
        "Australia": "Oceania",
        "Brazil": "South America",
        "Germany": "Europe",
        "Japan": "Asia",
        "India": "Asia",
        "Netherlands": "Europe",
        "South Africa": "Africa",
        # Add more mappings here
    }
    return continent_mapping.get(country, "Unknown")

# Generate a list of sample IP addresses
ip_addresses = [
    "228.10.0.1", "155.55.0.24", "157.20.30.10", "172.16.0.1",
    "201.24.35.67", "89.23.45.67", "120.25.45.67", "203.0.113.0",
    "54.240.196.186", "203.0.113.195"
]
urls = [
    "/index.html", "/images/games.jpg", "/searchsports.php", "/football.html",
    "/basketball.html", "/swimming.html", "/athletics.html", "/tennis.html"
]

# Generate random web server logs
def generate_logs(num_entries):
    logs = []
    base_time = datetime.now()
    for _ in range(num_entries):
        timestamp = base_time - timedelta(minutes=random.randint(0, 10000))
        ip = random.choice(ip_addresses)
        url = random.choice(urls)
        response_code = random.choice([200, 304, 404])
        logs.append([timestamp, ip, url, response_code])
    return logs

# Generate 1000 log entries
logs = generate_logs(1000)

# Create DataFrame
logs_df = pd.DataFrame(logs, columns=["Timestamp", "IP", "URL", "ResponseCode"])

# Preprocess logs data
def preprocess_logs(logs_df):
    # Convert Timestamp column to datetime format
    logs_df['Timestamp'] = pd.to_datetime(logs_df['Timestamp'])
    # Extract hour of the day
    logs_df['Hour'] = logs_df['Timestamp'].dt.hour
    # Map IP addresses to countries
    logs_df['Country'] = logs_df['IP'].apply(get_country_from_ip)
    # Extract sport from URL
    logs_df['Sport'] = logs_df['URL'].apply(lambda x: x.split('/')[-1].split('.')[0])
    # Map countries to continents
    logs_df['Continent'] = logs_df['Country'].apply(get_continent_from_country)
    # Generate random gender data
    logs_df['Gender'] = [random.choice(['Male', 'Female']) for _ in range(len(logs_df))]
    return logs_df

# Preprocess logs
logs_df = preprocess_logs(logs_df)

# Save DataFrame to CSV
csv_filename = 'web_server_log.csv'
logs_df.to_csv(csv_filename, index=False)

print(f"Log data generated and saved to '{csv_filename}'")
