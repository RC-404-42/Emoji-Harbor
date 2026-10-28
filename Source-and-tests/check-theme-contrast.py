from pathlib import Path
import re,json
css=Path('emoji-harbor-src/themes.css').read_text()
def lum(c):
 a=[int(c[i:i+2],16)/255 for i in (1,3,5)];return sum(v*w for v,w in zip([v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in a],[.2126,.7152,.0722]))
def ratio(a,b):
 a,b=sorted([lum(a),lum(b)]);return (b+.05)/(a+.05)
results=[]
for key,body in re.findall(r'data-popup-theme="(\w+)"\]\{([^}]+)\}',css):
 t=dict(re.findall(r'--t-([\w-]+):([^;]+)',body));checks=[]
 for ink in ['ink','muted','accent']:
  for bg in ['bg','card','control']:checks.append((ink,bg,ratio(t.get('accent-ink',t[ink]) if ink=='accent' else t[ink],t[bg])))
 for ink,bg,r in checks:assert r>=4.5,(key,ink,bg,r)
 results.append({'theme':key,'minimum_text_contrast':round(min(r for a,b,r in checks),2)})
print(json.dumps(results,ensure_ascii=False));Path('tooling/theme-contrast.json').write_text(json.dumps(results,indent=2))
