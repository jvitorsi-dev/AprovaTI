// Teste de navegação no DOM; não substitui um navegador real ou teste visual.
const {JSDOM, VirtualConsole} = require('jsdom');
const fs = require('fs'), os = require('os'), path = require('path'), net = require('net');
const {spawn} = require('child_process');
const root = path.resolve(__dirname, '..');
(async () => {
  const port = await new Promise((resolve, reject) => {
    const socket = net.createServer(); socket.on('error', reject);
    socket.listen(0, '127.0.0.1', () => {const p = socket.address().port; socket.close(() => resolve(p));});
  });
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'aprovati-ui-'));
  const server=spawn('python3',['server.py'],{cwd:root,env:{...process.env,PORT:String(port),APROVATI_DB:path.join(dir,'test.db')}});
  let dom;
  try {
    await new Promise((resolve,reject)=>{let timer=setTimeout(()=>reject(Error('Servidor não iniciou')),5000);server.stdout.once('data',()=>{clearTimeout(timer);resolve()});server.once('exit',()=>reject(Error('Servidor encerrou antes de iniciar')))});
    let errors=[];const vc=new VirtualConsole();vc.on('jsdomError',e=>errors.push(e.message));
    dom=new JSDOM(fs.readFileSync(path.join(root,'public/index.html'),'utf8'),{url:`http://127.0.0.1:${port}/`,runScripts:'outside-only',virtualConsole:vc});
    const w=dom.window;w.fetch=(url,opts)=>fetch(new URL(url,w.location.href),opts);w.alert=x=>{throw Error('alert: '+x)};w.confirm=()=>true;
    w.eval(fs.readFileSync(path.join(root,'public/app.js'),'utf8'));
    await new Promise(r=>setTimeout(r,350));
    for(const [page,text] of [['Dashboard','Prepare-se com propósito'],['Disciplinas','Ortografia e acentuação'],['Simulados','Monte seu simulado'],['Materiais','Todos os materiais'],['Minhas anotações','Suas anotações'],['Assistente IA','Perguntar à IA'],['Desempenho','Desempenho por assunto'],['Acervo','Bancas reais']]){
      w.go(page);await new Promise(r=>setTimeout(r,100));if(!w.document.body.textContent.includes(text)) throw Error(`${page} não carregou`);console.log(page,'OK');
    }
    w.go('Acervo'); if(!w.document.body.textContent.includes('44 / 1.200') || !w.document.body.textContent.includes('COBIT 2019 · 1 questões')) throw Error('Inventário inconsistente');
    w.study(encodeURIComponent('Docker'));if(!w.document.body.textContent.includes('Dockerfile reference'))throw Error('material Docker ausente');
    w.setup(encodeURIComponent('Docker'));if(w.document.querySelector('#scope').value!=='Docker')throw Error('filtro não selecionado');
    await new Promise(r=>setTimeout(r,150));if(errors.length)throw Error(errors.join('\n'));console.log('Assunto e filtro OK');
  } finally {if(dom)dom.window.close();server.kill();fs.rmSync(dir,{recursive:true,force:true})}
})().catch(e=>{console.error(e);process.exitCode=1});
