import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager

st.sidebar.title('WhatsApp Chat Analyzer')
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    else:
        pass
    user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox('Show analysis wrt', user_list)

    if st.sidebar.button('Show Analysis'):
        st.title('Top Statistics')
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header('Total Messages')
            st.title(num_messages)

        with col2:
            st.header('Total Words')
            st.title(words)

        with col3:
            st.header('Media Messages')
            st.title(num_media_messages)

        with col4:
            st.header('Total Links')
            st.title(num_links)

        st.title('Monthly Timeline')
        timeline = helper.monthly_timeline(selected_user, df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        st.title('Activity Map')
        col1,col2 = st.columns(2)
        with col1:
            st.header('Most Busy Day')
            busy_day = helper.weekly_activity_map(selected_user, df)
            fig,ax = plt.subplots()
            plt.xticks(rotation='vertical')
            ax.bar(busy_day.index, busy_day.values, color='green')
            st.pyplot(fig)

        with col2:
            st.header('Most Busy Month')
            busy_month = helper.monthly_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            plt.xticks(rotation='vertical')
            ax.bar(busy_month.index, busy_month.values, color='orange')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        activity_heatmap = helper.activity_map(selected_user,df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(activity_heatmap)
        st.pyplot(fig)


        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x,df_percent = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color = 'purple')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(df_percent)

        st.title("Wordcloud")
        mf = helper.preprocess_dataframe(df)
        df_wc = helper.create_wordcloud(selected_user, mf)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        st.title("Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1], color = 'purple')
        st.pyplot(fig)

        emoji_df = helper.most_common_emojis(selected_user, df)
        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            font_path = "Fonts/bobo.ttf"  
            prop = font_manager.FontProperties(fname=font_path)

            fig, ax = plt.subplots()
            sizes = emoji_df[1] 
            emoji_labels = emoji_df[0] 

            ax.pie(
                sizes,
                labels=emoji_labels,
                autopct="%1.1f%%",
                textprops={'fontproperties': prop}  
            )

            plt.axis('equal')  
            st.pyplot(fig)
