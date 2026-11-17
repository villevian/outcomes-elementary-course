"""Outcomes A1 — shared page shell (lesson / homework / extra).
Same sync logic as Business Partner (Supabase project "Business Partner": save_hw / get_my_hw),
Outcomes look: yellow lesson block, blue task numbers, light background, one task per screen.

page(code_label, title, tag, aims, lesson_key, student_code, sections, key, vocab)
  sections: list of (nav_label, html)
  key: {data-k: [accepted answers]}; prefix before the last "_" = one exercise (chkSet("e3") checks all e3_*)
"""
import json, re, html as H
try:
    from dict_unit8 import DICT
except Exception:
    DICT = {}

def esc(s): return H.escape(s, quote=True)

def page(num, title, tag, aims, lesson_key, code, sections, key, vocab=None, extra_js=""):
    nav = "".join('<button data-s="s%d"%s>%s</button>' % (i + 1, ' class="on"' if i == 0 else "", lab) for i, (lab, _) in enumerate(sections))
    body = "".join('<section id="s%d" class="sec%s">%s</section>' % (i + 1, " on" if i == 0 else "", h) for i, (_, h) in enumerate(sections))
    voc = ""
    if vocab:
        voc = ('<details class="voc" open><summary>📖 Vocabulary of this lesson — натисни на слово: переклад, транскрипція, колокації, приклади</summary><div class="vgs">%s</div></details>'
               % "".join('<div class="vg"><h4>%s</h4>%s</div>' % (t, "".join('<span data-t="%s" class="sw">%s</span>' % (esc(w), w) for w in ws)) for t, ws in vocab))
    wd = {}
    for _, ws in (vocab or []):
        for w in ws:
            if w in DICT:
                ua, ipa, col, exs = DICT[w]
                wd[w] = {"ua": ua, "ipa": ipa, "col": col, "ex": [H.escape(e).replace("**", "\u0001") for e in exs]}
    wdjs = json.dumps(wd, ensure_ascii=False).replace("\\u0001", "**")
    aims_html = "".join("<li>%s</li>" % a for a in aims)
    out = TPL
    for a, b in (("__NUM__", num), ("__TITLE__", title), ("__TAG__", tag), ("__AIMS__", aims_html), ("__VOC__", voc), ("__NAV__", nav),
                 ("__BODY__", body), ("__LESSON__", lesson_key), ("__CODE__", code), ("__KEY__", json.dumps(key, ensure_ascii=False)), ("__XJS__", extra_js), ("__WD__", wdjs)):
        out = out.replace(a, b)
    return out

# ---------- small builders ----------
def ins(n, en, ua=""):
    return '<div class="ins"><b class="x">%s</b>%s</div>%s' % (n, en, '<div class="ua">🇺🇦 %s</div>' % ua if ua else "")
def sh(t, sub=""): return '<div class="sh">%s%s</div>' % (t, ' <span>%s</span>' % sub if sub else "")
def fb(k): return '<span class="fb" id="fb_%s"><span class="h"></span></span>' % k
def inp(k, w=150, ph=""): return '<input class="g" data-k="%s" style="width:%dpx" placeholder="%s" autocomplete="off">' % (k, w, esc(ph))
def sel(k, opts, w=None): return '<select class="g" data-k="%s"%s><option value="">—</option>%s</select>' % (k, ' style="width:%dpx"' % w if w else "", "".join("<option>%s</option>" % o for o in opts))
def ta(k, ph="", h=None): return '<textarea class="g" data-k="%s" placeholder="%s"%s></textarea>' % (k, esc(ph), ' style="min-height:%dpx"' % h if h else "")
def ctl(p, extra=""): return '<div class="ctl"><button class="btn" onclick="chkSet(\'%s\')">Check</button>%s<span class="res" id="r_%s"></span></div>' % (p, extra, p)
def say(text, label="🔊"): return '<button class="say" data-t="%s" title="Listen">%s</button>' % (esc(text), label)
def dlg_btn(lines, label="▶ Listen"):
    return '<button class="say big" data-d="%s">%s</button>' % (esc(json.dumps(lines, ensure_ascii=False)), label)
def model(id_, txt, label="Show example answers"):
    return '<button class="btn l" onclick="model(\'%s\')">%s</button><div class="model" id="%s">%s</div>' % (id_, label, id_, txt)
def wbox(words): return '<div class="wbox">%s</div>' % "".join('<span>%s</span>' % w for w in words)
def ex(lines): return '<div class="exm">%s</div>' % "<br>".join(lines)
def audio_slot(src, label="Listen"):
    return ('<div class="aud">🎧 <b>%s</b><audio controls preload="none" src="../audio/%s"></audio></div>' % (label, src))
SELF = ('<div class="selfa"><div class="l">My outcomes</div><div class="r">How well can you do this now? 0 = I need more practice, 5 = I can do it well.'
        '<div class="score" id="score">' + "".join('<button data-v="%d">%d</button>' % (i, i) for i in range(6)) + '</div>'
        '<textarea class="g" data-k="q" style="min-height:60px;margin-top:8px" placeholder="Questions for your teacher (optional) / Питання до вчительки"></textarea></div></div>')

TPL = r"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__NUM__ __TITLE__ — __TAG__</title>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
<style>
:root{--y:#ffd200;--y2:#fff6c7;--ink:#1d1d1b;--blue:#1f5fae;--sky:#1d8bd0;--teal:#1b7f86;--tbg:#e3f0ee;--pur:#7a2a8c;--grey:#6d6e70;--line:#e2e3e4}
*{box-sizing:border-box}body{margin:0;font-family:"Source Sans 3",system-ui,sans-serif;color:var(--ink);background:#fff;font-size:17.5px;line-height:1.5}
header{display:flex;align-items:flex-end;gap:18px;padding:18px 24px 0;max-width:1060px;margin:0 auto}
header .n{background:var(--y);font:700 30px "Barlow Condensed","Arial Narrow",sans-serif;padding:6px 14px;line-height:1}
header h1{margin:0;font:700 46px/1 "Barlow Condensed","Arial Narrow",sans-serif}
header .tag{margin-left:auto;font:600 13px "Source Sans 3",sans-serif;background:var(--ink);color:#fff;padding:5px 10px;border-radius:3px;margin-bottom:6px}
.aims{max-width:1060px;margin:10px auto 0;padding:0 24px;display:flex;gap:16px;align-items:flex-start}
.aims .bar{flex:1;height:6px;background:var(--y);margin-top:12px}
.aims .box{border:2px solid var(--y);padding:6px 14px;font-size:14px;min-width:330px}.aims .box b{display:block;font-size:13px;letter-spacing:.3px}.aims ul{margin:2px 0 0;padding-left:18px}
.wrap{max-width:1060px;margin:0 auto;padding:0 24px}
details.voc{margin:14px 0 0;border:2px solid var(--y);background:#fffdf3}details.voc summary{cursor:pointer;padding:8px 16px;font-weight:600}
.vgs{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px;padding:4px 16px 14px}.vg h4{margin:4px 0 6px;color:var(--sky);font-weight:700;font-size:14px;text-transform:uppercase}
.vg span{display:inline-block;background:var(--y2);border-radius:12px;padding:2px 10px;margin:2px;font-size:15px;cursor:pointer}.vg span:hover{background:var(--y)}
.top{display:flex;justify-content:space-between;align-items:center;margin-top:12px;flex-wrap:wrap;gap:8px}.top a{color:var(--blue);text-decoration:none;font-weight:600;font-size:15px}
.stb{background:#f3f4f5;padding:6px 14px;border-radius:6px;font-size:14.5px}.st.ok{color:#2e7d4f}.st.err{color:#c0392b}
.tcom{display:none;margin-top:10px;background:var(--y2);border-left:5px solid var(--y);padding:10px 14px;font-size:15px;white-space:pre-wrap}.tcom b{display:block}
nav{margin:14px 0 0;display:flex;flex-wrap:wrap;gap:8px}nav button{min-width:44px;height:40px;border:2px solid var(--ink);background:#fff;color:var(--ink);border-radius:20px;font:600 16px "Source Sans 3",sans-serif;cursor:pointer;padding:0 12px}nav button.on{background:var(--y);border-color:var(--y)}
main{padding:4px 0 30px}.sec{display:none}.sec.on{display:block}
.sh{font:700 26px "Barlow Condensed","Arial Narrow",sans-serif;letter-spacing:.4px;text-transform:uppercase;margin:22px 0 6px}.sh span{color:var(--sky);text-transform:none;font-weight:600;margin-left:6px}
.ins{font-weight:700;margin:14px 0 2px;font-size:18px}.ins b.x{color:var(--blue);font-size:22px;margin-right:10px}
.ua{color:var(--grey);font-size:15px;margin:0 0 10px 32px}
.row{padding:7px 0;border-bottom:1px solid #f0f0f2}.row .w{display:inline-block;min-width:30px;font-weight:600;color:var(--grey)}
input.g,select.g{font:inherit;font-size:16.5px;border:1.5px solid #c8c9cb;border-radius:4px;padding:4px 7px;background:#fff}
textarea.g{width:100%;min-height:80px;font:inherit;font-size:16.5px;border:1.5px solid #c8c9cb;border-radius:6px;padding:8px 10px}
.right{border-color:#3a9d5d!important;background:#eaf7ee!important}.wrong{border-color:#d9534f!important;background:#fdecec!important}
.fb{display:none;font-size:14.5px;margin-left:8px}.fb.show{display:inline}.fb.ok{color:#2e7d4f}.fb.no{color:#b03a2e}
.ctl{display:flex;gap:10px;align-items:center;margin-top:14px;flex-wrap:wrap}.btn{background:var(--ink);color:#fff;border:0;border-radius:4px;padding:8px 18px;font:600 15px "Source Sans 3",sans-serif;cursor:pointer}.btn.l{background:#fff;color:var(--ink);border:1.5px solid #c8c9cb}.res{font-weight:600;color:var(--blue)}
.model{display:none;background:#f6f6f7;border-left:4px solid #8a8b8d;padding:8px 14px;margin-top:8px;font-size:16px}.model.show{display:block}
.wbox{background:#dcebf6;padding:8px 14px;display:flex;flex-wrap:wrap;gap:6px 18px;margin:6px 0 10px;font-size:17px}
.dlg{background:#fafafa;border-left:5px solid var(--y);padding:8px 16px;margin:8px 0}.dlg p{margin:3px 0}.dlg b{display:inline-block;width:26px}.pu{color:var(--pur);font-weight:700}
.gbox{background:var(--tbg);padding:12px 18px;margin:12px 0}.gbox .gh{color:var(--teal);font-weight:700;font-style:italic;font-size:21px;margin-bottom:4px}.gbox p{margin:5px 0}.gbox i{color:#333}
.dcbox{border-left:5px solid var(--y);padding:6px 16px;margin:10px 0}.dcbox .gh{color:var(--sky);font-weight:700;font-size:20px}
.exm{color:#2a7ab8;font-style:italic;margin:8px 0}
.say{border:1.5px solid #c8c9cb;background:#fff;border-radius:14px;cursor:pointer;font-size:14px;padding:1px 8px;margin-left:6px}.say.big{font:600 15px "Source Sans 3",sans-serif;padding:6px 14px;border-color:var(--ink);margin:6px 0}
.aud{background:#eef4fb;border:1.5px solid #9cbfe3;padding:8px 14px;border-radius:6px;font-size:15px;margin:8px 0;display:flex;align-items:center;gap:12px;flex-wrap:wrap}.aud audio{flex:1;min-width:260px;height:40px}
.cards{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.pc{border:1px solid var(--line);padding:10px;position:relative;background:#fbfbfb}.pc .pl{position:absolute;top:0;left:0;background:var(--ink);color:#fff;font-weight:700;padding:1px 8px}.pc .pe{font-size:46px;text-align:center}.pc p{font-size:14.5px;margin:4px 0 8px;min-height:44px}.pc input{width:100%}
.art{background:#f4efe9;padding:14px 20px}.art .lead{background:#e3ddd3;font-weight:700;text-align:center;padding:8px 14px;margin-bottom:12px}
.art .cols{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}.art .ph{font-size:18px;margin-bottom:8px}.art .ph b{background:#4a6a78;color:#fff;padding:0 7px;margin-right:6px}
.art p{font-size:15.5px;margin:6px 0 12px}.art .for{background:#2f7e86;color:#fff;font-weight:700;font-size:12.5px;padding:1px 6px;margin-right:6px}.art .ag{background:#b88b4a;color:#fff;font-weight:700;font-size:12.5px;padding:1px 6px;margin-right:6px}.art .by{font-style:italic;display:block}
.art h3{font:700 40px "Barlow Condensed","Arial Narrow",sans-serif;margin:0 0 6px;letter-spacing:.5px}
.flow{display:grid;grid-template-columns:1fr 60px 1fr;gap:4px 0;max-width:720px;margin:10px 0}.flow .a,.flow .b{background:#ece7f0;padding:6px 10px;font-style:italic}.flow .b{grid-column:3}.flow .a{grid-column:1}.flow .arr{grid-column:2;text-align:center;color:var(--pur);font-size:20px}
.flow input{width:150px;font-style:normal}
.selfa{display:flex;margin-top:18px;border:2px solid var(--y)}.selfa .l{background:var(--y);font-weight:700;padding:12px 16px}.selfa .r{flex:1;padding:10px 16px;font-size:15px}
.score button{width:42px;height:42px;border-radius:50%;border:2px solid #e1e2e3;background:#fff;font-size:16px;margin:6px 6px 0 0;cursor:pointer}.score button.on{border-color:var(--y);background:var(--y2)}
.done{display:none;margin-top:10px;background:#eaf7ee;color:#1e6b3d;padding:10px 14px;border-radius:6px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:6px 30px}.hint{font-size:14.5px;color:var(--grey)}
.out{display:none;background:#fffdf3;border:1.5px solid var(--y);padding:10px 16px;margin-top:10px}.out.show{display:block}
.wcov{display:none;position:fixed;inset:0;background:rgba(255,255,255,.75);z-index:50;align-items:center;justify-content:center;padding:16px}.wcov.show{display:flex}
.wc{background:#fff;border:2px solid var(--y);box-shadow:0 10px 30px rgba(0,0,0,.15);max-width:520px;width:100%;max-height:88vh;overflow:auto;padding:18px 22px;position:relative}
.wc .x{position:absolute;top:8px;right:10px;border:0;background:none;font-size:26px;cursor:pointer;color:#888}.wc h3{margin:0;font:700 30px "Barlow Condensed","Arial Narrow",sans-serif;display:flex;align-items:center;gap:8px;padding-right:30px}
.wc .ipa{color:var(--grey);font-size:16px;margin:2px 0}.wc .tr{background:var(--y2);padding:6px 12px;margin:10px 0;font-weight:600}.wc h4{margin:14px 0 4px;color:var(--sky);font-size:13px;text-transform:uppercase;letter-spacing:.4px}
.wc ul{margin:0;padding-left:20px}.wc li{margin:4px 0}.wc li b{color:var(--pur)}
footer{max-width:1060px;margin:0 auto;padding:0 24px 30px;font-size:12.5px;color:#77787b}
@media(max-width:800px){.cards,.two,.art .cols{grid-template-columns:1fr 1fr}.aims{flex-direction:column}.aims .box{min-width:0}header h1{font-size:36px}}
@media(max-width:560px){.cards,.two,.art .cols{grid-template-columns:1fr}}
</style></head><body>
<header><div class="n">__NUM__</div><h1>__TITLE__</h1><div class="tag">__TAG__</div></header>
<div class="aims"><div class="bar"></div><div class="box"><b>IN THIS LESSON, YOU:</b><ul>__AIMS__</ul></div></div>
<div class="wrap">__VOC__
<div class="top"><a href="../../../index.html">← Contents</a><div class="stb"><span class="st" id="st">Loading…</span></div></div>
<div class="tcom" id="tcom"><b>💬 Teacher’s comment</b><div id="tcomt"></div></div>
<nav>__NAV__</nav><main>__BODY__
<div class="ctl" style="margin-top:28px"><button class="btn" id="submit">Send to my teacher</button><span class="st" id="st2"></span></div>
<div class="done" id="done">✓ Sent to your teacher. You can still change your answers — they save automatically.</div></main></div>
<div class="wcov" id="wcov"><div class="wc"><button class="x" onclick="closeW()">×</button><div id="wcb"></div></div></div>
<footer>Outcomes A1 · interactive version for private lessons · Valentyna Hordiienko · Middle Learning Architect</footer>
<script>
const SB_URL="https://zuegojpfhgigsvyrnymt.supabase.co",SB_KEY="sb_publishable__Xn8xRhne9Hp2ckaXu6xCQ_MOe52bng";
const WD=__WD__;
const LESSON="__LESSON__";const STUDENT_CODE="__CODE__";const KEY=__KEY__;
const rpc=(f,b)=>fetch(SB_URL+"/rest/v1/rpc/"+f,{method:"POST",headers:{apikey:SB_KEY,"Content-Type":"application/json"},body:JSON.stringify(b)}).then(async r=>{const t=await r.text();if(!r.ok)throw new Error(t);return t?JSON.parse(t):null});
const $=id=>document.getElementById(id);let student="",timer=null,submitted=false,ready=false;
const norm=s=>(s||"").toLowerCase().replace(/[’`‘]/g,"'").replace(/\s+/g," ").replace(/[.!?]+$/,"").trim();
const okv=(k,v)=>KEY[k].some(x=>norm(x)===norm(v));
function collect(){const a={};document.querySelectorAll("input.g[data-k],select.g[data-k],textarea.g[data-k]").forEach(x=>a[x.dataset.k]=x.value);
 document.querySelectorAll("input[type=radio][data-k]:checked").forEach(x=>a[x.dataset.k]=x.value);const s=document.querySelector("#score .on");a.self=s?+s.dataset.v:null;return a}
function fill(a){document.querySelectorAll("input.g[data-k],select.g[data-k],textarea.g[data-k]").forEach(x=>{if(a[x.dataset.k]!=null)x.value=a[x.dataset.k]});
 document.querySelectorAll("input[type=radio][data-k]").forEach(x=>x.checked=a[x.dataset.k]===x.value);document.querySelectorAll("#score button").forEach(b=>b.classList.toggle("on",a.self!=null&&+b.dataset.v===a.self));if(window.afterFill)afterFill()}
function scores(){const a=collect(),r={};for(const k in KEY){const p=k.replace(/_[^_]+$/,"");r[p]=r[p]||[0,0];r[p][1]++;if(a[k]!=null&&okv(k,a[k]))r[p][0]++}const o={};for(const p in r)o[p]=r[p][0]+"/"+r[p][1];return o}
function status(t,c=""){$("st").textContent=t;$("st").className="st "+c}
function local(){try{localStorage.setItem("hw:"+LESSON+":"+(STUDENT_CODE||"preview"),JSON.stringify(collect()))}catch(e){}}
async function save(){if(!ready)return;local();if(!STUDENT_CODE){status("Template preview — answers stay on this device only.");return}status("Saving…");
 try{await rpc("save_hw",{p_code:STUDENT_CODE,p_lesson:LESSON,p_answers:collect(),p_score:scores(),p_submitted:submitted});status("Saved ✓ "+new Date().toLocaleTimeString().slice(0,5),"ok")}
 catch(e){status("Not saved online — check your internet. Your answers are kept on this device.","err")}}
function later(){clearTimeout(timer);timer=setTimeout(save,1200)}
async function start(){let a=null;if(STUDENT_CODE){try{const r=await rpc("get_my_hw",{p_code:STUDENT_CODE,p_lesson:LESSON});const d=r&&r[0];
 if(d){student=d.name;if(d.answers){a=d.answers;submitted=!!d.submitted;if(submitted)$("done").style.display="block"}if(d.teacher_comment){$("tcomt").textContent=d.teacher_comment;$("tcom").style.display="block"}}}catch(e){}}
 if(!a){try{a=JSON.parse(localStorage.getItem("hw:"+LESSON+":"+(STUDENT_CODE||"preview"))||"null")}catch(e){}}if(a)fill(a);ready=true;
 if(!STUDENT_CODE)status("Template preview — answers stay on this device only.");else status(student?(a?"Welcome back, "+student+"! Your answers are loaded.":"Hi, "+student+"! Your answers save automatically."):"Your answers save automatically.","ok")}
function fbk(k,ok,txt){const f=$("fb_"+k);if(!f)return;f.className="fb show "+(ok?"ok":"no");f.querySelector(".h").innerHTML=txt}
function chkSet(p){let n=0,t=0;for(const k in KEY){if(k.replace(/_[^_]+$/,"")!==p)continue;const el=document.querySelector(`.g[data-k="${k}"]`);if(!el)continue;t++;const ok=okv(k,el.value);if(ok)n++;
 el.classList.remove("right","wrong");el.classList.add(ok?"right":"wrong");fbk(k,ok,ok?"✓":"✗ <b>"+KEY[k][0]+"</b>")}$("r_"+p).textContent=n+" / "+t+(n===t?" ✓ Well done!":"");save()}
function model(id){$(id).classList.toggle("show")}
/* speech (browser voice) */
let VO=[];function loadV(){try{VO=speechSynthesis.getVoices().filter(v=>/^en[-_](GB|US)/i.test(v.lang))}catch(e){}}
if("speechSynthesis" in window){speechSynthesis.onvoiceschanged=loadV;loadV()}
function utt(t,i){const u=new SpeechSynthesisUtterance(t);u.lang="en-GB";u.rate=.88;if(VO.length)u.voice=VO[(i||0)%VO.length];if(i)u.pitch=.85;return u}
function say(t){if(!("speechSynthesis" in window))return;speechSynthesis.cancel();speechSynthesis.speak(utt(t,0))}
function playDlg(lines){if(!("speechSynthesis" in window))return;speechSynthesis.cancel();lines.forEach(([w,t])=>speechSynthesis.speak(utt(t,w==="A"?0:1)))}
const eh=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const sb=t=>'<button class="say" data-t="'+eh(t)+'">🔊</button>';
function openW(w){const d=WD[w];if(!d)return;const plain=x=>x.replace(/\*\*/g,"").replace(/&#x27;/g,"'").replace(/&amp;/g,"&").replace(/&quot;/g,'"');
 $("wcb").innerHTML="<h3>"+eh(w)+sb(w.replace("…","").replace("?",""))+"</h3><div class='ipa'>"+eh(d.ipa)+"</div><div class='tr'>🇺🇦 "+eh(d.ua)+"</div>"
 +"<h4>Collocations</h4><ul>"+d.col.map(c=>"<li>"+eh(c)+sb(c.replace("…",""))+"</li>").join("")+"</ul>"
 +"<h4>Examples</h4><ul>"+d.ex.map(x=>"<li>"+x.replace(/\*\*(.+?)\*\*/g,"<b>$1</b>")+sb(plain(x))+"</li>").join("")+"</ul>";$("wcov").classList.add("show")}
function closeW(){$("wcov").classList.remove("show")}
$("wcov").addEventListener("click",e=>{if(e.target.id==="wcov")closeW()});document.addEventListener("keydown",e=>{if(e.key==="Escape")closeW()});
document.addEventListener("click",e=>{const b=e.target.closest(".say,.vg span");if(!b)return;if(b.closest(".vg")&&WD[b.dataset.t]){openW(b.dataset.t);say(b.dataset.t.replace("…",""));return}
 if(b.dataset.d)playDlg(JSON.parse(b.dataset.d));else if(b.dataset.t)say(b.dataset.t)});
document.querySelectorAll("#score button").forEach(b=>b.onclick=()=>{document.querySelectorAll("#score button").forEach(x=>x.classList.remove("on"));b.classList.add("on");later()});
document.addEventListener("input",e=>{if(e.target.closest("main"))later()});document.addEventListener("change",e=>{if(e.target.closest("main"))later()});
document.querySelectorAll("nav button").forEach(b=>b.onclick=()=>{document.querySelectorAll("nav button,.sec").forEach(x=>x.classList.remove("on"));b.classList.add("on");$(b.dataset.s).classList.add("on");scrollTo(0,0)});
$("submit").onclick=async()=>{submitted=true;await save();$("done").style.display="block"};
__XJS__
start();
</script></body></html>"""
