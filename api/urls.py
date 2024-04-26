from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import JobApplicationViewSet

router = DefaultRouter()
router.register(r'data', JobApplicationViewSet, basename='job-application')

urlpatterns = [
    path('', include(router.urls)),
]
