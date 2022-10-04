from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi as drf_yasg_openapi
from drf_yasg import views as drf_yasg_views
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view


schema_view = drf_yasg_views.get_schema_view(
    drf_yasg_openapi.Info(
        title="MaxSoft Edu Crm API",
        default_version="v1",
        description="For Learning centers CRM API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=drf_yasg_openapi.Contact(email="info.kamalov@gmail.com"),
        license=drf_yasg_openapi.License(name="Proprietary software license"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    # IsAuthenticated
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API
    path('accounts/', include('api.v1.accounts.urls')),
    
    # Swagger
    path("docs/", include_docs_urls(title="MaxSoft Edu Crm API")),
    path("schema/", get_schema_view(title="APIs", description="MaxSoft Edu Crm API",), name="openapi-schema",),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui",),
    path("swagger/json/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/yaml/", schema_view.without_ui(cache_timeout=0), name="schema-yaml"),
]
