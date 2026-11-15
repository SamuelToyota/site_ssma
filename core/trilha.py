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
        "subtitle": "Posicionamento, método e rotina",
        "weeks": "Semanas 1–4",
        "schedule": "Comece com o diagnóstico e uma tarefa aplicada entre os encontros.",
        "description": "Combine o escopo com o gestor, diagnostique uma demanda real e organize sua rotina consultiva.",
        "deliverable": "Plano de Atuação de 90 dias",
        "modules": (
            ("Autoconhecimento e ponto de partida", "Assessment de valores e carreira, devolutiva, forças e pontos cegos.", 3, "Declaração de posicionamento"),
            ("Papel e independência do consultor interno", "Papéis da consultoria e como saber quando dizer não.", 3, "Classificação de três demandas reais"),
            ("Entender o negócio", "Leitura básica da DRE e do impacto de acidentes e multas nos custos.", 3, "Mapa de valor da sua unidade"),
            ("Ciclo da consultoria interna", "Contratação, diagnóstico, devolutiva, implementação e encerramento.", 5, "Simulação de contratação e roteiro de diagnóstico"),
            ("Rotina e Plano de 90 dias", "Rituais semanais, agenda de valor e indicadores da sua atuação.", 2, "Plano de Atuação de 90 dias"),
        ),
        "materials": (
            "Relatório comentado, declaração de posicionamento, mapa de valor, roteiro de contratação "
            "e diagnóstico, guia de rotina, Plano de Atuação de 90 dias e ebook-resumo."
        ),
    },
    {
        "title": "Gestão de Mudança e Aprendizagem",
        "subtitle": "Como transformar comportamentos",
        "weeks": "Semanas 5–8",
        "schedule": "Transforme o diagnóstico em uma intervenção que possa ser aplicada na operação.",
        "description": "Descubra o que impede a mudança e desenhe uma intervenção com quem vai colocá-la em prática.",
        "deliverable": "Plano de intervenção e sustentação",
        "modules": (
            ("Diagnóstico de causas", "Separe falhas de treinamento, processo, liderança e cultura.", 3, "Análise de causas do seu projeto"),
            ("Resistência e engajamento", "Use o modelo SCARF para planejar a abordagem de aliados e opositores.", 3, "Plano de abordagem de uma liderança resistente"),
            ("Intervenções enxutas", "Aplique aprendizagem de adultos e microaprendizagem ao trabalho real.", 4, "Plano de intervenção de uma página"),
            ("Facilitação e cultura justa", "Conduza conversas difíceis e investigue incidentes com foco em aprendizado.", 3, "Simulação com devolutiva"),
            ("Eficácia e sustentação", "Acompanhe indicadores de comportamento e prepare multiplicadores.", 3, "Plano de sustentação"),
        ),
        "materials": (
            "Diagnóstico de causas, plano de intervenção, modelo de desenho instrucional, roteiro "
            "de facilitação, plano de sustentação e ebook-resumo."
        ),
    },
    {
        "title": "Influência e Business Case",
        "subtitle": "Como defender um projeto",
        "weeks": "Semanas 9–12",
        "schedule": "Prepare a defesa do projeto e apresente-a em banca simulada na última semana.",
        "description": "Calcule o custo da inação, compare alternativas e pratique a defesa do projeto perante a liderança.",
        "deliverable": "Business case defendido em banca simulada",
        "modules": (
            ("Stakeholders e alianças", "Mapeie poder, influência e apoio antes da reunião.", 3, "Mapa de envolvidos no seu projeto"),
            ("Valor e risco", "Calcule custo da inação, ROI e ROSI e teste como mudanças nas premissas afetam o resultado.", 4, "Cálculo em planilha"),
            ("Business case e narrativa", "Estruture a proposta e apresente os dados com clareza.", 4, "Business case do seu projeto"),
            ("Comunicação executiva e negociação", "Pratique respostas a objeções e negocie expectativas.", 3, "Pitch de cinco minutos com devolutiva"),
            ("Banca simulada", "Defenda o business case e refine o plano de aprovação.", 2, "Apresentação em banca com feedback"),
        ),
        "materials": (
            "Mapa de stakeholders, calculadora de ROI/ROSI, business case, roteiro de pitch, plano "
            "de aprovação e ebook-resumo."
        ),
    },
)

TRILHA_FAQS = (
    {
        "pergunta": "Preciso ter cargo de liderança?",
        "resposta": "Não. A trilha trabalha influência sem cargo para técnicos, analistas e coordenadores de SSMA, ESG e Sustentabilidade.",
    },
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
            "de liderança. Se você procura certificação técnica ou não pretende aplicar o método no trabalho, "
            "esta formação não é o caminho indicado."
        ),
    },
    {
        "pergunta": "O que é o assessment do primeiro curso?",
        "resposta": (
            "É um instrumento de autoconhecimento sobre valores pessoais e de carreira, com devolutiva "
            "comentada. Ajuda a orientar seu posicionamento profissional e não é um diagnóstico psicológico."
        ),
    },
    {
        "pergunta": "Posso fazer só um dos cursos?",
        "resposta": "A trilha foi pensada em sequência: o mesmo projeto passa pelas três etapas. Consulte a equipe sobre a disponibilidade de cursos avulsos.",
    },
    {
        "pergunta": "A formação substitui o conhecimento técnico ou garante aprovação do projeto?",
        "resposta": "Não. A trilha complementa sua base técnica. Você aprende a estruturar uma proposta e pratica sua defesa em banca simulada, sem promessa de aprovação de orçamento.",
    },
    {
        "pergunta": "Como consulto valores, turmas e formas de pagamento?",
        "resposta": "Fale com a equipe para consultar datas, valores, formas de pagamento e condições de inscrição. Se sua empresa for custear a formação, aproveite para perguntar sobre a documentação necessária.",
    },
)
