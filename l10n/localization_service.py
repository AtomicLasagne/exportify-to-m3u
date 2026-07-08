from pathlib import Path
import json

L10N_DIR = Path(__file__).resolve().parent

# En as default.
_current = "en-US"
_languages = None
_cache = {}


def _load_language(code):
    if code in _cache:
        return _cache[code]

    file_path = L10N_DIR / f"{code}.json"

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            _cache[code] = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        _cache[code] = {}

    return _cache[code]


def set_language(code):
    global _current

    if _languages is None:
        languages()

    if code in _languages:
        _current = code
    else:
        raise ValueError(f"Unknown language code: {code}")


def t(key, **kw):
    text = (
            _load_language(_current).get(key)
            or _load_language("en-US").get(key)
            or key
    )

    return text.format(**kw) if kw else text


def languages():
    global _languages

    # Return cached value if already loaded
    if _languages is not None:
        return _languages

    file_path = L10N_DIR / "languages_manifest.json"  # Fixed typo

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            _languages = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        _languages = {"en-US": "English"}

    return _languages