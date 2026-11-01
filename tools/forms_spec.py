"""One description of every simple form. The form files and the converter are both built from it,
so the box names can never drift apart."""
import re
import unicodedata

from build_structure import STRUCTURE, EQ

NOT_SURE = "Not sure (the maintainers will place it)"
ACRONYMS = {"gce": "GCE", "ohada": "OHADA", "cemac": "CEMAC", "cap": "CAP", "bep": "BEP", "cep": "CEP", "fslc": "FSLC", "bepc": "BEPC", "tv": "TV"}


def human(name):
    words = name.strip("_").replace("-", " ").split()
    out = []
    for i, w in enumerate(words):
        out.append(ACRONYMS.get(w, w.capitalize() if i == 0 else w))
    return " ".join(out)


def _leaves(node, prefix=(), path=()):
    for name, (desc, types, children) in node.items():
        if name == "_inbox":
            continue
        if children:
            yield from _leaves(children, prefix + (human(name),), path + (name,))
        else:
            yield " / ".join(prefix + (human(name),)), "/".join(path + (name,)), types


def leaf_options(type_name=None):
    """(label, relative path) for every folder that is not an exam folder.

    Any sector can hold any kind of record: a question and answer about farming, a fact about a law,
    a translation in a health folder. Exam folders are left to the exam form.
    """
    return [(label, path) for label, path, types in _leaves(STRUCTURE) if types != EQ]


def resolve_folder(label, type_name):
    from common import ROOT
    if label and label != NOT_SURE:
        for lab, path in leaf_options(type_name):
            if lab == label:
                return ROOT / "data" / path
    return ROOT / "data" / "_inbox"


# ---- shared choices -------------------------------------------------------
LANG_CHOICES = ["English", "French", "Cameroon Pidgin English", "Camfranglais",
                "Another Cameroonian language (write its name in the next box)",
                "Several languages (write them in the next box)"]
REGION_CHOICES = ["Whole country", "Adamawa", "Centre", "East", "Far North", "Littoral", "North", "North-West", "South", "South-West", "West"]
SOURCE_CHOICES = {
    "Told to me by someone (oral tradition)": "oral_tradition",
    "My own knowledge or experience": "personal_knowledge",
    "A book": "book",
    "A newspaper or magazine": "newspaper_or_magazine",
    "A website": "website",
    "An official document": "official_publication",
    "A recording I made": "field_recording",
    "A radio or television broadcast": "broadcast",
    "Another source": "other",
}
RIGHTS_CHOICES = {
    "I created it myself, or I am sharing my own knowledge": "contributor_owned",
    "It is an official public document": "official_public_document",
    "It is in the public domain or under an open license": "open_license",
    "I have written permission from the owner": "permission_granted",
    "I am not sure": "unclear_needs_review",
}
SENSITIVITY_CHOICES = {
    "No, it is fine to share": "none",
    "I removed personal details from it": "personal_information_removed",
    "It is cultural knowledge the community should review": "needs_community_review",
    "It is culturally sensitive": "culturally_sensitive",
}
TEXT_KINDS = {
    "Proverb or saying": "proverb", "Folktale or legend": "folktale", "Song lyrics": "song_lyrics", "Poem": "poem",
    "Speech or statement": "speech", "Law or official text": "law_text", "News article": "news_article",
    "Article or essay": "article", "Description of a place, custom, dish or practice": "description", "Recipe": "recipe",
    "Dictionary entry": "dictionary_entry", "Oral history or testimony": "oral_history", "Other": "other",
}
FACT_KINDS = {
    "Place": "place", "Institution or office": "institution", "Law or rule": "law", "Crop or animal": "crop_or_animal",
    "Event": "event", "Organisation or association": "organisation", "Public figure": "public_figure",
    "Festival or ceremony": "festival_or_ceremony", "Dish or food": "dish", "Statistic": "statistic", "Other": "other",
}

LANG_CODES = {
    "english": "en", "french": "fr", "pidgin": "pcm", "cameroon pidgin": "pcm", "cameroon pidgin english": "pcm",
    "camfranglais": "fr-x-camfrang", "ewondo": "ewo", "duala": "dua", "douala": "dua", "basaa": "bas", "bassa": "bas",
    "bamum": "bax", "bulu": "bum", "ghomala": "bbj", "fefe": "fmp", "medumba": "byv", "yemba": "ybb", "kom": "bkm",
    "lamnso": "lns", "nso": "lns", "fulfulde": "fub", "hausa": "hau", "bakweri": "bri",
}


def _norm(text):
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z ]+", "", text.lower()).strip()


def resolve_one(text):
    """Return (code, note). Unknown languages become 'und' with the name kept in the note."""
    text = (text or "").strip()
    if re.fullmatch(r"[a-z]{2,3}", text):
        return text, ""
    code = LANG_CODES.get(_norm(text))
    return (code, "") if code else ("und", text)


def resolve_language(choice, other):
    c = (choice or "").lower()
    if c.startswith("english"):
        return ["en"], ""
    if c.startswith("french"):
        return ["fr"], ""
    if c.startswith("cameroon pidgin"):
        return ["pcm"], ""
    if c.startswith("camfranglais"):
        return ["fr-x-camfrang"], ""
    names = [n.strip() for n in re.split(r",|;| and ", other or "") if n.strip()] or [""]
    codes, notes = [], []
    for n in names:
        code, note = resolve_one(n)
        if code not in codes:
            codes.append(code)
        if note:
            notes.append(note)
    return codes, "; ".join(notes)


# ---- field builders --------------------------------------------------------
def inp(id, label, desc="", req=False):
    return {"kind": "input", "id": id, "label": label, "desc": desc, "req": req}


def area(id, label, desc="", req=False):
    return {"kind": "textarea", "id": id, "label": label, "desc": desc, "req": req}


def drop(id, label, options, desc="", req=True):
    return {"kind": "dropdown", "id": id, "label": label, "desc": desc, "req": req, "options": options}


def tail():
    return [
        drop("language", "Language", LANG_CHOICES, "The language the main text is written in."),
        inp("language_other", "Which language or languages?", "Only if you chose another or several. Write the name, or its three-letter code if you know it. If you do not know the code, the name is fine."),
        drop("region", "Region of Cameroon", REGION_CHOICES, "Where this comes from or where it is used."),
        drop("source_kind", "How do you know this?", list(SOURCE_CHOICES)),
        area("source_note", "Where does it come from?", "The person, book, place, year or website, so someone else could find it again.", True),
        drop("rights", "Your right to share it", list(RIGHTS_CHOICES), "Choose the option that is true. \"I am not sure\" is a good answer."),
        drop("sensitivity", "Does it need special care?", list(SENSITIVITY_CHOICES), "Some knowledge belongs to a community and should be reviewed by its members first."),
        inp("contributor", "Your name for credit", "If empty, your GitHub username is used."),
        {"kind": "checkboxes", "id": "agreement", "label": "Agreement", "req": True,
         "options": ["I removed phone numbers, home addresses and private information, and I understand the contribution is shared under the project's data license."]},
    ]


def folder_field(type_name):
    opts = [l for l, _ in leaf_options(type_name)] + [NOT_SURE]
    return drop("folder", "Folder", opts, "Choose where it belongs. If you are unsure, choose the last option.")


FORMS = {
    "text": {
        "file": "submit-text.yml", "type": "text_document", "marker": "The text", "label": "submit-text",
        "name": "Submit a text (proverb, story, speech, law, recipe, article ...)",
        "desc": "Share a written text from any part of Cameroonian life.",
        "title": "Text: ",
        "intro": "Share a proverb, a story, a speech, a law, a recipe, a description of a custom or any passage of text. Type it exactly as it is said or written. If it is in another language than English or French, add a translation if you can.",
        "fields": [
            folder_field("text_document"),
            drop("kind", "Kind of text", list(TEXT_KINDS)),
            inp("title", "Title", "Optional."),
            area("text", "The text", "Exactly as it is said or written.", True),
            area("meaning", "Meaning or context", "What it means, who says it, and when."),
            area("translation_en", "English translation", "If the text is in another language."),
            area("translation_fr", "French translation", "If the text is in another language."),
        ] + tail(),
    },
    "qa": {
        "file": "submit-question-answer.yml", "type": "qa_pair", "marker": "Question asked", "label": "submit-qa",
        "name": "Submit a question and its answer",
        "desc": "Local knowledge as a question with a reliable answer.",
        "title": "Q&A: ",
        "intro": "Write a question that people in Cameroon really ask, with the answer you know to be correct. Good answers can be checked somewhere.",
        "fields": [
            folder_field("qa_pair"),
            area("question", "Question asked", "", True),
            area("answer", "Answer given", "", True),
            inp("topic", "Topic", "For example voter registration."),
            inp("evidence", "Where can the answer be checked?", "A document, an office, a website."),
        ] + tail(),
    },
    "translation": {
        "file": "submit-translation.yml", "type": "parallel_text", "marker": "Text in the first language", "label": "submit-translation",
        "name": "Submit a translation",
        "desc": "The same sentence in two languages, including Pidgin, Camfranglais and national languages.",
        "title": "Translation: ",
        "intro": "Write the same sentence or phrase in two languages. Spell it the way people really say it, and note the dialect if it matters.",
        "fields": [
            folder_field("parallel_text"),
            inp("first_language", "First language", "For example English, French, Pidgin, Ewondo, or a code such as ewo.", True),
            area("first_text", "Text in the first language", "", True),
            inp("second_language", "Second language", "For example English, French, Pidgin, Ewondo, or a code such as ewo.", True),
            area("second_text", "Text in the second language", "", True),
            inp("domain", "Subject area", "For example greetings, health, farming, law."),
            inp("dialect_note", "Dialect or spelling note", "For example the village or the spelling system you use."),
        ] + tail(),
    },
    "fact": {
        "file": "submit-fact.yml", "type": "structured_record", "marker": "Details", "label": "submit-fact",
        "name": "Submit facts about a place, institution, law, crop or event",
        "desc": "Structured facts about one named thing.",
        "title": "Fact: ",
        "intro": "Use this for facts about one named thing: a town, a ministry, a law, a crop, a festival, a football club, a statistic. Write each detail on its own line in the form label: value.",
        "fields": [
            folder_field("structured_record"),
            drop("entity_type", "Kind of thing", list(FACT_KINDS)),
            inp("name", "Name", "The name of the thing.", True),
            area("details", "Details", "One per line, in the form label: value. For example capital: Yaounde", True),
            inp("as_of", "Date this was true", "Write it as 2025-12-31. Leave empty if it does not change."),
        ] + tail(),
    },
}
