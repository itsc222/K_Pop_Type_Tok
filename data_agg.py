import glob
import polars as pl

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