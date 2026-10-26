import pathlib,json,urllib.request,concurrent.futures,io
from PIL import Image
root=pathlib.Path('emoji-atelier-work/assets');raw=pathlib.Path('tooling/v110-assets/anim-raw');raw.mkdir(exist_ok=True)
out=pathlib.Path('emoji-harbor-src/anim');out.mkdir(exist_ok=True)
data=json.loads((root/'catalog.json').read_text())
extra=set('👍👎👋👏🙌🫶🤝🙏💪🫵👀💋🔥✨🎉🎂🎈🎁💩👻💀👽🤖🐱🐶🐈🐕🐼🐻🐸🐰🐹🐭🦊🐺🦁🐯🦄🐷🐮🐨🐧🐣🐥🦉🦋🐝🐢🐙🐳🐋🐬🐟🦈🐠🌸🌺🌻🌹🌷🍀🌈🌞🌝🌚⭐🌟☀️☁️⚡❄️🌊🍕🍔🍟🍿🍫🍩🍪🍰🧋☕🍵🥤🥂🍺🍷🍓🍒🍑🍉🍌🍍🥭🎮🎲🎵🎶❤️💔💖💕💓💗💙💚💛💜🖤🤍🩷')
candidates=[r for r in data['records'] if (r['group']=='Smileys & Emotion' or r['emoji'] in extra) and not any(0x1f3fb<=ord(c)<=0x1f3ff for c in r['emoji'])]
def job(r):
 key=r['key'];src=raw/(key+'.webp');dst=out/(key+'.webp')
 try:
  if not src.exists():src.write_bytes(urllib.request.urlopen('https://fonts.gstatic.com/s/e/notoemoji/latest/'+key.replace('-','_')+'/512.webp',timeout=20).read())
  im=Image.open(src)
  if getattr(im,'n_frames',1)<2:return None
  if not dst.exists():
   frames=[];durations=[]
   for i in range(im.n_frames):
    im.seek(i);f=im.convert('RGBA');durations.append(max(20,int(im.info.get('duration',60))));frames.append(f.resize((64,64),Image.Resampling.LANCZOS))
   step=2 if len(frames)>30 else 1
   keep=frames[::step];times=[sum(durations[i:i+step]) for i in range(0,len(frames),step)]
   keep[0].save(dst,format='WEBP',save_all=True,append_images=keep[1:],duration=times,loop=0,quality=52,method=4)
  return r
 except Exception:return None
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:success=[r for r in ex.map(job,candidates) if r]
keys={r['key'] for r in success};mapping={s:'anim/'+key+'.webp' for s,key in data['aliases'].items() if key in keys}
pathlib.Path('emoji-harbor-src/animation-data.js').write_text('globalThis.EH_ANIMATION = '+json.dumps({'assets':mapping,'count':len(success)},ensure_ascii=False,separators=(',',':'))+';\n')
(root/'animated-coverage.json').write_text(json.dumps({'attempted':len(candidates),'animated':len(success),'bytes':sum(p.stat().st_size for p in out.glob('*.webp'))}))
print('ANIMATED',len(success),'/',len(candidates),'bytes',sum(p.stat().st_size for p in out.glob('*.webp')),flush=True)
