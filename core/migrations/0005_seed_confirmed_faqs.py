from django.db import migrations


FAQS = [
    (
        "curso_cultura",
        "Preciso já atuar como consultor interno?",
        "Não. A formação é voltada a profissionais de SSMA e lideranças que querem ampliar sua capacidade de diagnosticar a cultura, comunicar prioridades e mobilizar pessoas.",
        1,
    ),
    (
        "curso_cultura",
        "O conteúdo é teórico ou aplicado?",
        "A proposta combina aulas gravadas, materiais, exercícios e duas mentorias ao vivo para conectar os conceitos à realidade de trabalho.",
        2,
    ),
    (
        "curso_cultura",
        "Posso estudar no meu ritmo?",
        "Sim. As aulas ficam disponíveis continuamente e a jornada sugerida é de quatro a seis semanas.",
        3,
    ),
    (
        "curso_teste",
        "O que está incluído no diagnóstico?",
        "A experiência inclui o mapeamento individual, um relatório personalizado e uma devolutiva para organizar a leitura dos resultados.",
        1,
    ),
    (
        "curso_teste",
        "Esse produto é um curso?",
        "Não. É uma experiência individual de diagnóstico e orientação, voltada a valores pessoais e decisões de carreira.",
        2,
    ),
    (
        "curso_teste",
        "Em que momento ele pode ser útil?",
        "Quando você está avaliando uma transição, comparando oportunidades ou buscando mais coerência entre valores e trabalho.",
        3,
    ),
]


def create_faqs(apps, schema_editor):
    FAQ = apps.get_model("core", "FAQ")
    for pagina, pergunta, resposta, ordem in FAQS:
        FAQ.objects.get_or_create(
            pagina=pagina,
            pergunta=pergunta,
            defaults={"resposta": resposta, "ordem": ordem, "ativa": True},
        )


def remove_faqs(apps, schema_editor):
    FAQ = apps.get_model("core", "FAQ")
    for pagina, pergunta, _, _ in FAQS:
        FAQ.objects.filter(pagina=pagina, pergunta=pergunta).delete()


class Migration(migrations.Migration):
    dependencies = [("core", "0004_case_categoriaconteudo_depoimento_faq_and_more")]

    operations = [migrations.RunPython(create_faqs, remove_faqs)]
