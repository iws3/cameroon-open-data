<!-- custom-readme -->
# GCE Ordinary Level

This is where we begin. For millions of Cameroonians, the Ordinary Level is the first big door: the paper you revised for until midnight, the result your family waited for, the certificate that opened the next class or the first job. Yet the questions that have shaped so many lives sit in photocopies, old exercise books and the memories of teachers. This folder is how we bring them into the open, so that a student in Mamfe has the same chance to practise as a student in Yaoundé, and so that the learning tools of the future are built on our real examinations.

You do not need to know anything about code. If you can read a question and type it, you can contribute.

## What we are collecting

We collect the questions of the GCE Ordinary Level examination, subject by subject and year by year. Each question is stored together with its marks, a plain description of any diagram it depends on, and, when you have it, the answer or marking guide. We also welcome worked solutions written by teachers, and short notes explaining how a topic is examined. Subjects have their own folders: English Language, Literature in English, French, Mathematics, Additional Mathematics, Physics, Chemistry, Biology, Human Biology, Computer Science, Geography, History, Citizenship Education, Economics, Commerce, Accounting, Religious Studies, Food and Nutrition, Physical Education and Sports, Logic, Art, Music and Technical Drawing. A subject that is not listed goes into `other-subjects`.

## Four ways to contribute, from easiest to most technical

**1. Fill in the question form (easiest, about five minutes per question).** Open the Issues tab of the repository, press New issue, and choose "Submit an exam question". It is an ordinary web form with boxes and drop-down lists. Type the question, choose the subject and exam, press Submit. The system turns your answers into the correct file automatically and a reviewer checks it. You never see a line of code.

**2. Share photos of a paper (no typing needed).** If you have a paper but no time to type it, open a new issue and choose "Share photos of a paper". Choose the exam, subject and year, drag your pictures into the box, and submit. Another volunteer will transcribe it. Please take pictures in good light, flat on a table, one page per picture, and make sure every line is readable. A blurry page cannot be transcribed reliably.

**3. Send a spreadsheet (best for teachers with many questions).** Download `templates/exam-questions-template.csv`, open it in Excel, Google Sheets or LibreOffice, and put one question on each row. Then open a new issue, choose "Send a spreadsheet of questions", and attach the file. A maintainer converts it for you.

**4. Add the file yourself (for developers).** Write a `.jsonl` file following `docs/FORMAT_GUIDE.md`, check it with `python tools/validate.py`, and open a pull request.

## What to type in the question form

| Box | What to write |
|---|---|
| Exam | Choose GCE Ordinary Level. |
| Subject | The subject name exactly as printed on the paper, for example Physics. |
| Year of the exam | Four digits. Leave it empty if you do not know. |
| Paper or section | For example Paper 2 or Section I. Leave it empty if the page does not say. |
| Question number | The number as printed, for example 5. |
| The question | The whole question, with all its parts (a), (b), (c) and so on, typed in the same order as on the paper. Keep the marks where they appear, for example (2 marks). |
| Marks | The total marks for the question, if you can add them up. |
| Describe any diagram, graph or table | Explain in words what the picture shows, so a person who cannot see it could still understand the question. |
| Answer or marking guide | Only if you are sure it is correct. Leave it empty otherwise. |
| Language | English or French. |
| Where did this question come from? | Be honest: a past paper you have, something you wrote, a textbook, or another source. |
| Your right to share it | Choose the option that is true. "I am not sure" is a perfectly good answer. |
| Your name for credit | The name you want attached to your contribution. |

## How to type a question properly

Type exactly what is printed, including spelling and punctuation, so that the record matches the original. Keep all the parts of one numbered question together in one submission, as they appear on the paper. Do not copy advertisements, website names, phone numbers or watermarks that sometimes appear at the top or bottom of circulating copies. Write mathematics in simple readable text, for example 2x + 3 = 11, m s^-1, 10^3, or x squared. If you know LaTeX you may use it, but nobody is expected to. If a question depends on a diagram, describe it and, if you can, attach a clear picture of the diagram to the issue. If you are not sure of a word because the page is blurry, write [unclear] instead of guessing.

## An example of a finished entry

The example below shows how the boxes of the form would be filled for one physics question. It is an illustration of the format, not a statement about which examination it came from.

| Box | Entry |
|---|---|
| Subject | Physics |
| Question number | 5 |
| The question | (a) State the law of conservation of linear momentum. (2 marks) (b) A car of mass 2500 kg moving with velocity of 30 m s^-1 collides with a stationary car of mass 1500 kg. After collision, the two cars lock together and move with a common velocity. Calculate: (i) the total momentum of the system just before collision. (2 marks) (ii) the common velocity with which the locked cars move. (2 marks) |
| Marks | 6 |
| Describe any diagram | No diagram. |
| Answer or marking guide | (Left empty because the contributor did not have the official answer.) |

Behind the scenes, the system saves this as one line in a file named after the year, subject and paper, inside the `physics` folder. You never have to create that file yourself.

## Where files end up

Every submission is placed in the folder of its subject, for example `physics`, in a file named with the year, the subject and the paper. Each file holds one question per line. Questions with the same year, subject and paper are gathered into the same file.

## Rights, honestly

Past papers belong to the body that sets them, and we take that seriously. The safest contributions are questions you wrote yourself, practice questions written by teachers, and anything you have permission to share. Official past papers are welcome to be submitted, but they are marked "rights unclear" until the maintainers have clarified with the examination body what may be shared publicly. Nothing marked that way leaves the private community without a decision by the members. Read `docs/RIGHTS_AND_PRIVACY.md` for more.

## How a question becomes trusted

Every submission is read by a reviewer. When another member with knowledge of the subject checks that the question is typed correctly, their name is added to the record as a verifier. The more careful eyes on a question, the more useful it is to students and to the machines that will learn from it.

## Thank you

A single question is a real contribution. If you only have time for one, send one. If you have a whole paper, send the whole paper. Your name will stay with it.
