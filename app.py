import streamlit as st
import matplotlib.pyplot as plt
import preprocessor
import helper
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    # actually jo file hai woh ek stream hai byte data ka we have to convert into utf-8 string
    data = bytes_data.decode("utf-8")
    # print this string file into st.text
    # st.text(data)
    # then we import and called preprocessor and then give it utf-8 string file and it will return dataframe
    df = preprocessor.preprocess(data)

    # to display the dataframe
    # st.dataframe(df)

    # fetch unique users
    user_list = df['User'].unique().tolist()

    # remove 'Unknown' from the user_list
    user_list.remove('Unknown')

    # sort the users in ascending order
    user_list.sort()

    # for group level analysis we used 'Overall' at begin index
    user_list.insert(0, 'Overall')

    # to display unique user
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    # "show analysis" button ko agar koi click kare then analysis will start
    if st.sidebar.button("Show Analysis"):
        # pass

        # stats Area  ------------------------>

        # call the function and get the values
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        # if button is click then we should do four analysis
        # beta_columns() is replaced by columns()
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            # I will display number of messages calculated by fetch_stats() function
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            # I will display number of words calculated by fetch_stats() function
            st.title(words)
        with col3:
            st.header("Media Shared")
            # I will display number of media messages calculated by fetch_stats() function
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            # I will display number of links calculated by fetch_stats() function
            st.title(num_links)

        # monthly timeline ----------------------->
        timeline = helper.monthly_timeline(selected_user, df)
        st.title("Monthly Timeline")
        fig, ax = plt.subplots()

        # then I will put 'Message' column in y-axis and 'time' column in the x-axis
        ax.plot(timeline['time'], timeline['Message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline ------------------------->
        daily_timelines = helper.daily_timeline(selected_user, df)
        st.title("Daily Timeline")
        fig, ax = plt.subplots()

        # then I will put 'Message' column in y-axis and 'time' column in the x-axis
        ax.plot(daily_timelines['only_date'], daily_timelines['Message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.weak_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # create activity heatmap ---------------------------------->
        st.title("Weekly Activity Map")
        activity_Heatmap = helper.activity_heatmap(selected_user, df)
        # Create the heatmap
        ax = sns.heatmap(activity_Heatmap)

        # Get the current figure from the axes
        fig = ax.get_figure()

        # Display the plot in Streamlit
        st.pyplot(fig)

        # finding the busiest user in the group(Group Level) ------------------------>
        # busiest users means -- user who type most of the messages
        if selected_user == 'Overall':
            st.title("Most Busy Users")
            # call the function
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # WordCloud ------------------->
        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        # imshow function used to display df_wc image
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # 20 words which is most of the time used in group and individual level --------------------->

        # call the function from helper file
        most_common_df = helper.most_common_words(selected_user, df)

        # then print the most common dataframe
        # st.dataframe(most_common_df)
        # 0th index is number of words and 1st index is occurrences of those words

        # we create a bar graph for this most common words
        fig, ax = plt.subplots()
        # most_common_df[0] plot it in the x-axis and this is the name of most common words
        # most_common_df[1] plot it in the y-axis and this is the numbers of occurrences of most common words
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')

        st.title("Most Common Words")
        # display the bar chart
        st.pyplot(fig)

        # emoji analysis ------------------------->
        emoji_df = helper.emoji_analysis(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        # printing dataframe
        with col1:
            st.dataframe(emoji_df)

        # printing pie chart
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df['Count'].head(), labels=emoji_df['Emoji'].head(), autopct="%0.2f%%")
            st.pyplot(fig)
