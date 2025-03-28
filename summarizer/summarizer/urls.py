from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from pdfprocessor import views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Authentication
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    
    # Document Processing
    path('', views.upload_pdf, name='upload_pdf'),
    path('summary/<int:pk>/', views.view_summary, name='view_summary'),
    path('accounts/register/', views.register, name='register'),
    
    # User History
    path('history/', views.UserDocumentHistoryView.as_view(), name='document_history'),
    
    # Search
    path('search/', views.legal_search, name='legal_search'),
    
    # Document Management
    path('delete/<int:pk>/', views.delete_document, name='delete_document'),
    path('accounts/password_reset/', views.custom_password_reset, name='password_reset'),
    path('accounts/password_reset/confirm/', views.custom_password_reset_confirm, name='password_reset_confirm'),
    
]