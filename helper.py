from urlextract import URLExtract
import re
import pandas as pd
from wordcloud import WordCloud , STOPWORDS
from collections import Counter
import emoji
extractor = URLExtract()
def fetch_stats(selected_user, df):

    if selected_user !='Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]

    words = []
    for message in df['message']:
        words.extend(message.split())

    rf = df.copy()
    rf['message'] = rf['message'].str.replace(r'\r\n|\r|\n', '', regex=True)  # Normalize line breaks
    rf['message'] = rf['message'].str.strip()
    num_media_messages = rf[rf['message'].str.contains("\u200edocument omitted|\u200evideo omitted|\u200eimage omitted", na=False)].shape[0]

    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    num_links = len(links)

    return num_messages, len(words), num_media_messages, num_links

def most_busy_users(df):
    x = df['user'].value_counts().head()
    pf = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'count': 'percentage', 'user': 'name'})
    return x, pf

# Clean text by removing unwanted patterns, emojis, and special characters
def clean_text(text):
    # Remove omitted media patterns
    text = re.sub(r"\u200e(?:document omitted|video omitted|image omitted|audio omitted|sticker omitted)", "", text)
    # Remove emojis and non-ASCII characters
    text = re.sub(r"[^\x00-\x7F]+", "", text)
    # Remove punctuation and special characters
    text = re.sub(r"[^\w\s]", "", text)
    # Remove numbers
    text = re.sub(r"\d+", "", text)
    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text

# Preprocess the messages directly on the copy of the DataFrame
def preprocess_dataframe(df):
    # Create a filtered copy
    mf = df.copy()
    # Filter out rows with omitted media patterns
    mf = mf[~mf['message'].str.contains(
        r"\u200e(?:document omitted|video omitted|image omitted|audio omitted|sticker omitted)",
        na=False
    )]
    # Clean the 'message' column
    mf['message'] = mf['message'].apply(clean_text)
    return mf

# WordCloud generation function
def create_wordcloud(selected_user, df):
    # Filter DataFrame by user if required
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Combine all messages into a single string
    combined_text = df['message'].dropna().str.cat(sep=" ").strip()
    if not combined_text:
        raise ValueError("No valid messages found to generate word cloud.")

    # Create the WordCloud object
    wc = WordCloud(
        background_color="white",
        width=500,
        height=500,
        max_words=200,
        stopwords=STOPWORDS,
        collocations=False  # Avoid joining words together
    )
    return wc.generate(combined_text)

def most_common_words(selected_user ,df):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = preprocess_dataframe(temp)
    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def most_common_emojis(selected_user ,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([char for char in message if char in emoji.EMOJI_DATA])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(5))
    return emoji_df


def monthly_timeline(selected_user ,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append((timeline['month'][i] + "-" + str(timeline['year'][i])))
    timeline['time'] = time
    return timeline

def weekly_activity_map(selected_user ,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def monthly_activity_map(selected_user ,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_map(selected_user ,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    activity_heatmap = df.pivot_table(index='day_name', columns='period', values='message',aggfunc='count').fillna(0)
    return activity_heatmap