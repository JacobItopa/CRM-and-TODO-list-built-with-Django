
from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from base.views import LandingPageView, SignupView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', include('base.urls')),
    path('', LandingPageView.as_view(), name='landing_page'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(next_page='landing_page'), name='logout'),
]
