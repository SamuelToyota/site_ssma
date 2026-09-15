from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Artigo


class StaticViewSitemap(Sitemap):
    protocol = "https"

    pages = {
        "home": (1.0, "weekly"),
        "cursos": (0.9, "weekly"),
        "curso_cultura": (0.9, "monthly"),
        "curso_teste": (0.8, "monthly"),
        "mentoria": (0.9, "monthly"),
        "para_empresas": (0.9, "monthly"),
        "conteudos": (0.8, "weekly"),
        "sobre": (0.7, "monthly"),
        "contato": (0.6, "monthly"),
        "privacidade": (0.3, "yearly"),
        "termos": (0.3, "yearly"),
    }

    def items(self):
        return list(self.pages)

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return self.pages[item][0]

    def changefreq(self, item):
        return self.pages[item][1]


class ArtigoSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7
    protocol = "https"

    def items(self):
        return Artigo.objects.publicados()

    def lastmod(self, obj):
        return obj.atualizado_em
