# WhatsApp Chat Analyzer

This project analyzes WhatsApp chat data and provides insights. You can either view group insights or individual insights by using the suitable option. The input (chat) file is obtained by using the export chat function in WhatsApp.

In the future, this project will be updated to integrate Natural Language Processing (NLP) and perform sentiment analysis to provide deeper insights into the tone and mood of the conversations.

## Project Structure

The project consists of the following files:

- **`app.py`**: Main Streamlit application for hosting the user interface and displaying the insights.
- **`helper.py`**: Contains helper functions for processing and analyzing the chat data.
- **`preprocessor.py`**: Handles data preprocessing and formatting for analysis.
- **`requirements.txt`**: Lists the necessary dependencies to run the project.
- **`stop_hinglish.txt`**: A file containing stopwords related to Hinglish (a blend of Hindi and English).
- **`Fonts/`**: Folder containing custom font files for emojis.

## Features

- **Total Words**: Displays the total number of words in the chat.
- **Total Messages**: Shows the total number of messages exchanged.
- **Media Messages**: Analyzes and displays the number of media messages (images, videos, etc.).
- **Total Links**: Counts the number of links shared in the chat.
- **Monthly Timeline**: Visualizes the chat activity over time by month.
- **Most Busy Day**: Identifies the day with the highest activity.
- **Most Busy Month**: Identifies the month with the highest activity.
- **Word Cloud**: Generates a word cloud of the most common words in the chat.
- **Most Used Emojis**: Displays the most frequently used emojis.
- **Most Common Words**: Identifies the most common words used in the chat.
- **Most Busy Users**: Identifies the users with the most messages sent.
- **Percentage Share in Chat by Users**: Displays the percentage share of each user in the chat activity.

## Installation

To set up the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/manav-panwar/WhatsApp-Chat-Analyzer.git
   ```

2. Navigate to the project directory:
   ```bash
   cd WhatsApp-Chat-Analyzer
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Export your WhatsApp chat and save the file.
2. Open the repository and run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
3. Open the app in your browser.
4. Upload your WhatsApp chat file to get insights.
5. Open streamlit's setting and toggle the wide-mode.

## Deployment

This project has been deployed on Web using Render. You can access the live app here:

[Live App](https://whatsapp-chat-analyzer-8xfo.onrender.com)

## Dependencies

- Streamlit
- pandas
- numpy
- matplotlib
- seaborn
- wordcloud
- emoji
- any other dependencies from `requirements.txt`
