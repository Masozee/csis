from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


admin.sites.AdminSite.site_header = 'Centre for Strategic and International Studies'
admin.sites.AdminSite.site_title = 'Centre for Strategic and International Studies'
admin.sites.AdminSite.index_title = 'Centre for Strategic and International Studies'

urlpatterns = [ 
    path('admin/clearcache/', include('clearcache.urls')),
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('', include('web.url')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('password-reset', auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"),
         name="password_reset"),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
         name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"),
         name="password_reset_confirm"),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
         name="password_reset_complete"),
]

handler404 = "web.views.page_not_found_view"

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)