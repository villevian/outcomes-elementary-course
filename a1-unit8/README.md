# Outcomes A1 — template

Interactive version of **Outcomes A1** for private lessons (same system as Business Partner: answers sync to the Supabase project "Business Partner", teacher sees them in bp-admin).

- `index.html` — Contents (units appear as they are added)
- `lessons/<id>/all/lesson.html` — coursebook lesson, one task per screen, numbering as in the book; `hw.html`, `extra.html` — added later
- Unit 8 Plans: `8-0` opener, `8a` What are your plans?, `8b` For and against, `8c` Hopes and dreams
- Lesson keys in the database: `oa1-<id>-lesson` / `-hw` / `-extra`

## Generators (`tools/`)
- `oa_page.py` — page shell (Outcomes style, sync, vocabulary box, browser voice 🔊)
- `build_unit8.py OUT_ROOT [STUDENT_CODE]` — Unit 8 pages (template: no code = preview, nothing is sent)
- `build_contents.py OUT.html [student.json]` — Contents; student.json = `{"name","code","assigned":{"8a":["lesson"]}}`

Audio: coursebook mp3 in `lessons/<id>/audio/` (compressed to 96 kbps mono).

Valentyna Hordiienko · Middle Learning Architect
