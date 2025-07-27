from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from Users import views as Users_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Pred_app/', include('Pred_app.urls')),  # Views classiques
    path('profile/', Users_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='Users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='Users/logout.html'), name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # This line is often needed

  
    #path('register/', Users_views.register,name='register'),
   