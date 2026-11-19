"""Outcomes A1 · 8B Extra — Lexical lab on 8B vocabulary in EVERYDAY contexts (not town plans, which the lesson already covers), A2+ texts.
Lexical approach (chunks, collocations, noticing → use) organised by Bloom's taxonomy:
REMEMBER (emoji) → UNDERSTAND (meanings) → APPLY (word partners, real-life sentences) → READ & NOTICE (Reddit-style thread: is an air fryer a good use of money?) →
LISTEN (radio phone-in: neighbours' endless renovation, going to work by train, solar panels — audio 8b-radio.mp3) → ANALYSE (for / against) →
EVALUATE (game: spend a €1,000 bonus) → CREATE (your own Reddit post). Situations are modelled on real Reddit / forum discussions; usernames are invented.
Usage: python3 build_extra_8b.py OUT_ROOT [STUDENT_CODE]
"""
import os, sys, json, random
sys.path.insert(0, os.path.dirname(__file__))
from oa_page import *
OUT = sys.argv[1] if len(sys.argv) > 1 else ".."
CODE = sys.argv[2] if len(sys.argv) > 2 else ""
K = {}
random.seed(88)
def shuf(o): o = list(o); random.shuffle(o); return o
def hid(k): return '<input type="hidden" class="g" data-k="%s">' % k
def bloom(level, ua): return '<div class="bl"><b>%s</b> · %s</div>' % (level, ua)

# 1 REMEMBER — emoji → word (everyday life, not town plans)
EMO = [("🏗️", "build"), ("👥", "crowded"), ("💶", "economy"), ("🏛️", "government"), ("🎓", "education"), ("🌍", "environment"),
       ("✅", "complete"), ("⏱️", "save time"), ("👍💶", "a good use of money"), ("🧑‍🍳", "employ")]
OPT1 = sorted(w for _, w in EMO)
EMO_S = shuf(EMO)
s1 = (bloom("1 REMEMBER", "згадати слова") + sh("Vocabulary", "Words from 8B") +
      ins(1, "Look at the emoji. Which word or phrase from 8B is it?", "Подивись на емодзі. Яке це слово з уроку 8B?") +
      "".join('<div class="row"><span class="emo">%s</span> %s%s</div>' % (e, sel("x1_%d" % i, OPT1, 230), fb("x1_%d" % i)) for i, (e, _) in enumerate(EMO_S)) + ctl("x1"))
for i, (_, w) in enumerate(EMO_S): K["x1_%d" % i] = [w]

# 2 UNDERSTAND — meanings
M2 = [("crowded", "with too many people or cars"), ("economy", "the money, jobs and business of a country or town"), ("government", "the people who control a country or a city"),
      ("environment", "nature: air, water, parks, animals"), ("employ", "give somebody a job"), ("complete", "finish something big, e.g. a new road"),
      ("save time", "do something faster, so you have more time"), ("a good use of money", "money spent on a useful thing")]
M2S = shuf(M2); OPT2 = sorted(w for w, _ in M2)
s2 = (bloom("2 UNDERSTAND", "зрозуміти значення") + sh("Vocabulary", "What does it mean?") +
      ins(2, "Read the meaning. Which word or phrase is it?", "Прочитай пояснення англійською. Яке це слово?") +
      "".join('<div class="row"><span class="w">%d</span>%s → %s%s</div>' % (i + 1, d, sel("x2_%d" % i, OPT2, 190), fb("x2_%d" % i)) for i, (_, d) in enumerate(M2S)) + ctl("x2"))
for i, (w, _) in enumerate(M2S): K["x2_%d" % i] = [w]

# 3 APPLY — collocations (click pairs) + gaps
PAIRS = [("build", "a bigger kitchen"), ("save", "time in the morning"), ("employ", "five people from our street"), ("help", "the local economy"),
         ("be bad", "for the environment"), ("take a year", "to complete"), ("spend money", "on education"), ("be", "a good use of money")]
s3 = (bloom("3 APPLY", "використати в словосполученнях") + sh("Lexical lab", "Word partners") +
      ins(3, "Words have partners! Click a verb on the left, then its partner on the right.", "Слова мають «пари». Натисни дієслово зліва, потім його пару справа.") +
      '<div class="pairs"><div class="pl">%s</div><div class="pr">%s</div></div>' % (
          "".join('<button class="pb" data-i="%d" data-s="L">%s</button>' % (i, a) for i, (a, _) in shuf(list(enumerate(PAIRS)))),
          "".join('<button class="pb" data-i="%d" data-s="R">%s</button>' % (i, b) for i, (_, b) in shuf(list(enumerate(PAIRS))))) +
      hid("prs") + '<p class="res" id="r_prs"></p>')
G4 = [("I love my air fryer. It’s going to ___ time on busy evenings.", "save"), ("Our little café is going to ___ two students this summer.", "employ"),
      ("Buy from small shops on your street — you ___ the local economy.", "help"), ("Cheap clothes you wear only once are bad for the ___.", "environment"),
      ("My neighbours started their new kitchen in March, and it’s still not ___!", "complete"), ("The gym is so ___ at 6 p.m. that I go at 6 a.m.", "crowded")]
OPT4 = sorted(a for _, a in G4)
s4 = (bloom("3 APPLY", "використати в реченнях") + sh("Lexical lab", "Complete the sentences") +
      ins(4, "Real-life sentences from people online. Complete them. Try from memory!", "Речення з реального життя людей. Доповни їх з пам’яті!") +
      "".join('<div class="row"><span class="w">%d</span>%s%s</div>' % (i + 1, q.replace("___", sel("x4_%d" % i, OPT4, 130)), fb("x4_%d" % i)) for i, (q, _) in enumerate(G4)) + ctl("x4"))
for i, (_, a) in enumerate(G4): K["x4_%d" % i] = [a]

# 4 READ — Reddit-style thread
THREAD = [("tired_mum_of_two", "Is an air fryer <b>a good use of money</b>? 🤔 It’s €150. My friends say it’s going to <b>save time</b>, but I already have an oven…", "post"),
          ("busy_dad", "Yes! I work late and it <b>saves time</b> every evening — dinner in 15 minutes. Now I use it more than my oven.", ""),
          ("honest_jen", "I bought one last year and used it twice. Save your money 😂", ""),
          ("green_kitchen", "It uses less electricity than a big oven, so it’s better for the <b>environment</b> — and for your bills.", ""),
          ("student_life", "€150? I’d spend it on <b>education</b>. An online course is a better use of money.", ""),
          ("local_first", "If you buy one, buy it from a small shop near you, not online. They <b>employ</b> people from our town and it helps the local <b>economy</b>.", ""),
          ("tired_mum_of_two", "Thanks, everyone! I’m going to buy one from the little shop on our street 😄", "")]
THR = '<div class="rd"><div class="rh">r/NoStupidQuestions · Is it worth it?</div>%s</div>' % "".join(
    '<div class="rc%s"><div class="ru">u/%s</div><p>%s</p><div class="rv">⬆ %d · 💬 Reply</div></div>' % (" op" if k == "post" else "", u, t, v)
    for (u, t, k), v in zip(THREAD, [212, 140, 186, 77, 59, 91, 33]))
FA = [("busy_dad", "buy it"), ("honest_jen", "don’t buy it"), ("green_kitchen", "buy it"), ("student_life", "don’t buy it"), ("local_first", "buy it in a local shop")]
s5 = (bloom("4 READ & NOTICE", "читати й помічати слова") + sh("Reading", "Is it a good use of money?") +
      ins(5, "A mum asks on Reddit: should she buy an air fryer? Read the answers. What does each person say?", "Мама питає на Reddit, чи купувати аерогриль. Що радить кожна людина?") + THR +
      "".join('<div class="row">u/%s → %s%s</div>' % (u, sel("x5_%d" % i, ["buy it", "don’t buy it", "buy it in a local shop"], 210), fb("x5_%d" % i)) for i, (u, _) in enumerate(FA)) + ctl("x5") +
      '<p class="hint">Usernames are invented. The situation is real: people on Reddit really ask if an air fryer is worth the money — and the answers are like these!</p>')
for i, (_, a) in enumerate(FA): K["x5_%d" % i] = [a]
WHO = [("It’s faster than cooking in the oven.", "busy_dad"), ("I didn’t really use mine.", "honest_jen"), ("It’s cheaper to use.", "green_kitchen"),
       ("Learning is more important.", "student_life"), ("Shop near your home.", "local_first")]
UOPT = sorted(set(u for u, _ in FA))
s6 = (bloom("4 READ & NOTICE", "знайти деталі") + sh("Reading", "Who says it?") +
      ins(6, "Who says this? The words are different in the thread — look for the meaning!", "Хто це каже? У тексті інші слова — шукай зміст.") +
      '<details class="dd"><summary>💬 Open the thread</summary>%s</details>' % THR +
      "".join('<div class="row"><span class="w">%d</span>%s → %s%s</div>' % (i + 1, q, sel("x6_%d" % i, UOPT, 190), fb("x6_%d" % i)) for i, (q, _) in enumerate(WHO)) + ctl("x6"))
for i, (_, a) in enumerate(WHO): K["x6_%d" % i] = [a]

# 5 LISTEN — street interviews
L1 = [("neighbours who are building a new kitchen", "yes"), ("going to work by train", "yes"), ("solar panels on a house", "yes"), ("a new job", "no"), ("a holiday", "no")]
s7 = (bloom("5 LISTEN", "слухати") + sh("Listening", "Radio: Good idea, bad idea?") +
      ins(7, "Three people call a radio show about their plans. What do they talk about?", "Троє людей дзвонять на радіо й розповідають про свої плани. Про що вони говорять? Перший раз — без пауз.") +
      audio_slot("8b-radio.mp3", "Good idea, bad idea? (1:25)") +
      "".join('<div class="row">%s → %s%s</div>' % (t, sel("x7_%d" % i, ["yes", "no"], 80), fb("x7_%d" % i)) for i, (t, _) in enumerate(L1)) + ctl("x7"))
for i, (_, a) in enumerate(L1): K["x7_%d" % i] = [a]
L2 = [("They started in March.", "Tom"), ("I can read on the train.", "Anna"), ("Our electricity bills are very high.", "George"),
      ("It’s going to save time.", "Anna"), ("I’m going to talk to them this weekend.", "Tom"), ("They employ ten people from our town.", "George")]
SCRIPT = ('<p><b>Host:</b> Hello and welcome to <i>Good Idea, Bad Idea?</i> — the show where you call us about your plans. Our first caller is Tom. Hi, Tom!</p>'
          '<p><b>Tom:</b> Hi! So, my neighbours are building a new kitchen. They started in March. It’s November now, and it’s still not complete! Every morning at eight o’clock: bang, bang, bang. And now they’re going to build a room on the roof too.</p>'
          '<p><b>Host:</b> Oh no! What are you going to do? — <b>Tom:</b> I’m going to talk to them this weekend. I don’t think it’s a good idea to wait.</p>'
          '<p><b>Host:</b> Good luck, Tom! Our next caller is Anna. Hi, Anna!</p>'
          '<p><b>Anna:</b> Hi! I want to sell my car and go to work by train. It’s good for the environment, and I can read on the train. But my husband doesn’t agree. He says the trains are very crowded in the morning.</p>'
          '<p><b>Host:</b> Hmm. Is the train faster? — <b>Anna:</b> Yes! It’s going to save time — about twenty minutes every day. And I’m not going to pay for parking.</p>'
          '<p><b>Host:</b> I think it’s a good idea, Anna! And our last caller is George.</p>'
          '<p><b>George:</b> Hello. The government is going to pay half of the money for solar panels on houses. My wife wants them. They cost six thousand euros.</p>'
          '<p><b>Host:</b> And is that a good use of money? — <b>George:</b> I think so. Our electricity bills are very high. And a local company is going to do the work. They employ ten people from our town, so it’s good for the local economy too.</p>'
          '<p><b>Host:</b> Brilliant! Thanks, everyone. Call us again next week!</p>')
s8 = (bloom("5 LISTEN", "слухати деталі") + sh("Listening", "Who says it?") +
      ins(8, "Listen again. Who says it: Tom, Anna or George? You can pause.", "Послухай ще раз. Хто це каже? Можна ставити на паузу.") +
      audio_slot("8b-radio.mp3", "Good idea, bad idea?") +
      "".join('<div class="row"><span class="w">%d</span>“%s” → %s%s</div>' % (i + 1, q, sel("x8_%d" % i, ["Tom", "Anna", "George"], 110), fb("x8_%d" % i)) for i, (q, _) in enumerate(L2)) + ctl("x8") +
      model("sc8", SCRIPT, "Show the script") +
      '<p class="hint">Shadowing: open the script, choose 3 sentences and say them with the speaker. Same speed, same feeling!</p>')
for i, (_, a) in enumerate(L2): K["x8_%d" % i] = [a]

# 6 ANALYSE — for / against sort
ARG = [("It’s going to help the economy.", "for"), ("It’s going to employ local people.", "for"), ("It’s going to save time.", "for"),
       ("It’s not a good use of money.", "against"), ("The roads are going to be crowded.", "against"), ("It’s going to be bad for the environment.", "against"),
       ("It’s going to take a long time to complete.", "against"), ("It’s good for education.", "for")]
SW = [a for a, _ in ARG]; SG = {a: g for a, g in ARG}
s9 = (bloom("6 ANALYSE", "розкласти аргументи") + sh("Lexical lab", "For or against?") +
      ins(9, "Your friend has a plan. Is each sentence a reason FOR the plan or AGAINST it? Click a sentence, then a box.", "У подруги є план. Це аргумент «за» чи «проти»? Натисни речення, потім коробку.") +
      '<div class="pool" id="pool">%s</div><div class="bins"><div class="bin" data-g="for"><b>👍 For</b><div class="in"></div></div><div class="bin" data-g="against"><b>👎 Against</b><div class="in"></div></div></div>' % "".join(
          '<span class="chip" data-w="%s">%s</span>' % (esc(w), w) for w in shuf(SW)) +
      "".join(hid("srt_%d" % i) for i in range(len(SW))) + '<div class="ctl"><button class="btn" onclick="sortChk()">Check</button><span class="res" id="r_srt"></span></div>')

# 7 EVALUATE — €1,000 bonus game
PROJ = [("fryer", "🍟 an air fryer", 150), ("course", "🎓 an online English course", 300), ("bike", "🚲 a bike for work", 400), ("trip", "✈️ a weekend in Rome", 500),
        ("gym", "🏋️ a gym for one year", 350), ("phone", "📱 a new phone", 900), ("shelter", "🐶 give to a dog shelter", 100), ("panel", "☀️ a solar panel for your balcony (the government pays half)", 300)]
s10 = (bloom("7 EVALUATE", "оцінити й вибрати") + sh("Game", "Your €1,000 bonus 💶") +
       ins(10, "Good news: you have a <b>€1,000 bonus</b> at work! How are you going to spend it? Choose, then press <b>Me in one year</b>.", "Тобі дали премію €1 000! На що витратиш? Обери й натисни «Me in one year».") +
       '<div class="proj">%s</div><div class="ctl"><span class="tm" id="left">€1,000 left</span><button class="btn" onclick="town()">🔮 Me in one year</button></div><div id="tout"></div>' % "".join(
           '<label class="pj"><input type="checkbox" data-p="%s" data-c="%d" onchange="budg()"> %s <b>€%d</b></label>' % (k, c, t, c) for k, t, c in PROJ) +
       hid("mayor") + '<p class="ins" style="margin-top:14px">Explain your choice: <i>I think … is a good use of money because it’s going to … I didn’t choose … because …</i></p>' +
       ta("x10", "I think … is a good use of money because …", 90))

# 8 CREATE — your Reddit comment
TW = ["build", "crowded", "economy", "government", "education", "environment", "complete", "save time", "a good use of money", "employ", "safety", "i agree", "i think it's a good idea", "i don't think", "it's going to"]
s11 = (bloom("8 CREATE", "створити свій текст") + sh("Writing", "Your post on Reddit") +
       ins(11, "Write your own Reddit post (40–60 words): <i>Is … a good use of money?</i> Tell people about a plan (a new phone, a course, a trip, a car…) and what you think. Use at least 5 words from this page.", "Напиши свій пост на Reddit (40–60 слів): «Чи варто купувати / робити …?» Розкажи про свій план і що ти думаєш. Використай щонайменше 5 слів зі сторінки.") +
       wbox(["a good use of money", "save time", "help the local economy", "employ", "crowded", "environment", "education", "complete", "I agree", "I don't think it's a good idea"]) +
       ta("x11", "Is a … a good use of money? I want to … I think it’s going to …", 140) + '<p class="res" id="wc"></p>' + SELF)

DATA = {"SW": SW, "SG": SG, "PN": len(PAIRS), "TW": TW}
XJS = r"""
const D=__D__;const $q=(s,r=document)=>r.querySelector(s),$a=(s,r=document)=>[...r.querySelectorAll(s)];
function hv(k){const e=$q(`.g[data-k="${k}"]`);return e?e.value:""}
function setH(k,v){const e=$q(`.g[data-k="${k}"]`);if(e){e.value=v;e.dispatchEvent(new Event("input",{bubbles:true}))}}
/* pairs */
let psel=null,pdone=new Set();function prMark(i){pdone.add(+i);$a(`.pb[data-i="${i}"]`).forEach(b=>{b.classList.remove("sel");b.classList.add("done")})}
function prSave(){setH("prs",[...pdone].join(","));$q("#r_prs").textContent=pdone.size+" / "+D.PN+(pdone.size===D.PN?" ✓ Well done!":"")}
document.addEventListener("click",e=>{const b=e.target.closest(".pb");if(!b||b.classList.contains("done"))return;if(b.dataset.s==="L"){$a(".pb.sel").forEach(x=>x.classList.remove("sel"));b.classList.add("sel");psel=b;return}
 if(!psel){$q("#r_prs").textContent="First click a word on the left.";return}if(psel.dataset.i===b.dataset.i){prMark(b.dataset.i);psel=null;prSave()}else{b.classList.add("bad");setTimeout(()=>b.classList.remove("bad"),600)}});
/* sort */
let csel=null;function chipTo(c,g){c.classList.remove("sel","ok","no");if(g){$q(`.bin[data-g="${g}"] .in`).appendChild(c)}else $q("#pool").appendChild(c)}
document.addEventListener("click",e=>{const c=e.target.closest(".chip");if(c){e.stopPropagation();const w=c.dataset.w;
 if(c.closest(".bin")&&csel&&csel!==c){const g=c.closest(".bin").dataset.g;chipTo(csel,g);setH("srt_"+D.SW.indexOf(csel.dataset.w),g);csel=null;return}
 if(c.closest(".bin")){chipTo(c,null);setH("srt_"+D.SW.indexOf(w),"");return}$a(".chip.sel").forEach(x=>x!==c&&x.classList.remove("sel"));c.classList.toggle("sel");csel=c.classList.contains("sel")?c:null;return}
 const b=e.target.closest(".bin");if(b&&csel){const w=csel.dataset.w;chipTo(csel,b.dataset.g);setH("srt_"+D.SW.indexOf(w),b.dataset.g);csel=null}},true);
function sortChk(){let n=0,left=$a("#pool .chip").length;$a(".bin .chip").forEach(c=>{const ok=D.SG[c.dataset.w]===c.closest(".bin").dataset.g;c.classList.add(ok?"ok":"no");if(ok)n++});
 $q("#r_srt").textContent=n+" / "+D.SW.length+(left?" · "+left+" not sorted yet":n===D.SW.length?" ✓ Well done!":" · red = wrong box")}
/* mayor */
function chosen(){return $a(".pj input:checked").map(i=>i.dataset.p)}
function budg(){const t=$a(".pj input:checked").reduce((a,i)=>a+ +i.dataset.c,0);const l=1000-t;$q("#left").textContent=(l<0?"⚠ over by €"+(-l):"€"+l+" left");$q("#left").className="tm"+(l<0?" bad":"");setH("mayor",chosen().join(","))}
function town(){const c=chosen(),has=x=>c.includes(x),t=$a(".pj input:checked").reduce((a,i)=>a+ +i.dataset.c,0);if(t>1000){$q("#tout").innerHTML="<p>⚠ Too expensive! Remove something.</p>";return}
 const R={fryer:"🍟 Dinner in 15 minutes! The air fryer saves time every evening.",course:"🎓 You finished the course. Your English is much better — a great use of money!",
 bike:"🚲 You go to work by bike. It saves time in traffic and it’s good for the environment.",trip:"✈️ Rome was beautiful! You still talk about the pizza 🍕",
 gym:"🏋️ You went to the gym… 6 times. It was always crowded at 6 p.m. 😅",phone:"📱 Nice phone! But nothing changed in your life.",
 shelter:"🐶 The shelter bought food for 20 dogs. They sent you a photo!",panel:"☀️ The solar panel is complete. Your electricity bill is 20% lower."};
 const L=c.map(k=>R[k]);if(!L.length)L.push("💰 You saved all the money. Was that a good idea?");if(1000-t>=200&&L.length)L.push("💰 You still have €"+(1000-t)+" for later.");
 $q("#tout").innerHTML=`<div class="rep"><b>🔮 You, one year later</b><ul>${L.map(x=>"<li>"+x+"</li>").join("")}</ul><p class="hint">Which choice was the best use of money? Why?</p></div>`}
/* word counter */
function wc(){const t=(hv("x11")||"").toLowerCase().replace(/[’]/g,"'");const used=D.TW.filter(w=>t.includes(w));const n=(t.match(/\S+/g)||[]).length;
 $q("#wc").textContent=n+" words · "+used.length+" lesson words"+(used.length?": "+used.join(", "):"")+(used.length>=5&&n>=40?" ✓ Great!":"")}
document.addEventListener("input",e=>{if(e.target.dataset&&e.target.dataset.k==="x11")wc()});
window.afterFill=function(){D.SW.forEach((w,i)=>{const g=hv("srt_"+i),c=$a(".chip").find(x=>x.dataset.w===w);if(c)chipTo(c,g||null)});
 (hv("prs")||"").split(",").filter(Boolean).forEach(prMark);if(pdone.size)$q("#r_prs").textContent=pdone.size+" / "+D.PN;
 const m=(hv("mayor")||"").split(",");$a(".pj input").forEach(i=>i.checked=m.includes(i.dataset.p));budg();wc()};
""".replace("__D__", json.dumps(DATA, ensure_ascii=False))
CSS = """<style>.bl{display:inline-block;background:var(--y2);border-left:4px solid var(--y);padding:3px 10px;font-size:13px;margin-bottom:6px}.bl b{color:var(--pur)}
.emo{font-size:30px;display:inline-block;width:46px}
.pairs{display:grid;grid-template-columns:1fr 1.3fr;gap:10px 24px;max-width:620px}.pl,.pr{display:flex;flex-direction:column;gap:8px}.pb{font:inherit;font-size:16px;text-align:left;padding:7px 12px;border:2px solid #ddd;background:#fff;cursor:pointer}.pb.sel{border-color:var(--y);background:var(--y2)}.pb.done{border-color:#2e9b57;background:#e7f6ec;color:#1e7a43;cursor:default}.pb.bad{border-color:#d9534f;background:#fdecec}
.rd{border:1px solid #ddd;border-radius:10px;background:#fff;max-width:720px;margin:10px 0}.rh{background:#ff4500;color:#fff;font-weight:600;padding:8px 14px;border-radius:10px 10px 0 0}.rc{padding:8px 14px 8px 24px;border-top:1px solid #eee}.rc.op{padding-left:14px;background:#fffaf5}.ru{font-size:13px;color:#888;font-weight:600}.rc p{margin:4px 0}.rv{font-size:12px;color:#999}
details.dd summary{cursor:pointer;color:var(--sky);font-weight:600;margin:6px 0}
.pool{display:flex;flex-wrap:wrap;gap:6px;min-height:44px;padding:10px;border:2px dashed #ddd;margin:8px 0 12px}.chip{font-size:15px;padding:5px 12px;border:2px solid var(--y);background:#fff;cursor:pointer;user-select:none}.chip.sel{background:var(--y)}.chip.ok{border-color:#2e9b57;background:#e7f6ec}.chip.no{border-color:#d9534f;background:#fdecec}
.bins{display:grid;grid-template-columns:1fr 1fr;gap:10px}.bin{border:2px solid #ddd;padding:8px;min-height:140px;cursor:pointer;background:#fafafa}.bin b{display:block;margin-bottom:6px}.bin .in{display:flex;flex-direction:column;gap:4px;align-items:flex-start}
.proj{display:grid;grid-template-columns:1fr 1fr;gap:8px;max-width:640px}.pj{border:2px solid #ddd;padding:8px 10px;cursor:pointer;background:#fff}.pj:has(input:checked){border-color:var(--y);background:var(--y2)}
.tm{font-weight:600;background:var(--y2);padding:4px 12px;margin-right:8px}.tm.bad{background:#fdecec;color:#b52b27}.rep{border:2px solid var(--y);background:#fffdf3;padding:10px 16px;margin-top:10px}.rep li{margin:4px 0}
@media(max-width:700px){.bins,.proj,.pairs{grid-template-columns:1fr}}</style>"""
sections = [("1", s1), ("2", s2), ("3", s3), ("4", s4), ("5", s5), ("6", s6), ("7", s7), ("8", s8), ("9", s9), ("10", s10), ("11", s11)]
vocab = [("Words", ["build", "crowded", "economy", "government", "education", "environment", "complete", "save time", "a good use of money", "employ"]),
         ("Opinions", ["I think it's a good idea.", "I don't think it's a good idea.", "I agree.", "It's going to be bad for …", "It's going to help …"])]
html = page("8B", "For and against", "Extra · Lexical lab", ["learn and use the 8B words step by step: remember → understand → use → create",
            "read a Reddit thread and listen to a radio show about everyday plans", "say what you think about plans: I think it's a good idea because …"],
            "oa1-8b-extra", CODE, sections, K, vocab, XJS)
html = html.replace("</head>", CSS + "</head>", 1)
p = os.path.join(OUT, "lessons/8b/all/extra.html"); os.makedirs(os.path.dirname(p), exist_ok=True)
open(p, "w", encoding="utf-8").write(html); print("wrote", p, len(K), "keys")
