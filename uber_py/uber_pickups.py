import streamlit 
import pandas as pd
import numpy as np

streamlit.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')



@streamlit.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data



data_load_state = streamlit.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache_data)")



if streamlit.checkbox('Show raw data'):
    streamlit.subheader('Raw data')
    streamlit.write(data)


streamlit.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
streamlit.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = streamlit.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

streamlit.subheader('Map of all pickups at %s:00' % hour_to_filter)
streamlit.map(filtered_data)