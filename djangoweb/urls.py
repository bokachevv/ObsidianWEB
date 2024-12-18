
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('webapp.urls')),
]

urlpatterns += i18n_patterns(

)
