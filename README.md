# AprovaTI — CETESB 2026

Aplicação individual local para o edital nº 01/2026, Analista de TI – Sistemas. Não há autenticação. Requer Python 3.9+; não há dependências externas para execução.

```sh
python3 server.py
# abra http://localhost:8000
```

O servidor escuta em `0.0.0.0` para suporte à prévia. Use somente em ambiente privado: não possui autenticação nem proteção para exposição pública. Dados persistem em `data/study.db` (SQLite), criado automaticamente. Faça backup desse arquivo; ele não é versionado. O PDF anexado está em `public/edital.pdf`.

## Escopo e limitações

- Conteúdo básico transcrito do Anexo III do PDF fornecido; tópicos específicos organizados para navegação. A transcrição completa específica deve ser conferida no PDF, páginas 59–60. Não houve verificação de retificações.
- Acervo limitado: três questões reais FCC, duas de outras bancas e oito exercícios editoriais inéditos. As questões reais foram identificadas em fontes secundárias. As respostas das três FCC foram verificadas tecnicamente, mas seus gabaritos definitivos originais não foram localizados; consulte a situação em cada questão. Não houve coleta automatizada persistente de provas nem busca exaustiva. Não há cobertura em muitos assuntos, incluindo disciplinas básicas. O gabarito da questão real foi conferido no comentário da fonte, não em gabarito original da banca.
- Questões editoriais tiveram validação estrutural e revisão textual; não há validação independente automatizada de unicidade ou correção técnica. Não há geração de questões por IA.
- Links de materiais técnicos são específicos aos assuntos listados, mas a disponibilidade não foi checada de forma automatizada; muitos subtemas não possuem material.
- Assistente e avaliações por IA estão explicitamente desativados: não há integração de provedor, RAG, histórico de conversas ou validação independente. Há uma busca simples de referências por palavras com contextos separados, sem geração de respostas; ausência de resultados não prova ausência no edital. Nenhum segredo é solicitado.
- Rotação exclui questões respondidas em simulados finalizados, globalmente e também em filtros sobrepostos. Questões não respondidas e simulados abandonados não contam como utilizadas. Repetição é opcional, com preferência por erros da última resposta quando solicitada. O ciclo pode ser reiniciado para o conjunto de filtros escolhido, sem apagar o histórico. Sem autenticação, o banco representa um único usuário. O relógio usa o navegador.
- Anotações aceitam Markdown como texto, sem editor visual ou renderização. Autosave é iniciado após breve pausa de digitação.
- Há uma verificação simples de similaridade de enunciado e alternativas ao acrescentar o acervo versionado; não substitui revisão manual. Não há coleta automatizada, testes gerados, busca semântica, ou indicadores de evolução temporal. Estatísticas são derivadas dos simulados finalizados. O histórico exibido é limitado aos dez mais recentes.

## Arquitetura

Servidor HTTP padrão da biblioteca Python e SQLite (`server.py`); interface responsiva estática (`public/`); conteúdo inicial em `data/seed.py` e `data/basics.json`. O servidor não envia gabaritos de simulados abertos. Dados de origem, autenticidade e validação aparecem na revisão. Materiais técnicos e edital são separados na interface. Como é aplicação local, sem contas, a API não deve ser publicada na internet.

## Fontes

- Edital CETESB nº 01/2026, PDF fornecido pelo usuário, Anexo III.
- Questões reais: fontes específicas em `data/real_questions.json` e https://www.qconcursos.com/questoes-de-concursos/questoes/544d5320-98
- Materiais específicos e instituições: cadastrados em `data/seed.py` e apresentados na aplicação.
- Pesquisa adicional: prova FCC TRF-3 2019, https://arquivos.qconcursos.com/prova/arquivo_prova/66070/fcc-2019-trf-3-regiao-analista-judiciario-informatica-prova.pdf; não foi incorporada por falta de verificação cruzada com gabarito definitivo.

Execute `python3 -m unittest discover -s tests -v` para os testes de integração isolados. Consulte `VALIDACAO.md` para resultados e pendências.

### Acompanhamento de estudo

A marcação manual por subtema é persistida em SQLite. O painel sugere revisão de tópicos com algum erro ou cuja marcação tenha sete dias ou mais. Esta regra é simples e não é um algoritmo adaptativo.

### Teste de navegação no DOM (opcional)

`npm ci && npm run test:ui` executa verificação de navegação com jsdom e banco temporário. É uma simulação de DOM, não um teste visual ou teste em navegador real. A aplicação em si continua requerendo apenas Python.
