import json
import tempfile
import threading
import unittest
from unittest import mock
import urllib.error
import urllib.request
from pathlib import Path
import server

class IntegrationTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tmp=tempfile.TemporaryDirectory(); server.DB=Path(cls.tmp.name)/'test.db'; server.init()
  cls.http=server.ThreadingHTTPServer(('127.0.0.1',0),server.Handler)
  cls.thread=threading.Thread(target=cls.http.serve_forever,daemon=True); cls.thread.start()
  cls.base='http://127.0.0.1:'+str(cls.http.server_port)
 @classmethod
 def tearDownClass(cls):
  cls.http.shutdown(); cls.http.server_close(); cls.thread.join(); cls.tmp.cleanup()
 def request(self,path,body=None):
  request=urllib.request.Request(self.base+path, data=json.dumps(body).encode() if body is not None else None,headers={'Content-Type':'application/json'})
  with urllib.request.urlopen(request) as response: return json.load(response)
 def test_a_seed_and_reinitialize(self):
  before=self.request('/api/data')['stats']; self.assertEqual(before['total'],29); self.assertEqual(before['kinds']['REAL — FCC'],16)
  server.init(); self.assertEqual(self.request('/api/data')['stats']['total'],29)
 def test_b_notes_persist(self):
  note=self.request('/api/notes',{'title':'Resumo','body':'conteúdo','topic':'Docker'})
  self.request('/api/notes',{'id':note['id'],'title':'Atualizado','body':'exemplo','topic':'Docker'})
  server.init(); self.assertTrue(any(x['id']==note['id'] and x['body']=='exemplo' for x in self.request('/api/notes')))
  self.request('/api/notes/delete',note); self.assertFalse(any(x['id']==note['id'] for x in self.request('/api/notes')))
 def test_c_exam_rotation_and_filter_reset(self):
  filters={'scope':'Git e controle de versões','count':5}; eid=self.request('/api/exam/start',filters)['id']; exam=self.request('/api/exam/'+str(eid)); self.assertEqual(len(exam['questions']),1)
  q=exam['questions'][0]; self.assertNotIn('answer',q); self.assertNotIn('explanation',q); self.assertNotIn('validation',q); self.assertNotIn('source',q); self.assertNotIn('answer_source',q)
  self.request('/api/exam/answer',{'exam':eid,'question':q['id'],'choice':0})
  self.request('/api/exam/finish',{'exam':eid,'elapsed':15}); self.assertEqual(self.request('/api/exam/'+str(eid))['questions'][0]['answer'],1)
  with self.assertRaises(urllib.error.HTTPError) as ctx: self.request('/api/exam/start',filters)
  self.assertEqual(ctx.exception.code,409)
  self.request('/api/exam/reset',filters); self.assertEqual(self.request('/api/exam/start',filters)['selected'],1)
  # O reinício para Docker não apaga o histórico e não altera outro filtro.
  self.assertEqual(self.request('/api/data')['stats']['answered'],1)
  with self.assertRaises(urllib.error.HTTPError): self.request('/api/exam/start',{'scope':'Git e controle de versões','kind':'real'})
 def test_d_real_fcc_and_exclude_other(self):
  with self.assertRaises(urllib.error.HTTPError) as ctx:
   self.request('/api/exam/start',{'scope':'Herança e polimorfismo','include_other':False})
  self.assertEqual(ctx.exception.code,409)
 def test_e_real_fcc_priority(self):
  eid=self.request('/api/exam/start',{'scope':'Bancos de Dados','count':1,'kind':'real'})['id']
  q=self.request('/api/exam/'+str(eid))['questions'][0]; self.assertEqual(q['kind'],'REAL — FCC'); self.assertEqual(q['board'],'FCC')
 def test_study_progress_persists(self):
  self.request('/api/study',{'subtopic':'Word 2024','studied':True}); server.init()
  self.assertTrue(any(x['subtopic']=='Word 2024' for x in self.request('/api/data')['studied']))
  self.request('/api/study',{'subtopic':'Word 2024','studied':False})
  self.assertFalse(any(x['subtopic']=='Word 2024' for x in self.request('/api/data')['studied']))
  with self.assertRaises(urllib.error.HTTPError): self.request('/api/study',{'subtopic':'inexistente'})
 def test_reference_source_separation(self):
  edital=self.request('/api/reference-search?mode=edital&q=Kubernetes')['results']
  self.assertTrue(edital); self.assertTrue(all(x['url'].startswith('/edital.pdf') for x in edital))
  tecnico=self.request('/api/reference-search?mode=tecnico&q=Docker')['results']
  self.assertTrue(tecnico); self.assertTrue(all(not x['url'].startswith('/edital.pdf') for x in tecnico))
  self.assertEqual(self.request('/api/reference-search?mode=edital&q=assuntoinexistente')['results'],[])
 def test_assistant_block_sources_history(self):
  for e in self.request('/api/exams/active'): self.request('/api/exam/discard',{'exam':e['id']})
  eid=self.request('/api/exam/start',{'scope':'Docker','count':1})['id']
  with mock.patch('server.model_response',return_value='Resposta [1]') as provider:
   with self.assertRaises(urllib.error.HTTPError) as ctx: self.request('/api/assistant',{'mode':'tecnico','question':'Explique Docker'})
   self.assertEqual(ctx.exception.code,409); provider.assert_not_called()
   self.request('/api/exam/discard',{'exam':eid})
   with self.assertRaises(urllib.error.HTTPError) as ctx: self.request('/api/assistant',{'mode':'tecnico','question':'Crie questões sobre Docker'})
   self.assertEqual(ctx.exception.code,400)
   response=self.request('/api/assistant',{'mode':'tecnico','question':'Explique Dockerfile'})
   self.assertEqual(response['answer'],'Resposta [1]'); self.assertTrue(all('docker.com' in r['url'] for r in response['sources']))
   args=provider.call_args.args; self.assertEqual(args[0],'tecnico'); self.assertTrue(all(not r['url'].startswith('/edital') for r in args[2]))
   response=self.request('/api/assistant',{'mode':'edital','question':'O edital cita Kubernetes?'})
   self.assertTrue(all(r['url'].startswith('/edital.pdf') for r in response['sources']))
   self.assertEqual(len(self.request('/api/assistant/history')),2)
  server.init(); self.assertEqual(len(self.request('/api/assistant/history')),2)
  with self.assertRaises(urllib.error.HTTPError) as ctx: self.request('/api/assistant',{'mode':'tecnico','question':'assuntoinexistente'})
  self.assertEqual(ctx.exception.code,404)
 def test_model_citation_validation(self):
  class Response:
   def __init__(self,content): self.content=content
   def __enter__(self): return self
   def __exit__(self,*args): pass
   def read(self,n): return json.dumps({'choices':[{'message':{'content':self.content}}]}).encode()
  refs=server.assistant_sources('tecnico','dockerfile')
  with mock.patch.dict('os.environ',{'APROVATI_AI_URL':'http://localhost:1234/v1/chat/completions','APROVATI_AI_MODEL':'test'}):
   for content in ['Sem referência', 'Fonte [9]', 'Fonte [1] https://exemplo.com']:
    with mock.patch('server.urllib.request.urlopen',return_value=Response(content)):
     with self.assertRaises(RuntimeError): server.model_response('tecnico','dockerfile',refs)
   with mock.patch('server.urllib.request.urlopen',return_value=Response('O Dockerfile contém instruções. [1]')):
    self.assertIn('[1]',server.model_response('tecnico','dockerfile',refs))
 def test_fcc_new_questions_editais_e_origem(self):
  c=server.db(); rows=list(c.execute('select * from questions where question_number is not null'))
  self.assertEqual(len(rows),10)
  basics=json.loads((server.ROOT/'data/basic_topics.json').read_text(encoding='utf-8'))
  subjects={**basics,**server.TOPICS}
  for q in rows:
   self.assertEqual(q['board'],'FCC'); self.assertIn(q['subtopic'],subjects[q['topic']])
   self.assertTrue(q['edital_basis']); self.assertTrue(q['answer_source'].startswith('https://'))
   self.assertIn('não foram confirmados',q['validation'])
  self.assertEqual({r['question_number'] for r in rows},{21,22,23,26,29,32,37,38,46,58})
  c.close()
 def test_json_files_use_explicit_utf8(self):
  original = Path.read_text
  seen = set()
  def checked(path, *args, **kwargs):
   if path.suffix == '.json':
    self.assertEqual(kwargs.get('encoding'), 'utf-8', str(path))
    seen.add(path.name)
   return original(path, *args, **kwargs)
  with mock.patch.object(Path, 'read_text', checked):
   server.init()
   self.request('/api/data')
   self.request('/api/study', {'subtopic':'Word 2024', 'studied':True})
   server.assistant_sources('edital', 'Kubernetes')
   server.assistant_sources('tecnico', 'Dockerfile')
  self.assertEqual(seen, {'real_questions.json','basics.json','basic_topics.json','specific.json','knowledge.json'})
  self.request('/api/study', {'subtopic':'Word 2024', 'studied':False})
 def test_f_duplicate_normalization(self):
  c=server.db(); q=c.execute('select prompt,options from questions limit 1').fetchone()
  self.assertTrue(server.duplicate(c,{'prompt':q['prompt'].upper(),'options':json.loads(q['options'])})); c.close()

class MojibakeMigrationTests(unittest.TestCase):
 def test_existing_database_migrates_and_preserves_history(self):
  previous = server.DB
  try:
   with tempfile.TemporaryDirectory() as temp:
    server.DB=Path(temp)/'legacy.db'
    c=server.db()
    c.executescript("""CREATE TABLE questions(id INTEGER PRIMARY KEY,topic TEXT,subtopic TEXT,prompt TEXT,options TEXT,answer INTEGER,explanation TEXT,kind TEXT,board TEXT,year INTEGER,origin TEXT,role TEXT,source TEXT,difficulty TEXT,validation TEXT,collected TEXT);
    CREATE TABLE notes(id INTEGER PRIMARY KEY,topic TEXT,title TEXT,body TEXT,updated TEXT DEFAULT CURRENT_TIMESTAMP);
    CREATE TABLE exams(id INTEGER PRIMARY KEY,created TEXT DEFAULT CURRENT_TIMESTAMP,finished TEXT,elapsed INTEGER DEFAULT 0,scope TEXT);
    CREATE TABLE answers(exam_id INTEGER,question_id INTEGER,choice INTEGER,marked INTEGER DEFAULT 0,position INTEGER, PRIMARY KEY(exam_id,question_id));""")
    q=json.loads((server.ROOT/'data/real_questions.json').read_text(encoding='utf-8'))[0]
    c.execute('INSERT INTO questions(id,topic,subtopic,prompt,options,answer,explanation,kind,board,year,origin,role,source,difficulty,validation,collected) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (42,q['topic'],q['subtopic'],q['prompt'],json.dumps(q['options']),q['answer'],q['explanation'],q['kind'],q['board'],q['year'],q['origin'],q['role'],q['source'],q['difficulty'],q['validation'],q['collected']))
    c.execute("INSERT INTO notes(id,title,body) VALUES(1,'Teste','preservado')")
    c.execute("INSERT INTO exams(id,scope,finished) VALUES(1,'SQL',CURRENT_TIMESTAMP)")
    c.execute('INSERT INTO answers(exam_id,question_id,choice,position) VALUES(1,42,2,0)')
    c.commit();c.close();server.init();server.init();c=server.db()
    self.assertEqual(c.execute('SELECT body FROM notes WHERE id=1').fetchone()[0],'preservado')
    self.assertEqual(c.execute('SELECT choice FROM answers WHERE exam_id=1 AND question_id=42').fetchone()[0],2)
    self.assertEqual(c.execute('SELECT count(*) FROM questions WHERE question_number IS NOT NULL').fetchone()[0],10)
    self.assertEqual(c.execute('SELECT count(*) FROM questions WHERE source=?',(q['source'],)).fetchone()[0],1)
    c.close()
  finally: server.DB=previous
 def test_repair_preserves_user_data_and_is_idempotent(self):
  previous = server.DB
  try:
   with tempfile.TemporaryDirectory() as temp:
    server.DB = Path(temp) / 'existing.db'
    server.init()
    c = server.db()
    q = c.execute("SELECT * FROM questions WHERE source LIKE '%a7c4739a-d4'").fetchone()
    corrupt = lambda value: value.encode('utf-8').decode('cp1252')
    c.execute('UPDATE questions SET prompt=?, kind=?, difficulty=?, explanation=? WHERE id=?',
              (corrupt(q['prompt']), corrupt(q['kind']), corrupt(q['difficulty']), 'Anotação editorial alterada', q['id']))
    other = c.execute("SELECT * FROM questions WHERE source LIKE '%17807e52-03'").fetchone()
    options = json.loads(other['options'])
    c.execute('UPDATE questions SET options=? WHERE id=?', (json.dumps([corrupt(x) for x in options],ensure_ascii=False), other['id']))
    note = c.execute('INSERT INTO notes(topic,title,body) VALUES(?,?,?)', ('SQL','Minha anotação','Não modificar Ã©')).lastrowid
    exam = c.execute("INSERT INTO exams(scope,finished) VALUES('SQL',CURRENT_TIMESTAMP)").lastrowid
    c.execute('INSERT INTO answers(exam_id,question_id,choice,position) VALUES(?,?,?,?)', (exam,q['id'],2,0))
    c.commit(); c.close()
    server.init(); server.init()
    c = server.db()
    updated = c.execute('SELECT * FROM questions WHERE id=?',(q['id'],)).fetchone()
    self.assertEqual(updated['prompt'],q['prompt'])
    self.assertEqual(updated['kind'],q['kind'])
    self.assertEqual(updated['difficulty'],q['difficulty'])
    self.assertEqual(updated['explanation'],'Anotação editorial alterada')
    self.assertEqual(json.loads(c.execute('SELECT options FROM questions WHERE id=?',(other['id'],)).fetchone()[0]), options)
    self.assertEqual(c.execute('SELECT body FROM notes WHERE id=?',(note,)).fetchone()[0],'Não modificar Ã©')
    self.assertEqual(c.execute('SELECT choice FROM answers WHERE exam_id=? AND question_id=?',(exam,q['id'])).fetchone()[0],2)
    self.assertEqual(c.execute('SELECT count(*) FROM questions').fetchone()[0],29)
    c.close()
  finally:
   server.DB = previous

if __name__=='__main__': unittest.main()
