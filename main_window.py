import os
import sys

from PySide6.QtWidgets import (
    QApplication, QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QFileDialog,
    QLabel,
    QTextEdit,
    QComboBox,
)
from PySide6.QtGui import QIcon

from music.scanner import MusicScanner
from music.matcher import match_tracks
from exportify.exportify_handler import load_csv
from playlist.m3u_writer import write_m3u
from l10n.localization_service import t, set_language, languages

#Local access
def resource_path(name):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, name)

#Import local items
ICON_PATH = resource_path("e2m_icon.ico")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.music_dir = ""
        self.csv_path = ""
        self.results = []

        self.setWindowIcon(QIcon(ICON_PATH))
        self.create_ui()
        self.connect_signals()
        self.translate_ui()

    def create_ui(self):
        self.central = QWidget()
        self.layout = QVBoxLayout(self.central)

        # Language
        self.lbl_language = QLabel()
        self.cmb_language = QComboBox()

        for code, name in languages().items():
            self.cmb_language.addItem(name, code)

        # Music folder
        self.lbl_music = QLabel()
        self.txt_music = QLineEdit()
        self.btn_music = QPushButton()

        # CSV
        self.lbl_csv = QLabel()
        self.txt_csv = QLineEdit()
        self.btn_csv = QPushButton()

        # Generate
        self.btn_generate = QPushButton()

        # Log
        self.log = QTextEdit()
        self.log.setReadOnly(True)

        widgets = [
            self.lbl_language,
            self.cmb_language,
            self.lbl_music,
            self.txt_music,
            self.btn_music,
            self.lbl_csv,
            self.txt_csv,
            self.btn_csv,
            self.btn_generate,
            self.log,
        ]

        for widget in widgets:
            self.layout.addWidget(widget)

        self.setCentralWidget(self.central)

    def connect_signals(self):
        self.btn_music.clicked.connect(self.pick_music)
        self.btn_csv.clicked.connect(self.pick_csv)
        self.btn_generate.clicked.connect(self.generate)
        self.cmb_language.currentIndexChanged.connect(
            self.change_language
        )

    def translate_ui(self):
        self.setWindowTitle(t("title"))

        self.lbl_language.setText(t("language"))

        self.lbl_music.setText(t("music_folder"))
        self.txt_music.setPlaceholderText(t("music_folder"))
        self.btn_music.setText(t("select_music"))

        self.lbl_csv.setText(t("exportify_csv"))
        self.txt_csv.setPlaceholderText(t("exportify_csv"))
        self.btn_csv.setText(t("select_csv"))

        self.btn_generate.setText(t("generate"))

    def change_language(self):
        code = self.cmb_language.currentData()

        if code:
            set_language(code)
            self.translate_ui()

    def pick_music(self):
        path = QFileDialog.getExistingDirectory(
            self,
            t("select_music"),
        )

        if path:
            self.txt_music.setText(path)

    def pick_csv(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            t("select_csv"),
            "",
            "CSV (*.csv)",
        )

        if path:
            self.txt_csv.setText(path)

    def generate(self):
        tracks = load_csv(self.txt_csv.text())

        music = MusicScanner(
            self.txt_music.text()
        ).scan()

        matches, missing = match_tracks(
            tracks,
            music,
        )

        out = "playlist.m3u"

        write_m3u(out, matches)

        self.log.append(
            t("matched", count=len(matches))
        )

        self.log.append(
            t("missing", count=len(missing))
        )

        self.log.append(
            t("saved", path=out)
        )


def run_app():
    app = QApplication([])
    app.setWindowIcon(QIcon(ICON_PATH))

    window = MainWindow()
    window.show()

    app.exec()