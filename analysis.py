import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import glob

# Load dataset
csv_files = glob.glob('Wind Farm B/datasets/*.csv')
dfs = [pd.read_csv(file, delimiter=';') for file in csv_files]
data = pd.concat(dfs, ignore_index=True)

# Basic statistics
print(data.describe())

# Correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(data.corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

# Distribution of each feature
data.hist(bins=30, figsize=(20, 15))
plt.suptitle('Feature Distributions')
plt.show()

# Pairplot
sns.pairplot(data)
plt.title('Pairplot of Features')
plt.show()

# Boxplot for each feature
plt.figure(figsize=(20, 10))
sns.boxplot(data=data)
plt.title('Boxplot of Features')
plt.show()

# Scatter plot for two specific features (example: 'sensor_0_avg' and 'sensor_1_avg')
plt.figure(figsize=(10, 6))
plt.scatter(data['sensor_0_avg'], data['sensor_1_avg'])
plt.xlabel('Sensor 0 Avg')
plt.ylabel('Sensor 1 Avg')
plt.title('Scatter Plot of Sensor 0 Avg vs Sensor 1 Avg')
plt.show()

# Clean the data
def clean_sensor_data(df):
    df['time_stamp'] = pd.to_datetime(df['time_stamp'])
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df[col] = df[col].clip(lower_bound, upper_bound)
        df[col] = df[col].fillna(df[col].median())
    return df

clean_data = clean_sensor_data(data.copy())

# Plot sensor distributions
def plot_sensor_distributions(df, n_cols=3, batch_size=10):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for start in range(0, len(numeric_cols), batch_size):
        batch_cols = numeric_cols[start:start + batch_size]
        n_rows = (len(batch_cols) + n_cols - 1) // n_cols
        plt.figure(figsize=(15, 5*n_rows))
        for i, col in enumerate(batch_cols):
            plt.subplot(n_rows, n_cols, i+1)
            sns.histplot(df[col].sample(n=10000), kde=True)
            plt.title(f'Distribution of {col}')
            plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

plot_sensor_distributions(clean_data)

# Plot time series
def plot_time_series(df, columns, window_size=24):
    plt.figure(figsize=(15, 5*len(columns)))
    for i, col in enumerate(columns):
        plt.subplot(len(columns), 1, i+1)
        plt.plot(df['time_stamp'], df[col], alpha=0.5, label='Raw')
        rolling_mean = df[col].rolling(window=window_size).mean()
        plt.plot(df['time_stamp'], rolling_mean, 'r', label=f'{window_size}h Rolling Mean')
        plt.title(f'Time Series of {col}')
        plt.legend()
    plt.tight_layout()
    plt.show()

key_columns = ['wind_speed_59_avg', 'power_62_avg', 'sensor_0_avg']
plot_time_series(clean_data, key_columns)
