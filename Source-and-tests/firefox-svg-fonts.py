from pathlib import Path
import base64,hashlib,json
from fontTools.ttLib import TTFont,newTable
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib.tables.S_V_G_ import SVGDocument
out=Path('tooling/firefox-svg-fonts');out.mkdir(exist_ok=True);results=[]
for source in Path('emoji-harbor-src/fonts').glob('*.woff2'):
 if source.stem=='mona':continue
 f=TTFont(source);order=f.getGlyphOrder();originalGSUB=f['GSUB'].compile(f);originalCmap=f.getBestCmap();strike=f['CBLC'].strikes[0].bitmapSizeTable;units=f['head'].unitsPerEm;sx=units/strike.ppemX;sy=units/strike.ppemY;docs=[];bitmaps=f['CBDT'].strikeData[0]
 for gid,name in enumerate(order):
  if name not in bitmaps:continue
  g=bitmaps[name];g.ensureDecompiled();m=g.metrics;data=base64.b64encode(g.imageData).decode()
  svg=f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><g id="glyph{gid}"><image x="{m.BearingX*sx:g}" y="{-m.BearingY*sy:g}" width="{m.width*sx:g}" height="{m.height*sy:g}" xlink:href="data:image/png;base64,{data}"/></g></svg>'
  docs.append(SVGDocument(svg,gid,gid,True))
 builder=FontBuilder(font=f);builder.isTTF=True;builder.setupGlyf({name:TTGlyphPen(None).glyph()for name in order});builder.setupMaxp();f['SVG ']=newTable('SVG ');f['SVG '].docList=docs;del f['CBDT'];del f['CBLC'];f.flavor='woff2';target=out/source.name;f.save(target)
 check=TTFont(target);assert check.getBestCmap()==originalCmap;assert check['GSUB'].compile(check)==originalGSUB;assert len(check['SVG '].docList)==len(bitmaps);assert len(docs)==3972
 # Verify every embedded bitmap matches its original byte for byte.
 import re
 for doc in check['SVG '].docList:
  image=base64.b64decode(re.search('base64,([^" ]+)',doc.data)[1]);assert image==bitmaps[order[doc.startGlyphID]].imageData
 results.append({'font':source.name,'glyphs':len(docs),'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()});print(source.name,len(docs),target.stat().st_size,flush=True)
(out/'validation.json').write_text(json.dumps(results,indent=2))
