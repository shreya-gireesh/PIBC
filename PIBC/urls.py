"""
URL configuration for PIBC project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from UserApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('update_status/<int:form_id>', views.update_status, name='update_status'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('application', views.loanform, name='form'),
    path('all-application', views.all_app, name='allapp'),
    path('loan-page/<str:form_id>', views.loan_page, name='loan-page'),
    path('create-user', views.createuser, name='create-user'),
    path('add-loan', views.addloan, name='addloan'),
    path('add-status', views.addstatus, name='addstatus'),
    path('add-bank', views.addbank, name='addbank'),
    path('delete_loan/<int:loan_id>/', views.delete_loan, name='delete_loan'),
    path('delete_status/<int:status_id>/', views.delete_status, name='delete_status'),
    path('delete_bank/<int:bank_id>/', views.delete_bank, name='delete_bank'),
    path('delete_user/<int:admin_id>/', views.delete_user, name='delete_user'),
    path('delete_loan_page/<int:form_id>/', views.delete_loanpage, name='delete_loan_page'),

    #chart
    path('loan-data/', views.get_loan_data, name='get_loan_data'),
    path('loan-totals/', views.get_loan_totals, name='get_loan_totals'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
