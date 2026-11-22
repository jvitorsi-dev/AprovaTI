# Conteúdo editorial inicial: questões inéditas revisadas, não são provas reais.
TOPICS = {
'Linguagens e Técnicas de Programação':['Tipos e representações de dados numéricos','Lógica de programação','Algoritmos e estruturas de dados','Complexidade de algoritmos','Listas e pilhas','Vetores e matrizes','Árvores e árvores balanceadas','Métodos de ordenação','Pesquisa e hashing','Orientação a objetos','Classes e objetos','Herança e polimorfismo','Encapsulamento','.NET, PHP, Python e Java','Plataforma .NET','Tipos e estruturas de dados .NET','Variáveis e enumerações .NET','Operações e expressões .NET','Instruções de controle .NET','Interfaces e classes abstratas .NET','Pacotes e exceções .NET','Coleções e tipos genéricos .NET','Attributes .NET','Sincronização e multithreading .NET','IDEs e ambientes de desenvolvimento','Jakarta EE','HTML, CSS e JavaScript'],
'Serviços Web':['API REST','JSON','XML','Microsserviços'],
'Bancos de Dados':['Bancos relacionais e multidimensionais','Modelagem conceitual, lógica e relacional','SQL ANSI/ISO','Triggers e stored procedures','Data Warehouse','Data Mining','Data Lake','Business Intelligence','Análise de Pontos de Função'],
'Metodologias de Desenvolvimento de Sistemas':['Metodologias estruturadas','Métodos ágeis','RUP','UML 2.5.1','Ferramentas CASE','Modelo de objetos e modelo relacional','Governança de Dados','Qualidade de software','Testes de software','Padrões de Projeto','Segurança no desenvolvimento','Integração de aplicações e objetos distribuídos'],
'Infraestrutura e Redes':['Modelo OSI','TCP/IP','IPv4 e IPv6','HTTP e HTTPS'],
'Acessibilidade e Usabilidade':['Conceitos e padrões','Tecnologias assistivas'],
'Inteligência Artificial':['IA generativa','RAG','Bancos de dados vetoriais','Engenharia de Prompt'],
'DevOps':['CI/CD','Git e controle de versões','Docker','Kubernetes'],
'Gestão de TI':['PMBOK 8ª edição','Governança de TI','COBIT 2019','ITIL Version 5'],
'Inglês Técnico':['Inglês Técnico']}
# título, instituição, url, descrição
MATERIALS={
'Docker':[('Dockerfile reference','Docker','https://docs.docker.com/reference/dockerfile/','Referência de instruções para construir imagens, incluindo FROM, RUN, COPY, CMD e ENTRYPOINT.')],
'Kubernetes':[('Kubernetes Components','Kubernetes','https://kubernetes.io/docs/concepts/overview/components/','Componentes do plano de controle e dos nós.')],
'Git e controle de versões':[('Getting Started - About Version Control','Git','https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control','Fundamentos de controle de versão.')],
'HTTP e HTTPS':[('HTTP Semantics, RFC 9110','IETF','https://www.rfc-editor.org/rfc/rfc9110.html','Semântica HTTP, métodos e códigos de status.')],
'API REST':[('HTTP request methods','MDN','https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods','Métodos HTTP e suas semânticas.')],
'JSON':[('The JSON Data Interchange Format, RFC 8259','IETF','https://www.rfc-editor.org/rfc/rfc8259.html','Sintaxe e interoperabilidade JSON.')],
'SQL ANSI/ISO':[('Table Expressions','PostgreSQL','https://www.postgresql.org/docs/current/queries-table-expressions.html','Expressões de tabela e tipos de JOIN; implementação PostgreSQL complementar ao SQL padrão.')],
'Herança e polimorfismo':[('Polymorphism in C#','Microsoft','https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/object-oriented/polymorphism','Polimorfismo, métodos virtuais e substituição em C#.')],
'Plataforma .NET':[('Interfaces - define behavior for multiple types','Microsoft','https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/interfaces','Interfaces e contratos em C#.')],
'HTML, CSS e JavaScript':[('HTML: HyperText Markup Language','MDN','https://developer.mozilla.org/en-US/docs/Web/HTML','Referência da linguagem de marcação HTML.')],
'RAG':[('Retrieval Augmented Generation','Microsoft','https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-overview','Arquitetura e fundamentos de RAG.')],
'Modelo OSI':[('Internet Protocol, RFC 791','IETF','https://www.rfc-editor.org/rfc/rfc791.html','Protocolo IP: referência complementar sobre a camada de rede.')],
}
# topic, prompt, options, answer zero-index, explanation
QUESTIONS=[
('SQL ANSI/ISO','Em uma consulta SQL, qual operação retorna todas as linhas da tabela à esquerda e as linhas correspondentes da tabela à direita, preenchendo com NULL quando não há correspondência?', ['INNER JOIN','LEFT JOIN','CROSS JOIN','INTERSECT','UNION'],1,'LEFT JOIN preserva todas as linhas da tabela à esquerda; INNER exige correspondência, CROSS combina pares, e INTERSECT e UNION são operações de conjuntos.'),
('HTTP e HTTPS','Qual método HTTP é definido como seguro e normalmente utilizado para recuperar uma representação de um recurso?',['POST','DELETE','GET','PATCH','CONNECT'],2,'GET solicita uma representação e é definido como método seguro. POST, DELETE e PATCH podem alterar estado; CONNECT estabelece um túnel.'),
('Git e controle de versões','Qual comando cria um novo commit com as alterações já adicionadas à área de preparação do Git?',['git status','git commit','git fetch','git branch','git diff'],1,'git commit registra o conteúdo preparado em um novo commit. Os demais comandos consultam estado ou diferenças, obtêm dados ou manipulam branches.'),
('Docker','Em um Dockerfile, qual instrução define a imagem base de um estágio de construção?',['COPY','RUN','FROM','EXPOSE','WORKDIR'],2,'FROM inicia um estágio e define sua imagem base. COPY copia arquivos, RUN executa comandos, EXPOSE documenta portas e WORKDIR define o diretório de trabalho.'),
('Complexidade de algoritmos','Se um algoritmo percorre uma lista de n elementos uma única vez, fazendo trabalho constante por elemento, sua complexidade de tempo é:',['O(1)','O(log n)','O(n)','O(n²)','O(2ⁿ)'],2,'Uma passagem com trabalho constante por elemento cresce linearmente: O(n). As demais expressões descrevem outras taxas de crescimento.'),
('Listas e pilhas','Em uma pilha, a política de retirada dos elementos é:',['FIFO','LIFO','Aleatória','Ordenada por prioridade','Por ordem alfabética'],1,'Uma pilha é LIFO: o último elemento inserido é o primeiro removido. FIFO caracteriza uma fila; as outras opções não definem uma pilha.'),
('JSON','Qual dos seguintes valores é um objeto JSON válido?',['{nome: João}','{"nome": "João"}','{\'nome\': \'João\'}','{"nome": undefined}','{"nome": João}'],1,'JSON exige nomes de propriedades e strings entre aspas duplas. undefined e identificadores não citados não são valores JSON.'),
('IA generativa','Em uma arquitetura RAG, qual é o papel da recuperação de informações?',['Substituir todos os dados de treinamento','Buscar documentos relevantes para fornecer contexto à geração','Garantir que toda resposta seja verdadeira','Eliminar a necessidade de fontes','Treinar o modelo novamente a cada pergunta'],1,'RAG recupera informações relevantes e as fornece como contexto. Isso não garante veracidade e não implica necessariamente retreinar o modelo.'),
]
