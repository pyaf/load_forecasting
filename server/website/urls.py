from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^$', 'swag.views.home_page', name='home_page'),
    url(r'^show_data/', 'swag.views.graph_plot' ,name = 'graph_plot'),
    url(r'^admin/', include(admin.site.urls)),
]