# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import polars as pl
import string
import langid
import glob

def get_lyrics_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        lyrics_div = soup.find("div", class_="entry-content")
        lyrics = lyrics_div.get_text(separator='\n')
        return soup, lyrics
    else:
        raise ConnectionError("Failed to retrieve the webpage.")

def process_lyrics(lyrics):
    index_start = lyrics.index("Hangul")
    index_end = lyrics.index("Translation")
    hangul_lyrics = lyrics[index_start + 1:index_end]

    def remove_punctuation_and_quotes(text):
        translator = str.maketrans('', '', string.punctuation + "‘’“”")
        return text.lower().translate(translator)

    word_list = hangul_lyrics.split()[1:]
    final_list = [remove_punctuation_and_quotes(word) for word in word_list]
    return final_list

def classify_words_language(words):
    langid.set_languages(['en', 'ko'])
    data = []
    for word in words:
        lang, confidence = langid.classify(word)
        data.append({"word": word, "language": lang})
    return data

def save_dataframe_to_csv(main_df, path):
    main_df.write_csv(path, separator=",")

def merge_csv_dataframes(dfs):
    main_df_data_agg = {
        "title": [],
        "artist": [],
        "date": [],
        "word": [],
        "language": []
    }
    main_df_agg = pl.DataFrame(main_df_data_agg, schema={'title': str, 'artist': str, 'date': str, 'word': str, 'language': str})

    for df in dfs:
        df = pl.read_csv(df)
        main_df_agg.extend(df)
    return main_df_agg

# Specify the URL of the webpage to scrape
url = "https://colorcodedlyrics.com/2016/05/01/bts-bangtansonyeondan-fire-bultaoreune/"

try:
    # Scrape the first process
    soup, lyrics = get_lyrics_from_url(url)
    final_list = process_lyrics(lyrics)
    og_title, rounded_date = get_meta_info(soup)
    word_data = classify_words_language(final_list)

    # Initialize main data table
    main_df_data = {
        "title": [og_title] * len(word_data),
        "artist": [""] * len(word_data),  # Provide the artist name if available
        "date": [str(rounded_date)] * len(word_data),
        "word": [entry["word"] for entry in word_data],
        "language": [entry["language"] for entry in word_data]
    }

    main_df = pl.DataFrame(main_df_data, schema={'title': str, 'artist': str, 'date': str, 'word': str, 'language': str})

    # Save the data to CSV
    path = "path/to/your/specified/folder/" + og_title + ".csv"
    save_dataframe_to_csv(main_df, path)

except ValueError:
    try:
        # Scrape the second process
        soup, lyrics = get_lyrics_from_url(url)
               # Find the table element using its HTML tag
        table = soup.find_all('table')

        # print(len(table))

        # print(table[1])

        if len(table) == 1:
            table = table[0]

        if len(table) > 1:
            table = (table[1])

        cells = table.find_all('td')

        hangul_lyrics = cells[1].text.strip()
    except IndexError:
        print("no can do, boss. Maybe try a different song?")
        quit()

# Merge all CSV files in the specified folder
dfs = glob.glob('path/to/your/specified/folder/*.csv')
main_df_agg = merge_csv_dataframes(dfs)

# Save the aggregated data to a new CSV
path = "path/to/your/specified/folder/all_data.csv"
save_dataframe_to_csv(main_df_agg, path)