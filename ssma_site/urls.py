from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.auth import views as auth_views
from django.urls import include, path

from core.sitemaps import ArtigoSitemap, StaticViewSitemap

sitemaps = {
    "paginas": StaticViewSitemap,
    "artigos": ArtigoSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("", include("core.urls")),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="aluno/login.html",
            extra_context={
                "page_title": "Área do aluno | Consultor Interno",
                "page_description": "Acesso reservado aos alunos do Consultor Interno.",
                "page_robots": "noindex,nofollow",
            },
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
]

handler404 = "core.views.erro_404"
