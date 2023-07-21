# -*- coding: utf-8 -*-
#Import packages

import requests
from bs4 import BeautifulSoup
import polars as pl
import string
from datetime import datetime
import langid
import glob
import csv
import os

# Specify the URL of the webpage to scrape

url = ['https://colorcodedlyrics.com/2021/04/19/day6-you-make-me/',
       'https://colorcodedlyrics.com/2020/05/11/day6-zombie/',
       'https://colorcodedlyrics.com/2019/10/22/day6-sweet-chaos/',
       'https://colorcodedlyrics.com/2019/07/15/day6-time-of-our-life-han-peijiga-doel-su-issge/',
       'https://colorcodedlyrics.com/2018/12/10/day6-days-gone-haengboghaessdeon-naldeulieossda/',
       'https://colorcodedlyrics.com/2017/12/05/day6-like-johahabnida/',
       'https://colorcodedlyrics.com/2017/12/05/day6-like-johahabnida/',
       'https://colorcodedlyrics.com/2018/06/26/day6-shoot-me/',
       'https://colorcodedlyrics.com/2018/09/14/day6-beautiful-feeling/',
       'https://colorcodedlyrics.com/2017/11/05/day6-alone-honjaya/',
       'https://colorcodedlyrics.com/2017/09/28/day6-love-someone-geuleohdeolagoyo/',
       'https://colorcodedlyrics.com/2017/09/05/day6-i-loved-you/',
       'https://colorcodedlyrics.com/2017/07/05/day6-hi-hello/',
       'https://colorcodedlyrics.com/2017/08/06/day6-can-joheungeol-mwo-eoddeoghae/',
       'https://colorcodedlyrics.com/2017/06/06/day6-smile-bandeusi-usneunda/',
       'https://colorcodedlyrics.com/2017/05/07/day6-dance-dance/',
       'https://colorcodedlyrics.com/2017/04/05/day6-m-serious-jangnan-aninde/',
       'https://colorcodedlyrics.com/2017/03/05/day6-can-say-eoddeohge-malhae/',
       'https://colorcodedlyrics.com/2017/02/05/day6-beautiful-yebbeosseo/',
       'https://colorcodedlyrics.com/2017/01/05/day6-wait-wae/',
       'https://colorcodedlyrics.com/2016/03/29/day6-letting-go-noha-noha-noha/',
       'https://colorcodedlyrics.com/2015/09/06/day6-congratulations/'
       ]

for url in url:
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
        except (IndexError, KeyError, NameError, AttributeError):
            print("no can do, boss. Maybe try a different song?")
            pass
    try:    
        path = "/Users/ischneid/Code Studio/K-Pop-Type-Tok/K_Pop_Type_Tok/WordByWordDF/" + artist + "-" + title + ".csv"
        main_df.write_csv(path, separator=",")
    except (NameError):
        pass

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

#remove dfs that have no lyrics inside

def is_single_row_csv(df):
    with open(df, "r") as file:
        csv_reader = csv.reader(file)
        row_count = sum(1 for row in csv_reader)
        if row_count == 1:
            os.remove(df)
            print("CSV file deleted successfully.")
        else:
            print("CSV file has more than one row, not deleted.")
    return
    
for df in dfs:
    is_single_row_csv(df)

dfs = glob.glob('WordByWordDF/*.csv')

for df in dfs:
        path = f'{df}'
        df = pl.read_csv(path)
        main_df_agg.extend(df)

print(main_df_agg)

#Write new comprehensive DF

path = "/Users/ischneid/Code Studio/K-Pop-Type-Tok/K_Pop_Type_Tok/all_data.csv"
main_df_agg.write_csv(path, separator=",")
        