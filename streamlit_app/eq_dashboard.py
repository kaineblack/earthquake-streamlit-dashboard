import requests
import pandas as pd
import numpy as np
import streamlit as st
from io import StringIO
import datetime
import plotly.express as px
import base64


def retrieve_data_from_usgs_api(start_date, end_date, min_mag=None):
    '''
    This function is used to query the USGS earthquake API to get data
    related to earthquakes around the world. The query can be filtered
    based on a time range, as well as a minimum magnitude of the 
    earthquakes to be considered.

    Parameters
    ----------
    start_date - str
        The start date from which we want to look for earthquake events.
        Should be in the form 'YYYY-MM-DD'.
    
    end_date - str
        The end date from which we want to look for earthquake events.
        Should be in the form 'YYYY-MM-DD'.

    min_mag - int or float
        The minimum magnitude for which we want to consider for earthquake
        events. This way we can filter out earthquakes with non-significant
        magnitudes if desired.

        
    Returns
    -------
    No object returned. This function simply formats the output of the streamlit
    dashboard to be displayed.
    '''

    # make sure the inputs are correct
    assert isinstance(start_date, datetime.date)
    assert isinstance(end_date, datetime.date)
    if min_mag:
        assert (isinstance(min_mag, float) or isinstance(min_mag, int)), "min_mag parameter should be a float or int number."

    # create the request string based on the inputs
    if min_mag:
        req_txt = f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime={start_date}&endtime={end_date}&minmagnitude={min_mag}'
    else:
        req_txt = f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime={start_date}&endtime={end_date}'
    
    # make the request to the API
    response = requests.get(req_txt)

    # check that the request was successful
    assert response.status_code == 200, 'There was a problem with the request. Try again or check the status of the USGS API.'

    # store the data as an IO String, then read it using pandas
    resp_text = StringIO(response.text)
    eq_df = pd.read_csv(resp_text)
    
    # display number of earthquakes, mean magnitude
    col1, col2 = st.columns(2)
    col1.metric("Number of Earthquakes", len(eq_df))
    col2.metric("Average Mag of Earthquakes", np.round(eq_df.mag.mean(), 2))

    # add some space in between
    st.write('')
    st.write('')

    # display the plotly graph for the locations of the earthquakes
    fig = px.scatter_geo(
        data_frame=eq_df,
        lat='latitude',
        lon='longitude',
        size=eq_df['mag']**2,
        custom_data=['place', 'mag']
    )

    # update the hover data with custom input (place and magnitude)
    fig.update_traces(
        hovertemplate="<br>".join([
        "Place: %{customdata[0]}",
        "Magnitude: %{customdata[1]}"
    ]))

    # put the plotly figure in the streamlit app
    st.plotly_chart(
        figure_or_data=fig,
        use_container_width=True
    )

    # add 
    st.dataframe(eq_df[['place', 'latitude', 'longitude', 'mag', 'depth']])
    st.markdown(get_table_download_link(eq_df), unsafe_allow_html=True)


# this function will allow users to download a csv file of the data
def get_table_download_link(df):
    '''
    This function is used to produce a CSV download link for the dataframe
    that is being used to display the given data. This way users who want
    to look into the data themselves can download the CSV.

    Parameters
    ----------
    df - pd.DataFrame
        The dataframe that we want to allow users to download

        
    Returns
    -------
    An href link that will download the CSV table for the user
    '''

    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download CSV file</a>'

    return href


# write the main body of text for the web application
st.write(
    '''
    # Earthquake Exploration Dashboard
    ## USGS API Data

    This dashboard can be used to explore and investigate earthquake data retrieved from the USGS API service.
    Use the input parameters on the left to adjust the date range and minimum magnitude to display earthquakes around the world! 
    '''
)
st.write('')
st.write('')

# add an start date selection on the sidebar
start_date = st.sidebar.date_input(
    label='Start Date: ',
    value=datetime.datetime.now() - datetime.timedelta(7)
)

# add an end date selection on the sidebar
end_date = st.sidebar.date_input(
    label='End Date: ',
    value=datetime.datetime.now(),
    max_value=datetime.datetime.now()
)

# end a minimum magnitude slider on the sidebar
mag = st.sidebar.slider(
    label='Minimum Magnitude Value: ',
    value=5.0,
    min_value=0.0,
    max_value=10.0,
    step=0.1
)

# run the main function
retrieve_data_from_usgs_api(
    start_date=start_date,
    end_date=end_date,
    min_mag=mag
)