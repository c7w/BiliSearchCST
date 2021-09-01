from django.conf.urls import include
from django.urls import path
from . import views
from utils import DataProcessor

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.root),
    path('video/<id>', views.video),
    path('videoList/', views.videoList),
    path('upList/', views.upList),
    path('up/<int:id>', views.up),
    path('search/', views.search),
    path('merge/', views.mergeData),
]
