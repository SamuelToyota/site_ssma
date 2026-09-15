# Auditoria estratégica e plano de evolução

## Objetivo

Transformar o Consultor Interno em uma plataforma profissional de autoridade, educação e relacionamento B2B para SSMA, com linguagem clara, identidade premium e caminhos distintos para profissionais e empresas.

## Diagnóstico inicial

### O que já funcionava

- Identidade visual consistente em branco, cinza e verde-escuro.
- Uso de fotografias reais e coerentes com Segurança do Trabalho.
- Duas ofertas existentes com páginas e links de checkout.
- Base Django simples, com área do aluno, cursos, módulos, aulas e matrículas.
- Frases de posicionamento fortes, preservadas na nova narrativa.

### Problemas críticos encontrados

- Login e cadastro públicos quebravam por falta de templates.
- Ausência de sitemap, robots.txt, canonical, Open Graph e dados estruturados.
- Configuração de produção insegura por padrão, com `DEBUG` e chave sensível inadequados.
- Formulário de contato pouco qualificado e envio de e-mail sem tratamento operacional adequado.
- Nenhuma página dedicada a mentoria, empresas, trajetória ou conteúdo.
- Falta de política de privacidade, termos e consentimento nos formulários.

### Lacunas de posicionamento e conversão

- O público principal não estava explícito no primeiro bloco da Home.
- Formação, mentoria e projetos empresariais competiam sem uma hierarquia clara.
- Havia repetição de promessas e pouca demonstração do problema vivido pelo público.
- O conceito de “Consultor Interno” não estava explicado.
- Não havia estrutura editorial, newsletter, prova social validada ou qualificação B2B.

### Riscos técnicos e operacionais

- Banco SQLite e dados de exemplo não são adequados como arquitetura definitiva de produção.
- Não havia testes automáticos das rotas e formulários críticos.
- Imagens PNG pesadas aumentavam o tempo de carregamento.
- Não existia integração configurada com CRM, e-mail marketing ou analytics.

## Arquitetura implementada

- `/` — Home e posicionamento central.
- `/cursos/` — central de formações.
- `/curso/cultura-seguranca/` — formação em Cultura de Segurança.
- `/curso/teste-perfil/` — diagnóstico de Perfil, Valores e Carreira.
- `/mentoria/` — mentoria individual.
- `/para-empresas/` — desenvolvimento B2B.
- `/conteudos/` e `/conteudos/<slug>/` — central editorial e artigos.
- `/sobre/` — Alan Silvério, visão e método.
- `/contato/` — contato qualificado por objetivo.
- `/politica-de-privacidade/` e `/termos/` — base legal.
- `/login/`, `/cadastro/` e `/aluno/` — acesso à plataforma.
- `/robots.txt`, `/sitemap.xml` e página 404 personalizada.

Rotas antigas de formação foram preservadas por redirecionamento permanente, evitando links quebrados.

## Prioridades adotadas

1. Segurança, rotas críticas, acessibilidade e SEO técnico.
2. Clareza da Home e separação dos caminhos individual e empresarial.
3. Mentoria, B2B, Sobre, Conteúdos e contato qualificado.
4. Evolução das páginas de produto e FAQ administrável.
5. Performance das imagens, testes e validação responsiva.
6. Integrações externas e prova social somente após validação.

## Conteúdo preservado e reorganizado

- “Segurança do trabalho com voz nas decisões.”
- “Conhecimento técnico é o começo. Influência gera mudança.”
- “Menos reação. Mais direção.”
- “Da operação à estratégia.”
- “SSMA presente onde as decisões acontecem.”
- Formação Especialista em Cultura de Segurança.
- Diagnóstico Perfil, Valores Pessoais e Carreira.
- Método D.E.S.T.A.Q.U.E., com nomenclaturas recuperadas do conteúdo anterior.

## Decisões de conteúdo

- Não foram criados depoimentos, cases, certificações, empresas atendidas ou resultados.
- Blocos de prova social e cases aparecem somente quando registros aprovados são publicados no painel administrativo.
- A mentoria não informa duração, quantidade de encontros ou entregáveis ainda não confirmados.
- A página B2B define frentes de conversa, mas deixa formato e escopo para diagnóstico.
- A central de conteúdo possui estado vazio profissional até que artigos reais sejam publicados.

## Estrutura de gestão criada

O painel administrativo agora permite cadastrar e controlar:

- categorias e artigos;
- depoimentos, inativos por padrão;
- cases, não publicados por padrão;
- perguntas frequentes;
- materiais gratuitos, inativos por padrão;
- contatos qualificados e inscrições na newsletter.

## Próximas evoluções recomendadas

- Confirmar os dados listados em `CONTEUDO_PENDENTE_ALAN.md`.
- Definir hospedagem, PostgreSQL, backups e rotina de publicação.
- Conectar SMTP transacional, CRM e plataforma de e-mail marketing.
- Configurar GA4/GTM e eventos de conversão após aprovação dos identificadores.
- Publicar artigos reais e um material de captura aprovado.
- Inserir somente depoimentos e cases autorizados.
- Fazer homologação final de conteúdo e política comercial antes de publicar.
