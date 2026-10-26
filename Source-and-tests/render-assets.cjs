const fs = require('fs');
const path = require('path');
let sharp;try{sharp=require('sharp')}catch{sharp=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/sharp')}
const root = path.resolve('emoji-atelier-work/assets');
const catalog = JSON.parse(fs.readFileSync(path.join(root, 'catalog.json')));
const norm = s => s.toLowerCase().split('-').filter(c=>c!=='fe0f').map(c=>parseInt(c,16).toString(16)).join('-');
async function main() {
  const apple = new Map(fs.readdirSync(path.join(root,'apple')).map(f=>[norm(f.slice(0,-4)),f]));
  const twemoji = new Map(fs.readdirSync(path.join(root,'twemoji')).map(f=>[norm(f.slice(0,-4)),f]));
  const counts={noto:0,apple:0,twemoji:0};
  for(const style of ['noto','apple','twemoji']) fs.mkdirSync(path.join(root,style+'-ready'),{recursive:true});
  let i=0;
  async function worker(){
    while(i<catalog.records.length){
      const item=catalog.records[i++];
      const target=path.join(root,'noto-ready',item.key+'.png');
      if(!fs.existsSync(target)){
        const xml=item.emoji.replaceAll('&','&amp;').replaceAll('<','&lt;');
        await sharp({text:{text:xml,fontfile:path.join(root,'NotoColorFull.ttf'),font:'Noto Color Emoji 64',rgba:true,dpi:72}}).resize(64,64,{fit:'contain',background:{r:0,g:0,b:0,alpha:0}}).png().toFile(target);
      }
      counts.noto++;
      for(const style of ['apple','twemoji']){
        const file=(style==='apple'?apple:twemoji).get(item.key);
        const dest=path.join(root,style+'-ready',item.key+'.png');
        if(file){
          if(!fs.existsSync(dest)) await sharp(path.join(root,style,file)).resize(64,64,{fit:'contain',background:{r:0,g:0,b:0,alpha:0}}).png().toFile(dest);
          counts[style]++;
        } else fs.copyFileSync(target,dest);
      }
    }
  }
  await Promise.all(Array.from({length:4},worker));
  fs.writeFileSync(path.join(root,'coverage.json'),JSON.stringify(counts));
  console.log(counts);
}
main().catch(e=>{console.error(e);process.exit(1)});
