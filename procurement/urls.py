from django.urls.conf import path
from django.views.generic.base import RedirectView

from .admin_site import procurement_admin

app_name = 'procurement'

urlpatterns = [
    path('admin/', procurement_admin.urls),
    path('', RedirectView.as_view(url='admin/'), name='home_url'),
]
