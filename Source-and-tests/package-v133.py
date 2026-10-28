from pathlib import Path
import zipfile,json,shutil,re,hashlib
base=Path('dist/Emoji-Harbor-v1.3.2');src=Path('emoji-harbor-src');root=Path('dist/Emoji-Harbor-v1.3.3');root.mkdir(parents=True,exist_ok=True)
assert 'ALL 145 CHECKS PASSED'in Path('tooling/validation-v133.log').read_text()
for p in base.iterdir():
 if p.is_file()and p.suffix!='.xpi':shutil.copy2(p,root/p.name)
chrome=root/'Chrome';shutil.copytree(src,chrome,dirs_exist_ok=True)
m=json.loads((chrome/'manifest.json').read_text());m['version']='1.3.3';m.pop('browser_specific_settings',None);(chrome/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
firefox=Path('tooling/firefox-v133');shutil.copytree(src,firefox,dirs_exist_ok=True)
m=json.loads((firefox/'manifest.json').read_text());m['version']='1.3.3';m['background']={'scripts':['core.js','background.js']};m['browser_specific_settings']=json.loads(Path('firefox-base/manifest.json').read_text())['browser_specific_settings'];assert m['browser_specific_settings']['gecko']['id']=='emoji-harbor@local.invalid';assert m['browser_specific_settings']['gecko']['data_collection_permissions']=={'required':['none']};(firefox/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
for p in Path('firefox-base/fonts').glob('*.woff2'):shutil.copy2(p,firefox/'fonts'/p.name)
for folder,original in [(chrome,base/'Chrome'),(firefox,Path('firefox-base'))]:
 for p in (folder/'fonts').glob('*.woff2'):assert p.read_bytes()==(original/'fonts'/p.name).read_bytes()
 info=json.loads((original/'build-info.json').read_text());info['version']='1.3.3';info['built']='2026-10-28';(folder/'build-info.json').write_text(json.dumps(info,ensure_ascii=False,indent=2))
 for page in folder.glob('*.html'):
  for ref in re.findall(r'(?:src|href)="([^"#]+)"',page.read_text()):
   if ':'not in ref:assert(folder/ref).is_file(),(page,ref)
 for name in ['options.html','help.html','test.html','privacy.html']:assert 'href="themes.css"'not in(folder/name).read_text()
 # Shared UI styles remain byte-identical; only the popup-only sheet changes.
 assert(folder/'ui.css').read_bytes()==(base/'Chrome/ui.css').read_bytes()
 assert(folder/'icons/theme-drop.svg').is_file()
xpi=Path('dist/Emoji-Harbor-Firefox-v1.3.3-unsigned.xpi')
with zipfile.ZipFile(xpi,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for p in sorted(firefox.rglob('*')):
  if p.is_file()and not any(v.startswith('.')for v in p.relative_to(firefox).parts):z.write(p,p.relative_to(firefox))
with zipfile.ZipFile(xpi)as z:
 assert z.testzip()is None;assert len([n for n in z.namelist()if n.startswith('fonts/')])==7;assert not any(n.startswith('META-INF/')for n in z.namelist())
shutil.copy2(xpi,root/xpi.name)
for source,target in [('help.html','Start-Here.html'),('privacy.html','Privacy.html')]:
 (root/target).write_text((src/source).read_text().replace('href="ui.css"','href="Chrome/ui.css"').replace('src="icons/128.png"','src="Chrome/icons/128.png"'))
shutil.copy2(src/'PRIVACY.md',root/'PRIVACY.md')
for n in ['README.md','README-先看我.txt']:
 p=root/n;t=p.read_text().replace('表情補給站 Emoji Harbor 1.3.2','表情補給站 Emoji Harbor 1.3.3');t=t.replace('Emoji-Harbor-v1.3.2','Emoji-Harbor-v1.3.3').replace('Firefox-v1.3.2','Firefox-v1.3.3');t+='\n\n1.3.3（2026-10-28）右上角選字盤在可容納的完整列之外多放一列，填補底下空白，允許最多約一列表情的短距離捲動，其餘繼續分頁。截圖常見高度下小／中／大／特大約為 32／24／12／4 個，實際依視窗高度調整。連續縮小、放大高度時保留原本附近的表情。設定頁使用 32／24／12／4 個的固定數量。櫻花歐蕾改為低飽和的櫻花奶粉底、柔和玫瑰色與莓灰文字，移除亮桃紅強調色。其他四款配色與其他 HTML 頁面的色彩不變。\n145 項模擬邏輯檢查通過，包含完整 1,927 個表情分頁、四款尺寸空白與捲動量計算、末頁、空結果及連續尺寸變化。五款主要／次要／強調文字與背景、卡片、輸入框的計算對比最低 4.93:1；尚未完成本版 Chrome／Windows Firefox 實機視覺驗證。\n';p.write_text(t)
dev=root/'Source-and-tests';shutil.copytree(base/'Source-and-tests',dev,dirs_exist_ok=True)
for name in ['test-v133.cjs','validation-v133.log','package-v133.py','update-v133.py','check-theme-contrast.py','theme-contrast.json']:shutil.copy2(Path('tooling')/name,dev/name)
(dev/'README.txt').write_text('Ready-to-load source is in Chrome/ and the XPI. Run current logic tests: npm install jsdom@26; node test-v133.cjs. Browser/FontFace/geometry APIs are mocked. Theme contrast calculation: python3 check-theme-contrast.py from project root (source folder named emoji-harbor-src). No native browser visual validation. Platform-specific font files and shared ui.css preserved unchanged.\n')
if Path('tooling/firefox-lint-v133.json').exists():shutil.copy2('tooling/firefox-lint-v133.json',dev/'firefox-lint-v133.json')
archive=Path('dist/Emoji-Harbor-v1.3.3.zip')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for p in sorted(root.rglob('*')):
  if p.is_file()and not any(v.startswith('.')for v in p.relative_to(root).parts):z.write(p,p.relative_to(root.parent))
with zipfile.ZipFile(archive)as z:assert z.testzip()is None;assert z.read(root.name+'/'+xpi.name)==xpi.read_bytes()
for p in [archive,xpi]:print(p.resolve(),p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest())
