"""
grounding/lang.py — BCP47 language hierarchy loader → Hierarchy.

24 EU official languages (Council Reg. No 1/1958) + Norwegian Bokmål (EEA).
Regional variants for EU/EEA member states + major non-EU codes.
"""
from __future__ import annotations
from .hierarchy import Hierarchy

# Format: (bcp47_tag, label, parent_tag | None)
_LANG = [
    # Germanic
    ("en","English",None),
    ("en-GB","English (United Kingdom)","en"),
    ("en-IE","English (Ireland)","en"),
    ("en-US","English (United States)","en"),
    ("en-AU","English (Australia)","en"),
    ("en-CA","English (Canada)","en"),
    ("de","German",None),
    ("de-DE","German (Germany)","de"),
    ("de-AT","German (Austria)","de"),
    ("de-CH","German (Switzerland)","de"),
    ("de-LU","German (Luxembourg)","de"),
    ("nl","Dutch",None),
    ("nl-NL","Dutch (Netherlands)","nl"),
    ("nl-BE","Dutch (Belgium)","nl"),
    ("sv","Swedish",None),
    ("sv-SE","Swedish (Sweden)","sv"),
    ("sv-FI","Swedish (Finland)","sv"),
    ("da","Danish",None),
    ("da-DK","Danish (Denmark)","da"),
    ("nb","Norwegian Bokmål",None),
    ("nb-NO","Norwegian Bokmål (Norway)","nb"),
    # Romance
    ("fr","French",None),
    ("fr-FR","French (France)","fr"),
    ("fr-BE","French (Belgium)","fr"),
    ("fr-CH","French (Switzerland)","fr"),
    ("fr-LU","French (Luxembourg)","fr"),
    ("fr-CA","French (Canada)","fr"),
    ("es","Spanish",None),
    ("es-ES","Spanish (Spain)","es"),
    ("es-MX","Spanish (Mexico)","es"),
    ("es-AR","Spanish (Argentina)","es"),
    ("it","Italian",None),
    ("it-IT","Italian (Italy)","it"),
    ("it-CH","Italian (Switzerland)","it"),
    ("pt","Portuguese",None),
    ("pt-PT","Portuguese (Portugal)","pt"),
    ("pt-BR","Portuguese (Brazil)","pt"),
    ("ro","Romanian",None),
    ("ro-RO","Romanian (Romania)","ro"),
    # Slavic
    ("pl","Polish",None),   ("pl-PL","Polish (Poland)","pl"),
    ("cs","Czech",None),    ("cs-CZ","Czech (Czechia)","cs"),
    ("sk","Slovak",None),   ("sk-SK","Slovak (Slovakia)","sk"),
    ("bg","Bulgarian",None),("bg-BG","Bulgarian (Bulgaria)","bg"),
    ("hr","Croatian",None), ("hr-HR","Croatian (Croatia)","hr"),
    ("sl","Slovenian",None),("sl-SI","Slovenian (Slovenia)","sl"),
    # Hellenic
    ("el","Greek",None),
    ("el-GR","Greek (Greece)","el"),
    ("el-CY","Greek (Cyprus)","el"),
    # Finno-Ugric
    ("fi","Finnish",None),  ("fi-FI","Finnish (Finland)","fi"),
    ("et","Estonian",None), ("et-EE","Estonian (Estonia)","et"),
    ("hu","Hungarian",None),("hu-HU","Hungarian (Hungary)","hu"),
    # Baltic
    ("lv","Latvian",None),  ("lv-LV","Latvian (Latvia)","lv"),
    ("lt","Lithuanian",None),("lt-LT","Lithuanian (Lithuania)","lt"),
    # Celtic
    ("ga","Irish",None),    ("ga-IE","Irish (Ireland)","ga"),
    # Semitic
    ("mt","Maltese",None),  ("mt-MT","Maltese (Malta)","mt"),
]


def _tag_to_tptp(tag: str) -> str:
    """en-GB → enGb, de-AT → deAt, en → en"""
    parts = tag.split("-")
    result = parts[0].lower()
    for p in parts[1:]:
        result += p[0].upper() + p[1:].lower()
    return result


def load_lang() -> Hierarchy:
    """Return BCP47 language hierarchy as a Hierarchy instance."""
    h = Hierarchy(
        name    = "BCP47 Language Tags — European Dataspace Languages",
        source  = "[1] https://www.iana.org/assignments/language-subtag-registry/\n"
                  "%            [2] https://www.rfc-editor.org/rfc/rfc5646",
        domain  = "taxonomic",
        profile = "bcp47-eu",
    )

    t2t: dict[str,str] = {tag: _tag_to_tptp(tag) for tag, _, _ in _LANG}

    for tag, label, parent in _LANG:
        t = t2t[tag]
        h.concepts.add(t)
        h.grounding[t] = f"BCP47:{tag} — {label}"
        if parent:
            h.edges.append((t, t2t[parent]))

    return h
