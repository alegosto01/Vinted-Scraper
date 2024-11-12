import pandas as pd
import re
import matplotlib.pyplot as plt
import os

class DataAnalyzer:
    def __init__(self, dictionary, base_dir="/home/ale/Desktop/Vinted-Web-Scraper"):
        # Construct the file path dynamically based on the provided search term and base directory
        self.file_path = os.path.join(base_dir, dictionary["search"], f"{dictionary["search"]}.csv")
        self.data = None

    def load_data(self):
        # Try to load the data and handle errors
        try:
            self.data = pd.read_csv(self.file_path)
        except FileNotFoundError:
            print(f"File not found: {self.file_path}")
        except pd.errors.EmptyDataError:
            print("CSV file is empty.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def price_trend_analysis(self):

        # Calculate average price
        average_price = self.data['Price'].mean()

        # Identify listings below the average price
        self.data['Below_Average_Price'] = self.data['Price'] < average_price

        # Display undervalued listings
        undervalued_listings = self.data[self.data['Below_Average_Price']]
        print("Undervalued Listings:")
        print(undervalued_listings[['Title', 'Price', 'Below_Average_Price']])


    def interest_price_analysis(self):

        # Plot Interested_count vs. Price
        plt.scatter(self.data['Price'], self.data['Interested_count'])
        plt.xlabel('Price')
        plt.ylabel('Interested Count')
        plt.title('Interest vs. Price Analysis')
        plt.show()

        # Calculate correlation
        correlation = self.data['Price'].corr(self.data['Interested_count'])
        print("Correlation between Price and Interest Count:", correlation)
    
    def demand_based_deal_identification(self):
        # Define threshold for high interest and low price
        high_interest_threshold = self.data['Interested_count'].quantile(0.75)
        low_price_threshold = self.data['Price'].quantile(0.25)

        # Filter listings that meet these criteria
        potential_deals = self.data[(self.data['Interested_count'] >= high_interest_threshold) & (data['Price'] <= low_price_threshold)]
        print("Potential Deals for Resale:")
        print(potential_deals[['Title', 'Price', 'Interested_count']])
    
    def slow_moving_items_analysis(self):
        # Define listings on sale for 2 weeks or longer (as an example)
        long_sale_duration = self.data['Upload_date'].str.extract(r'(\d+)').astype(float) >= 2  # Extract duration and convert to float

        # Filter items based on duration and views
        slow_moving_listings = self.data[long_sale_duration[0] & (self.data['View_count'] < data['View_count'].mean())]
        print("Slow-Moving Listings:")
        print(slow_moving_listings[['Title', 'View_count', 'Upload_date']])

    def size_analysis(self):
        # Group by Size and calculate average Interested_count and View_count
        size_demand = self.data.groupby('Size').agg({
            'Interested_count': 'mean',
            'View_count': 'mean',
            'Price': 'mean'
        }).reset_index()

        # Display most popular sizes by interest and view count
        print("Size-Specific Demand:")
        print(size_demand.sort_values(by=['Interested_count', 'View_count'], ascending=False))


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
