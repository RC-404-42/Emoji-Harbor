from pathlib import Path
import zipfile,json,shutil,re,hashlib
base=Path('dist/Emoji-Harbor-v1.3.4');src=Path('emoji-harbor-src');root=Path('dist/Emoji-Harbor-v1.3.5');root.mkdir(parents=True,exist_ok=True)
assert 'ALL 145 CHECKS PASSED'in Path('tooling/validation-v135.log').read_text()
for p in base.iterdir():
 if p.is_file()and p.suffix!='.xpi':shutil.copy2(p,root/p.name)
chrome=root/'Chrome';shutil.copytree(src,chrome,dirs_exist_ok=True)
m=json.loads((chrome/'manifest.json').read_text());m['version']='1.3.5';m.pop('browser_specific_settings',None);(chrome/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
firefox=Path('tooling/firefox-v135');shutil.copytree(src,firefox,dirs_exist_ok=True)
m=json.loads((firefox/'manifest.json').read_text());m['version']='1.3.5';m['background']={'scripts':['core.js','background.js']};m['browser_specific_settings']=json.loads(Path('firefox-base/manifest.json').read_text())['browser_specific_settings'];assert m['browser_specific_settings']['gecko']['id']=='emoji-harbor@local.invalid';assert m['browser_specific_settings']['gecko']['data_collection_permissions']=={'required':['none']};(firefox/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
for p in Path('tooling/firefox-fixed-fonts').glob('*.woff2'):shutil.copy2(p,firefox/'fonts'/p.name)
for folder,original in [(chrome,base/'Chrome'),(firefox,Path('tooling/firefox-fixed-fonts'))]:
 for p in (folder/'fonts').glob('*.woff2'):
  reference=(original/'fonts'/p.name)if folder==chrome else (Path('firefox-base/fonts')/p.name if p.stem=='mona' else original/p.name)
  assert p.read_bytes()==reference.read_bytes()
 info=json.loads(((base/'Chrome' if folder==chrome else Path('firefox-base'))/'build-info.json').read_text());info['version']='1.3.5';info['built']='2026-10-28';(folder/'build-info.json').write_text(json.dumps(info,ensure_ascii=False,indent=2))
 for page in folder.glob('*.html'):
  for ref in re.findall(r'(?:src|href)="([^"#]+)"',page.read_text()):
   if ':'not in ref:assert(folder/ref).is_file(),(page,ref)
 for name in ['options.html','help.html','test.html','privacy.html']:assert 'href="themes.css"'not in(folder/name).read_text()
 # Shared UI styles remain byte-identical; only the popup-only sheet changes.
 assert(folder/'ui.css').read_bytes()==(base/'Chrome/ui.css').read_bytes()
 assert(folder/'icons/theme-drop.svg').is_file()
xpi=Path('dist/Emoji-Harbor-Firefox-v1.3.5-unsigned.xpi')
with zipfile.ZipFile(xpi,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for p in sorted(firefox.rglob('*')):
  if p.is_file()and not any(v.startswith('.')for v in p.relative_to(firefox).parts):z.write(p,p.relative_to(firefox))
with zipfile.ZipFile(xpi)as z:
 assert z.testzip()is None;assert len([n for n in z.namelist()if n.startswith('fonts/')])==7;assert not any(n.startswith('META-INF/')for n in z.namelist())
shutil.copy2(xpi,root/xpi.name)
for source,target in [('help.html','Start-Here.html'),('privacy.html','Privacy.html')]:
 (root/target).write_text((src/source).read_text().replace('href="ui.css"','href="Chrome/ui.css"').replace('src="icons/128.png"','src="Chrome/icons/128.png"'))
shutil.copy2(src/'PRIVACY.md',root/'PRIVACY.md')
for n in ['README-先看我.txt']:
 p=root/n;t=p.read_text().replace('表情補給站 Emoji Harbor 1.3.3','表情補給站 Emoji Harbor 1.3.5').replace('Emoji-Harbor-v1.3.3','Emoji-Harbor-v1.3.5').replace('Firefox-v1.3.3','Firefox-v1.3.5');t+='\n\n1.3.5（2026-10-28）按鈕內的空心水滴縮小至 18×21px，維持按鈕外框大小；粉色款更名「玫瑰歐蕾」，保留既有配色與偏好。145 項模擬檢查通過，未完成本版 Chrome／Windows Firefox 實機視覺驗證。\n';p.write_text(t)
shutil.copy2('tooling/README-v135.md',root/'README.md')
shutil.copy2('tooling/CHANGELOG-v135.md',root/'CHANGELOG.md')
(root/'README-先看我.txt').write_text('表情補給站 Emoji Harbor 1.3.5\nGPT 協助開發編寫。\n\n請先開啟 Start-Here.html 閱讀安裝與更新說明。\nChrome 系列：載入 Chrome 資料夾。\nFirefox：正式安裝使用已簽署的 XPI；本包附帶未簽署開發包，可暫時載入。\n\n本版修正 Firefox 字型映射與組字，保留 Chrome 字型。更新後請重開選字盤、重新整理已開啟的網頁。Firefox 實機效果仍待確認。\n\n完整專案介紹：README.md\n歷史版本：CHANGELOG.md\n隱私聲明：PRIVACY.md\n')
dev=root/'Source-and-tests';shutil.copytree(base/'Source-and-tests',dev,dirs_exist_ok=True)
for name in ['test-v135.cjs','validation-v135.log','package-v135.py','check-theme-contrast.py','theme-contrast.json','fix-firefox-variation.py']:shutil.copy2(Path('tooling')/name,dev/name)
(dev/'README.txt').write_text('Ready-to-load source is in Chrome/ and the XPI. Run current logic tests: npm install jsdom@26; node test-v135.cjs. Browser/FontFace/geometry APIs are mocked. Theme contrast calculation: python3 check-theme-contrast.py from project root (source folder named emoji-harbor-src). Firefox-only variation repair: run fix-firefox-variation.py with fonttools, brotli, uharfbuzz. See firefox-variation-validation.json. Native Windows Firefox visual confirmation pending. Chrome fonts and shared ui.css unchanged.\n')
if Path('tooling/firefox-lint-v135.json').exists():shutil.copy2('tooling/firefox-lint-v135.json',dev/'firefox-lint-v135.json')
shutil.copy2('tooling/firefox-fixed-fonts/validation.json',dev/'firefox-variation-validation.json')
archive=Path('dist/Emoji-Harbor-v1.3.5.zip')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for p in sorted(root.rglob('*')):
  if p.is_file()and not any(v.startswith('.')for v in p.relative_to(root).parts):z.write(p,p.relative_to(root.parent))
with zipfile.ZipFile(archive)as z:assert z.testzip()is None;assert z.read(root.name+'/'+xpi.name)==xpi.read_bytes()
for p in [archive,xpi]:print(p.resolve(),p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest())
