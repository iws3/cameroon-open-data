#!/usr/bin/env python3
"""Regenerates the folder tree under data/ and the short guide inside each folder.

Run it after adding a new category to STRUCTURE below:
    python tools/build_structure.py
Existing data files are never touched. Only README.md guides are rewritten.
"""
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"

# Each leaf: (folder-name, what belongs here, recommended record types)
EQ = "exam_question, qa_pair"
TD = "text_document"
SR = "structured_record"
PT = "parallel_text, audio_transcript"

SUBJECTS_OL = {
    "english-language": ("GCE Ordinary Level English Language: past questions, marking guides and worked answers." if "english-language" != "other-subjects" else "English Language. Create a subfolder named after the subject if it has many files.", EQ, {}),
    "literature-in-english": ("GCE Ordinary Level Literature in English: past questions, marking guides and worked answers." if "literature-in-english" != "other-subjects" else "Literature in English. Create a subfolder named after the subject if it has many files.", EQ, {}),
    "french": ("GCE Ordinary Level French: past questions, marking guides and worked answers." if "french" != "other-subjects" else "French. Create a subfolder named after the subject if it has many files.", EQ, {}),
    "mathematics": ("GCE Ordinary Level Mathematics: past questions, marking guides and worked answers." if "mathematics" != "other-subjects" else "Mathematics. Create a subfolder named after the subject if it has many files.", EQ, {}),
    "additional-mathematics": ("GCE Ordinary Level Additional Mathematics: past questions, marking guides and worked answers." if "additional-mathematics" != "other-subjects" else "Additional Mathematics. Create a subfolder named after the subject if it has many files.", EQ, {}),
    "physics": ("GCE Ordinary Level Physics: past questions, marking guides and worked answers." if "physics" != "other-subjects" else "Physics. Create a subfolder named after the subject if it has many files.", EQ, {}),
    "chemistry": ("GCE Ordinary Level Chemistry: past questions, marking guides and worked answers." if "chemistry" != "other-subjects" else "Chemistry. Create a subfolder named after the subject if it has many files.", EQ, {}),
    "biology": ("GCE Ordinary Level Biology: past questions, marking guides and worked answers." if "biology" != "other-subjects" else "Biology. Create a subfolder named after the subject if it has many files.", EQ, {}),
    "human-biology": ("GCE Ordinary Level Human Biology: past questions, marking guides and worked answers." if "human-biology" != "other-subjects" else "Human Biology. Create a subfolder named after the subject if it has many files.", EQ, {}),
    "computer-science": ("GCE Ordinary Level Computer Science: past questions, marking guides and worked answers." if "computer-science" != "other-subjects" else "Computer Science. Create a subfolder named after the subject if it has many files.", EQ, {}),
    "geography": ("GCE Ordinary Level Geography: past questions, marking guides and worked answers." if "geography" != "other-subjects" else "Geography. Create a subfolder named after the subject if it has many files.", EQ, {}),
    "history": ("GCE Ordinary Level History: past questions, marking guides and worked answers." if "history" != "other-subjects" else "History. Create a subfolder named after the subject if it has many files.", EQ, {}),
    "citizenship-education": ("GCE Ordinary Level Citizenship Education: past questions, marking guides and worked answers." if "citizenship-education" != "other-subjects" else "Citizenship Education. Create a subfolder named after the subject if it has many files.", EQ, {}),
    "economics": ("GCE Ordinary Level Economics: past questions, marking guides and worked answers." if "economics" != "other-subjects" else "Economics. Create a subfolder named after the subject if it has many files.", EQ, {}),
    "commerce": ("GCE Ordinary Level Commerce: past questions, marking guides and worked answers." if "commerce" != "other-subjects" else "Commerce. Create a subfolder named after the subject if it has many files.", EQ, {}),
    "accounting": ("GCE Ordinary Level Accounting: past questions, marking guides and worked answers." if "accounting" != "other-subjects" else "Accounting. Create a subfolder named after the subject if it has many files.", EQ, {}),
    "religious-studies": ("GCE Ordinary Level Religious Studies: past questions, marking guides and worked answers." if "religious-studies" != "other-subjects" else "Religious Studies. Create a subfolder named after the subject if it has many files.", EQ, {}),
    "food-and-nutrition": ("GCE Ordinary Level Food and Nutrition: past questions, marking guides and worked answers." if "food-and-nutrition" != "other-subjects" else "Food and Nutrition. Create a subfolder named after the subject if it has many files.", EQ, {}),
    "physical-education-and-sports": ("GCE Ordinary Level Physical Education and Sports: past questions, marking guides and worked answers." if "physical-education-and-sports" != "other-subjects" else "Physical Education and Sports. Create a subfolder named after the subject if it has many files.", EQ, {}),
    "logic": ("GCE Ordinary Level Logic: past questions, marking guides and worked answers." if "logic" != "other-subjects" else "Logic. Create a subfolder named after the subject if it has many files.", EQ, {}),
    "art": ("GCE Ordinary Level Art: past questions, marking guides and worked answers." if "art" != "other-subjects" else "Art. Create a subfolder named after the subject if it has many files.", EQ, {}),
    "music": ("GCE Ordinary Level Music: past questions, marking guides and worked answers." if "music" != "other-subjects" else "Music. Create a subfolder named after the subject if it has many files.", EQ, {}),
    "technical-drawing": ("GCE Ordinary Level Technical Drawing: past questions, marking guides and worked answers." if "technical-drawing" != "other-subjects" else "Technical Drawing. Create a subfolder named after the subject if it has many files.", EQ, {}),
    "other-subjects": ("GCE Ordinary Level Any GCE Ordinary Level subject not listed above: past questions, marking guides and worked answers." if "other-subjects" != "other-subjects" else "Any GCE Ordinary Level subject not listed above. Create a subfolder named after the subject if it has many files.", EQ, {}),
}

STRUCTURE = {
    "_inbox": ("Not sure where your contribution belongs? Put it here. Maintainers will review it and move it to the right folder.", "any", {}),
    "education": ("Everything about learning and examinations in Cameroon.", "", {
        "gce": ("The Anglophone General Certificate of Education system, run by the GCE Board.", "", {
            "ordinary-level": ("GCE Ordinary Level past questions, marking guides and worked answers, by subject and year.", EQ, SUBJECTS_OL),
            "advanced-level": ("GCE Advanced Level past questions, marking guides and worked answers, by subject and year.", EQ, {}),
            "technical-ordinary-level": ("Technical and vocational GCE Ordinary Level papers, including practical and theory components.", EQ, {}),
            "technical-advanced-level": ("Technical and vocational GCE Advanced Level papers, including practical and theory components.", EQ, {}),
            "other-gce-examinations": ("Other examinations run by the GCE Board, such as professional and commercial certificates.", EQ, {}),
        }),
        "francophone-secondary": ("The Francophone secondary examination system. Write questions in their original French.", "", {
            "bepc": ("Brevet d'Etudes du Premier Cycle questions and corrections.", EQ, {}),
            "probatoire": ("Probatoire questions and corrections, by series and subject.", EQ, {}),
            "baccalaureat": ("Baccalauréat questions and corrections, by series and subject.", EQ, {}),
            "cap-bep": ("CAP and BEP technical certificate questions and corrections.", EQ, {}),
            "baccalaureat-technique": ("Technical Baccalauréat and Probatoire technique questions and corrections.", EQ, {}),
        }),
        "primary": ("Primary school certificates and entrance examinations in both systems.", "", {
            "fslc": ("First School Leaving Certificate questions and answers.", EQ, {}),
            "cep": ("Certificat d'Etudes Primaires questions and answers.", EQ, {}),
            "common-entrance": ("Common Entrance examination questions and answers.", EQ, {}),
            "concours-entree-sixieme": ("Entrance competition into form one on the Francophone side.", EQ, {}),
        }),
        "university-concours": ("Competitive entrance examinations for universities, grandes écoles and professional schools.", "", {
            "medicine-and-health": ("Concours for medical, nursing, pharmacy and health science schools.", EQ, {}),
            "engineering-and-technology": ("Concours for polytechnic, engineering and technology schools.", EQ, {}),
            "teacher-training": ("Concours for teacher training colleges and higher teacher training schools.", EQ, {}),
            "public-administration-and-law": ("Concours for administration, magistracy, finance and law schools.", EQ, {}),
            "agriculture-and-veterinary": ("Concours for agriculture, forestry and veterinary schools.", EQ, {}),
            "security-services": ("Recruitment and entrance competitions for the police, gendarmerie and armed forces.", EQ, {}),
            "other-concours": ("Any other competitive entrance or recruitment examination.", EQ, {}),
        }),
        "curricula-and-textbooks": ("Official syllabi, lesson notes and textbook content that may legally be shared.", TD + ", " + "qa_pair", {}),
    }),
    "culture": ("The traditions, arts and customs of Cameroon's peoples.", "", {
        "proverbs-and-sayings": ("Proverbs and sayings in any Cameroonian language, with their meaning.", TD, {}),
        "folktales-and-oral-literature": ("Folktales, legends, riddles and other oral literature.", TD + ", audio_transcript", {}),
        "music-and-dance": ("Descriptions of traditional and modern music and dance, and lyrics you have the right to share.", TD + ", " + SR, {}),
        "festivals-and-ceremonies": ("Festivals, rites of passage, weddings, funerals and other ceremonies.", TD + ", " + SR, {}),
        "food-and-cuisine": ("Dishes, recipes, ingredients and food customs by region and community.", TD + ", " + SR, {}),
        "art-and-craft": ("Sculpture, weaving, pottery, beadwork and other crafts, with their makers' communities.", TD + ", " + SR, {}),
        "chieftaincy-and-traditions": ("Traditional rulership, titles, palaces and customary institutions.", TD + ", " + SR, {}),
        "dress-and-attire": ("Traditional and modern dress and the occasions it belongs to.", TD + ", " + SR, {}),
    }),
    "languages": ("The languages Cameroonians speak, write and mix.", "", {
        "english": ("Cameroon English usage, vocabulary and writing.", TD + ", " + PT, {}),
        "french": ("Cameroon French usage, vocabulary and writing.", TD + ", " + PT, {}),
        "cameroon-pidgin-english": ("Cameroon Pidgin English text, speech and translations.", PT + ", " + TD, {}),
        "camfranglais": ("Camfranglais text, speech and translations.", PT + ", " + TD, {}),
        "national-languages": ("Text, speech and word lists in Cameroon's national languages. Use one subfolder per language, named by its ISO 639-3 code.", PT + ", " + TD, {}),
        "parallel-corpora": ("Aligned translations between any pair of languages spoken in Cameroon.", "parallel_text", {}),
        "speech-recordings": ("Recorded speech with careful transcripts and speaker consent.", "audio_transcript", {}),
        "dictionaries-and-glossaries": ("Word lists, dictionary entries and specialist glossaries.", TD + ", " + SR, {}),
    }),
    "politics-and-governance": ("How Cameroon is governed and how its public life works.", "", {
        "elections": ("Electoral rules, official results and election procedures.", SR + ", " + TD, {}),
        "parliament": ("The National Assembly and Senate, their rules and public proceedings.", SR + ", " + TD, {}),
        "political-parties": ("Registered parties, their founding and their published platforms.", SR + ", " + TD, {}),
        "government-institutions": ("Ministries, agencies, councils and their mandates.", SR, {}),
        "decentralization": ("Regions, councils and the laws and practice of decentralization.", SR + ", " + TD, {}),
        "speeches-and-communiques": ("Public speeches, official communiqués and decrees.", TD, {}),
        "public-administration": ("How citizens deal with the administration: procedures, forms and requirements.", TD + ", qa_pair", {}),
    }),
    "law-and-justice": ("The legal framework and the courts.", "", {
        "constitution-and-statutes": ("The Constitution and published laws, in English and French.", TD, {}),
        "ohada-and-regional-law": ("OHADA and CEMAC legal texts that apply in Cameroon.", TD, {}),
        "court-decisions": ("Published court decisions with personal details removed.", TD + ", " + SR, {}),
        "legal-procedures": ("Plain-language explanations of how legal procedures work.", TD + ", qa_pair", {}),
        "rights-and-citizenship": ("Citizens' rights, duties and civic education.", TD + ", qa_pair", {}),
    }),
    "history": ("Where Cameroon and its peoples come from.", "", {
        "precolonial": ("Kingdoms, migrations and societies before colonial rule.", TD + ", " + SR, {}),
        "colonial-period": ("German, French and British administration and its effects.", TD + ", " + SR, {}),
        "independence-and-reunification": ("The road to independence, the plebiscite and reunification.", TD + ", " + SR, {}),
        "post-independence": ("The republic, its institutions and major events since independence.", TD + ", " + SR, {}),
        "oral-histories": ("Recorded and written memories of elders and eyewitnesses, with consent.", "audio_transcript, text_document", {}),
        "archives-and-documents": ("Historical documents that may be freely shared, with full citations.", TD, {}),
    }),
    "geography-and-environment": ("The land, its divisions and its living things.", "", {
        "administrative-units": ("Regions, divisions, subdivisions and councils.", SR, {}),
        "places-and-place-names": ("Towns, villages, landmarks and the meaning and origin of their names.", SR + ", " + TD, {}),
        "climate-and-weather": ("Climate zones, seasons and weather records.", SR + ", " + TD, {}),
        "biodiversity-and-protected-areas": ("Plants, animals, parks and reserves.", SR + ", " + TD, {}),
        "natural-resources": ("Forests, water, minerals, oil and gas.", SR + ", " + TD, {}),
    }),
    "health": ("Health, care and wellbeing.", "", {
        "public-health": ("Disease patterns, campaigns and national health programmes.", SR + ", " + TD, {}),
        "health-facilities": ("Hospitals, clinics and health districts.", SR, {}),
        "medical-terms-in-local-languages": ("Health vocabulary in Cameroonian languages and Pidgin.", "parallel_text", {}),
        "health-education": ("Plain-language health guidance written for ordinary people.", TD + ", qa_pair", {}),
    }),
    "agriculture": ("Farming, fishing and the food chain.", "", {
        "crops": ("Crops, varieties and growing practices by region.", SR + ", " + TD, {}),
        "livestock-and-fisheries": ("Livestock, fishing and aquaculture practices.", SR + ", " + TD, {}),
        "farming-calendars": ("Planting and harvest seasons by region.", SR, {}),
        "markets-and-prices": ("Market locations and dated price observations.", SR, {}),
        "farmer-advice": ("Practical questions and answers for farmers.", "qa_pair, text_document", {}),
    }),
    "economy-and-business": ("How money and work move through Cameroon.", "", {
        "national-statistics": ("Published economic and demographic statistics, with source and date.", SR, {}),
        "trade-and-industry": ("Exports, imports, key industries and companies.", SR + ", " + TD, {}),
        "banking-and-mobile-money": ("Financial services, mobile money and how they are used.", SR + ", " + TD, {}),
        "taxation-and-customs": ("Tax and customs rules in plain language.", TD + ", qa_pair", {}),
        "jobs-and-labour": ("Occupations, labour rules and recruitment practices.", TD + ", " + SR, {}),
        "entrepreneurship": ("Starting and running a business in Cameroon.", TD + ", qa_pair", {}),
    }),
    "media-and-news": ("How Cameroon talks about itself.", "", {
        "newspapers-and-magazines": ("Articles you have the right to share, with full citation.", TD, {}),
        "radio-and-television": ("Transcripts of broadcasts, with the broadcaster named.", "audio_transcript, text_document", {}),
        "fact-checks": ("Claims circulating in Cameroon and what the evidence shows.", "qa_pair, text_document", {}),
    }),
    "religion-and-community": ("Beliefs, associations and community life.", "", {
        "religions-and-beliefs": ("Christian, Muslim, traditional and other beliefs and practices.", TD + ", " + SR, {}),
        "community-associations": ("Tontines, njangi groups, hometown unions and other associations.", TD + ", " + SR, {}),
        "social-customs": ("Greetings, etiquette, family structures and everyday customs.", TD + ", qa_pair", {}),
    }),
    "sports": ("Games and competition.", "", {
        "football": ("Clubs, competitions, players and history.", SR + ", " + TD, {}),
        "athletics-and-other-sports": ("Athletics, boxing, handball, basketball and other sports.", SR + ", " + TD, {}),
        "traditional-games": ("Traditional games, their rules and their communities.", TD, {}),
    }),
    "technology-and-infrastructure": ("The systems that connect the country.", "", {
        "telecommunications": ("Networks, operators, coverage and regulations.", SR + ", " + TD, {}),
        "energy-and-water": ("Electricity, water supply and related institutions.", SR + ", " + TD, {}),
        "transport-and-roads": ("Roads, railways, ports, airports and public transport.", SR + ", " + TD, {}),
        "digital-services": ("E-government, online services and tech organisations.", SR + ", " + TD, {}),
    }),
    "daily-life": ("The ordinary conversations and situations of living in Cameroon.", "", {
        "conversations-and-dialogues": ("Natural dialogues in any Cameroonian language or mixture of languages.", "audio_transcript, text_document, parallel_text", {}),
        "common-questions": ("Questions Cameroonians commonly ask, with accurate local answers.", "qa_pair", {}),
        "emergency-and-safety": ("Emergency numbers, safety guidance and where to seek help, verified and dated.", TD + ", " + SR, {}),
    }),
}

TEMPLATE = """# {title}

{desc}

**Recommended record types:** {types}

Every file in this folder is a `.jsonl` file with one record per line, checked against the schemas in the `schema` folder. Name your file with the year or a short description, for example `2021-short-description.jsonl`. Read `docs/FORMAT_GUIDE.md` for how each record type is written, and run `python tools/validate.py` before opening a pull request.
"""

PARENT = """# {title}

{desc}

This folder is organised into the subfolders below. Each subfolder has its own guide explaining what belongs in it.

{children}
"""


def walk(base, name, node):
    desc, types, children = node
    folder = base / name
    folder.mkdir(parents=True, exist_ok=True)
    title = name.strip("_").replace("-", " ").title()
    readme = folder / "README.md"
    custom = readme.exists() and "<!-- custom-readme -->" in readme.read_text(encoding="utf-8")
    if custom:
        for c, v in children.items():
            walk(folder, c, v)
        return
    if children:
        lines = "\n".join(f"- `{c}`: {v[0]}" for c, v in children.items())
        (folder / "README.md").write_text(PARENT.format(title=title, desc=desc, children=lines), encoding="utf-8")
        for c, v in children.items():
            walk(folder, c, v)
    else:
        (folder / "README.md").write_text(TEMPLATE.format(title=title, desc=desc, types=types), encoding="utf-8")


def main():
    DATA.mkdir(exist_ok=True)
    top = "\n".join(f"- `{k}`: {v[0]}" for k, v in STRUCTURE.items())
    (DATA / "README.md").write_text(
        "# Data\n\nAll contributed data lives here, arranged by sector. Choose the folder that fits best, or use `_inbox` if you are unsure.\n\n" + top + "\n",
        encoding="utf-8",
    )
    for name, node in STRUCTURE.items():
        walk(DATA, name, node)
    print("Structure written under", DATA)


if __name__ == "__main__":
    main()
