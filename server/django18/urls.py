from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^$', 'letter.views.home', name='home'),
    url(r'^show_data/', 'letter.views.cal' ,name = 'cal'),
    url(r'^admin/', include(admin.site.urls)),
]