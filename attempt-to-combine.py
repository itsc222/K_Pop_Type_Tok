# -*- coding: utf-8 -*-
#Import packages

import requests
from bs4 import BeautifulSoup
import polars as pl
import string
from datetime import datetime
import langid
import glob

#Initialize main data table

main_df_data = {
    "title": [],
    "artist": [],
    "date": [],
    "word": [],
    "language": []
}
main_df = pl.DataFrame(main_df_data, 
                       schema={'title': str, 
                               'artist': str, 
                               'date': str, 
                               'word': str, 
                               'language': str})

# Specify the URL of the webpage to scrape

url = "https://colorcodedlyrics.com/2016/05/01/bts-bangtansonyeondan-fire-bultaoreune/"

# Send a GET request to the webpage
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find the element that contains the lyrics
    lyrics_div = soup.find("div", class_="entry-content")
    
    # Extract the text from the lyrics element
    lyrics = lyrics_div.get_text(separator= '\n')
    
    # Print the lyrics
    #print(lyrics)
else:
    print("Failed to retrieve the webpage.")

try:

    #set indexes to extract only set of Hangul lyrics

    index_start = lyrics.index("Hangul")
    index_end = lyrics.index("Translation")
    # print(index_start)
    # print(index_end)

    #Use the indexes to extract only the Hangul lyrics
    hangul_lyrics = (lyrics[index_start + 1:index_end])

    # print(hangul_lyrics)

    def text_to_list(text):
        # Remove punctuation and convert the text to a list
        words = text.split()
        return words

    # Example usage
    input_text = hangul_lyrics
    word_list = text_to_list(input_text)

    word_list = word_list[1:]
    # print(word_list)

    #strip punctuation and tokenize
    def remove_punctuation_and_quotes(text):
        translator = str.maketrans('', '', string.punctuation + "‘’“”")
        text = text.translate(translator)
        return text.lower()


    final_list = []
    for word in word_list:
        final_list.append(remove_punctuation_and_quotes(word))
                        
    # print(final_list)

    # Find the meta tag with the property "og:title"
    og_title_tag = soup.find('meta', property='og:title')

    # Extract the content of the og:title tag
    og_title = og_title_tag['content']

    # Input string
    text = og_title

    # Split the string by spaces
    words = text.split(' – ')
    words = text.split(' - ')

    words = [word.split('Lyrics') for word in words]

    print(words)


    title = words[1][0]
    artist = words[0][0]

    # Find the meta tag with the property "article:published_time"
    published_time_tag = soup.find('meta', property='article:published_time')

    # Extract the content of the article:published_time tag
    published_time = published_time_tag['content']

    # Print the scraped article:published_time
    # print('Published Time:', published_time)

    # Input datetime string
    datetime_str = published_time

    # Convert datetime string to datetime object
    datetime_obj = datetime.fromisoformat(datetime_str)

    # Round the datetime to the nearest day
    rounded_date = datetime_obj.date()
    date = str(rounded_date)

    print(date)

    # Print the rounded date
    print('Rounded Date:', date)
    print('Title:', title)
    print('Artist:', artist)
    print('Lyrics:', final_list)

    word_list = final_list
    langid.set_languages(['en', 'ko'])

    for word in word_list:
        lang, confidence = langid.classify(word)
        # print(f"Word: {word} - Language: {lang} - Confidence: {confidence}")
        data = {
            "title": title,
            "artist": artist,
            "date": date,
            "word": word,
            "language": lang
        }
        df = pl.DataFrame(data, schema={'title': str, 'artist': str, 'date': str, 'word': str, 'language': str})
        main_df.extend(df)

    print(main_df)

except ValueError:
    try:
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

        # print(hangul_lyrics)

        import string

        def text_to_list(text):
            # Remove punctuation and convert the text to a list
            words = text.split()
            return words

        # Example usage
        input_text = hangul_lyrics
        word_list = text_to_list(input_text)

        word_list = word_list[1:]
        # print(word_list)

        #strip punctuation and tokenize
        def remove_punctuation_and_quotes(text):
            translator = str.maketrans('', '', string.punctuation + "‘’“”")
            text = text.translate(translator)
            return text.lower()

        final_list = [remove_punctuation_and_quotes(word) for word in word_list[1:]]
                            
        print(final_list)

        # Find the meta tag with the property "og:title"
        og_title_tag = soup.find('meta', property='og:title')

        # Extract the content of the og:title tag
        og_title = og_title_tag['content']

        # Input string
        text = og_title

        # Split the string by spaces
        words = text.split(' – ')
        words = text.split(' - ')
        words = [word.split('Lyrics') for word in words]

        # print(words)

        title = words[1][0]
        artist = words[0][0]

        # Find the meta tag with the property "article:published_time"
        published_time_tag = soup.find('meta', property='article:published_time')

        # Extract the content of the article:published_time tag
        published_time = published_time_tag['content']

        # Print the scraped article:published_time
        # print('Published Time:', published_time)

        from datetime import datetime

        # Input datetime string
        datetime_str = published_time

        # Convert datetime string to datetime object
        datetime_obj = datetime.fromisoformat(datetime_str)

        # Round the datetime to the nearest day
        rounded_date = datetime_obj.date()
        date = str(rounded_date)

        # print(date)

        # Print the rounded date
        # print('Rounded Date:', date)
        # print('Title:', title)
        # print('Artist:', artist)
        # print('Lyrics:', final_list)

        import langid

        word_list = final_list

        langid.set_languages(['en', 'ko'])


        for word in word_list:
            lang, confidence = langid.classify(word)
            # print(f"Word: {word} - Language: {lang} - Confidence: {confidence}")
            data = {
                    "title": title,
                    "artist": artist,
                    "date": date,
                    "word": word,
                    "language": lang}
            
            df = pl.DataFrame(data, schema = {'title': str,
                            'artist': str,
                            'date': str,
                            'word': str,
                            'language': str})

            main_df.extend(df)
    except IndexError:
        print("no can do, boss.")
        quit()

path = "/Users/ischneid/Code Studio/K-Pop-Type-Tok/K_Pop_Type_Tok/WordByWordDF/" + artist + "-" + title + ".csv"
main_df.write_csv(path, separator=",")

dfs = glob.glob('WordByWordDF/*.csv')

main_df_data_agg = {
            "title": [],
            "artist": [],
            "date": [],
            "word": [],
            "language": []}

main_df_agg = pl.DataFrame(main_df_data_agg, schema = {'title': str,
                       'artist': str,
                       'date': str,
                       'word': str,
                       'language': str})


for df in dfs:
    path = f'{df}'
    df = pl.read_csv(path)
    main_df_agg.extend(df)

print(main_df_agg)

path = "/Users/ischneid/Code Studio/K-Pop-Type-Tok/K_Pop_Type_Tok/all_data.csv"
main_df_agg.write_csv(path, separator=",")
    