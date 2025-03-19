import pandas as pd
import re
import matplotlib.pyplot as plt
import os
import searches as src



import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import skew, kurtosis

# Load your dataframes (replace with actual paths or data)
sold_items = pd.read_csv("/home/ale/Desktop/Vinted-Web-Scraper/csv_definitivi/sold_items.csv")
unsold_items = pd.read_csv("/home/ale/Desktop/Vinted-Web-Scraper/csv_definitivi/big_csv.csv")

def basic_statistics(df, name):
    print(f"\nBasic Statistics for {name}:\n")
    print(df.describe())

def laplacian_variance_analysis(df, name):
    print(f"\nLaplacian Variance Analysis for {name}:\n")
    stats_cols = ["Mean", "Standard Deviation", "Minimum", "Maximum", "Skewness", "Kurtosis"]
    print(df[stats_cols].describe())

def price_distribution(sold_df, unsold_df):
    plt.figure(figsize=(10,5))
    sns.histplot(sold_df["Price"], bins=30, kde=True, label="Sold Items", color="blue", alpha=0.6)
    sns.histplot(unsold_df["Price"], bins=30, kde=True, label="Unsold Items", color="red", alpha=0.6)
    plt.xlabel("Price")
    plt.ylabel("Frequency")
    plt.title("Price Distribution: Sold vs Unsold Items")
    plt.legend()
    plt.show()

def brand_analysis(sold_df, unsold_df):
    plt.figure(figsize=(12, 5))
    top_sold_brands = sold_df["Brand"].value_counts().head(10)
    top_unsold_brands = unsold_df["Brand"].value_counts().head(10)

    ax = plt.subplot(1, 2, 1)
    top_sold_brands.plot(kind="bar", color="blue", alpha=0.6)
    plt.title("Top 10 Brands (Sold Items)")
    plt.xticks(rotation=45)

    ax = plt.subplot(1, 2, 2)
    top_unsold_brands.plot(kind="bar", color="red", alpha=0.6)
    plt.title("Top 10 Brands (Unsold Items)")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

def size_analysis(sold_df, unsold_df):
    plt.figure(figsize=(10,5))
    sold_sizes = sold_df["Size"].value_counts().sort_values()
    unsold_sizes = unsold_df["Size"].value_counts().sort_values()

    sns.lineplot(x=sold_sizes.index, y=sold_sizes.values, marker="o", label="Sold")
    sns.lineplot(x=unsold_sizes.index, y=unsold_sizes.values, marker="s", label="Unsold")

    plt.xticks(rotation=45)
    plt.xlabel("Size")
    plt.ylabel("Count")
    plt.title("Size Popularity: Sold vs Unsold")
    plt.legend()
    plt.show()

def likes_analysis(sold_df, unsold_df):
    plt.figure(figsize=(10,5))
    sns.histplot(sold_df["Likes"], bins=20, kde=True, label="Sold Items", color="blue", alpha=0.6)
    sns.histplot(unsold_df["Likes"], bins=20, kde=True, label="Unsold Items", color="red", alpha=0.6)
    plt.xlabel("Likes")
    plt.ylabel("Frequency")
    plt.title("Likes Distribution: Sold vs Unsold")
    plt.legend()
    plt.show()

def image_count_analysis(sold_df, unsold_df):
    plt.figure(figsize=(10,5))
    sns.histplot(sold_df["ImageCount"], bins=10, kde=True, label="Sold Items", color="blue", alpha=0.6)
    sns.histplot(unsold_df["ImageCount"], bins=10, kde=True, label="Unsold Items", color="red", alpha=0.6)
    plt.xlabel("Image Count")
    plt.ylabel("Frequency")
    plt.title("Image Count Analysis")
    plt.legend()
    plt.show()

def skewness_kurtosis_analysis(df, name):
    print(f"\nSkewness & Kurtosis for {name}:\n")
    for col in ["Price", "Likes", "ImageCount"]:
        print(f"{col}: Skewness = {skew(df[col])}, Kurtosis = {kurtosis(df[col])}")

def correlation_analysis(df, name):
    plt.figure(figsize=(10,6))
    sns.heatmap(df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
    plt.title(f"Correlation Matrix - {name}")
    plt.show()

# Run all analyses
basic_statistics(sold_items, "Sold Items")
basic_statistics(unsold_items, "Unsold Items")

laplacian_variance_analysis(sold_items, "Sold Items")
laplacian_variance_analysis(unsold_items, "Unsold Items")

price_distribution(sold_items, unsold_items)
brand_analysis(sold_items, unsold_items)
size_analysis(sold_items, unsold_items)
likes_analysis(sold_items, unsold_items)
image_count_analysis(sold_items, unsold_items)

skewness_kurtosis_analysis(sold_items, "Sold Items")
skewness_kurtosis_analysis(unsold_items, "Unsold Items")

correlation_analysis(sold_items, "Sold Items")
correlation_analysis(unsold_items, "Unsold Items")

































# class DataAnalyzer:
#     def __init__(self, dictionary, base_dir="/home/ale/Desktop/Vinted-Web-Scraper"):
#         # Construct the file path dynamically based on the provided search term and base directory
#         self.file_path = os.path.join(base_dir, dictionary["search"], f"{dictionary['search']}.csv")
#         self.data = None

#     def load_data(self):
#         # Try to load the data and handle errors
#         try:
#             self.data = pd.read_csv(self.file_path)
#         except FileNotFoundError:
#             print(f"File not found: {self.file_path}")
#         except pd.errors.EmptyDataError:
#             print("CSV file is empty.")
#         except Exception as e:
#             print(f"An error occurred: {e}")

#     def price_trend_analysis(self):

#         # Calculate average price
#         average_price = self.data['Price'].mean()

#         # Identify listings below the average price
#         self.data['Below_Average_Price'] = self.data['Price'] < average_price

#         # Display undervalued listings
#         undervalued_listings = self.data[self.data['Below_Average_Price']]
#         print("Undervalued Listings:")
#         print(undervalued_listings[['Title', 'Price', 'Below_Average_Price']])


#     def interest_price_analysis(self):

#         # Plot Interested_count vs. Price
#         plt.scatter(self.data['Price'], self.data['Interested_count'])
#         plt.xlabel('Price')
#         plt.ylabel('Interested Count')
#         plt.title('Interest vs. Price Analysis')
#         plt.show()

#         # Calculate correlation
#         correlation = self.data['Price'].corr(self.data['Interested_count'])
#         print("Correlation between Price and Interest Count:", correlation)
    
#     def demand_based_deal_identification(self):
#         # Define threshold for high interest and low price
#         high_interest_threshold = self.data['Interested_count'].quantile(0.75)
#         low_price_threshold = self.data['Price'].quantile(0.25)

#         # Filter listings that meet these criteria
#         potential_deals = self.data[(self.data['Interested_count'] >= high_interest_threshold) & (data['Price'] <= low_price_threshold)]
#         print("Potential Deals for Resale:")
#         print(potential_deals[['Title', 'Price', 'Interested_count']])
    
#     def slow_moving_items_analysis(self):
#         # Define listings on sale for 2 weeks or longer (as an example)
#         long_sale_duration = self.data['Upload_date'].str.extract(r'(\d+)').astype(float) >= 2  # Extract duration and convert to float

#         # Filter items based on duration and views
#         slow_moving_listings = self.data[long_sale_duration[0] & (self.data['View_count'] < data['View_count'].mean())]
#         print("Slow-Moving Listings:")
#         print(slow_moving_listings[['Title', 'View_count', 'Upload_date']])

#     def size_analysis(self):
#         # Group by Size and calculate average Interested_count and View_count
#         size_demand = self.data.groupby('Size').agg({
#             'Interested_count': 'mean',
#             'View_count': 'mean',
#             'Price': 'mean'
#         }).reset_index()

#         # Display most popular sizes by interest and view count
#         print("Size-Specific Demand:")
#         print(size_demand.sort_values(by=['Interested_count', 'View_count'], ascending=False))


# data_analyzer = DataAnalyzer(src.cucinelli)
# data_analyzer.load_data()
# data_analyzer.price_trend_analysis()
# data_analyzer.interest_price_analysis()
# data_analyzer.demand_based_deal_identification()
# data_analyzer.slow_moving_items_analysis()
# data_analyzer.size_analysis()
# # Function to convert different time units to days
# def convert_to_days(duration_str):
#     match = re.search(r'(\d+)\s*(day|week|month)', duration_str, re.IGNORECASE)
#     if match:
#         number = int(match.group(1))
#         unit = match.group(2).lower()
        
#         # Convert to days based on the unit
#         if unit == 'day':
#             return number
#         elif unit == 'week':
#             return number * 7
#         elif unit == 'month':
#             return number * 30  # Approximate month length
#     return None  # Return None if the format isn't recognized

# # Apply the function to convert 'Upload_date' to days
# self.data['Sale_Duration_Days'] = self.data['Upload_date'].apply(convert_to_days)

# # Filter listings that have been on sale for 2 weeks or longer (14 days or more)
# long_sale_duration = self.data['Sale_Duration_Days'] >= 14

# # Select listings based on this condition
# slow_moving_listings = self.data[long_sale_duration]
