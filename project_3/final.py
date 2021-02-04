import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

files_dict = {'23 nov' : '23-11-2020.csv',
              '24 nov' : '24-11-2020.csv',
              '25 nov' : '25-11-2020.csv',
              '26 nov' : '26-11-2020.csv',
              '27 nov' : '27-11-2020.csv'}
st.title('Covid-19 Dashboard for Sentiment Analysis')
st.markdown(
    'The dashboard will visualize and represent the sentiment analysis that was done on the posts from social media websites: Twitter & Reddit')
st.sidebar.title('Visualization Selector')
st.sidebar.markdown('Select the Charts/Plots accordingly:')


# @st.cache(persist=True)( If you have a different use case where the data does not change so very often, you can simply use this)

def getter(c, stat):
    column_names = ["timestamp", "polarity"]
    df = pd.DataFrame(columns=column_names)
    for i in range(len(c)):
        if str(c['polarity'][i]) == stat:
            df = df.append({'timestamp': c['timestamp'][i], 'polarity': c['polarity'][i]}, ignore_index=True)
    return df

def words(df):
        posts = df
        comment_words = ''
        stopwords = set(STOPWORDS)
        stopwords.add("https")
        lst = []
        # iterate through the csv file
        for val in posts:
            # typecaste each val to string
            val = str(val)
            # split the value
            tokens = val.split()
            # Converts each token into lowercase
            for i in range(len(tokens)):
                tokens[i] = tokens[i].lower()

            comment_words += " ".join(tokens) + " "
        wordcloud = WordCloud(width=800, height=800,
                              background_color='black',
                              stopwords=stopwords,
                              min_font_size=10).generate(comment_words)

        # plot the WordCloud image
        plt.figure(figsize=(5, 5), facecolor=None)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

lst = ['Reddit', 'Twitter']
platform_input = st.sidebar.selectbox(
    'Platform', lst)

if platform_input == 'Reddit':
    DATA_URL = ('final_dat.csv')
    covid_data = pd.read_csv(DATA_URL)
if platform_input == 'Twitter':
     DATA_URL = ('twitter_1.csv')
     covid_data = pd.read_csv(DATA_URL)
     dates = ['23 nov', '24 nov', '25 nov', '26 nov', '27 nov']
     date_input = st.sidebar.selectbox(
    'Select date', dates)

lst2 = ['Bar', 'Line', 'WordCloud']
visualization = st.sidebar.selectbox(
    'Plot Type', lst2)

chk = st.sidebar.checkbox("Filters", True, key=1)
st.sidebar.markdown("Uncheck 'Filters' to see all sentiment together!")
select_status = st.sidebar.radio("Covid-19 patient's status", ('Postive',
                                                               'Neutral', 'Negative'))

if chk:
    # if false display all negative pos neu
    # select = st.sidebar.selectbox('Select a State',df['state'])
    st.markdown("NB Classifier Plots:")
    # st.markdown("NB Classifier Plots:")
    if platform_input == 'Reddit' and not st.checkbox('Hide Graph', False, key=1):
        if select_status == 'Postive':
            if visualization == 'Bar':
                state_total_graph = px.bar(
                    covid_data,
                    x='timestamp',
                    y='pos',
                    labels={'here'},
                    color='pos')
                st.plotly_chart(state_total_graph)
            if visualization == 'Line':
                state_total_graph = px.line(
                    covid_data,
                    x='timestamp',
                    y='pos',
                    labels={'here'})
                st.plotly_chart(state_total_graph)
            st.markdown("For Positive")
        if select_status == 'Negative':
            if visualization == 'Bar':
                state_total_graph = px.bar(
                    covid_data,
                    x='timestamp',
                    y='neg',
                    labels={'here'},
                    color='neg')
                st.plotly_chart(state_total_graph)
            if visualization == 'Line':
                state_total_graph = px.line(
                    covid_data,
                    x='timestamp',
                    y='neg',
                    labels={'here'})
                st.plotly_chart(state_total_graph)
            st.markdown("For Negative")
        if select_status == 'Neutral':
            if visualization == 'Bar':
                state_total_graph = px.bar(
                    covid_data,
                    x='timestamp',
                    y='neu',
                    labels={'here'},
                    color='neu')
                st.plotly_chart(state_total_graph)
            if visualization == 'Line':
                state_total_graph = px.line(
                    covid_data,
                    x='timestamp',
                    y='neu',
                    labels={'here'})
                st.plotly_chart(state_total_graph)
                st.markdown("For Neutral")
        if visualization == 'WordCloud':
            posts = pd.read_csv('posts.csv')
            comment_words = ''
            stopwords = set(STOPWORDS)
            lst = []
            # iterate through the csv file
            for val in posts.title:

                # typecaste each val to string
                val = str(val)

                # split the value
                tokens = val.split()

                # Converts each token into lowercase
                for i in range(len(tokens)):
                    tokens[i] = tokens[i].lower()

                comment_words += " ".join(tokens) + " "
            wordcloud = WordCloud(width=800, height=800,
                                  background_color='black',
                                  stopwords=stopwords,
                                  min_font_size=10).generate(comment_words)

            # plot the WordCloud image
            plt.figure(figsize=(5, 5), facecolor=None)
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.show()
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot()
            st.markdown("WordCloud is a compilation of all the polarity words")
    if platform_input == 'Twitter' and not st.checkbox('Hide Graph', False, key=1):
        for k, v in files_dict.items():
            if date_input == k:
                df = pd.read_csv(v)
                df['timestamp'] = pd.to_datetime(df['timestamp'], dayfirst=True)
                if select_status:
                    if select_status == 'Postive':
                        c = getter(df, 'pos')
                        # print(len(c))
                        c = c.resample('120min', on='timestamp').polarity.count()
                        st.markdown('Positive polarity count for ' + date_input)
                        if visualization == 'Bar':
                            st.bar_chart(c)
                        if visualization == 'Line':
                            st.line_chart(c)
                        if visualization == 'WordCloud':
                            words(df['title'])
                    if select_status == 'Negative':
                        c = getter(df, 'neg')
                        c = c.resample('120min', on='timestamp').polarity.count()
                        st.markdown('Negative polarity count for ' + date_input)
                        if visualization == 'Bar':
                            st.bar_chart(c)
                        if visualization == 'Line':
                            st.line_chart(c)
                        if visualization == 'WordCloud':
                            words(df['title'])
                    if select_status == 'Neutral':
                        c = getter(df, 'neu')
                        # print(len(c))
                        c = c.resample('120min', on='timestamp').polarity.count()
                        st.markdown('Neutral polarity count for ' + date_input)
                        if visualization == 'Bar':
                            st.bar_chart(c)
                        if visualization == 'Line':
                            st.line_chart(c)
                        if visualization == 'WordCloud':
                            words(df['title'])
else:
    if platform_input == 'Reddit':
        st.markdown("NB Classifier Plots:")
        if select_status:
            if visualization == 'Bar':
                c = pd.read_csv('Book1.csv')
                state_total_graph = px.bar(
                    c,
                    x='timestamp',
                    y='count',
                    labels={'here'},
                    color='polarity')
                st.plotly_chart(state_total_graph)
            if visualization == 'Line':
                c = pd.read_csv('Book1.csv')
                state_total_graph = px.line(
                    c,
                    x='timestamp',
                    y='count',
                    labels={'here'},
                    color='polarity')
                st.plotly_chart(state_total_graph)
            st.markdown("Plot for all polarities")

            if visualization == 'WordCloud':
                posts = pd.read_csv('posts.csv')
                comment_words = ''
                stopwords = set(STOPWORDS)
                lst = []
                # iterate through the csv file
                for val in posts.title:

                    # typecaste each val to string
                    val = str(val)

                    # split the value
                    tokens = val.split()

                    # Converts each token into lowercase
                    for i in range(len(tokens)):
                        tokens[i] = tokens[i].lower()

                    comment_words += " ".join(tokens) + " "
                wordcloud = WordCloud(width=800, height=800,
                                      background_color='black',
                                      stopwords=stopwords,
                                      min_font_size=10).generate(comment_words)

                # plot the WordCloud image
                plt.figure(figsize=(5, 5), facecolor=None)
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis("off")
                plt.show()
                st.set_option('deprecation.showPyplotGlobalUse', False)
                st.pyplot()
                st.markdown("WordCloud is a compilation of all the polarity words")

    if platform_input == 'Twitter' and not st.checkbox('Hide Graph', False, key=1):
        for k, v in files_dict.items():
            if date_input == k:
                df = pd.read_csv(v)
                df['timestamp'] = pd.to_datetime(df['timestamp'], dayfirst=True)
                data = df.groupby(df['polarity']).size()
                # print(data)
                if visualization == 'Bar':
                    st.markdown('Count of All polarities on ' + date_input)
                    data.plot(kind="bar", color=["red", "blue", "green"])
                    plt.xlabel("Polarity with date")
                    plt.ylabel("count")
                    st.pyplot()
                if visualization == 'Line':
                    st.markdown('Count of All polarities on ' + date_input)
                    data.plot(kind="line")
                    plt.xlabel("Polarity with date")
                    plt.ylabel("count")
                    st.pyplot()
                if visualization == 'WordCloud':
                    st.markdown("word cloud for the data on " + date_input)
                    words(df['title'])










