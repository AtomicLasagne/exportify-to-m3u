from PySide6.QtWidgets import QApplication,QMainWindow,QWidget,QVBoxLayout,QPushButton,QLineEdit,QFileDialog,QLabel,QTextEdit
from exportify.exportify_handler import load_csv
from music.scanner import MusicScanner
from music.matcher import match_tracks
from playlist.m3u_writer import write_m3u

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Exportify -> M3U")
        self.music_dir=''
        self.csv_path=''
        self.results=[]

        w=QWidget()
        l=QVBoxLayout(w)

        self.music=QLineEdit(); self.music.setPlaceholderText('Music folder')
        self.csv=QLineEdit(); self.csv.setPlaceholderText('Spotify CSV export')
        log=QTextEdit(); log.setReadOnly(True); self.log=log

        b1=QPushButton('Select music folder')
        b2=QPushButton('Select playlist CSV')
        b3=QPushButton('Generate M3U')

        b1.clicked.connect(self.pick_music)
        b2.clicked.connect(self.pick_csv)
        b3.clicked.connect(self.generate)

        for x in [QLabel('Music folder'),self.music,b1,QLabel('Playlist CSV'),self.csv,b2,b3,log]: l.addWidget(x)
        self.setCentralWidget(w)

    def pick_music(self):
        p=QFileDialog.getExistingDirectory(self,'Music folder')
        if p: self.music.setText(p)

    def pick_csv(self):
        p,_=QFileDialog.getOpenFileName(self,'Expotify CSV','','CSV (*.csv)')
        if p: self.csv.setText(p)

    def generate(self):
        tracks=load_csv(self.csv.text())
        music=MusicScanner(self.music.text()).scan()
        matches,missing=match_tracks(tracks,music)
        out='playlist.m3u'
        write_m3u(out,matches)
        self.log.append(f'Matched: {len(matches)}')
        self.log.append(f'Missing: {len(missing)}')
        self.log.append(f'Created: {out}')

def run_app():
    app=QApplication([])
    w=MainWindow()
    w.show()
    app.exec()
