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

## Coleta adicional

- Incluídas questões FCC sobre [RUP](https://www.qconcursos.com/questoes-de-concursos/questoes/1ee1aff0-58), [árvores](https://www.qconcursos.com/questoes-de-concursos/questoes/27f8da2a-57), [CSS](https://www.qconcursos.com/questoes-de-concursos/questoes/46262962-c8), [SQL](https://www.qconcursos.com/questoes-de-concursos/questoes/72ae1f92-16) e [padrões web](https://www.qconcursos.com/questoes-de-concursos/questoes/d5ff0e70-96), com respostas corroboradas por comentário em fonte secundária, não por gabarito definitivo. Acervo total: 37 questões (24 FCC, cinco de outras bancas e oito inéditas). Coleta e cobertura continuam incompletas.

- Primeiras questões de conhecimentos básicos: [crase](https://www.qconcursos.com/questoes-de-concursos/questoes/2d90a582-57), [raciocínio lógico](https://www.qconcursos.com/questoes-de-concursos/questoes/1dfb96f6-d7) e [liderança](https://www.qconcursos.com/questoes-de-concursos/questoes/5f248344-0c), todas FCC e com respostas verificadas em fonte secundária ou tecnicamente, mas sem gabarito definitivo original. Total: 40 (27 FCC, cinco de outras bancas e oito inéditas).

## Dimensionamento e inventário

- Meta inicial indicada: aproximadamente 1.200 questões, com prioridade para específicos; referências por subtema: 20 menores, 40 comuns, 60–100 centrais e acima de 100 quando houver disponibilidade. São metas, não dados coletados; a classificação e a distribuição detalhada por subtema permanecem pendentes. A soma das metas por subtema poderá superar a referência global aproximada, dependendo da classificação.
- Adicionadas quatro questões reais de outras bancas: [Kubernetes](https://www.qconcursos.com/questoes-de-concursos/questoes/bd6eecd5-7b), [COBIT 2019](https://www.qconcursos.com/questoes-de-concursos/questoes/a4151b66-76), [Singleton](https://www.qconcursos.com/questoes-de-concursos/questoes/f8a07ce4-38) e [Docker](https://www.qconcursos.com/questoes-de-concursos/questoes/6321429a-98). Fontes secundárias; alternativas verificadas tecnicamente ou por comentário secundário, sem confirmação de gabarito oficial definitivo.
- Banco novo: 44 questões, 27 FCC, 9 de outras bancas e 8 inéditas. A coleta está incompleta e distante das metas. Não se demonstrou esgotamento das questões reais disponíveis.
- A tela Acervo usa agregação do SQLite, mostra zeros para subtemas sem questões e separa inéditas de bancas reais por nível hierárquico. O progresso compara o total disponível à referência global, sem afirmar que a distribuição de metas individuais foi definida.
- Testados: 16 testes Python de integração e migração com locale ASCII; teste de navegação e inventário em DOM simulado. Não é teste visual em navegador ou Windows real.

## Auditoria e conflito no dimensionamento

- Os 128 subtemas atualmente organizados na aplicação implicam ao menos 2.560 questões usando a menor faixa solicitada (20 cada); faixas intermediárias e centrais elevam esse valor. Assim não é possível distribuir um total de aproximadamente 1.200 e simultaneamente cumprir as faixas mínimas em todos os subtemas. Não foram inventadas metas individuais abaixo dos mínimos nem declarada conclusão; é necessária decisão sobre a meta global ou o agrupamento dos subtemas.
- Migração adiciona estado e fonte da classificação do gabarito, sem modificar respostas ou histórico. Reais legadas foram marcadas como não confirmadas e inéditas como revisão editorial pendente. Não foi encontrada evidência de gabarito definitivo: 36 reais não confirmadas, oito inéditas pendentes, zero definitivos confirmados no banco inicial. O documento de gabarito do TRF-3 é reproduzido em repositório secundário e não teve condição definitiva comprovada; não foi reclassificado.
- A tela de revisão declara a situação e informa que correções de reais pendentes são provisórias. O painel Acervo distingue não confirmadas, preliminares, definitivas, anuladas e revisão editorial; uma classificação definitiva sem URL de fonte não conta como confirmada. O sistema ainda não possui interface para pesquisar ou validar documentos automaticamente e não se comprova inexistência de anulações nas questões antigas.
- Questões anuladas ou estruturalmente inválidas são excluídas de novos simulados; a contagem estrutural não é prova de ausência de duplicidades nem de revisão técnica independente. A lista de dois descartes é parcial, não um registro completo de todas as pesquisas. A tabela de metas explicita que a definição individual está pendente, sem fabricar números.
- Testados 18 testes de integração Python com locale ASCII, incluindo migração e preservação de histórico, situação de gabarito e exclusão de anuladas ou registros inválidos; navegação DOM simulada passou. Não houve teste em Windows real nem auditoria completa de fontes oficiais.

## Decisão sobre agrupamento das metas

- Em resposta ao conflito registrado acima, o usuário escolheu manter aproximadamente 1.200 questões e agrupar subtemas relacionados somente para definir metas, sem omitir conteúdos do edital. A decisão substitui a pendência de conciliação descrita na seção anterior.
- `data/question_goals.json` registra 42 grupos com metas compartilhadas, cobrindo cada um dos 128 subtemas da navegação exatamente uma vez. Há 28 grupos com meta 20, 12 com meta 40 e dois com meta 80, totalizando 1.200; conhecimentos específicos têm meta 800 e os básicos 400. É uma proposta editorial de prioridade, não um levantamento de disponibilidade de provas ou garantia de cobertura proporcional dentro de cada grupo.
- A tabela apresenta atual por subtema e atual/meta/faltante/percentual compartilhados pelo grupo. Esses valores do grupo se repetem nas suas linhas e não devem ser somados entre elas. As quantidades atuais excluem registros anulados e estruturalmente inválidos, mas ainda incluem gabaritos pendentes e não comprovam inexistência de duplicatas.
- Testes verificam cobertura única, total 1.200, prioridade de específicos, metas permitidas e soma dos registros elegíveis. 19 testes Python passaram com locale ASCII, assim como o teste UI em DOM simulado. A coleta, confirmação de gabaritos e auditoria de duplicação continuam incompletas; nenhuma alegação de conclusão.

### Continuação da coleta — 22/11/2026

- Adicionadas sete questões FCC pertinentes aos conhecimentos específicos: [UML Q39546](https://www.qconcursos.com/questoes-de-concursos/questoes/184c38e2-57), [HTML Q122703](https://www.qconcursos.com/questoes-de-concursos/questoes/03500f6b-92), [recursividade Q39539](https://www.qconcursos.com/questoes-de-concursos/questoes/0fcefcf4-57), [HTTP Q1965281](https://www.qconcursos.com/questoes-de-concursos/questoes/b311bf58-3a), [REST Q841091](https://www.qconcursos.com/questoes-de-concursos/questoes/7ad9ae11-9f), [mineração de dados Q841717](https://www.qconcursos.com/questoes-de-concursos/questoes/38de8c48-a2) e [SQL Q61264](https://www.qconcursos.com/questoes-de-concursos/questoes/b59f9e8e-ac). A resposta é técnica ou extraída de fonte secundária, **não comprovadamente definitiva**. A questão SQL adota a classificação de SELECT como DML expressa no contexto da própria prova.
- Descartadas desta coleta: Q62239 e Q62238, sinalizadas como anuladas na [fonte consultada](https://www.qconcursos.com/questoes-de-concursos/questoes?discipline_ids%5B%5D=96&examining_board_ids%5B%5D=1&page=75); Q39545, por comentário indicando possível ambiguidade; Q762153, por possuir quatro alternativas incompatíveis com o formato atual. Outras candidatas não foram consideradas revisadas ou esgotadas.
- Banco inicial atualizado: 51 questões, sendo 34 FCC, nove de outras bancas e oito inéditas; 43 reais sem confirmação de gabarito definitivo e oito inéditas aguardando revisão. Faltam 1.149 para a meta estrutural de 1.200. A auditoria integral de duplicidade e a confirmação oficial dos gabaritos permanecem pendentes; a contagem não comprova validação completa.
- Verificação: 19 testes Python sob locale ASCII e teste de navegação DOM passaram; não substituem testes em Windows real nem auditoria de conteúdo.

### Ampliação de inéditas — 22/11/2026

- Acrescentadas 24 questões geradas por IA, identificadas como **INÉDITA — ESTILO FCC**, em tópicos do edital que incluem estruturas de dados, .NET, serviços web, dados, segurança, redes, acessibilidade e IA. Cada uma traz cinco alternativas, uma resposta proposta e explicação. São exercícios autorais, não provas da FCC; todas continuam com revisão editorial independente pendente.
- O arquivo `data/original_questions.json` é importado em bancos novos e existentes sem remover respostas ou histórico; há verificação estrutural e comparação de similaridade na importação. Isso não constitui auditoria completa de duplicidade ou de qualidade pedagógica.
- Banco inicial: 75 questões estruturalmente válidas (34 FCC, nove de outras bancas e 32 inéditas). Das reais, 43 continuam sem gabarito definitivo confirmado; das inéditas, 32 aguardam revisão independente. Faltam 1.125 para a meta estrutural de 1.200; a meta de questões válidas e auditadas não foi atingida.

### Continuação — 22/11/2026

- Acrescentada a questão real FCC [Q807362](https://www.qconcursos.com/questoes-de-concursos/questoes/5e6c9bd8-2b), sobre testes caixa-preta e caixa-branca, com origem consultada em fonte secundária e resposta tecnicamente proposta; gabarito definitivo não confirmado. A candidata [Q948772](https://www.qconcursos.com/questoes-de-concursos/questoes/ce639137-ef) não foi importada: a alternativa sobre “iterações” merece conferência no caderno e no gabarito antes de se assumir que é “interações”. [Q1014870](https://www.qconcursos.com/questoes-de-concursos/questoes/633f3019-bc) também não foi importada, por imprecisão entre arquivo e diretório na alternativa aparentemente pretendida.
- Adicionadas 20 inéditas geradas por IA em tópicos do edital, identificadas e pendentes de revisão editorial independente. As explicações não substituem validação independente nem conferência integral de duplicidade.
- Banco inicial: 96 questões estruturalmente válidas (35 FCC, nove de outras bancas e 52 inéditas). Gabaritos de 44 reais não confirmados; 52 inéditas aguardam revisão. Faltam 1.104 para a meta estrutural de 1.200; a meta de questões válidas e auditadas ainda não foi alcançada.

### Pesquisa adicional FCC — 22/11/2026

- Adicionadas [Q264687, primeira forma normal](https://www.qconcursos.com/questoes-de-concursos/questoes/a3053797-09), [Q526147, camadas OSI](https://www.qconcursos.com/questoes-de-concursos/questoes/fb462444-28), [Q1165796, Abstract Factory](https://www.qconcursos.com/questoes-de-concursos/questoes/3738dadc-8f) e [Q585740, Factory Method](https://www.qconcursos.com/questoes-de-concursos/questoes/ece1bd14-9e). Origem e alternativas foram consultadas em fonte secundária; respostas são técnicas ou comentadas, sem confirmação de gabarito oficial definitivo. A fonte de Q1165796 reproduz “classes completas”; a formulação técnica é “classes concretas” e a conferência do caderno original continua pendente.
- Não importadas: [Q807357](https://www.qconcursos.com/questoes-de-concursos/questoes/5e5e13d2-2b), por formulações absolutas ou imprecisas sobre data warehouse; [Q841715](https://www.qconcursos.com/questoes-de-concursos/questoes/38d9158d-a2), pois a afirmação de que toda tabela fato deve conter atributos numéricos precisa de exame diante de tabelas fato sem fatos; [Q87894](https://www.qconcursos.com/questoes-de-concursos/questoes/6f93d8b3-61), por sobreposição substancial com questão inédita já cadastrada sobre comprimentos de endereços IP. Essas decisões não constituem auditoria global.
- Banco inicial: 100 questões estruturalmente válidas, 39 FCC, nove de outras bancas e 52 inéditas; 48 reais com gabarito não confirmado e 52 inéditas com revisão pendente. Faltam 1.100 para a meta estrutural, que não equivale à meta auditada.

### Pesquisa FCC — continuação de 22/11/2026

- Cadastradas [Q592746](https://www.qconcursos.com/questoes-de-concursos/questoes/256f2211-b5) (casos de uso UML), [Q370965](https://www.qconcursos.com/questoes-de-concursos/questoes/130a923b-ca) (pilhas) e [Q486739](https://www.qconcursos.com/questoes-de-concursos/questoes/af65e596-ce) (mineração de dados). Enunciados consultados em fonte secundária e respostas verificadas tecnicamente, sem prova de gabarito oficial definitivo. A questão UML cobra conceito geral e não identifica a versão da notação.
- Não importada [Q265044](https://www.qconcursos.com/questoes-de-concursos/questoes/61092f52-0d), por forte semelhança com Q370965, selecionada neste lote. Q463755 não foi importada por sobreposição com exercício já cadastrado sobre encapsulamento. Isso não substitui auditoria integral de duplicidade.
- Banco inicial: 103 questões estruturalmente válidas (42 FCC, nove de outras bancas, 52 inéditas). Permanecem 51 reais sem gabarito definitivo confirmado e 52 inéditas com revisão independente pendente. Faltam 1.097 para a meta estrutural; não se demonstrou a meta de questões auditadas.
