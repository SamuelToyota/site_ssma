from django.db import migrations


def deactivate_placeholders(apps, schema_editor):
    Curso = apps.get_model("core", "Curso")
    Modulo = apps.get_model("core", "Modulo")

    Curso.objects.filter(
        titulo="ESG",
        slug="esg",
        descricao="ooii",
        matriculas__isnull=True,
    ).update(
        titulo="Rascunho de curso",
        descricao="Registro legado desativado. Revise o conteúdo antes de publicar.",
        ativo=False,
    )
    Modulo.objects.filter(
        titulo="oi",
        descricao="oi",
        curso__slug="esg",
        curso__ativo=False,
    ).update(
        titulo="Módulo de teste",
        descricao="Conteúdo legado desativado.",
    )


def restore_placeholders(apps, schema_editor):
    Curso = apps.get_model("core", "Curso")
    Modulo = apps.get_model("core", "Modulo")

    Curso.objects.filter(
        titulo="Rascunho de curso",
        slug="esg",
        descricao="Registro legado desativado. Revise o conteúdo antes de publicar.",
        matriculas__isnull=True,
    ).update(titulo="ESG", descricao="ooii", ativo=True)
    Modulo.objects.filter(
        titulo="Módulo de teste",
        descricao="Conteúdo legado desativado.",
        curso__slug="esg",
    ).update(titulo="oi", descricao="oi")


class Migration(migrations.Migration):
    dependencies = [("core", "0005_seed_confirmed_faqs")]

    operations = [
        migrations.RunPython(deactivate_placeholders, restore_placeholders),
    ]
