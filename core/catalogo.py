"""Ofertas do catálogo público, incluindo a etapa final da trilha."""

from .trilha import TRILHA_COURSES

BUSINESS_CASE_COURSE = next(course for course in TRILHA_COURSES if course.get("route") == "curso_business_case")
BUSINESS_CASE_COVER = "images/course-business-case.svg"
BUSINESS_CASE_INQUIRY = "influencia-business-case"

COURSE_CATALOG = (
    {
        "route": "curso_cultura",
        "label": "Cultura de Segurança",
        "title": "Especialista em Cultura de Segurança",
        "category": "Formação em cultura de segurança",
        "description": "Para profissionais de SSMA e lideranças que querem compreender a cultura atual, mobilizar pessoas e sustentar decisões além do compliance.",
        "highlights": ("Diagnóstico da cultura atual", "Engajamento de líderes e equipes", "Métodos para demonstrar impacto"),
        "cover": "images/course_1.webp",
        "width": 1470,
        "height": 759,
        "duration": "4 a 6 semanas · online",
    },
    {
        "route": "curso_teste",
        "label": "Perfil e Carreira",
        "title": "Perfil, Valores Pessoais & Carreira",
        "category": "Diagnóstico individual",
        "description": "Para quem vive uma transição, avalia oportunidades ou precisa compreender o que orienta suas escolhas profissionais.",
        "highlights": ("Mapeamento de valores pessoais", "Relatório individual", "Devolutiva personalizada"),
        "cover": "images/course_2.webp",
        "width": 1427,
        "height": 777,
        "duration": "Experiência individual",
    },
    {
        "route": BUSINESS_CASE_COURSE["route"],
        "label": BUSINESS_CASE_COURSE["title"],
        "title": BUSINESS_CASE_COURSE["title"],
        "category": "Curso 03 · Trilha Consultor Interno",
        "description": BUSINESS_CASE_COURSE["description"],
        "highlights": ("Custo da inação e retorno sobre investimento", "Business case para a liderança", "Defesa em banca simulada com feedback"),
        "cover": BUSINESS_CASE_COVER,
        "width": 1480,
        "height": 800,
        "duration": "16h · Semanas 9 a 12 da trilha",
    },
)
