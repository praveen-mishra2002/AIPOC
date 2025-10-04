import pandas as pd

# Example: reading CAN data from CSV (with columns: 'Timestamp', 'ID', 'Data')
def read_can_data(filename):
    return pd.read_csv(filename)

def detect_anomalies(df, threshold=3):
    # Example anomaly: message frequency for each ID
    freq = df['ID'].value_counts()
    mean = freq.mean()
    std = freq.std()
    
    anomalies = freq[(freq > mean + threshold * std) | (freq < mean - threshold * std)]
    print("Anomalous IDs (frequency):", anomalies.index.tolist())
    
    # Example anomaly: flag data field outliers for each ID
    for can_id in df['ID'].unique():
        id_data = df[df['ID'] == can_id]['Data']
        # If data is numeric; adjust for actual data format
        try:
            numeric_data = pd.to_numeric(id_data, errors='coerce').dropna()
            if not numeric_data.empty:
                data_mean = numeric_data.mean()
                data_std = numeric_data.std()
                outliers = numeric_data[(numeric_data > data_mean + threshold * data_std) | 
                                       (numeric_data < data_mean - threshold * data_std)]
                if not outliers.empty:
                    print(f"Data outliers for ID {can_id}: {outliers.values}")
        except Exception as e:
            print(f"Skipping non-numeric data for ID {can_id}: {e}")

if __name__ == "__main__":
    filename = "can_log.csv"
    df = read_can_data(filename)
    detect_anomalies(df)