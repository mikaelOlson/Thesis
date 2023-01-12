import pandas as pd
df_state=pd.read_csv("file.csv")
dup = df_state[df_state.duplicated()]
print("\n\nDuplicated Rows: \n {}".format(dup))

df_rm_dup = df_state.drop_duplicates(keep='first')
df_rm_dup.to_csv('file_no_duplicate.csv')