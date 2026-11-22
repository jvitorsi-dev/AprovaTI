# AprovaTI — CETESB 2026

Aplicação individual local para o edital nº 01/2026, Analista de TI – Sistemas. Não há autenticação. Requer Python 3.9+; não há dependências externas para execução.

```sh
python3 server.py
# abra http://localhost:8000
```

O servidor escuta em `0.0.0.0` para suporte à prévia. Use somente em ambiente privado: não possui autenticação nem proteção para exposição pública. Dados persistem em `data/study.db` (SQLite), criado automaticamente. Faça backup desse arquivo; ele não é versionado. O PDF anexado está em `public/edital.pdf`.

A tela **Acervo** apresenta as contagens reais do SQLite por disciplina, tema, subtema, tipo e banca, incluindo assuntos ainda sem questões. A referência inicial é aproximadamente 1.200 questões; a classificação de subtemas por tamanho e as metas individuais ainda não foram estabelecidas.

## Escopo e limitações

- Conteúdo básico transcrito do Anexo III do PDF fornecido; tópicos específicos organizados para navegação. A transcrição completa específica deve ser conferida no PDF, páginas 59–60. Não houve verificação de retificações.
- Acervo limitado: vinte e sete questões reais FCC, nove de outras bancas e oito exercícios editoriais inéditos. Dez questões FCC vieram do caderno 02, tipo 001, de Analista de Informática do TRF-3 (2019), com relação aos tópicos de Sistemas explicitada na revisão. As questões reais foram identificadas em fontes secundárias. Os gabaritos definitivos das questões FCC não foram confirmados; dez foram conferidas com um gabarito divulgado e as anteriores foram verificadas tecnicamente; consulte a situação em cada questão. Não houve coleta automatizada persistente de provas nem busca exaustiva. Não há cobertura em muitos assuntos, inclusive em disciplinas básicas. A situação da verificação do gabarito é informada individualmente em cada questão.
- Questões editoriais tiveram validação estrutural e revisão textual; não há validação independente automatizada de unicidade ou correção técnica. Não há geração de questões por IA.
- Links de materiais técnicos são específicos aos assuntos listados, mas a disponibilidade não foi checada de forma automatizada; muitos subtemas não possuem material.
- A IA é opcional e experimental: exige um provedor configurado pelo operador e não está ativa por padrão. Tem busca lexical em um conjunto limitado de resumos, não possui RAG completo nem validação independente. Avaliações geradas permanecem indisponíveis; ausência de resultados não prova ausência no edital. Consulte a seção de configuração abaixo.
- Rotação exclui questões respondidas em simulados finalizados, globalmente e também em filtros sobrepostos. Questões não respondidas e simulados abandonados não contam como utilizadas. Repetição é opcional, com preferência por erros da última resposta quando solicitada. O ciclo pode ser reiniciado para o conjunto de filtros escolhido, sem apagar o histórico. Sem autenticação, o banco representa um único usuário. O relógio usa o navegador.
- Anotações aceitam Markdown como texto, sem editor visual ou renderização. Autosave é iniciado após breve pausa de digitação.
- Há uma verificação simples de similaridade de enunciado e alternativas ao acrescentar o acervo versionado; não substitui revisão manual. Não há coleta automatizada, testes gerados, busca semântica, ou indicadores de evolução temporal. Estatísticas são derivadas dos simulados finalizados. O histórico exibido é limitado aos dez mais recentes.

## Arquitetura

Servidor HTTP padrão da biblioteca Python e SQLite (`server.py`); interface responsiva estática (`public/`); conteúdo inicial em `data/seed.py` e `data/basics.json`. O servidor não envia gabaritos de simulados abertos. Dados de origem, autenticidade e validação aparecem na revisão. Materiais técnicos e edital são separados na interface. Como é aplicação local, sem contas, a API não deve ser publicada na internet.

## Fontes

- Edital CETESB nº 01/2026, PDF fornecido pelo usuário, Anexo III.
- Questões reais: fontes específicas em `data/real_questions.json` e https://www.qconcursos.com/questoes-de-concursos/questoes/544d5320-98
- Materiais específicos e instituições: cadastrados em `data/seed.py` e apresentados na aplicação.
- Prova FCC TRF-3 2019: https://arquivos.qconcursos.com/prova/arquivo_prova/66070/fcc-2019-trf-3-regiao-analista-judiciario-informatica-prova.pdf. Gabarito consultado: https://arquivos.qconcursos.com/prova/arquivo_gabarito/66070/fcc-2019-trf-3-regiao-analista-judiciario-informatica-gabarito.pdf. Não se confirmou que seja definitivo.

Execute `python3 -m unittest discover -s tests -v` para os testes de integração isolados. Consulte `VALIDACAO.md` para resultados e pendências.

### Acompanhamento de estudo

A marcação manual por subtema é persistida em SQLite. O painel sugere revisão de tópicos com algum erro ou cuja marcação tenha sete dias ou mais. Esta regra é simples e não é um algoritmo adaptativo.

### Teste de navegação no DOM (opcional)

`npm ci && npm run test:ui` executa verificação de navegação com jsdom e banco temporário. É uma simulação de DOM, não um teste visual ou teste em navegador real. A aplicação em si continua requerendo apenas Python.

### Assistente opcional (experimental)

A busca lexical continua funcionando sem serviço externo. Para gerar respostas, configure um servidor OpenAI-compatible Chat Completions acessível pelo processo Python e reinicie o servidor:

```sh
export APROVATI_AI_URL="http://localhost:1234/v1/chat/completions"
export APROVATI_AI_MODEL="nome-do-modelo"
# Opcional: APROVATI_AI_KEY em variável de ambiente no servidor, se o provedor exigir.
python3 server.py
```

A URL é configuração do servidor, não recebida do navegador. HTTP é aceito apenas para localhost; provedores remotos exigem HTTPS. Não versione segredos. Pergunta e trechos selecionados são enviados ao provedor configurado: evite informações sensíveis e confira as políticas de privacidade. Na prévia, conectividade externa é limitada e não há provedor pré-configurado.

O modo edital consulta exclusivamente trechos extraídos do PDF anexo; nenhuma retificação foi verificada. O modo técnico usa apenas quatro resumos editoriais com fontes documentais (`data/knowledge.json`); não baixa nem indexa páginas automaticamente. O aplicativo fornece os links, exige marcações de referência existentes e rejeita URLs geradas pelo modelo. Isso não verifica a veracidade de cada afirmação; modelos podem errar ou não seguir instruções. A geração de avaliações não está implementada e é proibida no prompt; filtros de texto não garantem bloqueio de pedidos indiretos. Não use respostas do modelo como material validado sem conferir as fontes. O histórico permanece no SQLite e não é enviado automaticamente em consultas seguintes. Enquanto existir qualquer simulado aberto, a API bloqueia novas respostas da IA; a tela Simulados permite continuar ou descartar simulados abertos.

### Textos com acentuação incorreta em bancos antigos

Após atualizar e reiniciar o servidor, o banco existente recebe uma correção automática para campos de questões distribuídas quando a corrupção de codificação pode ser identificada com segurança pela fonte versionada. Isso preserva IDs, respostas e anotações. Antes de atualizar, faça uma cópia de segurança de `data/study.db` com o servidor parado. Textos pessoais ou modificações diferentes da fonte não são corrigidos automaticamente.
