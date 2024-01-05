import pandas as pd

data = {
    "keyname1": [ "elem1", "elem2" ],
    "keyname2": [ "elem3", "elem4" ]
    }
df = pd.DataFrame(data)  # 别忘了转换

df2 = df.copy()
# print(type(df['keyname1'][0:2]))

print(df['keyname1'].str.extract(r'(elem)'))