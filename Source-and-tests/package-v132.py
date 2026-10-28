from pathlib import Path
import zipfile,json,shutil,re,hashlib
base=Path('dist/Emoji-Harbor-v1.3.1');src=Path('emoji-harbor-src');root=Path('dist/Emoji-Harbor-v1.3.2');root.mkdir(parents=True,exist_ok=True)
assert 'ALL 141 CHECKS PASSED'in Path('tooling/validation-v132.log').read_text()
for p in base.iterdir():
 if p.is_file()and p.suffix!='.xpi':shutil.copy2(p,root/p.name)
chrome=root/'Chrome';shutil.copytree(src,chrome,dirs_exist_ok=True)
m=json.loads((chrome/'manifest.json').read_text());m['version']='1.3.2';m.pop('browser_specific_settings',None);(chrome/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
firefox=Path('tooling/firefox-v132');shutil.copytree(src,firefox,dirs_exist_ok=True)
m=json.loads((firefox/'manifest.json').read_text());m['version']='1.3.2';m['background']={'scripts':['core.js','background.js']};m['browser_specific_settings']=json.loads(Path('firefox-base/manifest.json').read_text())['browser_specific_settings'];assert m['browser_specific_settings']['gecko']['id']=='emoji-harbor@local.invalid';assert m['browser_specific_settings']['gecko']['data_collection_permissions']=={'required':['none']};(firefox/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
for p in Path('firefox-base/fonts').glob('*.woff2'):shutil.copy2(p,firefox/'fonts'/p.name)
for folder,original in [(chrome,base/'Chrome'),(firefox,Path('firefox-base'))]:
 for p in (folder/'fonts').glob('*.woff2'):assert p.read_bytes()==(original/'fonts'/p.name).read_bytes()
 info=json.loads((original/'build-info.json').read_text());info['version']='1.3.2';info['built']='2026-10-28';(folder/'build-info.json').write_text(json.dumps(info,ensure_ascii=False,indent=2))
 for page in folder.glob('*.html'):
  for ref in re.findall(r'(?:src|href)="([^"#]+)"',page.read_text()):
   if ':'not in ref:assert(folder/ref).is_file(),(page,ref)
 for name in ['options.html','help.html','test.html','privacy.html']:assert 'href="themes.css"'not in(folder/name).read_text()
 # Shared UI styles remain byte-identical; only the popup-only sheet changes.
 assert(folder/'ui.css').read_bytes()==(base/'Chrome/ui.css').read_bytes()
 assert(folder/'icons/theme-drop.svg').is_file()
xpi=Path('dist/Emoji-Harbor-Firefox-v1.3.2-unsigned.xpi')
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
 p=root/n;t=p.read_text().replace('表情補給站 Emoji Harbor 1.3.1','表情補給站 Emoji Harbor 1.3.2');t=t.replace('Emoji-Harbor-v1.3.1','Emoji-Harbor-v1.3.2').replace('Firefox-v1.3.1','Firefox-v1.3.2');t+='\n\n1.3.2（2026-10-28）水滴按鈕改為淡淡的空心線條，跟隨主題文字色，中央完全透明。選字盤取消每頁固定 80 個，改為完整列分頁；右上角依可用高度與表情大小調整，每頁最多四列，其他表情放到下一頁。常見高度下小／中／大／特大約為 32／18／8／2 個；設定頁使用這組較少的固定數量。翻頁自動回到頂端，改變大小或高度時保留附近位置。\n141 項模擬邏輯檢查通過，包含全部 1,927 個表情分頁無重複或遺漏、末頁與空結果、尺寸變更及縮放高度。尚未完成本版 Chrome／Windows Firefox 實機視覺驗證。\n';p.write_text(t)
dev=root/'Source-and-tests';shutil.copytree(base/'Source-and-tests',dev,dirs_exist_ok=True)
for name in ['test-v132.cjs','validation-v132.log','package-v132.py','update-v132.py','check-theme-contrast.py','theme-contrast.json']:shutil.copy2(Path('tooling')/name,dev/name)
(dev/'README.txt').write_text('Ready-to-load source is in Chrome/ and the XPI. Run current logic tests: npm install jsdom@26; node test-v132.cjs. Browser/FontFace/geometry APIs are mocked. Theme contrast calculation: python3 check-theme-contrast.py from project root (source folder named emoji-harbor-src). No native browser visual validation. Platform-specific font files and shared ui.css preserved unchanged.\n')
if Path('tooling/firefox-lint-v132.json').exists():shutil.copy2('tooling/firefox-lint-v132.json',dev/'firefox-lint-v132.json')
archive=Path('dist/Emoji-Harbor-v1.3.2.zip')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for p in sorted(root.rglob('*')):
  if p.is_file()and not any(v.startswith('.')for v in p.relative_to(root).parts):z.write(p,p.relative_to(root.parent))
with zipfile.ZipFile(archive)as z:assert z.testzip()is None;assert z.read(root.name+'/'+xpi.name)==xpi.read_bytes()
for p in [archive,xpi]:print(p.resolve(),p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest())
