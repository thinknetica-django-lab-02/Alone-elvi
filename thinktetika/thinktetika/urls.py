from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.conf.urls import include
from main.views import ProfileUpdate, phone_number_confirmation

from django.views.generic.base import TemplateView
from django.contrib.sitemaps.views import sitemap
from main.sitemaps import StaticSitemap, GoodsSitemap

sitemaps = {
    'static': StaticSitemap,
    'goods': GoodsSitemap,
}

admin.autodiscover()

urlpatterns = [
    path('', include('main.urls'), name='home'),
    path('admin/', admin.site.urls, name='admin'),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('contacts/', include('django.contrib.flatpages.urls')),
    path('accounts/profile/',
         login_required(ProfileUpdate.as_view()),
         name='profile-update'),
    path('accounts/', include('django.contrib.auth.urls'),
         name='login'),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/phone_confirmation',
         phone_number_confirmation,
         name='phone-confirmation'),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt",
                                            content_type="text/plain"),
         ),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap')

]
