import json
import tempfile
import threading
import unittest
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
  before=self.request('/api/data')['stats']; self.assertEqual(before['total'],13); self.assertEqual(before['kinds']['REAL — FCC'],3)
  server.init(); self.assertEqual(self.request('/api/data')['stats']['total'],13)
 def test_b_notes_persist(self):
  note=self.request('/api/notes',{'title':'Resumo','body':'conteúdo','topic':'Docker'})
  self.request('/api/notes',{'id':note['id'],'title':'Atualizado','body':'exemplo','topic':'Docker'})
  server.init(); self.assertTrue(any(x['id']==note['id'] and x['body']=='exemplo' for x in self.request('/api/notes')))
  self.request('/api/notes/delete',note); self.assertFalse(any(x['id']==note['id'] for x in self.request('/api/notes')))
 def test_c_exam_rotation_and_filter_reset(self):
  filters={'scope':'Git e controle de versões','count':5}; eid=self.request('/api/exam/start',filters)['id']; exam=self.request('/api/exam/'+str(eid)); self.assertEqual(len(exam['questions']),1)
  q=exam['questions'][0]; self.assertNotIn('answer',q); self.assertNotIn('explanation',q); self.assertNotIn('validation',q); self.assertNotIn('source',q)
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
 def test_f_duplicate_normalization(self):
  c=server.db(); q=c.execute('select prompt,options from questions limit 1').fetchone()
  self.assertTrue(server.duplicate(c,{'prompt':q['prompt'].upper(),'options':json.loads(q['options'])})); c.close()
if __name__=='__main__': unittest.main()
