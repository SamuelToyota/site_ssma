from django.conf import settings
from django.templatetags.static import static


def site_context(request):
    site_url = settings.SITE_URL
    private_prefixes = ("/admin/", "/aluno/", "/login/", "/cadastro/", "/sucesso/")
    return {
        "site_url": site_url,
        "canonical_url": f"{site_url}{request.path}",
        "default_og_image": f"{site_url}{static('images/hero-profissionais-real.jpg')}",
        "gtm_id": settings.GTM_ID,
        "default_robots": (
            "noindex,nofollow" if request.path.startswith(private_prefixes) else "index,follow,max-image-preview:large"
        ),
    }
