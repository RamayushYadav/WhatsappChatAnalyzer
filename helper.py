import matplotlib.pyplot as plt
import pandas as pd
from urlextract import URLExtract
# import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import emoji


extractor = URLExtract()


def fetch_stats(selected_user, df):
    # if selected_user Overall hai then we do group level analysis
    if selected_user == 'Overall':
        # in group level we find the number of messages
        # 1. fetch the number of messages
        num_messages = df.shape[0]
        # 2. fetch the total number of words in messages
        words = []
        for message in df['Message']:
            words.extend(message.split())
        # 3. fetch of media message
        num_media_messages = df[df['Message'] == '<Media omitted>'].shape[0]
        # 4. fetch the total numbers of shared links
        links = []
        for message in df['Message']:
            links.extend(extractor.find_urls(message))

        return num_messages, len(words), num_media_messages, len(links)

    else:
        # else overall nahi hai toh joh bhi user selected hua hai user ne kitne messages type kiye hai
        # 1. fetch the number of message for single user
        new_df = df[df['User'] == selected_user]
        num_message = new_df.shape[0]
        # 2. fetch the number of words for single user
        words = []
        for message in new_df['Message']:
            words.extend(message.split())
        # 3. fetch of media message for single user
        num_media_messages = new_df[new_df['Message'] == '<Media omitted>'].shape[0]
        # 4. fetch the total numbers of shared links for single user
        links = []
        for message in new_df['Message']:
            links.extend(extractor.find_urls(message))

        return num_message, len(words), num_media_messages, len(links)


def most_busy_users(df):
    x = df['User'].value_counts().head()
    # name = x.index
    # count = x.values
    # plt.bar(name.count)
    # plt.xticks(rotation='vertical')
    # plt.show()

    # user chat percentage
    df = round((df['User'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'User': 'name', 'count': 'percent'})

    return x, df


# wordcloud function
def create_wordcloud(selected_user, df):
    # agar overall hai toh dataframe mein no changes
    if selected_user == 'Overall':
        wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
        df_wc = wc.generate(df['Message'].str.cat(sep=" "))
        return df_wc

    # agar overall nhi  koi particular user  then  we change dataframe
    else:
        df = df[df['User'] == selected_user]
        wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
        df_wc = wc.generate(df['Message'].str.cat(sep=" "))
        return df_wc


def most_common_words(selected_user, df):
    # we first check if user is single or its group level analysis
    # if there is single user analysis then we update our dataframe only for that particular user
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    # group notification wale messages ko remove kar new dataframe temp create karenge
    temp = df[df['User'] != 'Unknown']

    # we have to remove media omitted messages
    temp = temp[temp['Message'] != '<Media omitted>']

    # remove stop words from messages
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    words = []

    for message in temp['Message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    # then we last get the dataframe with most common 20 words
    most_common_df = pd.DataFrame(Counter(words).most_common(20))

    return most_common_df


def emoji_analysis(selected_user, df):
    # we first check if user is single or its group level analysis
    # if there is single user analysis then we update our dataframe only for that particular user
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    # Extract emojis from messages
    emojis = []
    for message in df['Message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    # Create a DataFrame with emoji counts
    emoji_counts = Counter(emojis)
    emoji_df = pd.DataFrame(emoji_counts.most_common(), columns=['Emoji', 'Count'])

    return emoji_df


def monthly_timeline(selected_user, df):
    # we first check if user is single or its group level analysis
    # if there is single user analysis then we update our dataframe only for that particular user
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    # first I will group by 'year','month_num','month' three columns, and then I will count the number of
    # messages and using reset_index() function I will convert it into dataframe
    timeline = df.groupby(['year', 'month_num', 'month']).count()['Message'].reset_index()

    # I will merge 'year' and 'month' columns
    time = []
    for i in range(timeline.shape[0]):
        # print(timeline['month'][i] + '-' + str(timeline['year'][i]))
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))

    # I will create new column in timeline dataframe called 'time'
    timeline['time'] = time

    return timeline


def daily_timeline(selected_user, df):
    # we first check if user is single or its group level analysis
    # if there is single user analysis then we update our dataframe only for that particular user
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    # first we create a new column in our dataframe which contains only dates
    df['only_date'] = df['Date_Time'].dt.date

    # then we create a new dataframe which contain date counts column
    daily_timelines = df.groupby('only_date').count()['Message'].reset_index()

    return daily_timelines

def weak_activity_map(selected_user, df):
    # we first check if user is single or its group level analysis
    # if there is single user analysis then we update our dataframe only for that particular user
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    # then I will return the series
    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):

    # then I will return the series
    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    # we first check if user is single or its group level analysis
    # if there is single user analysis then we update our dataframe only for that particular user
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    # create pivot table (fillna(0) means null values 0 se replace ho jayegi)
    activity_Heatmap = df.pivot_table(index='day_name', columns='period', values='Message', aggfunc='count').fillna(0)

    return activity_Heatmap
