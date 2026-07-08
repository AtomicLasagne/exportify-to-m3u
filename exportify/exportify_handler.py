import pandas as pd

def load_csv(path):
    df=pd.read_csv(path)
    cols=df.columns
    title=next((c for c in cols if 'track' in c.lower()), cols[0])
    artist=next((c for c in cols if 'artist' in c.lower()), cols[1])
    return [{'title':r[title],'artist':r[artist]} for _,r in df.iterrows()]
