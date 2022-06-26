import json
from turtle import heading
from urllib import response
import webbrowser

from matplotlib import ticker
from matplotlib.ft2font import HORIZONTAL
from nbformat import write
from simplejson import load
import streamlit as st
import pandas as pd
import spacy
#from stock import Stock
import datetime
from streamlit_option_menu import option_menu
from plotly import graph_objs as go
from st_aggrid import AgGrid
import requests
import bs4
from bs4 import BeautifulSoup
import feedparser
from streamlit_lottie import st_lottie

import yfinance as yf
#from prophet import Prophet
# from prophet.plot import plot_plotly
from plotly import graph_objs as go

# st.write("Hello Streamlit")
st.set_page_config(
        page_title="ByTheDip!",
        page_icon="chart_with_upwards_trend",
        layout="wide",
    )
st.markdown("""
<style>
.big-font {
    font-size:18px !important;
}
</style>
""", unsafe_allow_html=True)



#hide side navigation
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)


# side bar menus
with st.sidebar:
    selected = option_menu(
        menu_title="Dashboard",
        options=["Home", "Nifty 50", "BankNifty","Price Prediction", "Crpto Analysis", "Profile", "Feedback","Logout"],
        icons=['house', 'bank', 'kanban', 'cash-coin','currency-bitcoin','emoji-sunglasses','person-rolodex','box-arrow-right'],
    )


START = "2010-1-1"
TODAY = datetime.date.today().strftime("%Y-%m-%d")

#initialize session state
if "load_state" not in st.session_state:
    st.session_state.load_state = False

    

# for Home page
if selected == "Home":
    selected2 = option_menu(
        menu_title='',
        options=['Home','Buzzing News⚡'],
        icons=['rss-fill','newspaper'],
        orientation="horizontal",
                )

    if selected2 == "Home":
        col1 , col2 = st.columns([2,1])
        with col1:
            st.header("Investments are subject to Market Risk")
            st.caption("We recommend analyse fundamentally strong stocks!")
            st.subheader("Let's start from Learning!")
            st.video('https://youtu.be/L8-Y-BhF_wY')
            st.markdown("How to Diversify your portfolio by investing into Bonds | CA Rachana Ranade")
            st.video("https://youtu.be/WmgL7oAUrpw")
        

    if selected2 == "Buzzing News⚡":
            st.header("Today's Trending Market News 📢")

            nlp = spacy.load("en_core_web_sm")


                # stocks_df = pd.read_csv("ind_nifty50list.csv")
                # for title in headings:
                #     doc = nlp(title.text)
                #     for ent in doc.ents:
                #         try:
                #             if stocks_df['Company Name'].str.contains(ent.text).sum():
                #                 symbol = stocks_df[stocks_df['Company Name'].str.contains(ent.text)]['Symbol'].values[0]
                #                 org_name = stocks_df[stocks_df['Company Name'].str.contains(ent.text)]['Company Name'].values[0]

                #                 #sending yfinance symbol
                #                 stock_info = yf.Ticker(symbol+".NS").info



                #                 stock_info_dict['Org'].append(org_name)
                #                 stock_info_dict['Symbol'].append(symbol)
                #                 stock_info_dict['currentPrice'].append(stock_info['currentPrice'])
                #                 stock_info_dict['dayHigh'].append(stock_info['dayHigh'])
                #                 stock_info_dict['dayLow'].append(stock_info['dayLow'])
                #                 stock_info_dict['forwardPE'].append(stock_info['forwardPE'])
                #                 stock_info_dict['dividendYield'].append(stock_info['dividendYield'])
                #             else:
                #                 pass
                #         except:
                #             pass

                # output_df = pd.DataFrame(stock_info_dict)
                # return output_df
            #user_input = st.text_input("Add your RSS link here : ","https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms")
            #get finance headlines


            
            def generate_stock_info(headings):
                stock_info_dict = {
                    'Org': [],
                    'Symbol': [],
                    'currentPrice': [],
                    'dayHigh': [],
                    'dayLow': [],
                    'forwardPE': [],
                    'dividendYield': []
                }



            #idea of using feedparser
            url = "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms"
            f = feedparser.parse(url)
            
           
            with st.expander('Expand for financial stock news'):
                for entry in f.entries:
                    # st.write("* ",entry.title)
                    st.write("* ",entry.title)
                    #st.caption(entry.description)
                        #st.markdown('<p class="big-font">*  !!</p>', unsafe_allow_html=True)
                    st.write(entry.link)



            #fin_headings = extract_text_from_rss()

            #output 
            # output_df = generate_stock_info(fin_headings)
            # output_df.drop_duplicates(inplace=True)
            # st.dataframe(output_df)

            ##display headlines
            # with st.expander("Expand for financial stock news "):
            #     for heading in fin_headings:
            #         st.markdown("* "+heading.text)
            #         for desc in fin_headings:
            #             st.markdown()
                    




                            


        






# for Nifty 50
if selected == "Nifty 50":

    st.title("Know Your Nifty 50 Stock")
    #st.write("Query Parameters")


    stock_list = pd.read_csv('https://raw.githubusercontent.com/Ritishshelke007/Ritishshelke007/main/Nifty50.txt')
    st.subheader("Select Stock")
    stocks_symbol = st.selectbox("", stock_list)
    if stocks_symbol=="Select Your Stock":
        st.header("PLease Select stock before Proceeding further")

    tickerData = yf.Ticker(stocks_symbol)
    #n_years = st.slider("Years of Prediction : ", 1, 4)
    #period = n_years * 365


    @st.cache
    def load_data(ticker):
        data = yf.download(ticker, START, TODAY)
        data.reset_index(inplace=True)
        return data


    data_load_state = st.text("Load data...")
    data = load_data(stocks_symbol)
    data_load_state.text("Loading Data... Please wait for a while!")

    st.subheader("About Company")
    string_logo = '<img src=%s>' % tickerData.info['logo_url']
    st.markdown(string_logo, unsafe_allow_html=True)

    string_name = tickerData.info['longName']
    st.header('**%s**' % string_name)

    string_summary = tickerData.info['longBusinessSummary']
    st.info(string_summary)

    today = datetime.date.today()

    st.header('Price History')
    start_date = st.date_input(
        "From",
        today
    )

    end_date = st.date_input(
        "To",
        today
    )

    tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)
    st.write(tickerDf)

    st.subheader("Share Price since 2015")
    def plot_chart_for_range():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='stock_open'))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='stock_close'))
        fig.layout.update(title_text="Time Series Data",xaxis_rangeslider_visible=True)
        fig.update_layout(xaxis=dict(showgrid=False),
                          yaxis=dict(showgrid=False))
        st.plotly_chart(fig)

    plot_chart_for_range()



# bank nifty 

if selected =='BankNifty':
    st.title("Know Your Bank Nifty Stock")
    bank_stock_list = pd.read_csv('https://raw.githubusercontent.com/Ritishshelke007/Ritishshelke007/main/ind_niftybank.csv')
    st.subheader("Select Bank Stock")
    bank_stocks_symbol = st.selectbox("", bank_stock_list+".NS")
    if bank_stocks_symbol=="Select Your Stock":
        st.header("PLease Select stock before Proceeding further")


    tickerData = yf.Ticker(bank_stocks_symbol)
    #n_years = st.slider("Years of Prediction : ", 1, 4)
    #period = n_years * 365


    @st.cache
    def load_data(ticker):
        data = yf.download(ticker, START, TODAY)
        data.reset_index(inplace=True)
        return data


    data_load_state = st.text("Load data...")
    data = load_data(bank_stocks_symbol)
    data_load_state.text("Loading Data... Please wait for a while!")

    st.subheader("About Company")
    string_logo = '<img src=%s>' % tickerData.info['logo_url']
    st.markdown(string_logo, unsafe_allow_html=True)

    string_name = tickerData.info['longName']
    st.header('**%s**' % string_name)

    string_summary = tickerData.info['longBusinessSummary']
    st.info(string_summary)

    today = datetime.date.today()

    st.header('Price History')
    start_date = st.date_input(
        "From",
        today
    )

    end_date = st.date_input(
        "To",
        today
    )

    tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)
    st.write(tickerDf)

    st.subheader("Share Price since 2015")
    def plot_chart_for_range():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='stock_open'))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='stock_close'))
        fig.layout.update(title_text="Time Series Data",xaxis_rangeslider_visible=True)
        fig.update_layout(xaxis=dict(showgrid=False),
                          yaxis=dict(showgrid=False))
        st.plotly_chart(fig)

    plot_chart_for_range()

if selected == 'Profile':
    def load_lottiefile(filepath: str):
        with open(filepath, "r") as f:
            return json.load(f)

    def load_lottieurl(url : str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    lottie_hello = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_3vbOcw.json")

    st.markdown("<h1 style='text-align: center; color: white;'>Your Profile</h1>", unsafe_allow_html=True)
    st_lottie(
        lottie_hello,
        speed=1,
        reverse=False,
            loop=True,
            quality="low",
        height=400,
        width=500,

    )

    #st_lottie(lottie_hello, key="Hello")

if selected == "Price Prediction":
    link = 'https://stock-predict-app.herokuapp.com/'
    st.markdown('<a href="https://stock-predict-app.herokuapp.com/" target="_self">Click to continue</a>', unsafe_allow_html=True)
    #webbrowser.open("https://stock-predict-app.herokuapp.com/")
    

 

if selected == "Feedback":
    st.header(":mailbox: Get In Touch With Us!")


    contact_form = """
    <form action="https://formsubmit.co/ritishshelke007@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here"></textarea>
        <button type="submit">Send</button>
    </form>
    """

    st.markdown(contact_form, unsafe_allow_html=True)

    # Use Local CSS File
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


    local_css("style2.css")

if selected == "Crpto Analysis":
    st.header('What is cryptocurrency?')
    st.image('images.jpg')
    st.caption('Cryptocurrency is a digital payment system that doesnt rely on banks to verify transactions. It’s a peer-to-peer system that can enable anyone anywhere to send and receive payments. When you transfer cryptocurrency funds, the transactions are recorded in a public ledger. Cryptocurrency is stored in digital wallet .The first cryptocurrency was Bitcoin, which was founded in 2009 and remains the best known today.')

    st.markdown('<a href="https://ritishshelke007-crypto-app-app-91ic3s.streamlitapp.com/" target="_self">Curious about Crypto ? Lets Go for a Journey</a>', unsafe_allow_html=True)
