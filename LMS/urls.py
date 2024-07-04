from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
 
urlpatterns = [
    path('', TemplateView.as_view(template_name='users/index.html'), name='home'),
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('lottery.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
