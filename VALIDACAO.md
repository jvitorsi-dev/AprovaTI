# Relatório de validação

## Executado em 22/11/2026

- `python3 -m py_compile server.py data/seed.py` e `node --check public/app.js`: passaram.
- HTTP local: página inicial retornou 200; `/api/data` retornou 9 questões, 8 inéditas e 1 real de outra banca.
- Notas: criação, leitura e exclusão via API passaram.
- Simulado filtrado por Docker: seleção limitada ao estoque, ocultação do gabarito durante a prova, resposta, finalização e apresentação do gabarito passaram.
- Rotação: tentativa de novo simulado Docker após responder sua única questão retornou 409; com repetição permitida retornou uma questão.
- Reinício do servidor: banco SQLite e dados iniciais permaneceram disponíveis. Dados de teste foram removidos.
- Conferência manual: a questão FGV tem enunciado, alternativas, identificação e resposta D na página do QConcursos. As questões inéditas são identificadas como tais, não como provas reais.
- Os trechos de conhecimentos básicos e específicos foram extraídos do PDF fornecido; o PDF está disponível para conferência.

## Problemas e correções

- A extração de texto do PDF não estava disponível por padrão; usou-se pypdf apenas na preparação, sem dependência de execução.
- Extração do texto adicionava número de página ao programa específico; esse número foi removido da transcrição.
- Questões insuficientes são explicitadas e a seleção retorna apenas as disponíveis; a interface informa esgotamento e oferece repetição.

## Pendências importantes

- Não foi realizado teste automatizado de navegador, responsividade visual ou acessibilidade com tecnologia assistiva.
- Links técnicos não foram verificados automaticamente quanto à disponibilidade ou correspondência; a cobertura de materiais é parcial.
- Não se verificaram retificações, gabaritos oficiais da FCC ou coleta abrangente; nenhuma questão FCC foi incorporada. A fonte secundária da questão FGV informa o gabarito comentado, mas não foi cotejada com gabarito definitivo original.
- Não existe pipeline de coleta persistente; a verificação de similaridade foi adicionada posteriormente para o carregamento do acervo versionado. O conjunto inicial é pequeno e não contém duplicações intencionais; não foi submetido a uma ferramenta de similaridade.
- Não foi feita validação independente de correção, ambiguidades e alternativa única para as questões inéditas. A validação automatizada aplicada na inicialização verifica somente quantidade, alternativas distintas e índice de resposta válido.
- IA, avaliações geradas e suas validações não foram implementadas; a tela informa a indisponibilidade e não simula respostas.
- A organização dos tópicos básicos em subtemas navegáveis, cobertura individual de todos os subtemas, reinicialização de ciclo, preferência por erros e revisão baseada em tempo não foram implementadas.
- Não foi testado restauro de backup do SQLite. O sistema é de uso privado e não possui autenticação.

## Continuação — 22/11/2026

- Adicionadas duas questões identificadas como FCC e uma de outra banca, com fonte, ano, cargo, data de coleta e qualificação da validação. O gabarito definitivo original não foi localizado; as respostas FCC foram conferidas tecnicamente e não devem ser entendidas como cotejadas ao gabarito definitivo.
- Adicionada verificação de similaridade (normalização e comparação de enunciado e alternativas) na carga das novas questões; não cobre diferenças maiores ou detecção semântica.
- Corrigido vazamento potencial de resposta pela fonte e pelo campo de validação nas respostas da API durante o simulado.
- Adicionados reinício do ciclo por filtro, exclusão de outras bancas e prioridade para erros na repetição; reinício não exclui o histórico.
- `python3 -m unittest discover -s tests -v`: seis testes passaram, usando SQLite temporário. Verificam carga idempotente, notas, rotação, reset, ocultação do gabarito, filtros e duplicidade normalizada. Não cobrem navegação em navegador, disponibilidade de links, todas as combinações de filtros nem validação editorial completa.
- Continuam pendentes coleta automática abrangente, fontes oficiais de gabarito para essas questões, expansão do acervo e materiais, assistente IA e teste visual/responsivo.

## Navegação e cobertura — continuação

- Acrescentada questão FCC TRT-18 2023 sobre Docker, a partir da fonte secundária com comentário de gabarito; não houve cotejo com gabarito definitivo.
- Disciplinas básicas organizadas em assuntos navegáveis, marcação manual de assuntos estudados persistente e sugestão de revisão por erro ou sete dias desde a marcação.
- Corrigidas colisões com `window.top` e `window.performance` que impediam a abertura de telas no navegador.
- Sete testes de integração Python passaram. `npm run test:ui` passou em ambiente DOM simulado, verificando as sete telas e navegação para o assunto Docker. Isso não valida apresentação visual, telas móveis ou compatibilidade em navegadores reais.
- O número total de questões é 13; as principais pendências anteriores continuam, particularmente coleta em escala, verificação de gabaritos oficiais, cobertura de materiais e assistente IA.

- A tela do assistente agora oferece busca lexical sem IA, com segregação entre os trechos do edital e o catálogo de materiais técnicos. O teste automatizado verificou separação de URLs e retorno vazio para termos inexistentes. Ela não interpreta nem responde perguntas e não substitui um assistente ou mecanismo RAG.
- Foram executados oito testes Python e o teste de navegação em DOM após esta alteração.

## Assistente opcional — continuação

- Implementado cliente de Chat Completions opcional configurado por ambiente; nenhum modelo ou credencial está incluído, nem se realizou chamada a provedor real neste ambiente.
- Modo edital e modo técnico usam conjuntos separados. O modo técnico usa quatro resumos editoriais limitados, não uma cópia completa das fontes nem consulta em tempo real. A correspondência por palavras pode perder resultados ou recuperar conteúdo irrelevante.
- A resposta é rejeitada se não houver marcador de fonte válido ou se contiver URL gerada; essas verificações não garantem correção factual ou citação de todas as afirmações. Não há verificação independente do texto gerado.
- O servidor bloqueia consulta à IA quando há simulados abertos, verifica novamente após o provedor responder e permite descartar simulados pendentes. O histórico é persistido; testes usaram um provedor simulado, não um modelo real.
- A geração de avaliações permanece desativada, com orientação ao modelo e bloqueio textual preventivo; o filtro não garante resistência a pedidos indiretos.
- Dez testes de integração Python e navegação simulada em DOM foram executados com sucesso. A acessibilidade visual e o funcionamento com serviços reais ainda não foram testados.

## Correção de textos corrompidos por codificação

- As leituras JSON usam UTF-8 explícito desde o commit anterior. Foi adicionada uma migração na inicialização que repara exclusivamente textos de questões distribuídas cujo conteúdo é uma conversão reversível de UTF-8 para cp1252 ou latin-1 e coincide com a fonte versionada. Os IDs, respostas e anotações são preservados; não altera textos pessoais ou divergentes.
- Um teste cria um banco existente com enunciado, classificação, dificuldade e alternativas corrompidos, e verifica a restauração, a idempotência e a preservação de dados de usuário. A suíte de 12 testes passou com codificação padrão ASCII; navegação simulada em DOM também passou. Não foi executado teste em Windows real.

## Ampliação do banco — recorte da opção Sistemas

- Foram incorporadas dez questões da FCC, TRF-3, Analista de Informática, 2019, caderno 02, tipo 001: 21, 22, 23, 26, 29, 32, 37, 38, 46 e 58. As letras foram cotejadas com o gabarito publicado no repositório, mas não se confirmou sua condição definitiva ou a existência de anulações posteriores.
- A relação de cada nova questão com o edital de Sistemas é mostrada na revisão. Conceitos como Scrum, coesão e acoplamento, modelo espiral e formatos de caso de uso são aplicações de tópicos previstos, não termos necessariamente literais do edital; isso é explicitado na aplicação. Questões de CPM e BSC inicialmente consideradas foram retiradas para não ampliar indevidamente o escopo.
- A origem e o link do gabarito só são exibidos após a finalização; as colunas adicionais são migradas sem apagar as respostas. Testes cobrem migração de banco antigo, idempotência, vínculo com temas, rótulos e ocultação do gabarito.
- O acervo total passa a 25 questões (15 FCC, duas reais de outra banca e oito inéditas). Continua muito aquém do volume solicitado, sem coleta exaustiva, gabaritos definitivos ou cobertura integral de disciplinas e subtemas. A extração foi feita a partir de pesquisa nas fontes identificadas, não por um coletor automático persistente.

- Acrescentadas ainda questões FCC sobre pilhas (MPE-AP 2012, [Q251345](https://www.qconcursos.com/questoes-de-concursos/questoes/c7d336fd-e5)) e contêineres ([Q1965267](https://www.qconcursos.com/questoes-de-concursos/questoes/b2e68d96-3a)); respostas conferidas tecnicamente, sem localização de gabarito original definitivo.
- A questão 30 de APF do TRF-3 2019 foi excluída por divergência entre gabarito divulgado e correção independente; requer confirmação do caderno, gabarito definitivo e eventuais recursos. A questão [Q13900](https://www.qconcursos.com/questoes-de-concursos/questoes/e0bfdde0-07) foi descartada por ambiguidade no enunciado relativo a JOIN.

## Continuação da coleta

- Incluídas [Q1965284](https://www.qconcursos.com/questoes-de-concursos/questoes/b31b8eab-3a) (FCC, JSON), [Q892479](https://www.qconcursos.com/questoes-de-concursos/questoes/91f6bb62-57) (CESGRANRIO, JSON/JavaScript), [Q491591](https://www.qconcursos.com/questoes-de-concursos/questoes/5f53385f-d6) (CESGRANRIO, ordenação) e [Q1990150](https://www.qconcursos.com/questoes-de-concursos/questoes/7f08c6ea-6f) (CEBRASPE, JSON). Origens e alternativas consultadas em fonte secundária, respostas verificadas tecnicamente; gabaritos originais definitivos não confirmados.
- Total: 29 questões (16 FCC, 5 de outras bancas e 8 inéditas). A cobertura ainda não é integral e a coleta não é exaustiva.

- Acrescentadas questões FCC de [Data Warehouse/ETL](https://www.qconcursos.com/questoes-de-concursos/questoes/1541ecad-06), [IPv6](https://www.qconcursos.com/questoes-de-concursos/questoes/48fac23b-b9) e [teste de unidade](https://www.qconcursos.com/questoes-de-concursos/questoes/a334e16d-ce). Respostas conferidas tecnicamente; gabaritos definitivos não localizados. Total agora: 32 (19 FCC, 5 outras bancas, 8 inéditas); lacunas permanecem.
