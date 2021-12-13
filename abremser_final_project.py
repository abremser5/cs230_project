"""
Name: AJ Bremser
Course: CS230
Data: NCAA football stadiums
URL:

Description:
This program helps visualize the information about the 252 division 1 football
stadiums by using the file "stadums.csv". From this file, I created a data frame to
pull data from in order to make charts and maps. Streamlit, pandas, and
matplotlib.pyplot were especially useful in creating this project.
"""
# Import statements
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# Put our streamlit title info at the top
st.title("NCAA football stadiums data visualization project")
st.header("By AJ Bremser")
default_stadium_count = 25

# Define our filename and read it using pandas
def openfile():
    FILENAME = "stadums.csv"
    df_stadiums = pd.read_csv(FILENAME).set_index("stadium")
    return df_stadiums


# Open video to play for streamlit (this is a function that doesn't return a value)
# Did a video, which we didn't learn in class
def openvideo():
    st.sidebar.video("https://www.youtube.com/watch?v=FSqhicmUINQ")


# The lines below are mostly intro code to help better understand the data
# To get a preliminary look at our data, view the first five lines of it
print(openfile().head(5))
# View our file's column names
print(openfile().columns)

# check for missing data
print(openfile().isna().sum())
# 107 stadiums weren't expanded, would need to clean this data formatting if used
# The data itself is accurate and authentic in form
print(100 * "-")

# filter the data into fbs and fcs:
print("FBS teams:")
df_fbs = openfile()
df_fbs = df_fbs.loc[df_fbs["div"].isin(["fbs"])]
# Print corresponding team names of the first stadiums involved in the fbs division
print(df_fbs["team"].head(8))
# Average capacity of FBS stadiums
fbs_avg_cap = int(df_fbs["capacity"].mean())
print(fbs_avg_cap)
print()
print(100 * "-")
print()
print("FCS teams average capacity:")
df_fcs = openfile()
df_fcs = df_fcs.loc[df_fcs["div"] == "fcs"]
fcs_avg_cap = int(df_fcs["capacity"].mean())
# Average capacity of FCS stadiums
print(fcs_avg_cap)


def bar(selected_color, data_div):
    s = data_div
    x = ("FBS", "FCS")
    plt.title("FBS vs FCS stadium capacity")
    plt.bar(x, s, color=selected_color)
    return plt

# Creating a bar chart outside of a defined function to show there's many ways to code
data_div = [fbs_avg_cap, fcs_avg_cap]
# Use of dictionary
color_options = {"red": "r", "crimson": "crimson",
                 "dark orchid": "darkorchid", "hot pink": "hotpink",
                 "lime": "lime", "black": "k", "teal": "teal",
                 "blue": "b", "cyan": "c"}
color_names = list(color_options.keys())
selected_color = st.sidebar.radio('Bar Chart Color:', color_names)
# Produce the bar chart in streamlit
st.pyplot(bar(color_options[selected_color], data_div))
st.write(f"The average stadium capacity of a FBS team is {fbs_avg_cap:,}. "
         f"For a FCS team, the average capacity is {fcs_avg_cap:,}.")


def map_all_teams():
    df_stadiums = openfile()
    st.header("All Stadiums in NCAAF Division 1:")
    st.map(df_stadiums, zoom=st.slider("Choose a factor to zoom by", 0.5, 16.0, 0.5))


def find_biggest_stadiums(default_stadium_count):
    df_stadiums = openfile()
    # Make data frame of 25 largest NCAAF stadiums (counts for sorting data req.)
    huge_stadiums = df_stadiums.nlargest(default_stadium_count, ["capacity"])
    df_huge = pd.DataFrame(huge_stadiums, columns=["team", "capacity",
                                                   "latitude", "longitude"])
    st.header("Biggest 25 Stadiums in NCAAF:")
    st.dataframe(df_huge)
    st.map(df_huge)


default_states = ["GA", "MA", "TX", "WA", "WY"]
default_division = ["fbs"]


def filtered_data(state_name, division_name):
    df_stadiums = openfile()
    # Remove unnecessary columns
    df_stadiums.drop(["capacity", "city", "built", "expanded", "latitude",
                      "longitude"], axis=1, inplace=True)
    df_stadiums = df_stadiums.loc[df_stadiums["state"].isin(state_name)]
    df_stadiums = df_stadiums.loc[df_stadiums["div"].isin(division_name)]
    return df_stadiums

# This code section took me a bit of time, and I definitely am happy about how
# it turned out and how the f-string in the "if" statement simplifies file reading
def dropdown():
    st.subheader("Take a look at the biggest 8 stadiums in college football!")
    df_stadiums = openfile()
    df_top_8_size = df_stadiums.sort_values(by='capacity', ascending=False)[:8]
    team_names = df_top_8_size["team"].tolist()
    selected_name = st.selectbox("Select a team:", team_names)
    st.write(f"Viewing a picture of {selected_name}'s stadium")
    if selected_name in team_names:
        img = Image.open(f"{selected_name.lower()}_stadium.jpg")
        st.image(img, width=750)


def balloons():
    if st.sidebar.button("Celebrate when done!"):
        st.balloons()


# Run query of the function filtered_data
def query_piechart():
    df_filtered = filtered_data(default_states, default_division)
    # Frequency of each of the five default states in our data
    frequency = [df_filtered.loc[df_filtered["state"].isin([state])].shape[0] for state in default_states]
    explode_val = [0, 0.15, 0, 0, 0]
    plt.figure()
    plt.pie(frequency, labels=default_states, explode=explode_val,
            autopct="%.2f%%")
    for i in range(len(default_states)):
        st.write(f"The state {default_states[i]} has {frequency[i]} stadium(s) in the"
                 f" NCAA Football Bowl Subdivision (FBS).")
    return plt


def main():
    openvideo()
    map_all_teams()
    st.write("Only one state doesn't have a team in division one college football.")
    st.subheader("Filtered by teams in states GA, MA, TX, WA, and WY who are also in FBS")
    st.pyplot(query_piechart())
    find_biggest_stadiums(default_stadium_count)
    dropdown()
    #folium_map()
    balloons()
    # Print blank lines on streamlit to better space out the file
    st.subheader("")
    st.subheader("")
    st.subheader("I hope you enjoyed my work and my presentation. "
                 "Thank you for listening!")


main()


# References (just links and not in APA format since it wasn't specified):
# https://docs.streamlit.io/streamlit-cloud/get-started
# https://docs.streamlit.io/library/api-reference/media/st.video
# All 8 stadium images from google images
