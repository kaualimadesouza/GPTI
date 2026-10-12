# Ficha de leitura: AHP para escolher a linguagem do trabalho semestral

ACH2027, Turma T94, Grupo 7. Leitura antes dos 30 julgamentos par a par.

## 1. Para que serve esta ficha

Reúne o método, a escala e fatos sobre as quatro alternativas. Informa, não decide: os julgamentos
são do Kauã, e a ficha não ordena, não pontua nem aponta vencedor. Cada fato traz a fonte lida em
12/10/2026; o que não deu para verificar ficou de fora (fim da seção 6). Os fatos foram reunidos com
ajuda de IA: confira a fonte antes de usar um deles no documento.

## 2. Premissas

- Sistema: controle de acesso de pessoas e veículos à EACH (Nº USP ou CPF, visitantes, hierarquia
  por senha, pré-cadastro em lote para eventos, relatórios de frequência, catracas e cancelas).
- Critérios e alternativas dados pelo professor.
- Time: 5 a 8 alunos de SI da EACH no último ano, como estagiários (bolsistas, R$ 2.000/mês por 6
  meses, valor fixo), mais um analista de sistemas sênior.
- Cada alternativa é a linguagem com seu principal framework web: Java/Spring Boot, C#/ASP.NET Core,
  Python/Django, Go/Gin.
- Cada fator conta em um critério só (seção 3).
- Método: autovetor principal (Saaty). CI = (lambda_max - n) / (n - 1), CR = CI / RI, com RI = 0,90
  para n = 4 (Vargas 2010, Tabela 8, atribuída a Saaty). Consistente se CR < 0,10.

## 3. Os critérios

| Critério | Definição |
| --- | --- |
| Custo de desenvolvimento | Gastos em R$ que mudam com a linguagem: licenças, ferramentas, hospedagem, integração com catracas e cancelas. As bolsas são fixas e ficam de fora. |
| Prazo de entrega | O que o framework traz pronto para entregar os 4 módulos (controle de acesso, gestão de usuários e visitantes, rotinas especiais, relatórios), supondo um time que já sabe a linguagem. |
| Facilidade de mão de obra | Durante o projeto: achar bolsistas de SI da EACH que já sabem a linguagem, curva de aprendizado de quem não sabe, repor quem sair. |
| Facilidade de manutenção | Depois da implantação (a manutenção ficou fora do escopo do projeto): quão fácil é, para quem herdar o código, corrigir, evoluir e adaptar. |

A ISO/IEC 25010:2023 define *maintainability* como "Capability of a product to be modified by the
intended maintainers with effectiveness and efficiency" (reproduzida em quality.arc42.org). O tempo
de suporte das versões é acréscimo do grupo, não faz parte da norma.

## 4. A escala de Saaty

Saaty, "How to Make a Decision: The Analytic Hierarchy Process", Tabela 1, p. 8 do PDF.

| Intensidade | Definição | Explicação |
| --- | --- | --- |
| 1 | Importância igual | Os dois contribuem igualmente para o objetivo. |
| 3 | Importância moderada de um sobre o outro | A experiência e o julgamento favorecem um sobre o outro (ver nota). |
| 5 | Importância essencial ou forte | A experiência e o julgamento favorecem fortemente um sobre o outro. |
| 7 | Importância muito forte | Um é fortemente favorecido e seu domínio é demonstrado na prática. |
| 9 | Importância extrema | A evidência a favor de um é da mais alta ordem possível. |
| 2, 4, 6, 8 | Intermediários entre dois vizinhos | Quando é preciso um meio-termo. |
| Recíprocos | Se i recebe um desses números contra j, j recebe o recíproco contra i. | |

Nota: no PDF, a explicação do 3 repete a do 5 ("strongly favor"); o rótulo do 3 é "moderada", e
Vargas (2010) o chama de "Moderately preferred". Vargas observa que é comum usar só os ímpares e
deixar os pares para um meio-termo.

## 5. Como escrever um julgamento

Em `atividades/ahp/ahp.py`, agrupados por matriz, uma linha por par:

```python
Judgment("X", "Y", 5, "motivo opcional")
```

Lê-se: "X é fortemente preferível a Y" no critério daquela matriz.

- Intensidade: inteiro de 1 a 9; 1 quer dizer igual. Para favorecer o outro lado, troque os nomes
  (`Judgment("Y", "X", 5)`); não escreva frações. O motivo é opcional e ajuda a defender o número.
- 5 matrizes. Na dos critérios, os nomes são `"Custo de desenvolvimento"`, `"Prazo de entrega"`,
  `"Facilidade de manutenção"` e `"Facilidade de mão de obra"`: qual pesa mais na escolha? Nas
  outras quatro, uma por critério, os nomes são `"Java"`, `"C#"`, `"Python"` e `"Go"`: qual atende
  melhor aquele critério?
- 4 elementos dão 6 pares (com A, B, C, D: A-B, A-C, A-D, B-C, B-D, C-D). Total: 5 x 6 = 30.

Consistência: se X > Y com 3 e Y > Z com 3, X > Z deveria ficar bem acima de 3 (a consistência
perfeita daria 3 x 3 = 9). Contradições (X > Y, Y > Z, Z > X) sobem o CR. Se um CR passar de 0,10,
o script não gera as tabelas e mostra os julgamentos que mais destoam.

## 6. Fatos por critério

As linhas seguem a ordem do professor, não uma ordem de preferência.

### 6.1 Custo de desenvolvimento

| Alternativa | Fatos |
| --- | --- |
| Java / Spring Boot | OpenJDK: GPLv2 com *Classpath Exception* ([openjdk.org](https://openjdk.org/legal/gplv2+ce.html)); Spring Boot: Apache 2.0 ([GitHub](https://github.com/spring-projects/spring-boot)). Eclipse IDE: gratuito, EPL 2.0, suporta Java ([eclipseide.org](https://eclipseide.org/)). |
| C# / ASP.NET Core | .NET e ASP.NET Core: MIT ([runtime](https://github.com/dotnet/runtime/blob/main/LICENSE.TXT), [aspnetcore](https://github.com/dotnet/aspnetcore/blob/main/LICENSE.txt)); roda em Linux e Windows ([dotnet.microsoft.com](https://dotnet.microsoft.com/en-us/learn/dotnet/what-is-dotnet)). Visual Studio Community: grátis, mas em organização *enterprise* (mais de 250 PCs ou US$ 1 milhão de receita anual) só para código aberto, pesquisa acadêmica e sala de aula ([visualstudio.microsoft.com](https://visualstudio.microsoft.com/vs/community/)); o C# Dev Kit do VS Code segue o mesmo modelo ([Marketplace](https://marketplace.visualstudio.com/items?itemName=ms-dotnettools.csdevkit)). Se o projeto cabe nessas exceções é questão a avaliar. |
| Python / Django | Python: *PSF License Version 2*, código aberto ([docs.python.org](https://docs.python.org/3/license.html)); Django: licença estilo BSD de 3 cláusulas ([GitHub](https://github.com/django/django/blob/main/LICENSE)). |
| Go / Gin | Go: licença estilo BSD ([go.dev](https://go.dev/LICENSE)); Gin: MIT ([GitHub](https://github.com/gin-gonic/gin/blob/master/LICENSE)). Extensão Go do VS Code em golang/vscode-go, com o gopls mantido pelo time do Go ([code.visualstudio.com](https://code.visualstudio.com/docs/languages/go)). |

Para todas: o VS Code é "free for private or commercial use" ([FAQ](https://code.visualstudio.com/docs/supporting/faq)).
A API de acesso da Control iD é REST sobre TCP/IP (Ethernet), com login e sessão; a página não cita
SDK oficial e aponta exemplos em C#, Delphi, Java, NodeJS e Python, sem Go
([controlid.com.br](https://www.controlid.com.br/docs/access-api-pt/)).

### 6.2 Prazo de entrega

| Alternativa | Fatos |
| --- | --- |
| Java / Spring Boot | Spring Security: autenticação, autorização e proteção contra ataques comuns ([docs.spring.io](https://docs.spring.io/spring-security/reference/index.html)). Spring Data JPA: repositórios com paginação, consultas dinâmicas e auditoria ([spring.io](https://spring.io/projects/spring-data-jpa)). Migrações via Flyway ou Liquibase ([docs.spring.io](https://docs.spring.io/spring-boot/how-to/data-initialization.html)). |
| C# / ASP.NET Core | Identity: login, usuários, senhas, perfil, papéis (*roles*), *claims*, tokens, confirmação de e-mail ([learn.microsoft.com](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/identity)). EF Core: migrações que mudam o esquema aos poucos, preservando os dados ([learn.microsoft.com](https://learn.microsoft.com/en-us/ef/core/managing-schemas/migrations/)). |
| Python / Django | Admin automático a partir dos *models*, recomendado só como ferramenta interna ([admin](https://docs.djangoproject.com/en/stable/ref/contrib/admin/)). Usuários, permissões, grupos e telas de login; sem limite de tentativas de login, OAuth nem permissão por objeto, que ficam para pacotes de terceiros ([auth](https://docs.djangoproject.com/en/stable/topics/auth/)). ORM e migrações ([models](https://docs.djangoproject.com/en/stable/topics/db/models/), [migrations](https://docs.djangoproject.com/en/stable/topics/migrations/)). |
| Go / Gin | Roteamento, middleware em cadeia, validação de JSON, grupos de rotas, renderização JSON/XML/HTML. A introdução não cita ORM, migrações, usuários e papéis nem painel admin; o menu tem páginas sobre banco, sessões e middleware BasicAuth ([gin-gonic.com](https://gin-gonic.com/en/docs/introduction/)). |

As páginas lidas do Spring e do ASP.NET Core não falam de painel administrativo.

### 6.3 Facilidade de manutenção

| Alternativa | Fatos |
| --- | --- |
| Java / Spring Boot | *Statically typed*: todo tipo é conhecido na compilação ([JLS 25](https://docs.oracle.com/javase/specs/jls/se25/html/jls-4.html)). Oracle: LTS a cada dois anos (21, 25; próxima, 29, em set/2027); Java 25 com Premier Support até set/2030 no Oracle JDK comercial ([oracle.com](https://www.oracle.com/java/technologies/java-se-support-roadmap.html)); Eclipse Temurin: LTS por pelo menos 4 anos, Java 25 até set/2031 ou mais ([adoptium.net](https://adoptium.net/support/)). |
| C# / ASP.NET Core | *Strongly typed*: o compilador pega erros de tipo antes de rodar ([learn.microsoft.com](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/)). Versão nova todo novembro: pares LTS (3 anos), ímpares STS (2 anos); .NET 10 até 14/11/2028; vale para ASP.NET Core e EF Core ([dotnet.microsoft.com](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core)). |
| Python / Django | Anotações de tipo opcionais; o runtime não as verifica, só ferramentas externas (verificadores de tipo, IDEs, linters) ([docs.python.org](https://docs.python.org/3/library/typing.html)). Python: cerca de 2 anos de correções, depois só segurança, fim aos 5 anos ([devguide.python.org](https://devguide.python.org/versions/)). Django: LTS com 3 anos; a 5.2 vai até abr/2028 ([djangoproject.com](https://www.djangoproject.com/download/)). |
| Go / Gin | *Strongly typed*; o tipo estático vem da declaração ([spec](https://go.dev/ref/spec)). Cada versão principal vale até saírem duas mais novas (1.26 em fev/2026, 1.27 em ago/2026) ([go.dev](https://go.dev/doc/devel/release)). Promessa Go 1: código escrito para a especificação Go 1 continua compilando e rodando, salvo exceções como correções de segurança e de bugs ([go1compat](https://go.dev/doc/go1compat)). |

### 6.4 Facilidade de mão de obra

Para todas: na EACH, ACH2001 Introdução à Programação usa bibliografia em C (Paes; Schildt)
([JupiterWeb](https://uspdigital.usp.br/jupiterweb/obterDisciplina?sgldis=ACH2001)); ACH2016
Inteligência Artificial não nomeia linguagem ([JupiterWeb](https://uspdigital.usp.br/jupiterweb/obterDisciplina?sgldis=ACH2016)).
Nenhuma disciplina de SI com Python, C# ou Go foi verificada, o que não prova que não exista.

| Alternativa | Fatos |
| --- | --- |
| Java / Spring Boot | ACH2003 Computação Orientada a Objetos: o programa não nomeia linguagem; a bibliografia é de Java (Sestoft, Bloch, Deitel) ([JupiterWeb](https://uspdigital.usp.br/jupiterweb/obterDisciplina?sgldis=ACH2003)). Stack Overflow 2025: Java 29,6%, Spring Boot 15,6%. |
| C# / ASP.NET Core | Stack Overflow 2025: C# 29,9%, ASP.NET Core 21,3%. |
| Python / Django | Stack Overflow 2025: Python 54,8%, Django 11,7% (outros frameworks Python: FastAPI 15,1%, Flask 13,2%). |
| Go / Gin | Stack Overflow 2025: Go 17,4%; Gin não está na lista. JetBrains: 48% de quem tem Go como linguagem principal usava Gin em 2025 (41% em 2020) ([blog.jetbrains.com](https://blog.jetbrains.com/go/2025/11/10/go-language-trends-ecosystem-2025/); resumo da JetBrains, relatório original não aberto). |

Ressalva: o Stack Overflow ([survey.stackoverflow.co](https://survey.stackoverflow.co/2025/technology/),
desenvolvedores profissionais) e a JetBrains medem desenvolvedores do mundo todo, não alunos da EACH.

**Não verificado, ficou de fora:** preço de hospedagem por linguagem; IDEs da JetBrains e os termos
completos do Visual Studio (páginas não carregaram); painel admin no Spring e no ASP.NET Core além das
páginas lidas; curva de aprendizado e reposição de bolsistas; suporte do Spring Boot e do Gin; outra
disciplina de SI com Python, C# ou Go.

## 7. Fontes

Acessadas em 12/10/2026.

- Método: https://www.isahp-org.creativedecisions.net/uploads/1-how-to-make-a-decision-the-analytic-hierarchy-process-t-l-saaty.pdf;
  https://ricardo-vargas.com/articles/analytic-hierarchy-process/; https://quality.arc42.org/qualities/maintainability
- EACH: https://uspdigital.usp.br/jupiterweb/obterDisciplina?sgldis=ACH2001 (também `ACH2003` e `ACH2016`)
- Pesquisas: https://survey.stackoverflow.co/2025/technology/; https://blog.jetbrains.com/go/2025/11/10/go-language-trends-ecosystem-2025/
- Licenças: https://openjdk.org/legal/gplv2+ce.html; https://github.com/spring-projects/spring-boot;
  https://github.com/dotnet/runtime/blob/main/LICENSE.TXT; https://github.com/dotnet/aspnetcore/blob/main/LICENSE.txt;
  https://docs.python.org/3/license.html; https://github.com/django/django/blob/main/LICENSE; https://go.dev/LICENSE;
  https://github.com/gin-gonic/gin/blob/master/LICENSE
- Ferramentas: https://eclipseide.org/; https://visualstudio.microsoft.com/vs/community/;
  https://marketplace.visualstudio.com/items?itemName=ms-dotnettools.csdevkit; https://code.visualstudio.com/docs/supporting/faq;
  https://code.visualstudio.com/docs/languages/go; https://dotnet.microsoft.com/en-us/learn/dotnet/what-is-dotnet;
  https://www.controlid.com.br/docs/access-api-pt/
- Frameworks: https://docs.spring.io/spring-security/reference/index.html; https://spring.io/projects/spring-data-jpa;
  https://docs.spring.io/spring-boot/how-to/data-initialization.html; https://learn.microsoft.com/en-us/aspnet/core/security/authentication/identity;
  https://learn.microsoft.com/en-us/ef/core/managing-schemas/migrations/; https://docs.djangoproject.com/en/stable/ref/contrib/admin/;
  https://docs.djangoproject.com/en/stable/topics/auth/; https://docs.djangoproject.com/en/stable/topics/db/models/;
  https://docs.djangoproject.com/en/stable/topics/migrations/; https://gin-gonic.com/en/docs/introduction/
- Tipagem e suporte: https://docs.oracle.com/javase/specs/jls/se25/html/jls-4.html;
  https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/; https://docs.python.org/3/library/typing.html;
  https://go.dev/ref/spec; https://www.oracle.com/java/technologies/java-se-support-roadmap.html; https://adoptium.net/support/;
  https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core; https://devguide.python.org/versions/;
  https://www.djangoproject.com/download/; https://go.dev/doc/devel/release; https://go.dev/doc/go1compat
