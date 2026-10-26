const fs=require('fs'),path=require('path');const sharp=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/sharp');
const root=path.resolve('emoji-atelier-work/assets'),catalog=JSON.parse(fs.readFileSync(path.join(root,'catalog.json')));
const norm=s=>s.toLowerCase().split('-').filter(c=>c!=='fe0f').map(c=>parseInt(c,16).toString(16)).join('-');
(async()=>{const counts={};for(const style of ['fluent3d','fluentflat','openmoji']){
 const source=path.join(root,style+'-source'),dest=path.join(root,style+'-ready');fs.mkdirSync(dest,{recursive:true});
 const files=new Map(fs.readdirSync(source).map(f=>[norm(f.replace(/\.[^.]+$/,'')),f]));let index=0;counts[style]=0;
 async function worker(){while(index<catalog.records.length){const r=catalog.records[index++],file=files.get(r.key),out=path.join(dest,r.key+'.png');
  if(file){await sharp(path.join(source,file)).resize(64,64,{fit:'contain',background:{r:0,g:0,b:0,alpha:0}}).png().toFile(out);counts[style]++}
  else fs.copyFileSync(path.join(root,'noto-ready',r.key+'.png'),out);
 }}await Promise.all(Array.from({length:4},worker));console.log(style,counts[style]);
 }fs.writeFileSync(path.join(root,'extra-coverage.json'),JSON.stringify(counts));})().catch(e=>{console.error(e);process.exit(1)});
