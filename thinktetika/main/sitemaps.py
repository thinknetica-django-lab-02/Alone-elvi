from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from main.models import Product


class StaticSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return ['index', 'goods']

    def location(self, item):
        return reverse(item)


class GoodsSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Product.objects.filter(is_published=True)
