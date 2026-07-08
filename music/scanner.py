from pathlib import Path
from mutagen import File

class MusicScanner:
    def __init__(self,root):
        self.root=Path(root)

    def scan(self):
        songs=[]
        for ext in ('*.mp3','*.flac','*.m4a','*.ogg'):
            for f in self.root.rglob(ext):
                try:
                    a=File(f,easy=True)
                    songs.append({
                        'title':(a.get('title',[''])[0] if a else ''),
                        'artist':(a.get('artist',[''])[0] if a else ''),
                        'path':str(f)
                    })
                except Exception:
                    pass
        return songs
