"""Repair emoji presentation coverage and VS-insensitive ligatures; Firefox only."""
from pathlib import Path
from io import BytesIO
import json,hashlib
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._c_m_a_p import CmapSubtable
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
import uharfbuzz as hb
out=Path('tooling/firefox-fixed-fonts');out.mkdir(exist_ok=True)
def shaper(f):
 f.flavor=None;b=BytesIO();f.save(b);return hb.Font(hb.Face(b.getvalue()))
def shape(font,text):
 b=hb.Buffer();b.add_str(text);b.guess_segment_properties();hb.shape(font,b,{'rlig':True});return [i.codepoint for i,p in zip(b.glyph_infos,b.glyph_positions)if p.x_advance or p.y_advance]
results=[]
for p in sorted(Path('firefox-base/fonts').glob('*.woff2')):
 if p.stem=='mona':continue
 f=TTFont(p);oldmap=f.getBestCmap().copy();inverse={g:c for c,g in oldmap.items()};aliases={chr(c):g for c,g in oldmap.items()}
 for lookup in f['GSUB'].table.LookupList.Lookup:
  assert lookup.LookupType==4
  for st in lookup.SubTable:
   for first,ligs in st.ligatures.items():
    for lig in ligs:aliases[''.join(chr(inverse[g])for g in [first]+lig.Component)]=lig.LigGlyph
 oldfont=shaper(f);expected={text:shape(oldfont,text)for text in aliases}
 # Base and base+VS16 must identify the same actual color glyph, not an empty placeholder.
 mapping=oldmap.copy();pairs=set()
 for text,g in aliases.items():
  plain=text.replace('\ufe0f','')
  if len(plain)==1 and '\ufe0f'in text:mapping[ord(plain)]=g
  for i,c in enumerate(text):
   if c=='\ufe0f'and i:pairs.add(ord(text[i-1]))
 for table in f['cmap'].tables:
  if table.format in [4,12]:table.cmap={cp:mapping[cp]for cp in table.cmap}
 uvs=CmapSubtable.newSubtable(14);uvs.platformID=0;uvs.platEncID=5;uvs.language=0;uvs.cmap={};uvs.uvsDict={0xfe0f:[(cp,None)for cp in sorted(pairs)]};f['cmap'].tables.append(uvs)
 normalized={}
 for text,g in aliases.items():
  plain=text.replace('\ufe0f','')
  if len(plain)>1:
   assert plain not in normalized or normalized[plain]==g
   normalized[plain]=g
 rules=['sub '+' '.join(mapping[ord(c)]for c in text)+' by '+g+';'for text,g in sorted(normalized.items(),key=lambda v:(-len(v[0]),v[0]))]
 del f['GSUB'];addOpenTypeFeaturesFromString(f,'languagesystem DFLT dflt;\nfeature rlig {\n'+'\n'.join(rules)+'\n} rlig;')
 bitmapIDs={doc.startGlyphID for doc in f['SVG '].docList}
 for cp in pairs:assert f.getGlyphID(mapping[cp])in bitmapIDs or cp in [35,42,*range(48,58)]
 f.flavor='woff2';target=out/p.name;f.save(target)
 check=TTFont(target);newfont=shaper(check)
 for text,gids in expected.items():
  if gids:assert shape(newfont,text)==gids,(p.name,text,gids,shape(newfont,text))
 for text,g in normalized.items():assert shape(newfont,text)==[check.getGlyphID(g)],(p.name,text)
 # Artwork and glyph order remain exactly the same.
 old=TTFont(p);assert old.getGlyphOrder()==check.getGlyphOrder();assert [(d.startGlyphID,d.data)for d in old['SVG '].docList]==[(d.startGlyphID,d.data)for d in check['SVG '].docList]
 results.append({'font':p.name,'variation_pairs':len(pairs),'original_sequences_checked':len(expected),'normalized_ligatures_checked':len(normalized),'sha256':hashlib.sha256(target.read_bytes()).hexdigest()});print(results[-1],flush=True)
(out/'validation.json').write_text(json.dumps(results,indent=2))
