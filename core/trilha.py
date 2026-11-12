"""Conteúdo público da Trilha Consultor Interno."""

CONSULTING_STAGES = (
    {
        "name": "Contratar",
        "description": "Combinar com o gestor o problema, o papel de cada pessoa e o que será entregue.",
    },
    {
        "name": "Diagnosticar",
        "description": "Distinguir falhas de treinamento, de processo, de liderança e de cultura.",
    },
    {
        "name": "Devolver",
        "description": "Apresentar os achados de modo que o líder assuma a solução.",
    },
    {
        "name": "Implementar",
        "description": "Desenhar intervenções enxutas e lidar com a resistência à mudança.",
    },
    {
        "name": "Sustentar",
        "description": "Medir mudanças de comportamento e resultados para sustentar o avanço após o encerramento.",
    },
)

TRILHA_COURSES = (
    {
        "title": "O Consultor Interno",
        "weeks": "Semanas 1–4",
        "description": "Combine o escopo com o gestor, diagnostique uma demanda real e organize sua rotina consultiva.",
        "deliverable": "Plano de Atuação de 90 dias",
        "syllabus": (
            "Autoconhecimento e ponto de partida (3h) — assessment de valores e carreira, com devolutiva.\n"
            "Papel e independência técnica (3h) — diferencie papéis e pratique dizer não.\n"
            "Entender o negócio (3h) — leitura básica da DRE e dos custos de acidentes e multas.\n"
            "Ciclo da consultoria interna (5h) — simule a contratação e prepare o diagnóstico.\n"
            "Rotina e Plano de 90 dias (2h) — organize rituais, prioridades e indicadores.\n\n"
            "Você leva: relatório comentado, declaração de posicionamento, mapa de valor, roteiro de contratação "
            "e diagnóstico, guia de rotina, Plano de Atuação de 90 dias e ebook-resumo."
        ),
    },
    {
        "title": "Gestão de Mudança e Aprendizagem",
        "weeks": "Semanas 5–8",
        "description": "Descubra o que impede a mudança e desenhe uma intervenção com quem vai colocá-la em prática.",
        "deliverable": "Plano de intervenção e sustentação",
        "syllabus": (
            "Diagnóstico de causas (3h) — separe falhas de treinamento, processo, liderança e cultura.\n"
            "Resistência e engajamento (3h) — use o modelo SCARF para planejar a abordagem de lideranças.\n"
            "Intervenções enxutas (4h) — aplique aprendizagem de adultos e microaprendizagem ao trabalho real.\n"
            "Facilitação e cultura justa (3h) — simule conversas difíceis e investigue incidentes para aprender.\n"
            "Eficácia e sustentação (3h) — acompanhe indicadores de comportamento e prepare multiplicadores.\n\n"
            "Você leva: diagnóstico de causas, plano de intervenção, modelo de desenho instrucional, roteiro "
            "de facilitação, plano de sustentação e ebook-resumo."
        ),
    },
    {
        "title": "Influência e Business Case",
        "weeks": "Semanas 9–12",
        "description": "Calcule o custo da inação, compare alternativas e pratique a defesa do projeto perante a liderança.",
        "deliverable": "Business case defendido em banca simulada",
        "syllabus": (
            "Stakeholders e alianças (3h) — mapeie poder, influência e apoio antes da reunião.\n"
            "Valor e risco (4h) — calcule custo da inação, ROI e ROSI com premissas claras.\n"
            "Business case e narrativa (4h) — estruture a proposta e apresente os dados.\n"
            "Comunicação executiva e negociação (3h) — grave um pitch de 5 minutos e receba devolutiva.\n"
            "Banca simulada (2h) — defenda o business case e refine o plano de aprovação.\n\n"
            "Você leva: mapa de stakeholders, calculadora de ROI/ROSI, business case, roteiro de pitch, plano "
            "de aprovação e ebook-resumo. A banca é um exercício; não há promessa de aprovação de orçamento."
        ),
    },
)

TRILHA_FAQS = (
    {
        "pergunta": "Qual é a dedicação semanal?",
        "resposta": (
            "Cerca de 4 horas por semana de aulas e práticas, além da aplicação no seu projeto. "
            "Cerca de metade das 48 horas da trilha é dedicada à prática."
        ),
    },
    {
        "pergunta": "Como funciona o ciclo de consultoria da trilha?",
        "resposta": (
            "O ciclo se inspira no trabalho de Peter Block sobre consultoria, adaptado à rotina de SSMA e ESG.\n\n"
            + "\n".join(f"{stage['name']} — {stage['description']}" for stage in CONSULTING_STAGES)
        ),
    },
    {
        "pergunta": "Para quem a trilha faz sentido?",
        "resposta": (
            "Para profissionais de SSMA, ESG e Sustentabilidade com base técnica que querem participar "
            "das decisões do negócio e podem trazer uma demanda real da empresa. Não é preciso ter cargo "
            "de liderança. A trilha não é um curso de normas nem substitui as responsabilidades técnicas da função."
        ),
    },
    {
        "pergunta": "O que é o assessment do primeiro curso?",
        "resposta": (
            "É um instrumento de autoconhecimento sobre valores pessoais e de carreira, com devolutiva "
            "comentada. Ajuda a orientar seu posicionamento profissional e não é um diagnóstico psicológico."
        ),
    },
)
