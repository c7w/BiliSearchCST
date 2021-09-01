from django.conf.urls import include
from django.urls import path
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.root),
    path('video/<int:id>', views.video),
    path('videoList/', views.videoList),
    path('upList/', views.upList),
    path('up/<int:id>', views.up),
    path('search/', views.search),
]
