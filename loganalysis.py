import requests
import pandas as pd
import re
from io import StringIO
import time

# Function to parse log line
def parse_log_line(line):
    pattern = r"\[(.*?)\] Result: (.*?), IP Address: (.*?), Request: (.*?), Browser: (.*?), Device: (.*?), Email: (.*?), Form ID: (.*?), Response Time: (\d+) ms"
    match = re.match(pattern, line)
    if match:
        return {
            "Timestamp": match.group(1),
            "Result": match.group(2),
            "IP Address": match.group(3),
            "Request": match.group(4),
            "Browser": match.group(5),
            "Device": match.group(6),
            "Email": match.group(7),
            "Form ID": match.group(8),
            "Response Time": match.group(9)
        }
    else:
        return None

# Function to fetch log data from URL
def fetch_log_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to fetch log data.")
        return None

# Function to process log data
def process_log_data(log_data):
    log_lines = log_data.strip().split("\n")
    parsed_data = [parse_log_line(line) for line in log_lines]
    parsed_data = [data for data in parsed_data if data is not None]
    df = pd.DataFrame(parsed_data)
    return df

# Main function for real-time analysis
def realtime_analysis(log_url):
    while True:
        log_data = fetch_log_data(log_url)
        if log_data:
            df = process_log_data(log_data)
            # Perform analysis on df, e.g., print summary statistics
            print("Summary Statistics:")
            print(df.describe())
            print("\n")
        time.sleep(60)  # Fetch log data every 60 seconds

# URL of the log file
log_url = "https://ibmtrainings.theax.in/auth/log.txt"

# Start real-time analysis
realtime_analysis(log_url)
