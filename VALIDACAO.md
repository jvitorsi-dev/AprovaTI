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
