from django.contrib.sitemaps import Sitemap
from .models import Project, Task

class ProjectSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Project.objects.all().order_by('pk')

    def lastmod(self, obj):
        return obj.start_date

    def location(self, obj):
        return obj.get_absolute_url()

class TaskSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.6

    def items(self):
        return Task.objects.all().order_by('pk')

    def lastmod(self, obj):
        return obj.start_date

    def location(self, obj):
        return obj.get_absolute_url()
