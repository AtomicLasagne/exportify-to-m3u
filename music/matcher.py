from rapidfuzz import fuzz

def match_tracks(spotify_tracks,music_tracks,threshold=85):
    matches=[]
    missing=[]
    for s in spotify_tracks:
        best=None
        score=0
        target=f"{s['artist']} {s['title']}".lower()
        for m in music_tracks:
            candidate=f"{m['artist']} {m['title']}".lower()
            sc=fuzz.token_sort_ratio(target,candidate)
            if sc>score:
                score=sc; best=m
        if best and score>=threshold:
            matches.append(best['path'])
        else:
            missing.append(s)
    return matches,missing
