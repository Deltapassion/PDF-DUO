"""Traduction pour la loupe de PDF DUO.

Deux moteurs, au choix dans les réglages :
- en ligne : service gratuit MyMemory (aucun compte ; une adresse e-mail facultative augmente le quota
  journalier), ou un serveur LibreTranslate (adresse + clé éventuelle) ;
- hors ligne : modèles libres Argos Translate (CTranslate2 + SentencePiece), téléchargés une seule fois
  par paire de langues puis utilisés sans internet. Les paires absentes passent par l'anglais
  (ex. français → anglais → albanais).
Mode « automatique » : en ligne si internet répond, sinon hors ligne.

Toutes les fonctions de ce module sont bloquantes : la loupe les appelle dans un fil d'exécution séparé.
"""
import os
import re
import json
import shutil
import zipfile
import tempfile
import threading
import urllib.parse
import urllib.request

from PySide6.QtCore import QSettings, QStandardPaths

INDEX_URL = "https://raw.githubusercontent.com/argosopentech/argospm-index/main/index.json"
MYMEMORY_URL = "https://api.mymemory.translated.net/get"
UA = {"User-Agent": "PDF-DUO (logiciel libre, https://deltapassion.github.io/PDF-DUO)"}

# langues proposées (code, nom dans la langue elle-même) ; « pb » = portugais du Brésil chez Argos
LANGS = [
    ("fr", "Français"), ("en", "English"), ("es", "Español"), ("pt", "Português"), ("de", "Deutsch"),
    ("it", "Italiano"), ("el", "Ελληνικά"), ("zh", "中文"), ("ru", "Русский"), ("uk", "Українська"),
    ("ar", "العربية"), ("sq", "Shqip"), ("tr", "Türkçe"), ("ro", "Română"), ("pl", "Polski"),
    ("nl", "Nederlands"), ("bg", "Български"), ("cs", "Čeština"), ("hu", "Magyar"), ("sk", "Slovenčina"),
    ("sl", "Slovenščina"), ("fa", "فارسی"), ("ur", "اردو"), ("hi", "हिन्दी"), ("bn", "বাংলা"),
    ("vi", "Tiếng Việt"), ("th", "ไทย"), ("id", "Bahasa Indonesia"), ("ms", "Bahasa Melayu"),
    ("tl", "Tagalog"), ("sw", "Kiswahili"), ("ja", "日本語"), ("ko", "한국어"), ("he", "עברית"),
    ("az", "Azərbaycanca"), ("ky", "Кыргызча"), ("ca", "Català"), ("eu", "Euskara"), ("gl", "Galego"),
    ("ga", "Gaeilge"), ("sv", "Svenska"), ("da", "Dansk"), ("nb", "Norsk"), ("fi", "Suomi"),
    ("et", "Eesti"), ("lv", "Latviešu"), ("lt", "Lietuvių"), ("eo", "Esperanto"),
]
LANG_NAME = dict(LANGS)


class TranslateError(Exception):
    pass


def settings():
    return QSettings("Jacques Branas", "PDF DUO")


def data_dir():
    base = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation) or os.path.expanduser("~/.pdfduo")
    d = os.path.join(base, "traduction")
    os.makedirs(d, exist_ok=True)
    return d


def _get(url, timeout=8, data=None, headers=None):
    req = urllib.request.Request(url, data=data, headers={**UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def split_chunks(text, limit=450):
    """Découpe en morceaux de moins de `limit` caractères, aux fins de phrases si possible."""
    parts = re.split(r"(?<=[.!?;:。！？])\s+|\n+", text.strip())
    out, cur = [], ""
    for p in parts:
        p = p.strip()
        if not p:
            continue
        while len(p) > limit:                       # phrase très longue : on coupe aux espaces
            cut = p.rfind(" ", 0, limit)
            cut = cut if cut > 0 else limit
            if cur:
                out.append(cur); cur = ""
            out.append(p[:cut]); p = p[cut:].strip()
        if cur and len(cur) + 1 + len(p) > limit:
            out.append(cur); cur = p
        else:
            cur = (cur + " " + p).strip()
    if cur:
        out.append(cur)
    return out


# ------------------------------------------------------------------ en ligne
def online_translate(text, src, dst):
    st = settings()
    lt_url = (st.value("trad/lt_url", "") or "").strip()
    if lt_url:                                       # serveur LibreTranslate choisi par l'utilisateur
        body = {"q": text, "source": src, "target": dst, "format": "text"}
        key = (st.value("trad/lt_key", "") or "").strip()
        if key:
            body["api_key"] = key
        try:
            r = json.loads(_get(lt_url.rstrip("/") + "/translate", data=json.dumps(body).encode(),
                                headers={"Content-Type": "application/json"}))
        except Exception as e:
            raise TranslateError(str(e))
        if "translatedText" not in r:
            raise TranslateError(r.get("error", "LibreTranslate"))
        return r["translatedText"]
    email = (st.value("trad/email", "") or "").strip()
    res = []
    for chunk in split_chunks(text):
        mm = {"zh": "zh-CN", "nb": "no", "pt": "pt-PT"}
        q = {"q": chunk, "langpair": f"{mm.get(src, src)}|{mm.get(dst, dst)}"}
        if email:
            q["de"] = email
        try:
            r = json.loads(_get(MYMEMORY_URL + "?" + urllib.parse.urlencode(q)))
        except Exception as e:
            raise TranslateError(str(e))
        if int(r.get("responseStatus", 200)) != 200:
            raise TranslateError(str(r.get("responseDetails", "MyMemory")))
        res.append(r["responseData"]["translatedText"])
    return " ".join(res)


def online_available(timeout=4):
    try:
        _get(MYMEMORY_URL + "?q=ok&langpair=en|fr", timeout=timeout)
        return True
    except Exception:
        return False


# ------------------------------------------------------------------ hors ligne (modèles Argos)
_cache = {}
_online_down = 0.0
_lock = threading.Lock()


def model_dir(src, dst):
    return os.path.join(data_dir(), f"{src}_{dst}")


def installed_pairs():
    d = data_dir()
    return {tuple(n.split("_", 1)) for n in os.listdir(d) if "_" in n and os.path.isdir(os.path.join(d, n, "model"))}


def argos_code(c):
    return "pb" if c == "pt-BR" else c


def route(src, dst, pairs):
    """Chemin de traduction avec les paires disponibles : direct, ou par l'anglais."""
    if (src, dst) in pairs:
        return [(src, dst)]
    if src != "en" and dst != "en" and (src, "en") in pairs and ("en", dst) in pairs:
        return [(src, "en"), ("en", dst)]
    return None


def needed_pairs(src, dst):
    if src == "en" or dst == "en":
        return [(src, dst)]
    return [(src, "en"), ("en", dst)]


def fetch_index():
    return json.loads(_get(INDEX_URL, timeout=15))


def download_pair(src, dst, progress=None, index=None):
    """Télécharge et installe le modèle src→dst. progress(reçu, total) est appelé régulièrement."""
    index = index or fetch_index()
    pk = next((p for p in index if p["from_code"] == src and p["to_code"] == dst), None)
    if not pk:
        raise TranslateError(f"{src} → {dst}")
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".argosmodel")
    try:
        req = urllib.request.Request(pk["links"][0], headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            total = int(r.headers.get("Content-Length") or 0)
            got = 0
            while True:
                b = r.read(256 * 1024)
                if not b:
                    break
                tmp.write(b); got += len(b)
                if progress and progress(got, total) is False:
                    raise TranslateError("annulé")
        tmp.close()
        dest = model_dir(src, dst)
        work = dest + ".tmp"
        shutil.rmtree(work, ignore_errors=True)
        with zipfile.ZipFile(tmp.name) as z:
            z.extractall(work)
        inner = next((os.path.join(work, n) for n in os.listdir(work) if os.path.isdir(os.path.join(work, n, "model"))), work)
        shutil.rmtree(dest, ignore_errors=True)
        shutil.move(inner, dest)
        shutil.rmtree(work, ignore_errors=True)
    finally:
        try:
            os.unlink(tmp.name)
        except OSError:
            pass


def _load(src, dst):
    key = (src, dst)
    if key not in _cache:
        import ctranslate2
        import sentencepiece
        d = model_dir(src, dst)
        sp = sentencepiece.SentencePieceProcessor(model_file=os.path.join(d, "sentencepiece.model"))
        tr = ctranslate2.Translator(os.path.join(d, "model"), device="cpu", inter_threads=1,
                                    intra_threads=max(1, (os.cpu_count() or 2) // 2))
        meta = {}
        try:
            meta = json.load(open(os.path.join(d, "metadata.json"), encoding="utf-8"))
        except Exception:
            pass
        _cache[key] = (sp, tr, meta.get("target_prefix", ""))
    return _cache[key]


def _translate_pair(text, src, dst):
    sp, tr, prefix = _load(src, dst)
    sents = [s for s in re.split(r"(?<=[.!?;:。！？])\s+|\n+", text.strip()) if s.strip()]
    if not sents:
        return ""
    toks = [sp.encode(s, out_type=str) for s in sents]
    kw = dict(replace_unknowns=True, max_batch_size=32, beam_size=4, num_hypotheses=1, length_penalty=0.2)
    if prefix:
        kw["target_prefix"] = [[prefix]] * len(toks)
    res = tr.translate_batch(toks, **kw)
    out = []
    for r in res:
        t = r.hypotheses[0]
        if prefix and t and t[0] == prefix:
            t = t[1:]
        out.append(sp.decode(t))
    return " ".join(out)


def offline_translate(text, src, dst):
    path = route(src, dst, installed_pairs())
    if not path:
        raise TranslateError("modeles")
    with _lock:
        for a, b in path:
            text = _translate_pair(text, a, b)
    return text


def offline_ready(src, dst):
    try:
        import ctranslate2, sentencepiece  # noqa: F401
    except Exception:
        return False
    return route(src, dst, installed_pairs()) is not None


# ------------------------------------------------------------------ choix du moteur
def translate(text, src, dst):
    """Renvoie (traduction, 'en ligne' | 'hors ligne')."""
    text = (text or "").strip()
    if not text or src == dst:
        return text, ""
    mode = settings().value("trad/mode", "auto")
    if mode == "online":
        return online_translate(text, src, dst), "online"
    if mode == "offline":
        return offline_translate(text, src, dst), "offline"
    import time
    global _online_down
    if time.time() - _online_down > 60:              # automatique : on retente internet au plus une fois par minute
        try:
            return online_translate(text, src, dst), "online"
        except TranslateError:
            _online_down = time.time()
            if not offline_ready(src, dst):
                raise
    if offline_ready(src, dst):
        return offline_translate(text, src, dst), "offline"
    return online_translate(text, src, dst), "online"
