import nltk
import pandas as pd
from nltk.tokenize import RegexpTokenizer
from collections import Counter
import py3langid as langid

punc_tokenizer = nltk.RegexpTokenizer(r"\w+")

def k_pop_counter(path):

  with open(path) as f:
    rawline = [word.lower() for line in f for word in line.split()]

  a = []
  for word in rawline:   
    a.append(word.replace('(','').replace(')','') ) 

  b = []
  for word in a:
    b.append(word.replace(',','')) 

  a = []
  for word in b:
    a.append(word.replace('’',''))

  b = []
  for word in a:
    b.append(word.replace('"','')) 

  c = [punc_tokenizer.tokenize(line) for line in b]

  a = []
  for word in c:
    for line in word:
      a.append(line)

  set1 = set(a)

  langid.set_languages(['en', 'ko'])

  langs_tok = []
  for word in a:
    langs_tok.append(langid.classify(word)[0])

  langs_tok_edit = []
  for word in langs_tok:
    if word == 'ko':
      langs_tok_edit.append(word.replace('ko', 'ko_tok'))
    if word == 'en':
      langs_tok_edit.append(word.replace('en', 'en_tok'))
  
  langs_type = []
  for word in set1:
     langs_type.append(langid.classify(word)[0])
    
  langs_type_edit = []
  for word in langs_type:
    if word == 'ko':
      langs_type_edit.append(word.replace('ko', 'ko_type'))
    if word == 'en':
      langs_type_edit.append(word.replace('en', 'en_type'))
  
  type_count = Counter(langs_type_edit)
  tok_count = Counter(langs_tok_edit)
    
  dict1 = dict(type_count)
  dict2 = dict(tok_count)
    
  dict1.update(dict2)
    
  song_id_dict = {"song_id":path}
    
  dict1.update(song_id_dict)
      
  tok_stats = dict1

  return(pd.DataFrame.from_dict([tok_stats]))

    
  return(pd.concat([df_main, tok_stats], ignore_index = True))
#   # print(type_count)
#   # print(tok_count)
  
#   # print(f'types {Counter(langs_type)}')
#   # print(f'tokens {Counter(langs_tok)}')
#   # print(Counter(a))

# output = (k_pop_counter(path))

# print(df_main)
# print(output)
# print(type(output))

# Importing the os module
import os

# Give the directory you wish to iterate through
my_dir = "/home/runner/KPopTokenizeNew/Lyrics"

# Using os.listdir to create a list of all of the files in dir
dir_list = os.listdir(my_dir)
# print(dir_list)

# Use the for loop to iterate through the list you just created, and open the files

df_main = pd.DataFrame(columns = ['song_id','ko_tok','en_tok','ko_type', 'en_type'])


for f in dir_list:
  x = (k_pop_counter(f'Lyrics/{f}'))
  x.to_csv(f'DFs/{f}.csv')

df_dir = "/home/runner/KPopTokenizeNew/DFs"
df_dir_list = os.listdir(df_dir)

print(df_dir_list)

df_list = [pd.read_csv(f'DFs/{f}') for f in df_dir_list]

# print(df_list)

df_main = pd.concat(df_list, ignore_index = True)
df_main = df_main[["song_id", "ko_tok", "en_tok", "ko_type", "en_type"]]

print(df_main)
df_main.to_csv('tok_type_stats.csv', sep=',')