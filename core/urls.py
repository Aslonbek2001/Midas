from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('admin/', admin.site.urls),
    
    path('users/', include("users.urls")),
    path('cafe/', include("cafe.urls")),
    path('order/', include("order.urls")),
    # path('payment/', include("payment.urls")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)