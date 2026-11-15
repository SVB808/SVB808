"""Regenerate the profile's editable SVG assets with the Python standard library."""
from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'assets'
INK, MUTED, TEAL, BLUE, EDGE = '#edf4fc', '#a5b6cc', '#5eead4', '#86baff', '#263b54'

def text(x, y, value, size=20, fill=INK, weight=400, extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" {extra}>{escape(value)}</text>'

def svg(width, height, title, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title">'
            f'<title id="title">{escape(title)}</title>'
            '<defs><linearGradient id="bg" x2="1" y2="1">'
            '<stop stop-color="#101f33"/><stop offset="1" stop-color="#09131f"/>'
            '</linearGradient></defs>'
            f'<rect width="{width}" height="{height}" rx="18" fill="url(#bg)"/>'
            '<g font-family="Arial, Helvetica, sans-serif">'+body+'</g></svg>\n')

def write(name, content):
    path=A/name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)

def pill(x, y, width, label, color=TEAL):
    return (f'<rect x="{x}" y="{y}" width="{width}" height="30" rx="15" fill="#122a3a" stroke="{EDGE}"/>'
            +text(x+width/2, y+20, label, 12, color, 600, 'text-anchor="middle"'))

# Static text and motion limited to the abstract signal paths on the right.
hero = text(44, 49, 'SVB808  /  SOFTWARE ENGINEER', 15, MUTED, 600, 'letter-spacing="2.5"')
hero += text(40, 139, 'Shrutha V Bhat', 67, INK, 700, 'letter-spacing="-2"')
hero += text(44, 190, 'Backend systems. Applied AI.', 28, '#d8e7f6')
hero += text(44, 225, 'Java / Spring Boot · Cloud storage · Developer tools', 19, MUTED)
hero += pill(44, 270, 135, 'PREVIOUSLY DELL') + pill(191, 270, 142, 'BENGALURU, INDIA')
hero += pill(345, 270, 194, 'OPEN TO OPPORTUNITIES')
hero += '<g opacity="0.38" stroke="#31526c" fill="none"><path d="M800 0V350M880 0V350M960 0V350M1040 0V350M770 60H1120M770 140H1120M770 220H1120M770 300H1120"/></g>'
hero += '<g fill="none" stroke-linecap="round" stroke-width="2"><path d="M813 94H1020V175H844V259H1035" stroke="#34546d"/>'
hero += '<path class="signal" d="M813 94H1020V175H844V259H1035" stroke="#5eead4" stroke-dasharray="45 595"/></g>'
for x,y,label in [(813,94,'SOURCE'),(1020,175,'VERIFY'),(844,259,'SHIP')]:
    hero += f'<circle cx="{x}" cy="{y}" r="15" fill="#102738" stroke="#42657d"/><circle cx="{x}" cy="{y}" r="5" fill="{TEAL}"/>'
    hero += text(x+25 if x<1000 else x-25, y+6, label, 12, '#c2d4e8', 600,
                 'letter-spacing="1.8"'+(' text-anchor="end"' if x>=1000 else ''))
hero += text(1068, 320, 'BUILD / VERIFY / SHIP', 11, '#738ba4', 500, 'text-anchor="end" letter-spacing="2"')
static=svg(1120,350,'Shrutha V Bhat. Backend systems and applied AI. Previously Dell. Bengaluru, India.',hero)
motion='<style>.signal{animation:travel 14s linear infinite}@keyframes travel{to{stroke-dashoffset:-640}}@media(prefers-reduced-motion:reduce){.signal{animation:none;stroke-dasharray:none;opacity:.35}}</style>'
write('profile-banner.svg',static.replace('<defs>',motion+'<defs>',1))
write('profile-banner-static.svg',static.replace('stroke-dasharray="45 595"','opacity="0.35"'))
mobile_hero=text(25,34,'SVB808 / SOFTWARE ENGINEER',12,MUTED,600,'letter-spacing="1.5"')
mobile_hero+=text(23,102,'Shrutha V Bhat',43,INK,700,'letter-spacing="-1.5"')
mobile_hero+=text(25,146,'Backend systems. Applied AI.',23,'#d8e7f6')
mobile_hero+=text(25,180,'Java / Spring Boot · Cloud storage',16,MUTED)
mobile_hero+=pill(25,213,135,'PREVIOUSLY DELL')+pill(173,213,142,'BENGALURU, INDIA')
mobile_hero+=text(25,286,'OPEN TO OPPORTUNITIES',12,TEAL,600,'letter-spacing="1.4"')
mobile_hero+='<path d="M25 317H515" stroke="#34546d" stroke-width="2"/><path class="signal" d="M25 317H515" stroke="#5eead4" stroke-width="2" stroke-dasharray="45 595"/>'
mobile_static=svg(540,340,'Shrutha V Bhat. Backend systems and applied AI. Previously Dell. Bengaluru, India.',mobile_hero)
write('profile-banner-mobile.svg',mobile_static.replace('<defs>',motion+'<defs>',1))
write('profile-banner-mobile-static.svg',mobile_static.replace('stroke-dasharray="45 595"','opacity="0.35"'))

# Consistent frames; the actual technology marks are vendored Devicon SVGs.
labels={'java':'Java','spring':'Spring','python':'Python','postgresql':'PostgreSQL','docker':'Docker','react':'React','typescript':'TypeScript','git':'Git'}
for name,label in labels.items():
    source=(A/'vendor/devicon'/f'{name}.svg').read_text()
    source=re.sub(r'<\?xml[^>]*\?>','',source)
    source=re.sub(r'<!DOCTYPE[\s\S]*?>','',source)
    start=source.index('<svg')
    source=source[start:]
    source=re.sub(r'<svg\b([^>]*)>',lambda m:'<svg '+re.sub(r'\s(?:width|height|x|y)="[^"]*"','',m.group(1))+' x="23" y="14" width="40" height="40">',source,count=1)
    icon='<rect x=".5" y=".5" width="85" height="85" rx="12" fill="#101f33" stroke="#263b54"/>'+source+text(43,73,label,11.5,'#d8e7f6',500,'text-anchor="middle"')
    write(f'tech/{name}.svg',svg(86,86,label,icon))

# Original symbolic glyphs, with explicit tool labels, for the GenAI toolkit.
# These are illustrations rather than third-party brand marks.
VIOLET = '#c4b5fd'
ai_glyphs = {
    'spring-ai': ('Spring AI', '<path d="M29 44c-3-15 10-22 29-19 3 19-4 30-20 27M28 55l25-25M38 45l-1-11M43 40l11 1"/><path d="m62 39 2 5 5 2-5 2-2 5-2-5-5-2 5-2z"/>'),
    'langchain4j': ('LangChain4j', '<rect x="23" y="24" width="27" height="17" rx="8" transform="rotate(-35 36.5 32.5)"/><rect x="36" y="34" width="27" height="17" rx="8" transform="rotate(-35 49.5 42.5)"/><path d="m38 38 10-7"/>'),
    'langgraph': ('LangGraph', '<path d="M29 25h27M29 25v26h27M56 25v26M29 25l27 26"/><circle cx="29" cy="25" r="5" fill="#182438"/><circle cx="56" cy="25" r="5" fill="#182438"/><circle cx="29" cy="51" r="5" fill="#182438"/><circle cx="56" cy="51" r="5" fill="#182438"/>'),
    'ollama': ('Ollama', '<path d="M31 32c-6-4-8-16-4-17 4-2 10 8 10 13M49 28c0-13 5-17 8-13 4 5 1 14-2 18M32 31c6-5 17-6 23 0 10 11 5 24-12 24S22 41 32 31z"/><path d="M35 39h1m13 0h1M40 46q3 3 6 0"/>'),
    'openai-api': ('OpenAI API', '<rect x="22" y="22" width="42" height="34" rx="7"/><path d="m31 34 7 5-7 5M44 44h11M32 17v5m22-5v5M32 56v5m22-5v5"/>'),
    'rag': ('RAG', '<path d="M27 21h22l9 9v25H27zM49 21v10h9M34 36h13M34 43h9"/><circle cx="53" cy="48" r="9" fill="#182438"/><path d="m60 55 6 6"/>'),
    'mcp': ('MCP', '<path d="M29 34h12M45 40v12M34 52h11M53 28h9M61 28v17M61 45h-8"/><rect x="22" y="27" width="13" height="14" rx="4"/><rect x="40" y="20" width="14" height="16" rx="4"/><rect x="40" y="45" width="14" height="16" rx="4"/>'),
}
for name, (label, glyph) in ai_glyphs.items():
    frame='<rect x=".5" y=".5" width="85" height="85" rx="12" fill="#101f33" stroke="#514b78"/>'
    drawing=f'<g fill="none" stroke="{VIOLET}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{glyph}</g>'
    write(f'tech/{name}.svg',svg(86,86,label,frame+drawing+text(43,73,label,11.5,'#e0dafa',500,'text-anchor="middle"')))

# Local, wrapping badges keep each project's technology stack prominent.
badges = {
    'python': ('Python', 94, BLUE), 'java': ('Java', 78, BLUE),
    'langgraph': ('LangGraph', 126, VIOLET), 'ollama': ('Ollama', 98, VIOLET),
    'openai-api': ('OpenAI API', 130, VIOLET),
    'api-evaluation': ('API evaluation', 150, TEAL),
    'rust': ('Rust', 78, BLUE), 'tauri': ('Tauri', 82, TEAL),
    'react': ('React', 86, BLUE), 'typescript': ('TypeScript', 124, BLUE),
    'sqlite': ('SQLite', 94, TEAL),
}
for name,(label,width,color) in badges.items():
    body=f'<rect x=".5" y=".5" width="{width-1}" height="31" rx="7" fill="#142338" stroke="{color}" stroke-opacity=".65"/>'
    body+=f'<circle cx="15" cy="16" r="3" fill="{color}"/>'
    body+=text(27,21,label,14,'#f0f6ff',600)
    write(f'stack/{name}.svg',svg(width,32,label,body))

def contact(name,label,width,icon):
    body=icon+text(44,23,label,13,INK,600)
    write(f'contact/{name}.svg',svg(width,36,label,body))
contact('linkedin','LinkedIn',124,'<rect x="14" y="10" width="18" height="18" rx="3" fill="#86baff"/>'+text(17,24,'in',15,'#09131f',700))
contact('email','Email',104,'<rect x="14" y="11" width="20" height="14" rx="3" fill="none" stroke="#5eead4" stroke-width="1.6"/><path d="m15 12 9 7 9-7" fill="none" stroke="#5eead4" stroke-width="1.6"/>')

# A source-grounded architecture illustration, not a simulated terminal report.
cg=text(32,39,'01 / CHANGEGUARD',15,TEAL,700,'letter-spacing="2"')
cg+=pill(895,18,192,'RELEASE CANDIDATE',BLUE)
cg+=text(32,85,'See what a Spring change could break.',31,INK,700)
cg+=text(32,117,'Change-impact analysis for Java microservices',18,MUTED)
cards=[(32,'01','Source changes','Java / Spring AST'),(398,'02','Affected consumers','Feign · WebClient · RestTemplate'),(764,'03','Verification plans','Bound to the analyzed revision')]
for x,n,title,detail in cards:
    cg+=f'<rect x="{x}" y="149" width="324" height="96" rx="12" fill="#12243a" stroke="{EDGE}"/>'
    cg+=text(x+18,177,n,12,TEAL,700)+text(x+18,204,title,21,INK,600)+text(x+18,229,detail,14,MUTED)
for x in [368,734]:
    cg+=f'<path d="M{x} 196h18m-5-5 5 5-5 5" fill="none" stroke="#5eead4" stroke-width="2"/>'
cg+=text(32,280,'ARCHITECTURE OVERVIEW',11,'#738ba4',600,'letter-spacing="1.8"')
cg+=text(1088,280,'Python  /  Java  /  LangGraph',13,MUTED,400,'text-anchor="end"')
write('projects/changeguard.svg',svg(1120,304,'ChangeGuard architecture: source changes, affected consumers, revision-bound verification plans.',cg))

# Published values, with bar lengths proportional to median milliseconds.
b=text(26,35,'02 / API WORKFLOW BENCHMARK',13,TEAL,700,'letter-spacing="1.4"')
b+=text(26,78,'Measure the trade-offs.',27,INK,700)
b+=text(26,108,'Median latency · milliseconds · lower is better',15,MUTED)
for y,label,value,color,formatted in [(144,'Decisions',126.84,TEAL,'126.84'),(206,'Responses',1468.97,BLUE,'1,468.97')]:
    b+=text(26,y+21,label,17,INK,500)
    bar=value/1500*338
    b+=f'<rect x="154" y="{y}" width="338" height="30" rx="5" fill="#16273d"/><rect x="154" y="{y}" width="{bar:.4f}" height="30" rx="5" fill="{color}"/>'
    if bar>270:b+=text(480,y+21,formatted,15,'#09131f',700,'text-anchor="end"')
    else:b+=text(154+bar+10,y+21,formatted,15,INK,600)
b+=text(26,277,'200 calls / workflow · 40 scenarios × 5 paraphrases',13,MUTED)
b+=text(26,306,'Published experiment · Oct 2026 · exploratory results',12,'#7d96af')
write('projects/benchmark.svg',svg(540,330,'Published API benchmark. Median Decisions latency 126.84 ms; Responses 1468.97 ms. Exploratory workflow comparison.',b))

f=text(26,35,'03 / DESKTOP FOCUS COMPANION',13,TEAL,700,'letter-spacing="1.1"')
f+=text(26,78,'Context. Focus. Recovery.',27,INK,700)
f+=text(26,108,'Windows · local history · optional local AI',15,MUTED)
for x,title,detail in [(26,'App context','Win32 capture'),(200,'Classification','Rules / Ollama'),(374,'Companion','React / Tauri')]:
    f+=f'<rect x="{x}" y="142" width="140" height="88" rx="11" fill="#12243a" stroke="{EDGE}"/>'
    f+=text(x+70,178,title,15,INK,600,'text-anchor="middle"')+text(x+70,204,detail,12,MUTED,400,'text-anchor="middle"')
for x in [175,349]:f+=f'<path d="M{x} 186h15m-5-5 5 5-5 5" fill="none" stroke="{TEAL}" stroke-width="2"/>'
f+=text(26,277,'Rust native core  /  SQLite history',14,MUTED)
f+=text(26,306,'ARCHITECTURE OVERVIEW · IN DEVELOPMENT',11,'#7d96af',600,'letter-spacing=".7"')
write('projects/flowpet.svg',svg(540,330,'Desktop companion architecture overview: app context, classification, and companion UI with local SQLite history. In development.',f))

o='<circle cx="51" cy="67" r="25" fill="#252547"/><g fill="none" stroke="#bca6ff" stroke-width="2.5"><circle cx="45" cy="53" r="4"/><circle cx="45" cy="81" r="4"/><circle cx="61" cy="66" r="4"/><path d="M45 57v20m0-16c0 5 12 0 12 5"/></g>'
o+=text(96,43,'MERGED / HIERO JAVA SDK',12,'#bca6ff',700,'letter-spacing="1.5"')
o+=text(96,77,'A focused contribution, with validation.',26,INK,700)
o+=text(96,105,'TopicUpdateTransaction Javadoc correction',16,MUTED)
o+=text(1064,77,'PR #3042 →',18,TEAL,600,'text-anchor="end"')
write('activity.svg',svg(1120,140,'Merged Hiero Java SDK pull request 3042: TopicUpdateTransaction Javadoc correction.',o))

# Wide cards for desktop; the compact originals act as mobile alternatives.
wide_b=text(32,42,'02 / API WORKFLOW BENCHMARK',14,TEAL,700,'letter-spacing="1.5"')
wide_b+=text(32,103,'Measure the trade-offs.',34,INK,700)
wide_b+=text(32,144,'Latency, accuracy, and error patterns.',20,MUTED)
wide_b+=text(32,193,'Published results + raw measurements',17,INK)
wide_b+=text(32,242,'EXPLORATORY EXPERIMENT',11,'#7d96af',600,'letter-spacing="1.6"')
wide_b+='<path d="M554 35v210" stroke="#263b54"/>'
wide_b+=text(591,51,'Median latency · ms · lower is better',16,MUTED)
for y,label,value,color,formatted in [(85,'Decisions',126.84,TEAL,'126.84'),(143,'Responses',1468.97,BLUE,'1,468.97')]:
    bar=value/1500*320
    wide_b+=text(591,y+20,label,17,INK,500)
    wide_b+=f'<rect x="710" y="{y}" width="320" height="29" rx="5" fill="#16273d"/><rect x="710" y="{y}" width="{bar:.4f}" height="29" rx="5" fill="{color}"/>'
    wide_b+=text(1018 if bar>270 else 720+bar,y+20,formatted,14,'#09131f' if bar>270 else INK,600,'text-anchor="end"' if bar>270 else '')
wide_b+=text(591,215,'200 calls / workflow · 40 scenarios × 5 paraphrases',13,MUTED)
wide_b+=text(591,241,'Different output contracts · Oct 2026',12,'#7d96af')
write('projects/benchmark-wide.svg',svg(1120,276,'Published API benchmark. Decisions median 126.84 ms; Responses median 1468.97 ms. Exploratory comparison.',wide_b))

wide_f=text(32,42,'03 / DESKTOP FOCUS COMPANION',14,TEAL,700,'letter-spacing="1.4"')
wide_f+=text(32,103,'Context. Focus. Recovery.',34,INK,700)
wide_f+=text(32,144,'A companion for returning to your work.',20,MUTED)
wide_f+=text(32,193,'Rust · Tauri · React · SQLite',17,INK)
wide_f+=text(32,242,'IN DEVELOPMENT / WORKING TITLE: FLOWPET',11,'#7d96af',600,'letter-spacing=".7"')
wide_f+='<path d="M554 35v210" stroke="#263b54"/>'
wide_f+=text(591,51,'ARCHITECTURE OVERVIEW',12,MUTED,600,'letter-spacing="1.5"')
for x,title,detail in [(591,'App context','Win32 capture'),(765,'Classification','Rules / Ollama'),(939,'Companion','React / Tauri')]:
    wide_f+=f'<rect x="{x}" y="85" width="146" height="94" rx="11" fill="#12243a" stroke="{EDGE}"/>'
    wide_f+=text(x+73,122,title,15,INK,600,'text-anchor="middle"')+text(x+73,150,detail,12,MUTED,400,'text-anchor="middle"')
for x in [744,918]:wide_f+=f'<path d="M{x} 132h12m-4-4 4 4-4 4" fill="none" stroke="{TEAL}" stroke-width="2"/>'
wide_f+=text(591,216,'Local history in SQLite · optional model assistance',14,MUTED)
write('projects/flowpet-wide.svg',svg(1120,276,'Desktop focus companion architecture. Windows context, rules or model classification, companion, and local history. In development.',wide_f))

mobile_cg=text(25,37,'01 / CHANGEGUARD',14,TEAL,700,'letter-spacing="1.6"')
mobile_cg+=text(25,81,'See what a Spring change',27,INK,700)+text(25,115,'could break.',27,INK,700)
for y,n,title,detail in [(141,'01','Source changes','Java / Spring AST'),(238,'02','Affected consumers','Feign · WebClient · RestTemplate'),(335,'03','Verification plans','Bound to the analyzed revision')]:
    mobile_cg+=f'<rect x="25" y="{y}" width="490" height="78" rx="11" fill="#12243a" stroke="{EDGE}"/>'
    mobile_cg+=text(43,y+31,n,14,TEAL,700)+text(80,y+31,title,21,INK,600)+text(80,y+57,detail,15,MUTED)
mobile_cg+=text(25,446,'ARCHITECTURE OVERVIEW · RELEASE CANDIDATE',11,'#7d96af',600,'letter-spacing=".6"')
write('projects/changeguard-mobile.svg',svg(540,468,'ChangeGuard: source changes, affected consumers, revision-bound verification plans. Release candidate.',mobile_cg))
mobile_o=text(25,33,'MERGED / HIERO JAVA SDK',13,'#bca6ff',700,'letter-spacing="1.1"')
mobile_o+=text(25,74,'TopicUpdateTransaction',26,INK,700)+text(25,108,'Javadoc correction',24,INK,600)
mobile_o+=text(25,151,'View merged PR #3042 →',18,TEAL,600)
write('activity-mobile.svg',svg(540,178,'Merged Hiero Java SDK PR 3042: TopicUpdateTransaction Javadoc correction.',mobile_o))
print('Generated responsive headers, icons, contacts, project visuals, and open-source activity card.')
