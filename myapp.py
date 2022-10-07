import streamlit as st
import pandas as pd
import altair as alt
from datetime import date, datetime
import calendar
import requests
from streamlit_lottie import st_lottie

### Animation assets ###

left_column, center_column, right_column = st.columns(3)

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_coding = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_p1nm0xis.json")

def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():

    st.title("Gridaxon -- ERCOT DASHBOARD")
    st.write(
        "An efficient and effective way to analyze ERCOT Data"
    )

    st.header("Monthly Analysis")

    col1, col2 = st.columns(2)

    # with col1:
    #     start_date = st.date_input(
    #         "Select start date",
    #         date(2020, 1, 1),
    #         min_value=datetime.strptime("2020-01-01", "%Y-%m-%d"),
    #         max_value=datetime.now(),
    #     )

    with col1:
        year_selected = st.selectbox(
            "Select the year", ("2021", "2022")
        )

    with col2:
        month_selected = st.selectbox(
            "Select the month", ("January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December")
        )

    df = pd.read_csv('rpt.00013091.0000000000000000.20220101080017.DAMASMCPC_2021.csv')
    # ts_df = df[['Delivery Date','REGDN']]
    ts_df = df[['Delivery Date', 'Hour Ending','REGDN']]
    ts_df = ts_df.replace('24:00', '00:00')
    # ts_df['Delivery Date'] = pd.to_datetime(ts_df['Delivery Date'] +' '+ ts_df['Hour Ending']).dt.date
    ts_df['Delivery Date'] = pd.to_datetime(ts_df['Delivery Date'] +' '+ ts_df['Hour Ending'])

    # ts_df = ts_df.set_index('Delivery Date')
    # pd.to_datetime(ts_df['Delivery Date'])

    # st.line_chart(ts_df[:1000])

    month_names = list(calendar.month_name)
    month_number = month_names.index(month_selected)

    start_date = pd.to_datetime(date(int(year_selected), month_number, 1))
    end_date = pd.to_datetime(date(int(year_selected), month_number, calendar.monthrange(int(year_selected), month_number)[1]))

    mask = (ts_df['Delivery Date'] >= start_date) & (ts_df['Delivery Date'] <= end_date)


    source = ts_df[mask]

    hover = alt.selection_single(
        fields=['Delivery Date'], #Cross check what exactly this does
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(source)
        .mark_line(point="transparent")
        .encode(x='Delivery Date',y='REGDN')
        # .transform_calculate(color='datum.delta < 0 ? "red" : "green"')
    )

    # Draw points on the line, highlight based on selection, color based on delta
    points = (
        lines.transform_filter(hover)
        .mark_circle(size=65)
        .encode()
    )

    # Draw an invisible rule at the location of the selection
    tooltips = (
        alt.Chart(source)
        .mark_rule(opacity=0)
        .encode(
            x='Delivery Date',
            y='REGDN',
            tooltip=['Delivery Date', 'Hour Ending','REGDN'],
        )
        .add_selection(hover)
    )

    # c = alt.Chart(ts_df[:1000]).mark_line().encode(x='Delivery Date',y='REGDN', tooltip=['Delivery Date', 'Hour Ending','REGDN'])

    st.altair_chart((lines + points + tooltips).interactive(), use_container_width=True)


    ### Second chart ###

    st.header("Custom Date Analysis")

    col3, col4 = st.columns(2)

    with col3:
        start_date_2 = st.date_input(
            "Select start date",
            date(2021, 1, 1),
            min_value=datetime.strptime("2021-01-01", "%Y-%m-%d"),
            max_value=datetime.now(),
        )

    with col4:
        end_date_2 = st.date_input(
            "Select end date",
            date(2021, 1, 1),
            min_value=datetime.strptime("2021-01-01", "%Y-%m-%d"),
            max_value=datetime.now(),
        )

    # start_date_2 = ts_df['Delivery Date'][0]
    # end_date_2 = ts_df['Delivery Date'][len(ts_df['Delivery Date'])-1]

    start_date_2 = pd.to_datetime(start_date_2)
    end_date_2 = pd.to_datetime(end_date_2)

    mask = (ts_df['Delivery Date'] >= start_date_2) & (ts_df['Delivery Date'] <= end_date_2)


    source = ts_df[mask]

    hover = alt.selection_single(
        fields=['Delivery Date'], #Cross check what exactly this does
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(source)
        .mark_line(point="transparent")
        .encode(x='Delivery Date',y='REGDN')
        # .transform_calculate(color='datum.delta < 0 ? "red" : "green"')
    )

    # Draw points on the line, highlight based on selection, color based on delta
    points = (
        lines.transform_filter(hover)
        .mark_circle(size=65)
        .encode()
    )

    # Draw an invisible rule at the location of the selection
    tooltips = (
        alt.Chart(source)
        .mark_rule(opacity=0)
        .encode(
            x='Delivery Date',
            y='REGDN',
            tooltip=['Delivery Date', 'Hour Ending','REGDN'],
        )
        .add_selection(hover)
    )

    # c = alt.Chart(ts_df[:1000]).mark_line().encode(x='Delivery Date',y='REGDN', tooltip=['Delivery Date', 'Hour Ending','REGDN'])

    st.altair_chart((lines + points + tooltips).interactive(), use_container_width=True)

with center_column:
    st_lottie(lottie_coding, height=300, key="coding")