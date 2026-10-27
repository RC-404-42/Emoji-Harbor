from pathlib import Path
import shutil,zipfile,json,re,hashlib
src=Path('emoji-harbor-src');base=Path('base/Emoji-Harbor-v1.1.4');root=Path('dist/Emoji-Harbor-v1.2.4');root.mkdir(parents=True,exist_ok=True)
assert 'ALL 109 CHECKS PASSED'in Path('tooling/validation-v124.log').read_text()
for p in base.iterdir():
 if p.is_file()and p.suffix!='.xpi':shutil.copy2(p,root/p.name)
shutil.copytree(src,root/'Chrome',dirs_exist_ok=True)
m=json.loads((root/'Chrome/manifest.json').read_text());m.pop('browser_specific_settings',None);(root/'Chrome/manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
firefox=Path('tooling/firefox-v124');shutil.copytree(src,firefox,dirs_exist_ok=True);m=json.loads((firefox/'manifest.json').read_text());m['background']={'scripts':['core.js','background.js']};m['browser_specific_settings']={'gecko': {'id': 'emoji-harbor@local.invalid', 'strict_min_version': '142.0', 'data_collection_permissions': {'required': ['none']}}};(firefox/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
assert len(list(Path('tooling/firefox-svg-fonts').glob('*.woff2')))==6
for font in Path('tooling/firefox-svg-fonts').glob('*.woff2'):shutil.copy2(font,firefox/'fonts'/font.name)
info=json.loads((firefox/'build-info.json').read_text());info['font_format']='OpenType SVG WOFF2 (embedded original 64px PNG), Mona unchanged COLR v0';(firefox/'build-info.json').write_text(json.dumps(info,ensure_ascii=False,indent=2))
for folder in [root/'Chrome',firefox]:
 for html in folder.glob('*.html'):
  for ref in re.findall(r'(?:src|href)="([^"#]+)"',html.read_text()):
   if ':'not in ref:assert(folder/ref).is_file(),(html,ref)
xpi=Path('dist/Emoji-Harbor-Firefox-v1.2.4-unsigned.xpi')
with zipfile.ZipFile(xpi,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for p in sorted(firefox.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(firefox))
with zipfile.ZipFile(xpi)as z:
 assert z.testzip()is None;manifest=json.loads(z.read('manifest.json'));assert manifest['browser_specific_settings']['gecko']['id']=='emoji-harbor@local.invalid';assert manifest['browser_specific_settings']['gecko']['data_collection_permissions']=={'required':['none']};assert 'scripts'in manifest['background']and'service_worker'not in manifest['background'];assert len([n for n in z.namelist()if n.startswith('fonts/')])==7;assert json.loads(z.read('manifest.json'))['version']=='1.2.4';assert not any(n.startswith('META-INF')for n in z.namelist())
shutil.copy2(xpi,root/xpi.name)
for source,target in [('help.html','Start-Here.html'),('privacy.html','Privacy.html')]:
 (root/target).write_text((src/source).read_text().replace('href="ui.css"','href="Chrome/ui.css"').replace('src="icons/128.png"','src="Chrome/icons/128.png"'))
shutil.copy2(src/'PRIVACY.md',root/'PRIVACY.md');shutil.copy2('tooling/Mona-Preview.png',root/'Mona-Preview.png')
for name in ['README.md','README-先看我.txt']:
 p=root/name;s=p.read_text().replace('1.1.4','1.2.4').replace('86 項','109 項').replace('六套','七套').replace('六種','七種');s+='\n\n1.2.4（2026-10-27）：設定頁新增預設選字盤分頁（全部／最近使用），以及小、中、大、特大表情尺寸；不影響網頁字形尺寸。加入 Mona12 彩色像素風格（OFL 1.1），缺字由 Noto 後備，複合表情支援取決於字型。字型來源及版本見 Chrome/build-info.json。\n選字盤偏好不廣播重套頁面字型，快取膚色結果，每批通知最多4個分頁；背景分頁暫停動畫，切回不再全頁重掃。\nTelegram 動畫本版未加入。未完成真實瀏覽器效能與視覺驗證，未與 Emoji Swap 實測比較。\n';p.write_text(s)
dev=root/'Source-and-tests';dev.mkdir(exist_ok=True)
for utility in ['build-fonts.py','render-assets.cjs','render-extra.cjs','download-animations.py','font-catalog.json']:
 shutil.copy2(base/'Source-and-tests'/utility,dev/utility)
for n in ['test-v124.cjs','validation-v124.log','package-v124.py']:
 shutil.copy2(Path('tooling')/n,dev/n)
(dev/'README.txt').write_text('Runtime source is in Chrome and the XPI. No build required. Logic tests: npm install jsdom@26; node test-v124.cjs. Tests use mocked browser, fonts and geometry APIs; not native browser performance validation. Mona-Preview.png is rendered from original COLR layer paths, not a browser screenshot.\n')
shutil.copy2('tooling/firefox-svg-fonts.py',dev/'firefox-svg-fonts.py')
shutil.copy2('tooling/firefox-svg-fonts/validation.json',dev/'firefox-font-validation.json')
if Path('tooling/firefox-lint-v124.json').exists():shutil.copy2('tooling/firefox-lint-v124.json',dev/'firefox-lint-v124.json')
with(root/'README-先看我.txt').open('a')as f:f.write('\nFirefox 1.2.4 採 OpenType SVG 字型；請先暫時載入確認 Windows Firefox 顯示，再重新送簽。此環境尚未完成實機驗證。\n')
archive=Path('dist/Emoji-Harbor-v1.2.4.zip')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for p in sorted(root.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(root.parent))
with zipfile.ZipFile(archive)as z:
 assert z.testzip()is None;assert z.read(root.name+'/'+xpi.name)==xpi.read_bytes();assert 'browser_specific_settings'not in json.loads(z.read(root.name+'/Chrome/manifest.json'))
for p in [archive,xpi]:print(p.resolve(),p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest())
