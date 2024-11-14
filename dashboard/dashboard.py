import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    # load data per day and hour
    daily_data = pd.read_csv("bike_data_day.csv")
    hourly_data = pd.read_csv("bike_data_hour.csv")
    
    # drop index column
    daily_data = daily_data.drop('instant', axis=1)
    hourly_data = hourly_data.drop('instant', axis=1)
    
    # convert date column
    daily_data['dteday'] = pd.to_datetime(daily_data['dteday'])
    hourly_data['dteday'] = pd.to_datetime(hourly_data['dteday'])
    
    # unnormalize data
    daily_data['temp'] =  daily_data['temp'] * 41
    daily_data['atemp'] = daily_data["atemp"] * 50
    daily_data['hum'] = daily_data['hum'] * 100
    daily_data['windspeed'] = daily_data['windspeed'] * 67
    
    hourly_data['temp'] =  hourly_data['temp'] * 41
    hourly_data['atemp'] = hourly_data["atemp"] * 50
    hourly_data['hum'] = hourly_data['hum'] * 100
    hourly_data['windspeed'] = hourly_data['windspeed'] * 67
    
    # rename columns
    daily_data['weathersit'] = daily_data['weathersit'].astype('category')
    daily_data['weathersit'] = daily_data['weathersit'].cat.rename_categories({1: "Clear", 2: "Cloudy", 3: "Light Rain", 4: "Heavy Rain"})
    
    hourly_data['weathersit'] = hourly_data['weathersit'].astype('category')
    hourly_data['weathersit'] = hourly_data['weathersit'].cat.rename_categories({1: "Clear", 2: "Cloudy", 3: "Light Snow", 4: "Heavy Snow"})
    
    daily_data['weekday'] = daily_data['weekday'].astype('category')
    daily_data['weekday'] = daily_data['weekday'].cat.rename_categories({0: "Sun", 1: "Mon", 2: "Tue", 3: "Wed", 4: "Thur", 5: "Fri", 6: "Sat"})
    
    hourly_data['weekday'] = hourly_data['weekday'].astype('category')
    hourly_data['weekday'] = hourly_data['weekday'].cat.rename_categories({0: "Sun", 1: "Mon", 2: "Tue", 3: "Wed", 4: "Thur", 5: "Fri", 6: "Sat"})
    
    daily_data['season'] = daily_data['season'].astype('category')
    daily_data['season'] = daily_data['season'].cat.rename_categories({1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"})

    hourly_data['season'] = hourly_data['season'].astype('category')
    hourly_data['season'] = hourly_data['season'].cat.rename_categories({1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"})
    
    return daily_data, hourly_data

daily_data, hourly_data = load_data()

# set the title
st.title("Bike Sharing Analysis Dashboard from 2011 to 2012")
st.write("Explore bike-sharing data with daily and hourly records from Washington D. C. USA")

# sidebar feature
data_type = st.sidebar.radio("Select Data Type", ["Daily Data", "Hourly Data"])

# condition for data display
if data_type == "Daily Data":
    data = daily_data
else:
    data = hourly_data

# sidebar filter
st.sidebar.subheader("Select Date Range")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2011-01-01"), min_value=pd.to_datetime("2011-01-01"), max_value=pd.to_datetime("2012-12-31"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2012-12-31"), min_value=pd.to_datetime("2011-01-01"), max_value=pd.to_datetime("2012-12-31"))

filtered_data = data[(data['dteday'] >= pd.to_datetime(start_date)) & (data['dteday'] <= pd.to_datetime(end_date))]

# displaying number of total rider
st.subheader('Daily Riders')
 
col1, col2 = st.columns(2)
 
with col1:
    total_reg = filtered_data.registered.sum()
    st.metric("Total Registered Riders", value=total_reg)
 
with col2:
    total_casual = filtered_data.casual.sum()
    st.metric("Total Casual Riders", value=total_casual)

# bar plot of total rides by day
st.subheader('Total Rides by Week')
plt.bar(filtered_data['weekday'], filtered_data['cnt'], width = 0.4)

plt.ylabel("Number of Ride")
st.pyplot(plt)

# bar plot of total rides by season
st.subheader("Total Rides by Season")
season_totals = filtered_data.groupby('season')['cnt'].sum()
plt.figure(figsize=(7, 4))
sns.barplot(x=season_totals.index, y=season_totals.values, palette="viridis")
plt.xlabel("Season")
plt.ylabel("Total Number of Rides")
st.pyplot(plt)

# line chart of for casual vs registered riders
st.subheader("Casual vs Registered Riders Over Time")

# group it by seasonal
seasonal_data = filtered_data.groupby('season')[['casual', 'registered']].sum()
plt.figure(figsize = (12, 6))
plt.plot(seasonal_data.index, seasonal_data['casual'], marker='o', label='Casual Riders')
plt.plot(seasonal_data.index, seasonal_data['registered'], marker='o', label='Registered Riders')
plt.xlabel("Season")
plt.ylabel("Number of Rides")
plt.title("Number of Rides for Registered vs Casual Riders by Season")
plt.legend()
st.pyplot(plt)
 
# group it by day
seasonal_data = filtered_data.groupby('weekday')[['casual', 'registered']].sum()
    
# plot with line plot
plt.figure(figsize = (12, 6))
plt.plot(seasonal_data.index, seasonal_data['casual'], marker='o', label='Casual Riders')
plt.plot(seasonal_data.index, seasonal_data['registered'], marker='o', label='Casual Riders')
   
plt.xlabel("Day")
plt.ylabel("Number of Rides")
plt.title("Number of Rides for Registered vs Casual Riders by Day")
plt.legend(["Casual Riders", "Registered Riders"])
st.pyplot(plt)

# line chart of registered and casual riders 
# group it by hour
seasonal_data = hourly_data.groupby('hr')[['casual', 'registered']].sum()

# plot with line plot
plt.figure(figsize = (12, 6))
plt.plot(seasonal_data.index, seasonal_data['casual'], marker='o', label='Casual Riders')
plt.plot(seasonal_data.index, seasonal_data['registered'], marker='o', label='Casual Riders')

plt.xlabel("Hour")
plt.ylabel("Number of Rides")
plt.title("Number of Rides for Registered vs Casual Riders by Season")
plt.legend(["Casual Riders", "Registered Riders"])
st.pyplot(plt)
    
# bar plot of total rides by weather situation
st.subheader("Total Rides by Weather Situation")
season_totals = filtered_data.groupby('weathersit')['cnt'].sum()
plt.figure(figsize=(7, 4))
sns.barplot(x=season_totals.index, y=season_totals.values, palette="viridis")
plt.xlabel("Weather Situation")
plt.ylabel("Total Number of Rides")
st.pyplot(plt)

# scatter plot of relation between temperature feels like and number of rider
# add the title
st.subheader('Total Rides by Temperature Feels Like')
plt.figure(figsize = (12, 6))

# plot the data
plt.scatter(filtered_data['temp'], filtered_data['cnt'])

# labelling axes
plt.xlabel('Temperature Feels Like (Celsius)')
plt.ylabel('Number of Rides')
st.pyplot(plt)

