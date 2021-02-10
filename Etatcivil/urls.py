from django.contrib import admin
from django.conf.urls import include, url
from ajax_select import urls as ajax_select_urls
from gestciv import views

urlpatterns = [
    url(r'admin/', admin.site.urls),
    url(r'', include(('gestciv.urls', 'gestciv'), namespace='gestciv')),
    url(r'^gestciv', include(('gestciv.urls', 'gestciv'), namespace='gestciv')),
    url(r'^gestciv/ajax_lookups/', include(ajax_select_urls)),
]
