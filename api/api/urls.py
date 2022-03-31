from django.urls import path, include
from django.urls import include, path, re_path
from rest_framework import routers
from django.contrib import admin
from bridge import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView
)

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'userinfos', views.UserInfoViewSet)
router.register(r'chatmessage', views.ChatMessageViewSet)

router.register(r'notify', views.NotifyViewSet)

sub_patterns = [
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path("admin/", admin.site.urls),
    path('wu/activate/<uid>/<token>/', views.ActivateUser.as_view()),
    path('wu/changeemail/', views.ChangeEmail.as_view()),
    path('wu/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
]
urlpatterns = [
    path('api/', include(sub_patterns)),
]
