"""Outcomes A1 · 8A Extra — vocabulary practice (Plans for the week + going to + suggestions).
Usage: python3 build_extra_8a.py OUT_ROOT [STUDENT_CODE]
"""
import os, sys, json, random
sys.path.insert(0, os.path.dirname(__file__))
from oa_page import *

OUT = sys.argv[1] if len(sys.argv) > 1 else ".."
CODE = sys.argv[2] if len(sys.argv) > 2 else ""
K = {}

CARDS = [("a wedding", "весілля"), ("a gas bill", "рахунок за газ"), ("pay a bill", "оплатити рахунок"), ("pack my things", "спакувати речі"),
         ("book a ticket", "забронювати / купити квиток"), ("a doctor's appointment", "запис до лікаря"), ("a business trip", "відрядження"),
         ("give someone a lift", "підвезти когось"), ("go camping", "поїхати в похід з наметом"), ("a show", "вистава, шоу"),
         ("I don't mind.", "Мені все одно. / Я не проти."), ("do some shopping", "зробити покупки"), ("go to the gym", "піти в спортзал"),
         ("meet some friends", "зустрітися з друзями"), ("go out", "піти кудись (розважитися)"), ("How about …?", "Як щодо …? (пропозиція)")]

# 1 flashcards
s1 = (sh("Vocabulary", "Plans for the week") + ins(1, "Flashcards. Click a card to see the meaning. Click 🔊 to listen and repeat.",
                                               "Натисни на картку — побачиш переклад. Послухай і повтори вголос.")
      + '<div class="fc">' + "".join('<div class="fcard" onclick="this.classList.toggle(\'flip\')"><div class="en">%s %s</div><div class="ua2">%s</div></div>' % (en, say(en.replace("…", "the cinema")), ua) for en, ua in CARDS) + "</div>"
      + '<p class="hint">Tip: say the English first, then click to check.</p>')

# 2 meaning
M2 = [("wedding", "весілля"), ("bill", "рахунок"), ("pack", "пакувати"), ("book", "бронювати"), ("appointment", "запис (до лікаря)"), ("trip", "поїздка"),
      ("lift", "підвезти (give a lift)"), ("camping", "похід з наметом"), ("show", "вистава"), ("mind", "бути проти (I don't mind)")]
opts = sorted(u for _, u in M2)
s2 = ins(2, "Match the words with the meanings.", "З’єднай слово з перекладом.")
for i, (w, u) in enumerate(M2, 1):
    k = "x2_%d" % i; K[k] = [u]
    s2 += '<div class="row"><span class="w">%d</span><b style="display:inline-block;width:150px">%s</b>%s %s%s</div>' % (i, w, say(w), sel(k, opts, 250), fb(k))
s2 += ctl("x2")

# 3 collocations
C3 = [("___ my gas bill", "pay"), ("___ my things for the trip", "pack"), ("___ a train ticket", "book"), ("___ you a lift to the station", "give"),
      ("___ camping in the mountains", "go"), ("___ a doctor's appointment", "have"), ("___ some shopping", "do"), ("___ some friends in the café", "meet"),
      ("___ on a business trip", "go"), ("___ to the gym", "go")]
verbs = ["pay", "pack", "book", "give", "go", "have", "do", "meet"]
s3 = ins(3, "Which verb goes with each phrase? Choose.", "Яке дієслово підходить? (Деякі дієслова — двічі.)") + wbox(verbs)
for i, (t, v) in enumerate(C3, 1):
    k = "x3_%d" % i; K[k] = [v]
    s3 += '<div class="row"><span class="w">%d</span>%s %s%s</div>' % (i, sel(k, verbs, 90), t.replace("___ ", ""), fb(k))
s3 += ctl("x3")

# 4 choose the correct word
C4 = [("I can't come on Friday. I have a dentist's ___.", ["appointment", "show", "wedding"], "appointment"),
      ("It's my sister's ___ on Saturday. I need a new dress!", ["trip", "wedding", "bill"], "wedding"),
      ("My flight is at 7. I need to ___ my bag tonight.", ["book", "pack", "pay"], "pack"),
      ("It's raining. I can give you a ___ home.", ["lift", "trip", "show"], "lift"),
      ("We want to go ___ by the lake. We have a big tent.", ["shopping", "camping", "running"], "camping"),
      ("A: Pizza or pasta? B: I don't ___. You choose.", ["mind", "know", "want"], "mind"),
      ("My husband is in Berlin on a business ___.", ["bill", "trip", "show"], "trip"),
      ("I need to ___ a table at the restaurant for eight people.", ["pack", "book", "give"], "book")]
s4 = ins(4, "Choose the correct word.", "Обери правильне слово.")
for i, (t, o, a) in enumerate(C4, 1):
    k = "x4_%d" % i; K[k] = [a]
    s4 += '<div class="row"><span class="w">%d</span>%s%s</div>' % (i, t.replace("___", sel(k, o, 140)), fb(k))
s4 += ctl("x4")

# 5 dictation
D5 = ["I need to pay my gas bill.", "I'm going to book a train ticket.", "Can you give me a lift?", "I have a doctor's appointment.", "We're going to go camping.", "How about seven thirty?"]
s5 = ins(5, "🔊 Listen and write the sentence.", "Послухай і напиши речення. Можна слухати кілька разів.")
for i, t in enumerate(D5, 1):
    k = "x5_%d" % i; K[k] = [t] + ([t.replace("I'm", "I am")] if "I'm" in t else []) + ([t.replace("We're", "We are")] if "We're" in t else []) + ([t.replace("7.30", "")] if False else [])
    if "seven thirty" in t: K[k].append("How about 7.30?"); K[k].append("How about 7:30?")
    s5 += '<div class="row"><span class="w">%d</span>%s %s%s</div>' % (i, say(t, "🔊 Listen"), inp(k, 420), fb(k))
s5 += ctl("x5")

# 6 conversation (messenger)
bank6 = ["plans", "going to", "appointment", "How about", "lift", "mind", "pack", "book"]
CH = [("A", "Hi! What are your {0} for the weekend?", ["plans"]), ("B", "On Saturday morning I have a doctor's {0}. Then I'm {1} do some shopping.", ["appointment", "going to"]),
      ("A", "Do you want to go to the cinema on Sunday?", []), ("B", "Yes, great! I can {0} the tickets online.", ["book"]),
      ("A", "Perfect. What time?", []), ("B", "{0} six?", ["How about"]), ("A", "Six or seven — I don't {0}. Can you give me a {1}? My car is at the garage.", ["mind", "lift"]),
      ("B", "Sure! And on Monday I'm going on a business trip, so on Sunday night I need to {0} my bag.", ["pack"])]
s6 = ins(6, "Complete the chat with the words in the box.", "Доповни переписку словами з рамки.") + wbox(bank6) + '<div class="chat">'
for n, (w, t, ans) in enumerate(CH):
    for j, a in enumerate(ans):
        k = "x6_%d%s" % (n + 1, "ab"[j]); K[k] = [a]
        t = t.replace("{%d}" % j, inp(k, 120) + fb(k))
    s6 += '<div class="msg %s"><b>%s</b> %s</div>' % ("me" if w == "B" else "", "Olia" if w == "A" else "You", t)
s6 += "</div>" + ctl("x6")

# 7 write
TARGET = ["wedding", "bill", "pack", "book", "appointment", "trip", "lift", "camping", "show", "mind", "shopping", "gym", "friends", "how about", "going to"]
s7 = (ins(7, "Write about your plans for this week. Use <i>going to</i> and at least 5 words from this lesson.", "Напиши 5–7 речень про свої плани на тиждень. Використай going to і щонайменше 5 слів з уроку.")
      + wbox(TARGET) + ta("x7", "On Monday I'm going to …", 160) + '<p class="res" id="wc">0 lesson words used</p>'
      + model("m7", "On Monday I'm going to pay my gas bill. On Wednesday I have a doctor's appointment. On Thursday I'm going to book a train ticket because my friend's wedding is on Saturday. On Friday evening I'm going to pack my things. My brother is going to give me a lift to the station.") + SELF)

xjs = r"""
const TW=%s;function wc(){const t=(document.querySelector('[data-k="x7"]').value||"").toLowerCase();const used=TW.filter(w=>t.includes(w));
 $("wc").textContent=used.length+" lesson words used"+(used.length?": "+used.join(", "):"")+(used.length>=5?" — great! ✓":"")}
document.addEventListener("input",e=>{if(e.target.dataset&&e.target.dataset.k==="x7")wc()});window.afterFill=wc;
""" % json.dumps(TARGET)
CSS = """<style>.fc{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:8px 0}.fcard{border:2px solid var(--y);background:#fffdf3;min-height:92px;padding:12px;cursor:pointer;display:flex;flex-direction:column;justify-content:center;text-align:center}
.fcard .en{font-weight:600;font-size:17px}.fcard .ua2{display:none;color:var(--blue);margin-top:4px}.fcard.flip{background:var(--y2)}.fcard.flip .ua2{display:block}
.chat{max-width:640px;display:flex;flex-direction:column;gap:8px;background:#f3f4f5;padding:12px;border-radius:10px}.msg{background:#fff;border-radius:10px;padding:8px 12px;max-width:85%%;line-height:2}.msg.me{align-self:flex-end;background:#fff6c7}.msg b{display:block;font-size:13px;color:var(--grey);line-height:1.2}
@media(max-width:700px){.fc{grid-template-columns:1fr 1fr}}</style>"""
sections = [("1", s1), ("2", s2), ("3", s3), ("4", s4), ("5", s5), ("6", s6), ("7", s7)]
vocab = [("Plans for the week", ["appointment", "book", "camping", "gas bill", "lift", "mind", "pack", "show", "trip", "wedding"]),
         ("Phrases", ["pay a bill", "pack my things", "book a ticket", "give someone a lift", "go camping", "have an appointment", "go on a business trip", "I don't mind"]),
         ("Plans & suggestions", ["I'm going to …", "What are your plans?", "How about …?"])]
html = page("8A", "What are your plans?", "Extra · Vocabulary", ["remember and use the vocabulary of 8A: plans for the week", "use the words with going to and How about …?"],
            "oa1-8a-extra", CODE, sections, K, vocab, xjs)
html = html.replace("</head>", CSS + "</head>", 1)
p = os.path.join(OUT, "lessons/8a/all/extra.html"); os.makedirs(os.path.dirname(p), exist_ok=True)
open(p, "w", encoding="utf-8").write(html); print("wrote", p, len(K), "keys")
