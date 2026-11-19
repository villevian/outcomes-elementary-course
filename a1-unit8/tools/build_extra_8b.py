"""Outcomes A1 · 8B Extra — Lexical lab on 8B vocabulary (town plans), A2+ texts.
Lexical approach (chunks, collocations, noticing → use) organised by Bloom's taxonomy:
REMEMBER (cards, emoji) → UNDERSTAND (meanings) → APPLY (collocations, gaps) → READ & NOTICE (Reddit-style thread) →
LISTEN (street interviews, audio 8b-street.mp3) → ANALYSE (for / against) → EVALUATE (Mayor for a day) → CREATE (your comment).
Thread and interviews are based on real local debates discussed on Reddit and in local news (stadium vs library, street lights off
at night, a German town where you phone to switch the lights on); the town, names and usernames are invented.
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

# 1 REMEMBER — emoji town
EMO = [("🏟️", "a new stadium"), ("✈️", "a new airport"), ("🚇", "a new metro line"), ("💡", "more street lights"), ("📚", "a bigger library"),
       ("🏥", "a new hospital"), ("🛍️", "a new shopping centre"), ("🏫", "more schools"), ("🛣️", "better roads"), ("📶", "better wi-fi")]
OPT1 = sorted(w for _, w in EMO)
EMO_S = shuf(EMO)

s1 = (bloom("1 REMEMBER", "згадати слова") + sh("Vocabulary", "Our town needs …") +
      ins(1, "What does our town need? Look at the picture and choose the phrase.", "Що потрібно місту? Подивись на емодзі й обери фразу.") +
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
PAIRS = [("build", "a new stadium"), ("save", "time"), ("employ", "local people"), ("help", "the economy"), ("protect", "the environment"),
         ("take a long time", "to complete"), ("spend money", "on education"), ("be bad", "for safety")]
s3 = (bloom("3 APPLY", "використати в словосполученнях") + sh("Lexical lab", "Word partners") +
      ins(3, "Words have partners! Click a verb on the left, then its partner on the right.", "Слова мають «пари». Натисни дієслово зліва, потім його пару справа.") +
      '<div class="pairs"><div class="pl">%s</div><div class="pr">%s</div></div>' % (
          "".join('<button class="pb" data-i="%d" data-s="L">%s</button>' % (i, a) for i, (a, _) in shuf(list(enumerate(PAIRS)))),
          "".join('<button class="pb" data-i="%d" data-s="R">%s</button>' % (i, b) for i, (_, b) in shuf(list(enumerate(PAIRS))))) +
      hid("prs") + '<p class="res" id="r_prs"></p>')
G4 = [("The metro is going to ___ time for everyone.", "save"), ("The new shopping centre is going to ___ 200 local people.", "employ"),
      ("Tourists are going to ___ the economy.", "help"), ("Dark streets are bad for ___.", "safety"),
      ("A new road can take a long time to ___.", "complete"), ("We need to ___ the environment — please don't build in the park!", "protect")]
OPT4 = sorted(a for _, a in G4)
s4 = (bloom("3 APPLY", "використати в реченнях") + sh("Lexical lab", "Complete the sentences") +
      ins(4, "Complete the sentences with the partners from Exercise 3. Try from memory!", "Доповни речення. Спробуй з пам’яті!") +
      "".join('<div class="row"><span class="w">%d</span>%s%s</div>' % (i + 1, q.replace("___", sel("x4_%d" % i, OPT4, 130)), fb("x4_%d" % i)) for i, (q, _) in enumerate(G4)) + ctl("x4"))
for i, (_, a) in enumerate(G4): K["x4_%d" % i] = [a]

# 4 READ — Reddit-style thread
THREAD = [("greenford_mum", "Council meeting news 📢 They want to build a <b>new stadium</b> by the river (€40 million!) — and the library is going to close on Sundays to save money. Is this <b>a good use of money</b>??", "post"),
          ("footballdad77", "I think it’s a good idea. The stadium is going to <b>employ</b> 300 local people and it’s going to <b>help the economy</b>. Cafés and shops are going to make more money on match days.", ""),
          ("bookworm_lena", "I don’t think it’s a good idea. The library is the only free place for kids and students in our town. <b>Education</b> is more important than football!", ""),
          ("cyclist_greenford", "Nobody is talking about traffic. The roads near the river are already <b>crowded</b>. On match days it’s going to be terrible.", ""),
          ("eco_tom", "It’s going to be bad for the <b>environment</b>. They’re going to <b>build</b> on the park by the river! Why not use the old factory?", ""),
          ("realist_99", "In my old city they built a stadium. It took seven years to <b>complete</b> and it cost double. <b>Nothing</b> is going to change here — the <b>government</b> always does this 😅", ""),
          ("greenford_mum", "Wow, so many opinions! How about a vote? 🗳️", "")]
THR = '<div class="rd"><div class="rh">r/Greenford · Our town, our plans</div>%s</div>' % "".join(
    '<div class="rc%s"><div class="ru">u/%s</div><p>%s</p><div class="rv">⬆ %d · 💬 Reply</div></div>' % (" op" if k == "post" else "", u, t, v)
    for (u, t, k), v in zip(THREAD, [128, 64, 97, 41, 55, 73, 12]))
FA = [("footballdad77", "for"), ("bookworm_lena", "against"), ("cyclist_greenford", "against"), ("eco_tom", "against"), ("realist_99", "against")]
s5 = (bloom("4 READ & NOTICE", "читати й помічати слова") + sh("Reading", "r/Greenford") +
      ins(5, "Read the Reddit thread about a new stadium. Is each person <b>for</b> or <b>against</b> the stadium?", "Прочитай обговорення. Людина «за» чи «проти» стадіону?") + THR +
      "".join('<div class="row">u/%s → %s%s</div>' % (u, sel("x5_%d" % i, ["for", "against"], 110), fb("x5_%d" % i)) for i, (u, _) in enumerate(FA)) + ctl("x5") +
      '<p class="hint">The town and usernames are invented. The situation is real: people on Reddit and in local news often argue about money for stadiums vs libraries.</p>')
for i, (_, a) in enumerate(FA): K["x5_%d" % i] = [a]
WHO = [("The stadium is going to be good for jobs.", "footballdad77"), ("Kids need a free place to study.", "bookworm_lena"), ("There are too many cars near the river.", "cyclist_greenford"),
       ("They are going to build in the park.", "eco_tom"), ("Big projects often cost more than they say.", "realist_99")]
UOPT = sorted(set(u for u, _ in FA))
s6 = (bloom("4 READ & NOTICE", "знайти деталі") + sh("Reading", "Who says it?") +
      ins(6, "Who says this? The words are different in the thread — look for the meaning!", "Хто це каже? У тексті інші слова — шукай зміст.") +
      '<details class="dd"><summary>💬 Open the thread</summary>%s</details>' % THR +
      "".join('<div class="row"><span class="w">%d</span>%s → %s%s</div>' % (i + 1, q, sel("x6_%d" % i, UOPT, 190), fb("x6_%d" % i)) for i, (q, _) in enumerate(WHO)) + ctl("x6"))
for i, (_, a) in enumerate(WHO): K["x6_%d" % i] = [a]

# 5 LISTEN — street interviews
L1 = [("street lights at night", "yes"), ("a new stadium", "yes"), ("a new hospital", "no"), ("a new metro line to the airport", "yes"), ("more parks", "no")]
s7 = (bloom("5 LISTEN", "слухати") + sh("Listening", "Our Town Today: street interviews") +
      ins(7, "Listen to a radio reporter in the street. Which plans do people talk about?", "Послухай вуличні інтерв’ю. Про які плани говорять люди? Перший раз — без пауз.") +
      audio_slot("8b-street.mp3", "Our Town Today (1:30)") +
      "".join('<div class="row">%s → %s%s</div>' % (t, sel("x7_%d" % i, ["yes", "no"], 80), fb("x7_%d" % i)) for i, (t, _) in enumerate(L1)) + ctl("x7"))
for i, (_, a) in enumerate(L1): K["x7_%d" % i] = [a]
L2 = [("I walk my dog late at night.", "Tom"), ("I’d like to see the stars at night!", "Anna"), ("Our kids need a bigger library.", "George"),
      ("The roads are already crowded.", "George"), ("It’s going to save time for everyone.", "Tom"), ("Now it takes an hour by bus.", "Anna")]
SCRIPT = ('<p><b>Reporter:</b> Good morning! This is Our Town Today. The council has three big plans this year … The council is going to switch off the street lights from one to five in the morning, to save money. What do you think?</p>'
          '<p><b>Tom:</b> I don’t think it’s a good idea. I walk my dog late at night, and the streets are going to be very dark. It’s going to be bad for safety.</p>'
          '<p><b>Anna:</b> Actually, I think it’s a good idea. It’s going to save money, and it’s good for the environment. And I’d like to see the stars at night!</p>'
          '<p><b>Reporter:</b> In a small town in Germany, you can call a number on your phone, and the street lights come on for fifteen minutes. — <b>Anna:</b> Ha! That’s brilliant. I’d really like that here.</p>'
          '<p><b>Reporter:</b> The second plan is a new stadium by the river. It’s going to cost forty million euros.</p>'
          '<p><b>George:</b> Forty million? That’s not a good use of money. They’re going to close the library on Sundays, but they have money for a stadium? Our kids need more schools and a bigger library, not more football. … The roads are already crowded. On match days, it’s going to be terrible.</p>'
          '<p><b>Reporter:</b> And the last plan: a new metro line to the airport. It’s going to take six years to complete.</p>'
          '<p><b>Tom:</b> Six years! That’s a long time. But I agree with the plan. It’s going to save time for everyone, and it’s going to employ a lot of local people. — <b>Anna:</b> I agree. Now it takes an hour to get to the airport by bus.</p>')
s8 = (bloom("5 LISTEN", "слухати деталі") + sh("Listening", "Who says it?") +
      ins(8, "Listen again. Who says it: Tom, Anna or George? You can pause.", "Послухай ще раз. Хто це каже? Можна ставити на паузу.") +
      audio_slot("8b-street.mp3", "Our Town Today") +
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
      ins(9, "Sort the arguments: is it a reason FOR a plan or AGAINST it? Click a sentence, then a box.", "Розклади аргументи: «за» чи «проти». Натисни речення, потім коробку.") +
      '<div class="pool" id="pool">%s</div><div class="bins"><div class="bin" data-g="for"><b>👍 For</b><div class="in"></div></div><div class="bin" data-g="against"><b>👎 Against</b><div class="in"></div></div></div>' % "".join(
          '<span class="chip" data-w="%s">%s</span>' % (esc(w), w) for w in shuf(SW)) +
      "".join(hid("srt_%d" % i) for i in range(len(SW))) + '<div class="ctl"><button class="btn" onclick="sortChk()">Check</button><span class="res" id="r_srt"></span></div>')

# 7 EVALUATE — Mayor for a day
PROJ = [("stadium", "🏟️ a new stadium", 40), ("metro", "🚇 a new metro line", 60), ("library", "📚 a bigger library", 10), ("hospital", "🏥 a new hospital", 50),
        ("lights", "💡 more street lights", 5), ("schools", "🏫 two new schools", 30), ("wifi", "📶 free wi-fi in the centre", 5), ("park", "🌳 a new park", 15)]
s10 = (bloom("7 EVALUATE", "оцінити й вибрати") + sh("Game", "Mayor for a day 🏛️") +
       ins(10, "You are the mayor of Greenford! You have <b>€100 million</b>. Choose the projects. Then press <b>Greenford in 2030</b>.", "Ти — мерка Ґрінфорда! Маєш €100 млн. Обери проєкти й натисни «Greenford in 2030».") +
       '<div class="proj">%s</div><div class="ctl"><span class="tm" id="left">€100 million left</span><button class="btn" onclick="town()">🔮 Greenford in 2030</button></div><div id="tout"></div>' % "".join(
           '<label class="pj"><input type="checkbox" data-p="%s" data-c="%d" onchange="budg()"> %s <b>€%dm</b></label>' % (k, c, t, c) for k, t, c in PROJ) +
       hid("mayor") + '<p class="ins" style="margin-top:14px">Explain your choice to your teacher (or write): <i>I chose … because it’s going to … I didn’t choose … because …</i></p>' +
       ta("x10", "I chose … because it’s going to …", 90))

# 8 CREATE — your Reddit comment
TW = ["build", "crowded", "economy", "government", "education", "environment", "complete", "save time", "a good use of money", "employ", "safety", "i agree", "i think it's a good idea", "i don't think", "it's going to"]
s11 = (bloom("8 CREATE", "створити свій текст") + sh("Writing", "Your comment on r/Greenford") +
       ins(11, "Write your own comment for the thread (40–60 words). Are you for or against the stadium? Use at least 5 words from this page.", "Напиши свій коментар (40–60 слів). Ти «за» чи «проти» стадіону? Використай щонайменше 5 слів зі сторінки.") +
       wbox(["a good use of money", "help the economy", "employ local people", "crowded", "environment", "education", "save time", "take a long time to complete", "I agree", "I don't think it's a good idea"]) +
       ta("x11", "u/maria: I think … / I don't think …", 140) + '<p class="res" id="wc"></p>' + SELF)

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
function budg(){const s=$a(".pj input:checked").reduce((a,i)=>a+ +i.dataset.c,0);const l=100-s;$q("#left").textContent=(l<0?"⚠ over budget by €"+(-l):"€"+l)+" million"+(l<0?"":" left");$q("#left").className="tm"+(l<0?" bad":"");setH("mayor",chosen().join(","))}
function town(){const c=chosen(),has=x=>c.includes(x),s=$a(".pj input:checked").reduce((a,i)=>a+ +i.dataset.c,0);if(s>100){$q("#tout").innerHTML="<p>⚠ Too expensive! Remove a project.</p>";return}
 const L=[];L.push(has("metro")?"🚇 The metro line is complete. It saves time for everyone — 20 minutes to the airport!":"🚌 There is no metro. The buses are very crowded in the morning.");
 L.push(has("stadium")?"🏟️ The stadium employs 300 people and helps the economy — but the roads are crowded on match days.":"⚽ No stadium. Football fans are not happy, but the river park is still green.");
 L.push(has("library")||has("schools")?"📚 More kids study after school. Good for education!":"📕 The library is closed on Sundays. Students study in cafés.");
 L.push(has("hospital")?"🏥 The new hospital is great. People don't wait for a doctor for weeks.":"🏥 People wait a long time for a doctor.");
 L.push(has("lights")?"💡 The streets are safe at night.":"🌌 The streets are dark at night… but you can see the stars!");
 if(has("park"))L.push("🌳 The new park is good for the environment. Families love it.");if(has("wifi"))L.push("📶 Free wi-fi! Tourists post photos of Greenford everywhere.");
 const happy=Math.min(100,30+c.length*9+(has("hospital")?8:0)+(has("library")?6:0));
 $q("#tout").innerHTML=`<div class="rep"><b>📰 Greenford News, 2030 · People are ${happy}% happy</b><ul>${L.map(x=>"<li>"+x+"</li>").join("")}</ul><p class="hint">Do you agree? Was it a good use of money?</p></div>`}
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
vocab = [("Town plans", ["a new airport", "a bigger library", "better roads", "a new stadium", "a new metro line", "a new shopping centre", "a new hospital", "more street lights", "more schools", "better wi-fi"]),
         ("Words", ["build", "crowded", "economy", "government", "education", "environment", "complete", "save time", "a good use of money", "employ"]),
         ("Opinions", ["I think it's a good idea.", "I don't think it's a good idea.", "I agree.", "It's going to be bad for …", "It's going to help …"])]
html = page("8B", "For and against", "Extra · Lexical lab", ["learn and use the 8B words step by step: remember → understand → use → create",
            "read a Reddit thread and listen to street interviews about town plans", "say what you think about plans: I think it's a good idea because …"],
            "oa1-8b-extra", CODE, sections, K, vocab, XJS)
html = html.replace("</head>", CSS + "</head>", 1)
p = os.path.join(OUT, "lessons/8b/all/extra.html"); os.makedirs(os.path.dirname(p), exist_ok=True)
open(p, "w", encoding="utf-8").write(html); print("wrote", p, len(K), "keys")
