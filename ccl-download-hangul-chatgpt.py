import requests
from bs4 import BeautifulSoup

# Specify the URL of the webpage to scrape
url = "https://colorcodedlyrics.com/2023/05/01/le-sserafim-unforgiven-feat-nile-rodgers/"

# Send a GET request to the webpage
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find the element that contains the lyrics
    lyrics_div = soup.find("div", class_="entry-content")
    
    # Extract the text from the lyrics element
    lyrics = lyrics_div.get_text(separator= ' ')
    
    # Print the lyrics
    #print(lyrics)
else:
    print("Failed to retrieve the webpage.")


#set indexes to extract only set of Hangul lyrics

index_start = lyrics.index("Hangul")
index_end = lyrics.index("Translation")
print(index_start)
print(index_end)

#Use the indexes to extract only the Hangul lyrics
hangul_lyrics = (lyrics[index_start + 1:index_end])

print(hangul_lyrics)