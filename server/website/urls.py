from django.conf.urls import include, url
from django.contrib import admin
from swag.views import *
from users.views import *


urlpatterns = [
    # Examples:
    url(r'^$', home_page, name='home_page'),
    url(r'^form/$', FormView, name='form_page'),
    url(r'^login/$', LoginView, name='form_page'),
    url(r'^register/$', RegistrationView, name='form_page'),
    url(r'^logout/$', LogoutView),
    url(r'^show_data/$', graph_plot, name = 'home_page'),
    url(r'^admin/', admin.site.urls),
    url(r'^show_forecasted_smavg_data/$', forecasted_plot, name='home_page')
]