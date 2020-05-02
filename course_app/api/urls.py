from django.urls import path, include


urlpatterns = [
    path('v1/', include('course_app.api.v1.urls')),
    path('auth/', include('oauth2_provider.urls')),
    path('auth/register/', include('rest_auth.registration.urls')),

]