from django.urls import include, path, re_path
from rest_framework import routers
from . import views

API = routers.DefaultRouter()
API.register(r'users', views.UserViewSet)
API.register(r'groups', views.GroupViewSet)
API.register(r'jobs', views.JobViewSet)

#urlpatterns = router.urls
# pylint: disable=invalid-name
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('jobs/', views.JobList.as_view(), name='jobs'),
    path('jobs/<uuid:pk>', views.JobDetail.as_view(), name='job'),
    path('job/<uuid:pk>/delete/', views.JobDelete.as_view(), name='job-delete'),
    path('api/', include(API.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^docs/*', views.docs, name='docs')
]

#urlpatterns += ROUTES.urls
