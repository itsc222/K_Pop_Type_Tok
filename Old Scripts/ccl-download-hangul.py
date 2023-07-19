import requests
import re
from bs4 import BeautifulSoup

#code for scraping the raw html file, write a loop to create multiple txt files for a corpus. 

URL = "https://colorcodedlyrics.com/2023/05/01/le-sserafim-unforgiven-feat-nile-rodgers/"
page = requests.get(URL)
test_list = []

#parse html using <span>

soup = BeautifulSoup(page.text, "html.parser")
for span in soup.find_all('span'):
      print(span.text)
      test_list.append (span.text)

#set index for the subset including Hangul lyrics

#print(test_list)

index_start = test_list.index("Hangul")
index_end = test_list.index("Translation")
print(index_start)
print(index_end)

test_list = (test_list[index_start + 1:index_end])

# write list as text file.

test_list = str(test_list)
file = open ('test2.txt','w',encoding="UTF-8")
file.write(test_list)
file.close()

# find metadata

title = soup.find("meta", property="og:title")

title_text = str(title)

title_text = title_text.split(sep = '-')
artist = title_text[0].split(sep = '"')[1]
song_title = title_text[1].split(sep = 'Lyrics')[0]

print(artist)
print(song_title)
print(test_list)







#
#print("PYTHON JOBS\n==============================\n")
#python_jobs = results.find_all(
#    "h2", string=lambda text: "python" in text.lower()
#)
#python_job_elements = [
#    h2_element.parent.parent.parent for h2_element in python_jobs
#]
#
#for job_element in python_job_elements:
#    title_element = job_element.find("h2", class_="title")
#    company_element = job_element.find("h3", class_="company")
#    location_element = job_element.find("p", class_="location")
#    print(title_element.text.strip())
#    print(company_element.text.strip())
#    print(location_element.text.strip())
#    link_url = job_element.find_all("a")[1]["href"]
#    print(f"Apply here: {link_url}\n")
#    print()