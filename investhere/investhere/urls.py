from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view as yasg_get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from .views import LogoutView

# Definindo a documentação
schema_view = yasg_get_schema_view(
    openapi.Info(
        title="Investments API",
        default_version='v1',
        description="Documentation of the Investments API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@investments.local"),
        license=openapi.License(name="License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('investimentos.urls')),  # Inclusão das URLs do app investimentos
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-docs'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-docs'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
]
