from django.urls import path
from . import views


urlpatterns = [
    path('', views.jobs, name='jobs'),
    path('prospects/add/', views.create_prospect, name='create-prospect'),
    path('prospects/', views.list_prospects, name='list-prospects'),
    path('prospects/<int:pk>/', views.detail_prospect, name='prospect-detail'),
    path('prospects/<int:pk>/delete/', views.delete_prospect, name='delete-prospect'),
    path('prospects/<int:pk>/change/', views.edit_prospect, name='edit-prospect'),
    path('prospects/<int:pk>/contacts/add/', views.ContactCreateView.as_view(), name='contact-create'),
    path('applications/', views.ApplicationListView.as_view(), name='application-list'),
    path('applications/add', views.ApplicationCreateView.as_view(), name='application-create'),
    path('applications/<int:pk>/', views.ApplicationDetailView.as_view(), name='application-detail'),
    path('applications/<int:pk>/change/', views.ApplicationUpdateView.as_view(), name='application-update'),
    path('applications/<int:pk>/mails/add/', views.MailCreateView.as_view(), name='mail-create'),
    path('letters/<int:pk>/', views.LetterDetailView.as_view(), name='letter'),
    path('mailbox/<int:pk>/', views.MailboxView.as_view(), name='mailbox'),
]
