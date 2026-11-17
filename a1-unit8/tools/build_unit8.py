"""Outcomes A1 · Unit 8 Plans — opener, 8A, 8B, 8C lesson pages.
Usage: python3 build_unit8.py OUT_ROOT [STUDENT_CODE]
  OUT_ROOT = repo root (template) or a student's repo root; STUDENT_CODE empty = template preview (no sync).
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from oa_page import *

OUT = sys.argv[1] if len(sys.argv) > 1 else ".."
CODE = sys.argv[2] if len(sys.argv) > 2 else ""

def write(rel, html):
    p = os.path.join(OUT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(html); print("wrote", p)

def variants(s):
    """Accept full and short forms: I'd / I would, wouldn't / would not, 'm / am ..."""
    out = {s}
    pairs = [("'d ", " would "), ("wouldn't", "would not"), ("'m ", " am "), ("isn't", "is not"), ("aren't", "are not"), ("'s not", " is not")]
    changed = True
    while changed:
        changed = False
        for x in list(out):
            for a, b in pairs:
                for y in (x.replace(a, b), x.replace(b, a)):
                    y = " ".join(y.split()).replace(" '", "'")
                    if y not in out: out.add(y); changed = True
    return sorted(out, key=lambda v: (v != s, len(v)))

# =====================================================================
# UNIT OPENER (p.74–75)
# =====================================================================
def opener():
    K = {}
    s1 = (sh("Speaking") + ins(1, "Work in pairs. Discuss the questions.", "Обговоріть питання. Напиши коротко свої відповіді — на уроці говоримо усно.")
          + '<div class="pc" style="max-width:520px;margin:10px 0"><div class="pe">🎮👴🏻👨🏻</div><p style="min-height:0"><i>Old friends play video games together.</i> (photo in the book, p.74–75)</p></div>')
    qs = ["Look at the photo. Do you ever do things like this?",
          "Where do you most like to spend your free time? Who do you usually spend it with?",
          "Are you happy with how much free time you have? If not, why not?",
          "What different ways of enjoying yourself are there where you live?",
          "How often do you go out in the evening? Where to?"]
    for i, q in enumerate(qs, 1):
        s1 += '<div class="row"><span class="w">%d</span>%s %s<br>%s</div>' % (i, q, say(q), ta("o1_%d" % i, "My answer…", 50))
    items = ["doing some shopping", "going to the library", "tidying your flat / house", "paying a bill", "going to the cinema",
             "going swimming / cycling / running", "doing some drawing / painting", "going for a walk"]
    s2 = (sh("Speaking") + ins(2, "Work with a new partner. Which of these things do you enjoy doing? Which are you planning to do this week?",
                               "Що з цього тобі подобається робити? Що ти плануєш зробити цього тижня?")
          + '<div class="row hint"><span class="w"></span><b style="display:inline-block;width:330px">activity</b><b style="display:inline-block;width:170px">Do I enjoy it?</b><b>This week?</b></div>')
    for i, it in enumerate(items, 1):
        s2 += '<div class="row"><span class="w">%d</span><span style="display:inline-block;width:330px">%s %s</span>%s %s</div>' % (
            i, it, say(it), sel("o2_%da" % i, ["I enjoy it 🙂", "It’s OK 😐", "I don’t enjoy it 🙁"], 160), sel("o2_%db" % i, ["Yes, I’m planning to", "No, not this week"], 190))
    s2 += ex(["I enjoy going for a walk. I’m planning to go for a walk on Saturday.", "I don’t enjoy paying bills! But I need to pay my gas bill this week."]) + SELF
    sections = [("1", s1), ("2", s2)]
    return page("8", "Plans", "Unit opener", ["discuss plans", "say how you feel about government plans", "decide how to improve places you know"],
                "oa1-8-0-lesson", CODE, sections, K,
                vocab=[("Free time", ["doing some shopping", "going to the library", "tidying your flat", "paying a bill", "going to the cinema", "going swimming", "doing some drawing", "going for a walk"])])

# =====================================================================
# 8A What are your plans? (p.76–77)
# =====================================================================
def lesson_8a():
    K = {}
    D1 = [("A", "What are your plans for today?"), ("B", "I'm going to do some shopping this afternoon and then just go home. What about you?"),
          ("A", "I'm going to go to the gym. Then I'm going to meet some friends."), ("B", "What about tomorrow? Do you want to go out somewhere?"),
          ("A", "Yes. Great. Where?"), ("B", "How about the Old Town?"), ("A", "OK. Fine. What time?"), ("B", "How about twelve?"), ("A", "Perfect.")]
    pu = {"do some shopping": 1, "just go home": 2, "go to the gym": 3, "meet some friends": 4, "Old Town": 5, "twelve": 6}
    def purple(t):
        for w in pu: t = t.replace(w, '<span class="pu">%s</span>' % w)
        return t
    dl = "".join("<p><b>%s:</b> %s</p>" % (w, purple(t)) for w, t in D1)
    s1 = (sh("Speaking") + ins(1, "▶ Work in pairs. Listen to the conversation between two friends. Then say it.",
                               "Послухай розмову двох друзів. Потім прочитай її вголос (на уроці — в парі з учителькою).")
          + audio_slot("8a-ex01.mp3", "Listen – conversation") + '<div class="dlg">%s</div>' % dl)

    s2 = (sh("Speaking") + ins(2, "Change the words in purple. Use a dictionary if you need to. Then practise your new conversation with your partner. Exchange roles and repeat.",
                               "Заміни фіолетові слова своїми. Натисни «Show my conversation» — і прочитай свою розмову.")
          + '<div class="two">' + "".join('<div class="row"><span class="pu" style="display:inline-block;width:170px">%s</span> → %s</div>' % (w, inp("e2_%d" % n, 210, w))
                                           for w, n in pu.items()) + '</div>'
          + '<div class="ctl"><button class="btn" onclick="myDlg()">Show my conversation</button></div><div class="out" id="my2"></div>')

    words3 = ["appointment", "book", "camping", "gas", "lift", "mind", "pack", "show", "trip", "wedding"]
    S3 = [("I need to buy some clothes for a friend's {w}. I want to look my best.", ["wedding"]),
          ("I need to pay my {w} <b>bill</b> today – before I forget.", ["gas"]),
          ("I'm going away for a few days so I need to {w} my things tonight.", ["pack"]),
          ("I want to visit my parents this weekend, so I have to {w} a train ticket.", ["book"]),
          ("I can't come to class tomorrow because I have a doctor's {w}.", ["appointment"]),
          ("My wife is away on a <b>business</b> {w} this week.", ["trip"]),
          ("I have my car with me, so I can give you a {w} to the shops if you want.", ["lift"]),
          ("A: We're planning to go {w} next weekend. Do you want to come with us?<br>B: I can't. I have tickets to a {w} at the theatre that Saturday.", ["camping", "show"]),
          ("A: So what time do you want to meet?<br>B: I don't {w}. What time's best for you?", ["mind"])]
    s3 = sh("Vocabulary", "Plans for the week") + ins(3, "Complete the sentences with these words.", "Доповни речення словами з рамки.") + wbox(words3)
    for i, (t, ans) in enumerate(S3, 1):
        parts = t.split("{w}"); h = parts[0]
        for j, a in enumerate(ans):
            k = "e3_%d%s" % (i, "abc"[j] if len(ans) > 1 else ""); K[k] = [a]
            h += inp(k, 130) + fb(k) + parts[j + 1]
        s3 += '<div class="row"><span class="w">%d</span>%s</div>' % (i, h)
    s3 += ctl("e3")

    s4 = (ins(4, "Ⓟ ▶ Listen to the words from Exercise 3 and practise saying them on their own and in a phrase. Which words / phrases do you find hard to say? Practise saying them again.",
              "Послухай запис і повторюй. 🔊 біля слова — щоб послухати окремо ще раз. Запиши, які слова важкі.")
          + audio_slot("8a-ex04.mp3", "Listen and repeat")
          + "".join('<div class="row"><span class="w"></span><b style="display:inline-block;width:150px">%s</b>%s <span style="display:inline-block;width:300px;margin-left:16px">%s</span>%s</div>'
                    % (w, say(w), p, say(p)) for w, p in [("wedding", "a friend's wedding"), ("gas bill", "pay my gas bill"), ("pack", "pack my things"), ("book", "book a train ticket"),
                                                          ("appointment", "have a doctor's appointment"), ("business trip", "away on a business trip"), ("lift", "give you a lift"),
                                                          ("camping", "go camping"), ("show", "a show at the theatre"), ("mind", "I don't mind")])
          + '<p>Hard words / phrases for me:</p>' + ta("e4_hard", "e.g. appointment, a doctor's appointment…", 50))

    s5 = ins(5, "Work in pairs. Look at Exercise 3 and say:", "Подивись на вправу 3 і скажи (напиши коротко):")
    for i, q in enumerate(["which things you often do.", "which things you never do – or don't often do.", "which things you're planning to do this week.", "which things you most / least enjoy doing."], 1):
        s5 += '<div class="row"><span class="w">%d</span>%s<br>%s</div>' % (i, q, ta("e5_%d" % i, "", 44))
    s5 += model("m5", "I often pay bills online. I never go camping. This week I'm going to book a train ticket. I most enjoy going to a show. I least enjoy packing!")

    s6 = (sh("Listening") + ins(6, "▶ Listen to three conversations about plans. Match the conversations (1–3) with the places where they happen (a–c).",
                                "Послухай три розмови. Де вони відбуваються?")
          + audio_slot("8a-ex06-07.mp3", "Three conversations") + wbox(["a  at work", "b  at university", "c  on holiday"])
          + "".join('<div class="row">Conversation %d → %s%s</div>' % (i, sel("e6_%d" % i, ["a – at work", "b – at university", "c – on holiday"], 200), fb("e6_%d" % i)) for i in (1, 2, 3)) + ctl("e6"))
    K.update({"e6_1": ["b – at university"], "e6_2": ["c – on holiday"], "e6_3": ["a – at work"]})
    s7 = ins(7, "▶ Listen again. Write the correct conversation (1, 2 or 3).", "Послухай ще раз. У якій розмові (1, 2 чи 3)?") + audio_slot("8a-ex06-07.mp3", "Three conversations")
    for i, t in enumerate(["Someone is going to go to a restaurant.", "Someone arranges where to meet.", "Someone invites another person out for dinner.",
                           "Someone has to go and get another person.", "Someone doesn't want to meet.", "Someone is going to fly somewhere soon."]):
        k = "e7_%s" % "abcdef"[i]; K[k] = [str([3, 2, 1, 3, 1, 2][i])]
        s7 += '<div class="row"><span class="w">%s</span><span style="display:inline-block;width:420px">%s</span>%s%s</div>' % ("abcdef"[i], t, sel(k, ["1", "2", "3"], 70), fb(k))
    s7 += ctl("e7")

    gb = ('<div class="gbox"><div class="gh">Going to</div><p>We use the present form of the verb <i>be</i> + <i>going to</i> + verb to talk about the future – and especially the plans we have.</p>'
          '<p><i><b>I\'m going to go</b> running by the river later.</i> %s</p><p><i>She<b>\'s not going to have</b> time today.</i> %s</p><p><i>What about tonight? <b>Are</b> you <b>going to be</b> busy then?</i> %s</p>'
          '<p class="hint">🇺🇦 be (am / is / are) + going to + дієслово = мої плани на майбутнє.</p></div>') % (
        say("I'm going to go running by the river later."), say("She's not going to have time today."), say("What about tonight? Are you going to be busy then?"))
    S8 = [("A: My parents {g} me for dinner tonight. (take)", ["are going to take"]), ("B: That's nice. Where {g}? (go)", ["are you going to go", "are you going", "are they going to go", "are they going"]),
          ("A: I {g} tomorrow. My flight is at six in the morning! (leave)", ["'m going to leave", "am going to leave"]), ("B: Really? That's early. What time {g}? (get up)", ["are you going to get up"]),
          ("A: Some friends {g} next week. (visit)", ["are going to visit"]), ("B: That's nice. How long {g}? (stay)", ["are they going to stay"]),
          ("A: I spoke to Tymofiy. He {g}. He's got another bad headache. (not come)", ["isn't going to come", "is not going to come", "'s not going to come"]),
          ("B: Really? I hope it isn't anything serious. {g} to the doctor's? (go)", ["Is he going to go", "Is he going"])]
    s8 = sh("Grammar") + gb + ins(8, "Complete the sentences with the correct form of <i>going to</i> and the verbs in brackets.", "Встав going to + дієслово в дужках у правильній формі.")
    for i, (t, a) in enumerate(S8):
        k = "e8_%d%s" % (i // 2 + 1, "ab"[i % 2]); K[k] = a
        pre, post = t.split("{g}")
        s8 += '<div class="row"><span class="w">%s</span>%s%s%s%s</div>' % (str(i // 2 + 1) if i % 2 == 0 else "", pre, inp(k, 230), post, fb(k))
    s8 += ctl("e8") + '<p class="hint">G — See Grammar reference 8A.</p>'

    s9 = ins(9, "Work in pairs. Which of these things are you going to do today / tomorrow / this week / this month? When? Ask each other questions to find out more.",
             "Що з цього ти збираєшся робити і коли? Напиши речення з going to.")
    for i, t in enumerate(["meet a friend", "cook dinner / lunch", "go on holiday", "write some emails", "watch TV", "do some studying / homework", "go shopping", "get up early / late"], 1):
        s9 += '<div class="row"><span class="w">%d</span><span style="display:inline-block;width:240px">%s</span>%s %s</div>' % (
            i, t, sel("e9_%dw" % i, ["today", "tomorrow", "this week", "this month", "not going to"], 140), inp("e9_%d" % i, 380, "I'm going to …"))
    s9 += ex(["A: I'm going to meet some friends tonight.", "B: Really? Nice. Where are you going to meet?", "A: In the centre of town. We're going to have dinner."])

    order = {"a": 4, "b": 6, "c": 8, "d": 1, "e": 9, "f": 3, "g": 2, "h": 7, "i": 5}
    L10 = {"a": "How about in the main square, under the big clock?", "b": "Is six OK?", "c": "Oh, sorry. Well, how about seven thirty?", "d": "What are your plans for later?",
           "e": "Perfect! See you later. Bye.", "f": "Yes. Great. Where?", "g": "I don't have any. Why? Do you want to meet somewhere?", "h": "It's quite early.", "i": "Yes, fine. What time?"}
    s10 = (sh("Developing conversations") + '<div class="dcbox"><div class="gh">Making suggestions</div><p>We often make suggestions using <i>How about …?</i></p>'
           '<p><i>A: Do you want to meet somewhere?<br>B: Yes, OK. Where?<br>A: <b>How about</b> in the main square at eight?</i></p></div>'
           + ins(10, "Number the sentences in the correct order (1–9) to make a conversation.", "Пронумеруй речення 1–9, щоб вийшла розмова."))
    for l, t in L10.items():
        k = "e10_%s" % l; K[k] = [str(order[l])]
        s10 += '<div class="row"><span class="w">%s</span>%s %s%s</div>' % (l, sel(k, [str(n) for n in range(1, 10)], 70), t, fb(k))
    s10 += ctl("e10")
    seq = sorted(order, key=order.get)
    D11 = [("A" if n % 2 == 0 else "B", L10[l]) for n, l in enumerate(seq)]
    s11 = (ins(11, "▶ Listen and check your ideas.", "Послухай і перевір свій порядок.") + audio_slot("8a-ex11.mp3", "Listen and check")
           + model("m11", "".join("<p><b>%s:</b> %s</p>" % (w, t) for w, t in D11), "Show the conversation"))

    s12 = ins(12, "Respond to each question by writing a suggestion with <i>How about …?</i>", "Відповідай на кожне питання пропозицією з How about …?")
    for i, q in enumerate(["What do you want to see at the cinema?", "What are we going to get her for her birthday?", "What do you want to eat tonight?", "Do you know a good place to have a party?"], 1):
        s12 += '<div class="row"><span class="w">%d</span>%s %s<br>%s</div>' % (i, q, say(q), inp("e12_%d" % i, 520, "How about …?"))
    s12 += model("m12", "1 How about the new Mission Impossible film? · 2 How about some flowers? · 3 How about pizza? · 4 How about the sports centre?")

    F = [("a", "What are your plans for today?"), ("b", "I'm going to {i1}. What about you?"), ("a", "I'm going to {i2}."),
         ("b", "What about tomorrow? Do you want to go out somewhere?"), ("a", "Yes, great. Where?"), ("b", "How about {i3}?"),
         ("a", "OK. Fine. What time?"), ("b", "How about {i4}?"), ("a", "Perfect. See you later. Bye.")]
    fl = '<div class="flow"><div class="a" style="text-align:center;font-style:normal;font-weight:700;background:#fff;border:1.5px solid #333">Student A</div><div></div><div class="b" style="text-align:center;font-style:normal;font-weight:700;background:#fff;border:1.5px solid #333">Student B</div>'
    for n, (who, t) in enumerate(F):
        for j in range(1, 5): t = t.replace("{i%d}" % j, inp("e13_%d" % j, 150, "…"))
        fl += ('<div class="a">%s</div><div class="arr">↘</div><div></div>' % t) if who == "a" else ('<div></div><div class="arr">↙</div><div class="b">%s</div>' % t)
    fl += "</div>"
    s13 = (sh("Conversation practice") + ins(13, "Work in pairs. Have conversations about plans. Use this guide to help you. Take turns to begin.",
                                             "Склади розмову за схемою: заповни пропуски і натисни «Show / Listen». Потім — те саме усно з учителькою.")
           + fl + '<div class="ctl"><button class="btn" onclick="flowDlg()">Show & listen to my conversation</button></div><div class="out" id="my13"></div>' + SELF)

    xjs = r"""
const D1=%s;const PU=%s;
function myDlg(){const sub={};PU.forEach((w,i)=>{const v=document.querySelector('[data-k="e2_'+(i+1)+'"]').value.trim();sub[w]=v||w});
 const L=D1.map(([w,t])=>{let x=t;for(const k in sub)x=x.replace(k,sub[k]);return [w,x]});
 $("my2").innerHTML=L.map(([w,t])=>"<p><b>"+w+":</b> "+t+"</p>").join("")+'<button class="say big" id="p2">▶ Listen</button>';$("my2").classList.add("show");$("p2").onclick=e=>{e.stopPropagation();playDlg(L)}}
const F=%s;
function flowDlg(){const g=j=>document.querySelector('[data-k="e13_'+j+'"]').value.trim()||"…";
 const L=F.map(([w,t])=>[w==="a"?"A":"B",t.replace("{i1}",g(1)).replace("{i2}",g(2)).replace("{i3}",g(3)).replace("{i4}",g(4))]);
 $("my13").innerHTML=L.map(([w,t])=>"<p><b>"+w+":</b> "+t+"</p>").join("")+'<button class="say big" id="p13">▶ Listen</button>';$("my13").classList.add("show");$("p13").onclick=e=>{e.stopPropagation();playDlg(L)}}
""" % (json.dumps(D1), json.dumps(list(pu)), json.dumps(F))
    sections = [("1", s1), ("2", s2), ("3", s3), ("4", s4), ("5", s5), ("6", s6), ("7", s7), ("8", s8), ("9", s9), ("10", s10), ("11", s11), ("12", s12), ("13", s13)]
    vocab = [("Plans for the week", words3 + ["business trip", "gas bill", "a doctor's appointment", "give someone a lift", "I don't mind"]),
             ("Grammar: going to", ["I'm going to …", "She's not going to …", "Are you going to …?", "What are you going to do?"]),
             ("Making suggestions", ["How about …?", "Do you want to meet somewhere?", "What time?", "Is six OK?", "Perfect! See you later."])]
    return page("8A", "What are your plans?", "Lesson", ["discuss plans", "discuss things people are planning to do this week",
                "practise listening to three conversations about plans", "make suggestions"], "oa1-8a-lesson", CODE, sections, K, vocab, xjs)

# =====================================================================
# 8B For and against (p.78–79)
# =====================================================================
ART = """<div class="art"><h3>WHAT DO YOU THINK?</h3><div class="lead">Our town is changing fast, and we always want to know what you think. We asked six local people about three big new plans.</div><div class="cols">
<div><div class="ph"><b>1</b>The local government wants to {h1}</div>
<p><span class="for">FOR</span>Great idea! It's going to help local companies, and more people are going to come and work here. At the moment, I fly to the capital and then take a train home. It takes hours! <span class="by">– Jamila</span></p>
<p><span class="ag">AGAINST</span>My flat isn't near it, but I still don't want lots of planes here. They're going to be very noisy and bad for the air. And they want to build it on green fields outside the city. <span class="by">– Cass</span></p></div>
<div><div class="ph"><b>2</b>The government is planning to {h2}</div>
<p><span class="for">FOR</span>Good. The government spends too much money. I work hard for my money and I don't want to pay more tax. Something needs to change. <span class="by">– Gavin</span></p>
<p><span class="ag">AGAINST</span>This is a bad plan. Lots of doctors, nurses and teachers are going to leave their jobs. Some people can pay for a private doctor or extra lessons, but most families can't. <span class="by">– Selina</span></p></div>
<div><div class="ph"><b>3</b>Our government wants to {h3}</div>
<p><span class="for">FOR</span>Fantastic! Lots of fans are going to come here and spend money in our cafés and hotels. They're going to see our country too. And I love football – I hope the tickets aren't going to be expensive! <span class="by">– Gloria</span></p>
<p><span class="ag">AGAINST</span>It isn't a good use of money. Sport isn't the most important thing in life. How about a free laptop or free English lessons for every student? That's a better way to spend the money. <span class="by">– Elijah</span></p></div>
</div><p class="hint" style="margin:6px 0 0">Text written for this course (A1) in the style of the coursebook page.</p></div>"""

def lesson_8b():
    K = {}
    ch = ["a new airport", "a bigger library", "better roads", "a new stadium", "a new metro line", "better water", "a new shopping centre", "a new museum", "better wi-fi",
          "a new hospital", "more street lights", "more schools"]
    s1 = sh("Speaking") + ins(1, "Work in groups. Discuss the questions.<br><span style='font-weight:400'>1 How important are these changes for your town or city?<br>2 Say if they are very important, quite important or not very important. Explain why.</span>",
                              "Наскільки важливі ці зміни для твого міста? Обери і поясни коротко чому.")
    for i, c in enumerate(ch, 1):
        s1 += '<div class="row"><span class="w">•</span><span style="display:inline-block;width:210px">%s %s</span>%s %s</div>' % (
            c, say(c), sel("b1_%d" % i, ["very important", "quite important", "not very important"], 175), inp("b1_%dw" % i, 330, "because …"))
    pairs = ["build / crowded", "economy / government", "education / digital", "environment / complete", "nothing / save", "use / employ"]
    S2 = [("A: If more people travel by train, it's better for the {w}.<br>B: Yes, maybe, but it's a big plan. It's going to take a long time to {w}.", ["environment", "complete"]),
          ("A: I don't want them to {w} new houses in the countryside.<br>B: But people need to live somewhere – and most cities are already very {w}.", ["build", "crowded"]),
          ("A: I think it's good for the {w} if people work longer.<br>B: Yes, and the {w} doesn't want to look after a lot of people who aren't working.", ["economy", "government"]),
          ("A: Libraries are important. They're good for {w}.<br>B: Yes, but we don't need them. Everything is {w} now – you can find everything online.", ["education", "digital"]),
          ("A: I'm glad they're going to build a new shopping centre. It's a good {w} of money.<br>B: Yes, I agree. I hope they're going to {w} a lot of local people.", ["use", "employ"]),
          ("A: {w} is going to change if they build these new stations.<br>B: Really? I think they're going to improve transport and {w} time for everyone.", ["Nothing", "save"])]
    s2 = sh("Vocabulary", "Discussing plans") + ins(2, "Complete the conversations with these pairs of words.", "Доповни діалоги парами слів з рамки.") + wbox(pairs)
    for i, (t, ans) in enumerate(S2, 1):
        parts = t.split("{w}"); h = parts[0]
        for j, a in enumerate(ans):
            k = "b2_%d%s" % (i, "ab"[j]); K[k] = [a]; h += inp(k, 130) + fb(k) + parts[j + 1]
        s2 += '<div class="row"><span class="w">%d</span>%s</div>' % (i, h)
    s2 += ctl("b2")
    s3 = (ins(3, "Work in pairs. How many words from Exercise 2 can you use to talk about the changes in Exercise 1?", "Скільки слів з вправи 2 ти можеш використати, щоб говорити про зміни з вправи 1? Напиши 4–6 речень.")
          + ex(["A new airport is going to be bad for the environment.", "A new stadium is (not) a good use of money."]) + ta("b3", "A new metro line is going to save time…", 140))
    s4 = ins(4, "Work in groups. Discuss the questions.", "Обговоримо на уроці. Напиши коротко свої думки.")
    for i, q in enumerate(["Are they building anything in your city or area at the moment? What? Where? Is it a good idea?", "Can you think of something that was a good use of public money?",
                           "Can you think of something that took a very long time to complete?", "Can you think of something that was good for the environment?",
                           "What's the most crowded part of your town / city?", "Can you think of three things that save people time?"], 1):
        s4 += '<div class="row"><span class="w">%d</span>%s<br>%s</div>' % (i, q, ta("b4_%d" % i, "", 44))
    art5 = ART.replace("{h1}", inp("b5_1", 200, "…")).replace("{h2}", inp("b5_2", 200, "…")).replace("{h3}", inp("b5_3", 200, "…"))
    s5 = (sh("Reading") + ins(5, "Read the opinions about the local government's plans. What do you think the plans are? Complete the headings (1–3) with your ideas.",
                              "Прочитай думки людей. Які це плани? Допиши заголовки 1–3 своїми словами.") + art5
          + audio_slot("8b-reading.mp3", "Audio: the coursebook text, p.79 (book version – read along in your book)")
          + model("m5", "1 … build a new airport. · 2 … cut spending / spend less money. · 3 … build a sports stadium.", "Show possible headings"))
    art = ART.replace("{h1}", "…").replace("{h2}", "…").replace("{h3}", "…")
    artd = '<details class="ad" style="margin:8px 0"><summary style="cursor:pointer;color:var(--blue);font-weight:600">📄 Show the text again</summary>%s</details>' % art
    s6 = (ins(6, "Work in pairs. Compare your ideas for Exercise 5. Who has the best heading for each plan?", "Порівняй свої заголовки з ідеями вчительки. Чий заголовок найкращий?")
          + ta("b6", "My best heading is … because …", 70))
    names = ["Jamila", "Cass", "Gavin", "Selina", "Gloria", "Elijah"]
    Q7 = [("Who would like more tourists?", "Gloria|Jamila"), ("Who would like to improve education?", "Elijah"), ("Who wants to save time?", "Jamila"),
          ("Who wants to save money?", "Gavin"), ("Who likes sport?", "Gloria"), ("Who is worried about the environment?", "Cass")]
    s7 = ins(7, "Read again. Answer the questions.", "Прочитай ще раз. Хто це?") + artd
    for i, (q, a) in enumerate(Q7, 1):
        k = "b7_%d" % i; K[k] = a.split("|")
        s7 += '<div class="row"><span class="w">%d</span><span style="display:inline-block;width:380px">%s</span>%s%s</div>' % (i, q, sel(k, names, 130), fb(k))
    s7 += ctl("b7")
    s8 = ins(8, "Work in pairs. Which opinions do you agree with? Which do you disagree with? Why?", "З якими думками ти згодна / не згодна? Чому?") + artd
    for n in names:
        s8 += '<div class="row"><span style="display:inline-block;width:90px;font-weight:600">%s</span>%s %s</div>' % (n, sel("b8_%s" % n.lower(), ["I agree", "I disagree", "I'm not sure"], 140), inp("b8_%sw" % n.lower(), 420, "because …"))
    P9 = ["The government is planning to build new high-speed train lines.", "The government wants to stop people building in the countryside or next to the sea.",
          "The government is going to change the age when people can stop working from 65 to 68.", "The local government is going to close all the libraries and put digital books online for free.",
          "The local government wants to build a shopping centre in your area with 100 shops and a car park."]
    s9 = sh("Speaking") + ins(9, "Decide which of these plans and ideas you think are good and which you think are bad. Write one reason why for each.", "Які плани добрі, а які погані? Напиши одну причину для кожного.")
    for i, p in enumerate(P9, 1):
        s9 += '<div class="row"><span class="w">%d</span>%s<br>%s %s</div>' % (i, p, sel("b9_%d" % i, ["good 👍", "bad 👎"], 110), inp("b9_%dw" % i, 520, "It's going to …"))
    s10 = (ins(10, "Ⓜ Work in groups. Discuss your opinions about the plans.", "Обговоримо на уроці. Підготуй, що скажеш.")
           + ex(["A: I think building new high-speed train lines is good. There are going to be more jobs.", "B: I agree – and it's going to save everyone time.", "C: I think it's a bad idea. It's going to be bad for the environment."])
           + ta("b10", "I think … is a good / bad idea. It's going to …", 120) + SELF)
    sections = [("1", s1), ("2", s2), ("3", s3), ("4", s4), ("5", s5), ("6", s6), ("7", s7), ("8", s8), ("9", s9), ("10", s10)]
    vocab = [("Changes in a town", ch),
             ("Discussing plans", ["build", "crowded", "economy", "government", "education", "digital", "environment", "complete", "nothing", "save time", "a good use of money", "employ"]),
             ("Agreeing / disagreeing", ["I think it's a good idea.", "I don't think it's a good idea.", "I agree.", "It's going to be bad for …", "It's going to help …"])]
    return page("8B", "For and against", "Lesson", ["say how you feel about government plans", "talk about changes your town / city needs",
                "look at ways of agreeing / disagreeing with plans", "read a local website discussion"], "oa1-8b-lesson", CODE, sections, K, vocab)

# =====================================================================
# 8C Hopes and dreams (p.80–81)
# =====================================================================
def lesson_8c():
    K = {}
    P = [("a", "🚗📸", "A man in a car. Lots of photographers are taking his photo."), ("b", "🎨💻", "A person is drawing pictures on a computer and a tablet."),
         ("c", "🌱🧤", "A person is working in a garden with plants and flowers."), ("d", "🥋", "Two people in white and blue clothes are doing a fighting sport.")]
    cards = '<div class="cards">' + "".join('<div class="pc"><span class="pl">%s</span><div class="pe">%s</div><p>%s</p>%s</div>' % (l, e, d, inp("c1_%s" % l, 200, "He / She wants to …")) for l, e, d in P) + "</div>"
    s1 = (sh("Listening") + ins(1, "You're going to hear four people talking about things they want to do. The photos show what each person is thinking. Work in pairs. What do you think each person wants to do?",
                                "Подивись на фото (у книзі, с.80). Що, на твою думку, хоче робити кожна людина?") + cards)
    s2 = ins(2, "▶ Listen and match the speakers (1–4) with the photos (a–d). Then work in pairs. Compare your ideas.", "Послухай і з’єднай мовців 1–4 з фото a–d.") + audio_slot("8c-ex02-04.mp3", "Four people")
    s2 += "".join('<div class="row">Speaker %d → %s%s</div>' % (i, sel("c2_%d" % i, ["a", "b", "c", "d"], 70), fb("c2_%d" % i)) for i in range(1, 5)) + ctl("c2")
    K.update({"c2_1": ["d"], "c2_2": ["b"], "c2_3": ["c"], "c2_4": ["a"]})
    s3 = (ins(3, "Ⓕⓢ ▶ In fast speech, the word <i>to</i> often just sounds like /tə/. Listen to eight phrases. Which include <i>to</i>?",
              "У швидкому мовленні <i>to</i> звучить як /tə/. Послухай 8 фраз. У яких є <i>to</i>?") + audio_slot("8c-ex03.mp3", "Eight phrases")
          + "".join('<div class="row">Phrase %d → %s%s</div>' % (i, sel("c3_%d" % i, ["with to", "without to"], 130), fb("c3_%d" % i)) for i in range(1, 9)) + ctl("c3")
          + '<p class="hint">Practice: %s %s %s</p>' % (say("I want to go."), say("I'd like to learn."), say("I'm going to start.")))
    K.update({"c3_%d" % i: ["with to" if i % 2 == 0 else "without to"] for i in range(1, 9)})
    T4 = [("Conversation 1", ["The man is from Manchester.", "He already does Brazilian jiu-jitsu."]), ("Conversation 2", ["The woman is planning to leave her job this year.", "She wants to have children before starting a business."]),
          ("Conversation 3", ["The woman thinks not working is going to be good.", "She wants to grow flowers."]), ("Conversation 4", ["The man wants to be rich.", "He wants to drive a big expensive car."])]
    s4 = ins(4, "▶ Listen again. Are the statements true (T) or false (F)?", "Послухай ще раз. Правда (T) чи неправда (F)?") + audio_slot("8c-ex02-04.mp3", "Four people")
    n = 0
    for c, sts in T4:
        s4 += "<p style='font-weight:700;margin:12px 0 2px'>%s</p>" % c
        for t in sts:
            n += 1; k = "c4_%d" % n; K[k] = ["FTFFTFTF"[n - 1]]
            s4 += '<div class="row"><span class="w">%d</span><span style="display:inline-block;width:470px">%s</span>%s%s</div>' % (n, t, sel(k, ["T", "F"], 60), fb(k))
    s4 += ctl("c4")
    s5 = (ins(5, "Work in groups. Would you like to do any of the things the people talk about? Why? / Why not?", "Ти б хотіла робити щось із цього? Чому так / ні?")
          + ex(["A: I wouldn't like to do that. It looks difficult.", "B: I'd like to be famous and have lots of money."]) + ta("c5", "I'd like to … / I wouldn't like to …", 100))
    S6 = [("I {w} a golf club last year.", "joined", "приєднався, вступив"), ("I travelled across Indonesia on a {w}.", "motorbike", "мотоцикл"),
          ("I started going to the {w}.", "opera", "опера"), ("I was the {w} of the school play.", "star", "зірка, головна роль"),
          ("I was {w} until I was 32.", "single", "неодружений, без пари"), ("I got my {w} when I was 16.", "driving licence", "водійські права"),
          ("I want to go in a {w}.", "helicopter", "гелікоптер"), ("I just want to have a {w} life.", "normal", "звичайний"),
          ("I want to be famous {w} in the world.", "everywhere", "всюди"), ("I'm going to change the colour of my hair. I want it {w}.", "blonde", "світле (блонд)"),
          ("I'm going to make my own {w}.", "album", "музичний альбом"), ("I'm going to start my own YouTube {w}.", "channel", "канал")]
    ua_opts = sorted(x[2] for x in S6)
    s6 = sh("Vocabulary", "In my life") + ins(6, "Work in pairs. Check you understand the words in bold. Use a dictionary if you need to.", "Перевір, чи розумієш слова жирним: обери переклад.")
    for i, (t, w, ua) in enumerate(S6, 1):
        k = "c6_%d" % i; K[k] = [ua]
        s6 += '<div class="row"><span class="w">%d</span><span style="display:inline-block;width:500px">%s %s</span>%s%s</div>' % (i, t.replace("{w}", "<b>%s</b>" % w), say(t.replace("{w}", w)), sel(k, ua_opts, 220), fb(k))
    s6 += ctl("c6")
    s7 = ins(7, "Work with a new partner. Which things from Exercise 6 do you think are good and which aren't? Why?", "Що з вправи 6 добре, а що ні? Чому?")
    for i, (t, w, _) in enumerate(S6, 1):
        s7 += '<div class="row"><span class="w">%d</span><span style="display:inline-block;width:150px"><b>%s</b></span>%s %s</div>' % (i, w, sel("c7_%d" % i, ["good 👍", "not good 👎", "not sure"], 130), inp("c7_%dw" % i, 360, "because …"))
    s8 = (ins(8, "With your partner, use words from Exercise 6 to talk about your life up to now and your plans for the future.", "Використай слова з вправи 6, щоб розповісти про своє життя і плани.")
          + ex(["I went to the opera once – and I don't want to go again. It's not for me!"]) + ta("c8", "I got my driving licence when I was … / I'm going to …", 140))
    gb = ('<div class="gbox"><div class="gh">Would like to</div><p>We use <i>would like to</i> + verb to talk about things we want to do – or hope to do. We often write (and say) <i>would</i> as <i>\'d</i>.</p>'
          '<p><i>I<b>\'d like to go</b> to Japan one day. I\'m sure it\'s really interesting.</i> %s</p><p><i>He<b>\'d</b> really <b>like to learn</b> Spanish.</i> %s</p>'
          '<p>We make negatives using <i>wouldn\'t like to</i> + verb.</p><p><i>I <b>wouldn\'t like to do</b> his job! It\'s hard!</i> %s</p>'
          '<p>We make questions using <i>Would</i> + person + <i>like to</i> + verb.</p><p><i><b>Would</b> you <b>like to go</b> in a helicopter?</i> %s</p>'
          '<p class="hint">🇺🇦 would like to = хотів би / хотіла б (мрія, бажання). I\'d = I would.</p></div>') % (
        say("I'd like to go to Japan one day. I'm sure it's really interesting."), say("He'd really like to learn Spanish."), say("I wouldn't like to do his job! It's hard!"), say("Would you like to go in a helicopter?"))
    S9 = [("I / really / spend a year in India.", "I'd really like to spend a year in India."), ("I / really / meet him sometime. I loved his last album!", "I'd really like to meet him sometime."),
          ("My brother / learn how to cook.", "My brother would like to learn how to cook."), ("She / change jobs sometime soon.", "She'd like to change jobs sometime soon."),
          ("I / not / be famous!", "I wouldn't like to be famous!"), ("It's a nice apartment, but I / not / live in that area.", "It's a nice apartment, but I wouldn't like to live in that area."),
          ("you / join a band?", "Would you like to join a band?"), ("you / come shopping with me tomorrow?", "Would you like to come shopping with me tomorrow?")]
    s9 = sh("Grammar") + gb + ins(9, "Use the notes to make sentences with the correct form of <i>would / wouldn't like (to)</i>.", "Склади речення з would / wouldn't like to.")
    for i, (t, a) in enumerate(S9, 1):
        k = "c9_%d" % i; acc = variants(a)
        if "his last album" in t: acc += variants(a + " I loved his last album!")
        if a.startswith("My brother would"): acc += variants(a.replace("My brother would", "My brother'd"))
        K[k] = acc
        s9 += '<div class="row"><span class="w">%d</span>%s<br>%s%s</div>' % (i, t, inp(k, 560), fb(k))
    s9 += ctl("c9") + '<p class="hint">G — See Grammar reference 8C.</p>'
    I10 = ["buy my own house / flat", "make a lot of money", "get fitter", "move to a different country", "speak really good English", "buy a motorbike", "stop working at 50", "write a book", "eat less meat", "learn another language"]
    s10 = (ins(10, "Work in pairs. Discuss which of these things you'd like to do sometime in the future. Explain your decisions.", "Що з цього ти хотіла б зробити в майбутньому? Поясни.")
           + ex(["I'd really like to buy my own house one day.", "I'm OK just renting. I think it's easier."]))
    for i, t in enumerate(I10, 1):
        s10 += '<div class="row"><span class="w">%d</span><span style="display:inline-block;width:250px">%s</span>%s %s</div>' % (i, t, sel("c10_%d" % i, ["I'd like to", "I wouldn't like to", "I'm not sure"], 160), inp("c10_%dw" % i, 330, "because …"))
    s11 = ins(11, "Work in groups. Tell each other about:", "Розкажи про:")
    for i, t in enumerate(["a place you'd really like to visit.", "a person you'd really like to meet.", "something you'd really like to do.", "something you'd like to learn.", "something you'd like to stop doing."], 1):
        s11 += '<div class="row"><span class="w">%d</span><span style="display:inline-block;width:320px">%s</span>%s</div>' % (i, t, inp("c11_%d" % i, 400, "I'd really like to …"))
    s12 = (sh("Speaking task") + ins(12, "Work in pairs. You are going to think of different ways to improve one of these places. Choose the place you want to talk about. Discuss what you'd like to change – and why.",
                                     "Обери місце і напиши, що б ти хотіла змінити і чому.")
           + wbox(["a  your classroom", "b  your school", "c  your area", "d  your country"])
           + '<p>My place: %s</p>' % sel("c12_place", ["a – my classroom", "b – my school / my office", "c – my area", "d – my country"], 220)
           + ex(["I'd like to have more windows in this classroom. It's very dark.", "I'd like to start school a bit later. We start very early.", "We need more jobs in this area – more jobs that pay well.",
                 "We need to spend more money on schools and hospitals in this country."]) + ta("c12", "I'd like to … because … / We need …", 140))
    s13 = (ins(13, "Ⓜ Tell the rest of the class about your ideas. As a class, decide what the best plan for each place is.", "Розкажи вчительці свої ідеї. Разом виберемо найкращий план.")
           + ta("c13", "Our best plan is …", 70)
           + '<div class="sh" style="margin-top:26px">■ My outcomes</div>' + ins("", "Work in pairs. Discuss the questions.", "Підсумок юніту 8: дай відповіді.")
           + "".join('<div class="row"><span class="w">%d</span>%s<br>%s</div>' % (i, q, ta("c13_mo%d" % i, "", 44)) for i, q in enumerate(
               ["Which of the texts are you going to read / listen to again?", "What plans and opinions can you now share in English?",
                "How many words from the vocabulary exercises can you remember?", "What can you do to remember more vocabulary?"], 1)) + SELF)
    sections = [("1", s1), ("2", s2), ("3", s3), ("4", s4), ("5", s5), ("6", s6), ("7", s7), ("8", s8), ("9", s9), ("10", s10), ("11", s11), ("12", s12), ("13", s13)]
    vocab = [("In my life", [w for _, w, _ in S6]), ("Grammar: would like to", ["I'd like to …", "I'd really like to …", "I wouldn't like to …", "Would you like to …?"]),
             ("Future plans", ["buy my own flat", "make a lot of money", "get fitter", "move to a different country", "stop working", "write a book", "learn another language"])]
    return page("8C", "Hopes and dreams", "Lesson", ["decide how to improve places you know", "practise listening to people talking about things they want to do",
                "talk about life events and plans"], "oa1-8c-lesson", CODE, sections, K, vocab)

write("lessons/8-0/all/lesson.html", opener())
write("lessons/8a/all/lesson.html", lesson_8a())
write("lessons/8b/all/lesson.html", lesson_8b())
write("lessons/8c/all/lesson.html", lesson_8c())
