from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from .sitemap import (
    HomeSiteMap,
    PageSiteMap,
    BlogSitemap,
    BuyGameSitemap,
    SellGameSitemap,
)
from django.views.generic.base import TemplateView

sitemaps = {
    "home": HomeSiteMap,
    "page": PageSiteMap,
    "blog": BlogSitemap,
    "buy-game": BuyGameSitemap,
    "sell-game": SellGameSitemap,
}


urlpatterns = [
    # sitemap
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    # robots.txt
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    # other views
    path("admin/", admin.site.urls),
    path("user/", include("accounts.urls")),
    path("accounts/", include("allauth.urls")),
    path("shop/", include("shop.urls")),
    path("payment/", include("payment.urls")),
    path("currencies/", include("currencies.urls")),
    path("blog/", include("blog.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("", include("main.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
