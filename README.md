# Cameroon Open Data

### A home for everything Cameroon knows, written down by Cameroonians, before someone else writes it for us.

---

## Why this exists

Think about the last time you asked an AI system a question about Cameroon. Maybe you asked about a past GCE paper, a proverb your grandmother used, how a council election works, or what a certain dish is called in your village. Maybe the answer came back thin, or confidently wrong, or written as though Cameroon were a footnote to somewhere else. If that has happened to you, you already understand why this repository exists.

The machines being built today learn from what humanity has written down. Whatever is not written down, in a form a computer can read, is invisible to them. Our languages are spoken in markets and compounds but barely appear online. Our exam questions are photocopied until the print fades. Our oral histories live in the memories of people who are growing older every year. Our laws, our councils, our crops, our songs, our Pidgin and our Camfranglais are all real and alive, and almost none of it is waiting in a place where the next generation of tools can learn from it.

If we stay silent, the future will still be built. It will simply be built without us in it, or with a version of us drawn by people who never walked our roads. This repository is our refusal to let that happen.

## What we are building

Cameroon Open Data is an open, organized, community-run collection of Cameroonian knowledge, stored as plain files that anyone can read, check and improve. It covers education, culture, languages, politics and governance, law, history, geography, health, agriculture, the economy, the media, religion and community life, sport, technology, and the ordinary details of daily life. If it is part of living in Cameroon, it has a place here.

The collection is meant to serve three groups at once. Students and teachers can use it to revise and to build better learning tools. Researchers, journalists and developers can use it to build things that understand Cameroon properly. And the people who will train the AI systems of the next decade can use it to make sure those systems know us accurately and treat us fairly.

## How it is organized

Everything lives inside the `data` folder, and the folders are arranged the way a Cameroonian would naturally think about the country. Education, for example, does not sit in one pile. It is split into the Anglophone GCE system and the Francophone secondary system, because they are different worlds with different exams. Inside the GCE folder you will find Ordinary Level, Advanced Level, Technical Ordinary Level, Technical Advanced Level and a place for other examinations. The Francophone side has the BEPC, the Probatoire, the Baccalauréat, the CAP and BEP, and the technical Baccalauréat. There are folders for primary school examinations such as the FSLC and the CEP, and a whole section for university and professional entrance competitions, grouped by field: medicine and health, engineering, teacher training, public administration and law, agriculture and veterinary science, and the security services.

Every other sector follows the same habit. Culture holds proverbs, folktales, music and dance, ceremonies, food, craft, chieftaincy and traditional dress. Languages holds English, French, Cameroon Pidgin English, Camfranglais, the national languages, parallel translations, speech recordings and dictionaries. Politics and governance holds elections, parliament, parties, institutions, decentralization and public speeches. The same pattern continues through the rest of the folders, and each one contains its own short guide explaining what belongs inside it. If you are not sure where something goes, put it in `data/_inbox` and the maintainers will place it for you. Nobody should ever be turned away by a folder name.

```
cameroon-open-data/
├── README.md
├── CONTRIBUTING.md
├── ACCESS.md
├── CODE_OF_CONDUCT.md
├── schema/               the rules every record follows
│   ├── meta.schema.json
│   ├── record.schema.json
│   └── types/            one schema per kind of record
├── docs/                 easy start guide, format guide, rights and privacy, examples
├── templates/            spreadsheet template for contributors with many questions
├── tools/                checks and converters that run behind the scenes
└── data/
    ├── _inbox/
    ├── education/
    │   ├── gce/
    │   │   ├── ordinary-level/
    │   │   ├── advanced-level/
    │   │   ├── technical-ordinary-level/
    │   │   ├── technical-advanced-level/
    │   │   └── other-gce-examinations/
    │   ├── francophone-secondary/
    │   ├── primary/
    │   ├── university-concours/
    │   └── curricula-and-textbooks/
    ├── culture/
    ├── languages/
    ├── politics-and-governance/
    ├── law-and-justice/
    ├── history/
    ├── geography-and-environment/
    ├── health/
    ├── agriculture/
    ├── economy-and-business/
    ├── media-and-news/
    ├── religion-and-community/
    ├── sports/
    ├── technology-and-infrastructure/
    └── daily-life/
```

## One format that everyone can follow

A collection is only useful if every piece of it can be read the same way. So every contribution is written as a simple text file in a format called JSON Lines, where each line is one complete record. You do not need to be a programmer to produce it. A spreadsheet can be exported to it, and the format guide in the `docs` folder walks through every kind of record step by step with worked illustrations.

There are six kinds of record: exam questions, question and answer pairs, text documents such as proverbs or speeches, parallel texts for translation, audio transcriptions, and structured records for facts like institutions, places and statistics. Every record, whatever its kind, also carries a small block of honest information about itself: who contributed it, what language it is in, where it came from, which region of Cameroon it belongs to, and whether we have the right to share it. That last part matters more than it might seem, and it is the reason a future researcher can trust what they find here.

You never have to write this format yourself. The question form and the spreadsheet template are converted into it automatically, and a friendly check runs on every contribution so that mistakes are caught early and kindly.

## Who this is for, and why it is for Cameroonians

This project is built by Cameroonians, for Cameroon. That is a deliberate choice and not a gate to keep people out. Our knowledge has too often been collected, packaged and sold by outsiders, and we want the decisions about what is gathered, how it is described and who gets to use it to stay in our own hands. Access to the repository is therefore limited to people with a real connection to Cameroon, whether they live here, were born here, or carry the country in their family and their heart. The `ACCESS.md` file explains exactly how membership works. It relies on trust and on members vouching for one another, and it never asks you to upload an identity document.

Inside that community, everyone is welcome. A form four student with a stack of old papers, a retired teacher, a village elder who knows a story no book has recorded, a software developer, a student of linguistics, a journalist: each of you has something the others do not.

## How to contribute

Once you have been given access, you can contribute without writing a single line of code. Open the Issues tab, press New issue, and choose a form. If you have a question to type, the question form has simple boxes for the exam, the subject, the year and the question itself. If you have a paper but no time to type, share photos of it and another volunteer will transcribe it. If you are a teacher with many questions, fill in our spreadsheet template and send it. Developers can also add files directly through a pull request. A reviewer checks every contribution, and once it is accepted your name stays attached to it permanently.

You do not have to give us a thousand records. One carefully recorded proverb, with the language and the region it comes from, is a real contribution. A single corrected record is a real contribution. Translating a sentence into your mother tongue is a real contribution. The `CONTRIBUTING.md` file explains every step in more detail, and you can also contribute without writing any data at all by reviewing other people's work, finding mistakes, or proposing a folder that does not exist yet.

## What we ask of you

We ask you to be careful in three ways. First, respect ownership. Past examination papers and published books belong to the bodies and authors who produced them, so we ask you to say honestly what the rights situation is, and we prefer material that is public, openly licensed, officially published for public use, or that you have the right to give. Second, protect people. Never include private phone numbers, home addresses, national identity numbers, medical details about a named person, or anything that could put a living person at risk. Third, respect culture. Some knowledge belongs to a community and is not meant to be shared with everyone, so mark it as sensitive and let the right people review it before it is shared. The `docs/RIGHTS_AND_PRIVACY.md` file explains all of this in plain language.

## Licensing

The code in this repository is released under the MIT license. The data contributed by the community is shared under the Creative Commons Attribution-ShareAlike 4.0 license, described in `DATA_LICENSE.md`, unless an individual record states a different and compatible permission. This means the data stays open, contributors are credited, and improvements made by others are shared back with everyone.

## A last word

Somewhere in Cameroon right now, a child is practising for an examination with a paper that has been copied so many times the numbers are barely readable. Somewhere else, an elder is telling a story to a room that is getting smaller each year. A developer in Douala, Yaoundé, Bamenda or Buea is trying to build something useful and cannot find a single clean dataset to build it on. All of these are the same problem, and we can solve it together, one record at a time.

We are not waiting for anyone to come and document us. We are doing it ourselves, carefully, generously and in the open. If something in these folders makes you feel that this is your country and your story, then please add to it. Bring what you know. Bring what your family knows. Bring your village, your language and your questions. The future is going to learn from something, and it should learn from us.

Welcome home.
