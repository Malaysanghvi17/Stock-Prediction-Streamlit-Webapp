# streamlit run integrated.py

import requests
import smtplib
from string import Template
from bs4 import BeautifulSoup
from matplotlib.pyplot import axis
import streamlit as st  # streamlit library
import pandas as pd  # pandas library
import yfinance as yf  # yfinance library
import datetime  # datetime library
from datetime import date
from plotly import graph_objs as go  # plotly library
from plotly.subplots import make_subplots
from prophet import Prophet  # prophet library
# plotly library for prophet model plotting
from prophet.plot import plot_plotly
import time  # time library
from streamlit_option_menu import option_menu  # select_options library
import streamlit as st
import streamlit_authenticator as stauth
hashed_passwords = stauth.Hasher(['abc', 'def']).generate()
import yaml
from yaml.loader import SafeLoader
import bcrypt
from streamlit_lottie import st_lottie
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

        
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
    
lottie_coding = load_lottiefile("ani1.json")  # replace link to local lottie file
def get_stock_data(company_name):
    print(company_name, '\n')
    company_name = company_name.replace('.NS', '')
    print(company_name, '\n')
    
    
    f_url = "https://www.google.com/finance/quote/"
    # e_url = ":NSE?sa=X&ved=2ahUKEwjY-rKLvuaBAxWNklYBHf-yCLEQ3ecFegQIXhAf"
    e_url = ":NSE"
    
    url = f_url + company_name + e_url
    print(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    try:
        price = soup.find('div', class_="YMlKec fxKbKc").text
        print(price, '\n')
    except Exception:
        price = "No Data Available"
        print()

    try:
        # pc = soup.find('div', class_="mfs7Fc").text
        pcp = soup.find('div', class_="P6K39c").text
        
        # print(pc, '\n')
        print(pcp, '\n')
        
    except Exception:
        pc, pcp = "No Data Available", "No Data Available"

    try:
        # dr = soup.find_all('div', class_="mfs7Fc")[1].text
        drp = soup.find_all('div', class_="P6K39c")[1].text
        
        # print(dr, '\n')
        print(drp, '\n')
        
    except Exception:
        dr, drp = "No Data Available", "No Data Available"

    try:
        # yr = soup.find_all('div', class_="mfs7Fc")[2].text
        yrp = soup.find_all('div', class_="P6K39c")[2].text
        
        # print(yr, '\n')
        print(yrp, '\n')
        
    except Exception:
        yr, yrp = "No Data Available", "No Data Available"

    try:
        # mc = soup.find_all('div', class_="mfs7Fc")[3].text
        mcp = soup.find_all('div', class_="P6K39c")[3].text
        
        # print(mc, '\n')
        print(mcp, '\n')
        
    except Exception:
        mc, mcp = "No Data Available", "No Data Available"
        
    # Details about the Company
    print(f"Details about the Company - {company_name}\n")
    
    try:
        about = soup.find('div', class_ = "bLLb2d")
        print(about.text)
        print()
    except Exception as e:
        print(f'No Data Available\n')
        
    #News about the company

    try:
        print("Latest News about the company")
        print()

        np1 = soup.find_all('div', class_ = "sfyJob")[0]
        print(np1.text)

        n1 = soup.find_all('div', class_ = "Yfwt5")[0]
        print(n1.text)
        print()
        
    except Exception as e:
        print(f'No Latest news Available\n')

    try:
        np2 = soup.find_all('div', class_ = "sfyJob")[1]
        print(np2.text)
        print()

        n2 = soup.find_all('div', class_ = "Yfwt5")[1]
        print(n2.text)
        print()

    except Exception as e:
        print(f'No other News Available\n')

    # np3 = soup.find_all('div', class_ = "sfyJob")[2]
    # print(np3.text)

    # n3 = soup.find_all('div', class_ = "Yfwt5")[2]
    # print(n3.text)
    # print()

    # except Exception as e:
    #     print(f"No News Available")

    return price, pcp, drp, yrp, mcp, about, np1, n1, np2, n2



def stock_analysis():
    # st.set_page_config(layout="wide", initial_sidebar_state="expanded")

    def add_meta_tag():
        meta_tag = """
            <head>
                <meta name="google-site-verification" content="QBiAoAo1GAkCBe1QoWq-dQ1RjtPHeFPyzkqJqsrqW-s" />
            </head>
        """
        st.markdown(meta_tag, unsafe_allow_html=True)

    # Main code
    add_meta_tag()

    # Sidebar Section Starts Here
    today = date.today()  # today's date
    st.write('''# StockStream ''')  # title
    # st.sidebar.image("Images/StockStreamLogo1.png", width=250,
    #                 use_column_width=False)  # logo

    with st.sidebar:
                  
        st_lottie(
            lottie_coding,
            speed=1,
            reverse=False,
            loop=True,
            quality="low",
            height=None,
            width=None,
            key=None,   
        )

    st.sidebar.write('''# StockStream ''')

    with st.sidebar: 
            selected = option_menu("Utilities", ["Stocks Performance Comparison", "Real-Time Stock Price", "Stock Prediction", 'About'])

    start = st.sidebar.date_input(
        'Start', datetime.date(2022, 1, 1))  # start date input
    end = st.sidebar.date_input('End', datetime.date.today())  # end date input
    # Sidebar Section Ends Here

    # read csv file
    stock_df = pd.read_csv("StockStreamTickersData.csv")

    # Stock Performance Comparison Section Starts Here
    if(selected == 'Stocks Performance Comparison'):  # if user selects 'Stocks Performance Comparison'
        st.subheader("Stocks Performance Comparison")
        tickers = stock_df["Company Name"]
        # dropdown for selecting assets
        dropdown = st.multiselect('Pick your assets', tickers)

        with st.spinner('Loading...'):  # spinner while loading
            time.sleep(2)
            # st.success('Loaded')

        dict_csv = pd.read_csv('StockStreamTickersData.csv', header=None, index_col=0).to_dict()[1]  # read csv file
        symb_list = []  # list for storing symbols
        for i in dropdown:  # for each asset selected
            val = dict_csv.get(i)  # get symbol from csv file
            symb_list.append(val)  # append symbol to list

        def relativeret(df):  # function for calculating relative return
            rel = df.pct_change()  # calculate relative return
            cumret = (1+rel).cumprod() - 1  # calculate cumulative return
            cumret = cumret.fillna(0)  # fill NaN values with 0
            return cumret  # return cumulative return

        if len(dropdown) > 0:  # if user selects atleast one asset
            df = relativeret(yf.download(symb_list, start, end))[
                'Adj Close']  # download data from yfinance
            # download data from yfinance
            raw_df = relativeret(yf.download(symb_list, start, end))
            raw_df.reset_index(inplace=True)  # reset index

            closingPrice = yf.download(symb_list, start, end)[
                'Adj Close']  # download data from yfinance
            volume = yf.download(symb_list, start, end)['Volume']
            
            st.subheader('Raw Data {}'.format(dropdown))
            st.write(raw_df)  # display raw data
            chart = ('Line Chart', 'Area Chart', 'Bar Chart')  # chart types
            # dropdown for selecting chart type
            dropdown1 = st.selectbox('Pick your chart', chart)
            with st.spinner('Loading...'):  # spinner while loading
                time.sleep(2)

            st.subheader('Relative Returns {}'.format(dropdown))
                    
            if (dropdown1) == 'Line Chart':  # if user selects 'Line Chart'
                st.line_chart(df)  # display line chart
                # display closing price of selected assets
                st.write("### Closing Price of {}".format(dropdown))
                st.line_chart(closingPrice)  # display line chart

                # display volume of selected assets
                st.write("### Volume of {}".format(dropdown))
                st.line_chart(volume)  # display line chart

            elif (dropdown1) == 'Area Chart':  # if user selects 'Area Chart'
                st.area_chart(df)  # display area chart
                # display closing price of selected assets
                st.write("### Closing Price of {}".format(dropdown))
                st.area_chart(closingPrice)  # display area chart

                # display volume of selected assets
                st.write("### Volume of {}".format(dropdown))
                st.area_chart(volume)  # display area chart

            elif (dropdown1) == 'Bar Chart':  # if user selects 'Bar Chart'
                st.bar_chart(df)  # display bar chart
                # display closing price of selected assets
                st.write("### Closing Price of {}".format(dropdown))
                st.bar_chart(closingPrice)  # display bar chart

                # display volume of selected assets
                st.write("### Volume of {}".format(dropdown))
                st.bar_chart(volume)  # display bar chart

            else:
                st.line_chart(df, width=1000, height=800,
                            use_container_width=False)  # display line chart
                # display closing price of selected assets
                st.write("### Closing Price of {}".format(dropdown))
                st.line_chart(closingPrice)  # display line chart

                # display volume of selected assets
                st.write("### Volume of {}".format(dropdown))
                st.line_chart(volume)  # display line chart

        else:  # if user doesn't select any asset
            st.write('Please select atleast one asset')  # display message
    # Stock Performance Comparison Section Ends Here
    
    
    # Real-Time Stock Price Section Starts Here
    elif selected == 'Real-Time Stock Price':
        st.subheader("Real-Time Stock Price")
        tickers = stock_df["Company Name"]  # get company names from csv file
        a = st.selectbox('Pick a Company', tickers)  # dropdown for selecting company

        with st.spinner('Loading...'):  # spinner while loading
            time.sleep(2)

        dict_csv = pd.read_csv('StockStreamTickersData.csv', header=None, index_col=0).to_dict()[1]  # read csv file
        symb_list = []  # list for storing symbols
        val = dict_csv.get(a)  # get symbol from csv file
        symb_list.append(val)  # append symbol to list

        if "button_clicked" not in st.session_state:  # if button is not clicked
            st.session_state.button_clicked = False  # set button clicked to false

        def callback():  # function for updating data
            # if button is clicked
            st.session_state.button_clicked = True  # set button clicked to true

        if (
            st.button("Search", on_click=callback)  # button for searching data
            or st.session_state.button_clicked  # if button is clicked
        ):
            if a == "":  # if user doesn't select any company
                st.write("Click Search to Search for a Company")
                with st.spinner('Loading...'):  # spinner while loading
                    time.sleep(2)
            else:  # if user selects a company
                # download data from yfinance
                data = yf.download(symb_list, start=start, end=end)
                data.reset_index(inplace=True)  # reset index
                st.subheader('Raw Data of {}'.format(a))  # display raw data
                st.write(data)  # display data

                def plot_raw_data():  # function for plotting raw data
                    fig = go.Figure()  # create figure
                    fig.add_trace(go.Scatter(  # add scatter plot
                        x=data['Date'], y=data['Open'], name="stock_open"))  # x-axis: date, y-axis: open
                    fig.add_trace(go.Scatter(  # add scatter plot
                        x=data['Date'], y=data['Close'], name="stock_close"))  # x-axis: date, y-axis: close
                    fig.layout.update(  # update layout
                        title_text='Line Chart of {}'.format(a), xaxis_rangeslider_visible=True)  # title, x-axis: rangeslider
                    st.plotly_chart(fig)  # display plotly chart

                def plot_candle_data():  # function for plotting candle data
                    fig = go.Figure()  # create figure
                    fig.add_trace(go.Candlestick(x=data['Date'],  # add candlestick plot
                                                # x-axis: date, open
                                                open=data['Open'],
                                                high=data['High'],  # y-axis: high
                                                low=data['Low'],  # y-axis: low
                                                close=data['Close'], name='market data'))  # y-axis: close
                    fig.update_layout(  # update layout
                        title='Candlestick Chart of {}'.format(a),  # title
                        yaxis_title='Stock Price',  # y-axis: title
                        xaxis_title='Date')  # x-axis: title
                    st.plotly_chart(fig)  # display plotly chart

                chart = ('Candle Stick', 'Line Chart')  # chart types
                # dropdown for selecting chart type
                dropdown1 = st.selectbox('Pick your chart', chart)
                with st.spinner('Loading...'):  # spinner while loading
                    time.sleep(2)
                if dropdown1 == 'Candle Stick':  # if user selects 'Candle Stick'
                    plot_candle_data()  # plot candle data
                elif dropdown1 == 'Line Chart':  # if user selects 'Line Chart'
                    plot_raw_data()  # plot raw data
                else:  # if user doesn't select any chart
                    plot_candle_data()  # plot candle data

                # Call get_stock_data to fetch real-time stock data
                price, pcp, drp, yrp, mcp, about, np1, n1, np2, n2 = get_stock_data(val)

                # Display the real-time stock data
                st.subheader('Real-Time Stock Data for {}'.format(a))
                st.write("Current Price:", price)
                st.write("Percentage Change:", pcp)
                st.write("Day's Range Percentage:", drp)
                st.write("52-Week Range Percentage:", yrp)
                st.write("Market Cap Percentage:", mcp)
                
                st.subheader("About the Company")
                
                st.markdown(about, unsafe_allow_html=True)
                
                st.subheader("NEWS About the Company")
                
                st.markdown(np1, unsafe_allow_html=True)
                st.markdown(n1, unsafe_allow_html=True)
                st.markdown(np2, unsafe_allow_html=True)
                st.markdown(n2, unsafe_allow_html=True)
    # Real-Time Stock Price Section Ends Here

    # Stock Price Prediction Section Starts Here
    elif(selected == 'Stock Prediction'):  # if user selects 'Stock Prediction'
        st.subheader("Stock Prediction")

        tickers = stock_df["Company Name"]  # get company names from csv file
        # dropdown for selecting company
        a = st.selectbox('Pick a Company', tickers)
        with st.spinner('Loading...'):  # spinner while loading
                time.sleep(2)
        dict_csv = pd.read_csv('StockStreamTickersData.csv', header=None, index_col=0).to_dict()[1]  # read csv file
        symb_list = []  # list for storing symbols
        val = dict_csv.get(a)  # get symbol from csv file
        symb_list.append(val)  # append symbol to list
        if(a == ""):  # if user doesn't select any company
            st.write("Enter a Stock Name")  # display message
        else:  # if user selects a company
            # download data from yfinance
            data = yf.download(symb_list, start=start, end=end)
            data.reset_index(inplace=True)  # reset index
            st.subheader('Raw Data of {}'.format(a))  # display raw data
            st.write(data)  # display data

            def plot_raw_data():  # function for plotting raw data
                fig = go.Figure()  # create figure
                fig.add_trace(go.Scatter(  # add scatter plot
                    x=data['Date'], y=data['Open'], name="stock_open"))  # x-axis: date, y-axis: open
                fig.add_trace(go.Scatter(  # add scatter plot
                    x=data['Date'], y=data['Close'], name="stock_close"))  # x-axis: date, y-axis: close
                fig.layout.update(  # update layout
                    title_text='Time Series Data of {}'.format(a), xaxis_rangeslider_visible=True)  # title, x-axis: rangeslider
                st.plotly_chart(fig)  # display plotly chart

            plot_raw_data()  # plot raw data
            # slider for selecting number of years
            n_years = st.slider('Years of prediction:', 1, 4)
            period = n_years * 365  # calculate number of days

            # Predict forecast with Prophet
            # create dataframe for training data
            df_train = data[['Date', 'Close']]
            df_train = df_train.rename(
                columns={"Date": "ds", "Close": "y"})  # rename columns

            m = Prophet()  # create object for prophet
            m.fit(df_train)  # fit data to prophet
            future = m.make_future_dataframe(
                periods=period)  # create future dataframe
            forecast = m.predict(future)  # predict future dataframe

            # Show and plot forecast
            st.subheader('Forecast Data of {}'.format(a))  # display forecast data
            st.write(forecast)  # display forecast data

            st.subheader(f'Forecast plot for {n_years} years')  # display message
            fig1 = plot_plotly(m, forecast)  # plot forecast
            st.plotly_chart(fig1)  # display plotly chart

            st.subheader("Forecast components of {}".format(a))  # display message
            fig2 = m.plot_components(forecast)  # plot forecast components
            st.write(fig2)  # display plotly chart

    # Stock Price Prediction Section Ends Here
    elif(selected == 'About'):
        st.subheader("About")
        
        st.markdown("""
            <style>
        .big-font {
            font-size:25px !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<p class="big-font">StockStream is a web application that allows users to visualize Stock Performance Comparison, Real-Time Stock Prices and Stock Price Prediction. This application is developed using Streamlit. Streamlit is an open source app framework in Python language. It helps users to create web apps for Data Science and Machine Learning in a short time. This Project is developed by Vishesh Rathi, Ansh Bhimani, Chintan Patil, Malay Sanghvi and Yash Lakhani. You can find more about the developers on their GitHub Profiles shared below.<br>Hope you are able to employ this application well and get your desired output.<br> Cheers!</p>', unsafe_allow_html=True)

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

authenticator.login('Login', 'main')

if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main', key='unique_key')
    with st.sidebar:
        selected_option = st.selectbox("Select an action", ["Other Action", "Reset Password"])

        if selected_option == "Reset Password":
            try:
                if authenticator.reset_password(st.session_state["username"], 'Reset password'):
                    st.success('Password modified successfully')
                with open('config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
            except Exception as e:
                st.error(e)

    st.subheader(f'Welcome *{st.session_state["name"]}*')
    stock_analysis()
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')

# else:
if not(st.session_state["authentication_status"]):
        try:
            if authenticator.register_user('Register user', preauthorization=False):
                st.success('User registered successfully')
        except Exception as e:
            st.error(e)
        try:
            username_of_forgotten_password, email_of_forgotten_password, new_random_password = authenticator.forgot_password('Forgot password')
            if username_of_forgotten_password:
                email_address = "python.project.smtp@gmail.com"
                password = "kbxwsbiftmwwlade"
                # def read_template():
                    # with open("message.txt", 'r', encoding='utf-8') as template_file:
                    #     template_file_content = template_file.read()
                    # return Template(template_file_content)

                def send_email(email, name, subject, message):
                    s = smtplib.SMTP('smtp.gmail.com', 587)
                    s.starttls()
                    s.login(email_address, password)
                    s.sendmail(email_address, email, message)
                    s.quit()   


                send_email(email_of_forgotten_password,"password sent!","reset password",new_random_password)
                st.success('New password to be sent securely over mail!')
                # Random password should be transferred to user securely
                with open('config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
            else:
                st.error('Username not found')
        except Exception as e:
            st.error(e)
        # try:
        #     username_of_forgotten_password, email_of_forgotten_password, new_random_password = authenticator.forgot_password('Forgot password')
        #     if username_of_forgotten_password:
        #         st.success('New password to be sent securely')
        #         # Random password should be transferred to user securely
        #     else:
        #         st.error('Username not found')
        except Exception as e:
            st.error(e)
        if st.session_state["authentication_status"]:
            try:
                if authenticator.update_user_details(st.session_state["username"], 'Update user details'):
                    st.success('Entries updated successfully')
            except Exception as e:
                st.error(e)
        with open('config.yaml', 'w') as file:
            yaml.dump(config, file, default_flow_style=False)