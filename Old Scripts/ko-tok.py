import polars as pl
import konlpy
from konlpy.tag import Kkma

kkma = Kkma()

print(kkma.morphs(u'공부를 하면할수록 모르는게 많다는 것을 알게 됩니다.'))


df = pl.read_csv('/Users/ischneid/Code Studio/K-Pop-Type-Tok/K_Pop_Type_Tok/all_data.csv')

korean_filter = df.filter(pl.col('language') == 'ko')

print(korean_filter)

language = korean_filter.select(['title', 'artist', 'word'])

for cell in language['word']:
    print(kkma.morphs(cell))
    