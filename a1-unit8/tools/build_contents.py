"""Outcomes A1 — Contents page.
Usage: python3 build_contents.py OUT.html [student.json]
student.json (optional): {"name": "...", "code": "...", "assigned": {"8a": ["lesson"], ...}}
Template (no student file) shows every page that exists.
"""
import sys, json

OUT = sys.argv[1]
ST = json.load(open(sys.argv[2], encoding="utf-8")) if len(sys.argv) > 2 else None

# Units are added as the coursebook pages arrive. pages: which of lesson / hw / extra exist in the template.
UNITS = [
    {"n": 8, "title": "Plans", "lessons": [
        {"id": "8-0", "code": "8", "title": "Unit opener", "aims": ["discuss plans", "free time and things to do this week"], "pages": ["lesson"]},
        {"id": "8a", "code": "8A", "title": "What are your plans?", "aims": ["vocabulary: plans for the week", "grammar: going to", "making suggestions: How about …?"], "pages": ["lesson", "extra"]},
        {"id": "8b", "code": "8B", "title": "For and against", "aims": ["vocabulary: discussing plans", "reading: a local website discussion", "agreeing / disagreeing with plans"], "pages": ["lesson", "extra"]},
        {"id": "8c", "code": "8C", "title": "Hopes and dreams", "aims": ["vocabulary: in my life", "grammar: would like to", "speaking task: improve a place you know"], "pages": ["lesson"]},
    ]},
]
LABEL = {"lesson": "Lesson", "hw": "Homework", "extra": "Extra"}

def card(u, l):
    links = ""
    for p in ("lesson", "hw", "extra"):
        on = p in l["pages"] and (ST is None or p in ST.get("assigned", {}).get(l["id"], []))
        href = "lessons/%s/all/%s.html" % (l["id"], p)
        links += '<a href="%s"%s>%s</a>' % (href, "" if on else ' class="off"', LABEL[p])
    aims = "".join("<li>%s</li>" % a for a in l["aims"])
    return '<div class="ls" data-l="%s"><div class="lh"><span class="n">%s</span><span class="t">%s</span></div><ul class="lb">%s</ul><div class="lf"><div class="links">%s</div><div class="st" id="st_%s"></div></div></div>' % (
        l["id"], l["code"], l["title"], aims, links, l["id"])

units = "".join('<div class="unit"><div class="uh"><b>%d</b><span>%s</span></div><div class="grid">%s</div></div>' % (u["n"], u["title"], "".join(card(u, l) for l in u["lessons"])) for u in UNITS)
who = ('Student<b>%s</b>' % ST["name"]) if ST else 'Template<b>all pages</b>'
HTML = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Outcomes A1 — Contents</title>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box}body{margin:0;font-family:"Source Sans 3",system-ui,sans-serif;color:#1d1d1b;background:#fff}
header{max-width:1180px;margin:0 auto;padding:20px 22px 0;display:flex;align-items:flex-end;gap:16px}
header .lv{background:#ffd200;font:700 30px "Barlow Condensed","Arial Narrow",sans-serif;padding:6px 14px;line-height:1}header h1{margin:0;font:700 46px/1 "Barlow Condensed","Arial Narrow",sans-serif}
header .who{margin-left:auto;text-align:right;font-size:14px;color:#6d6e70}header .who b{display:block;color:#1d1d1b;font-size:16px}
.ybar{max-width:1180px;margin:10px auto 0;padding:0 22px}.ybar div{height:6px;background:#ffd200}
.note{max-width:1180px;margin:10px auto 0;padding:0 22px;font-size:14px;color:#6d6e70}
main{max-width:1180px;margin:0 auto;padding:6px 22px 40px}
.unit{margin-top:22px;border:1px solid #d5d6d7}.uh{display:flex;align-items:stretch;background:#1d1d1b;color:#fff}.uh b{background:#ffd200;color:#1d1d1b;font:700 28px "Barlow Condensed","Arial Narrow",sans-serif;padding:2px 16px}
.uh span{align-self:center;padding-left:14px;font:700 24px "Barlow Condensed","Arial Narrow",sans-serif;letter-spacing:.4px;text-transform:uppercase}
.grid{display:grid;grid-template-columns:repeat(4,1fr)}.ls{border-right:1px solid #d5d6d7;display:flex;flex-direction:column;min-height:200px}.ls:last-child{border-right:0}
.lh{background:#fff6c7;padding:8px 12px;min-height:56px;border-bottom:1px solid #d5d6d7}.lh .n{font:700 22px "Barlow Condensed","Arial Narrow",sans-serif;margin-right:8px}.lh .t{font-weight:600;font-size:15px}
.lb{flex:1;margin:0;padding:10px 12px 10px 28px;font-size:13.5px;line-height:1.45;color:#333}
.lf{padding:8px 12px 12px;border-top:1px dashed #d5d6d7}.links{display:flex;gap:6px;flex-wrap:wrap}
.links a{font-size:13px;font-weight:600;text-decoration:none;padding:3px 10px;border-radius:12px;border:1.5px solid #1d1d1b;color:#1d1d1b}.links a:hover{background:#ffd200;border-color:#ffd200}
.links a.off{border-color:#d5d6d7;color:#b5b6b8;pointer-events:none}.st{font-size:12px;color:#6d6e70;margin-top:6px}
footer{max-width:1180px;margin:0 auto;padding:0 22px 30px;font-size:12.5px;color:#77787b}
@media(max-width:860px){.grid{grid-template-columns:1fr 1fr}}@media(max-width:520px){.grid{grid-template-columns:1fr}}
</style></head><body>
<header><div class="lv">A1</div><h1>Outcomes — Contents</h1><div class="who">__WHO__</div></header>
<div class="ybar"><div></div></div>
<div class="note">Each lesson: <b>Lesson</b> (coursebook page, interactive, one task per screen) · <b>Homework</b> · <b>Extra</b>. Grey buttons = not open yet.</div>
<main>__UNITS__</main>
<footer>Valentyna Hordiienko · Middle Learning Architect</footer>
<script>
const ST=__ST__;const SB_URL="https://zuegojpfhgigsvyrnymt.supabase.co",SB_KEY="sb_publishable__Xn8xRhne9Hp2ckaXu6xCQ_MOe52bng";
if(ST&&ST.code){fetch(SB_URL+"/rest/v1/rpc/get_my_progress",{method:"POST",headers:{apikey:SB_KEY,"Content-Type":"application/json"},body:JSON.stringify({p_code:ST.code})})
 .then(r=>r.json()).then(rows=>{(rows||[]).forEach(r=>{const m=/^oa1-(.+)-(lesson|hw|extra)$/.exec(r.lesson||"");if(!m)return;const el=document.getElementById("st_"+m[1]);if(el)el.textContent+=(el.textContent?" · ":"")+m[2]+(r.submitted?" ✓ sent":" — in progress")})}).catch(()=>{})}
</script></body></html>"""
html = HTML.replace("__WHO__", who).replace("__UNITS__", units).replace("__ST__", json.dumps({"name": ST["name"], "code": ST["code"]} if ST else None, ensure_ascii=False))
open(OUT, "w", encoding="utf-8").write(html); print("wrote", OUT)
