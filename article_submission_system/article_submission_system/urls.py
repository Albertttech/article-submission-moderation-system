# article_submission_system/urls.py

from django.contrib import admin
from django.urls import path, include
from admin_panel.views import home, team_login

urlpatterns = [
    path('', home, name='home'), 
    path('admin/', admin.site.urls),
    path('admin_panel/', include('admin_panel.urls')),
    path('editor/', include('editor_panel.urls')),
    path('moderator/', include('moderator_panel.urls')),  
    path('membership/', include('membership.urls')), 
    path('public/', include('public.urls')),
    path('team/', team_login, name='team_login'),
]