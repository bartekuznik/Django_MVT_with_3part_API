from django.urls import path
from .api_views import contacts, change_contact
from .views import ContactListView, ContactDetailView, ContactCreateView, ContactUpdateView, ContactDeleteView

urlpatterns = [
    #API views

    path('api/contacts/', contacts, name='contacts'),
    path('api/contacts/<int:id>/', change_contact, name='change_contact'),

    #MVT views
    path('', ContactListView.as_view(),name='contact_list'),
    path('contacts/', ContactListView.as_view(),name='contact_list'),
    path('contacts/<str:order>/', ContactListView.as_view(),name='contact_list_ordered'),
    path('contact/<int:id>/', ContactDetailView.as_view(),name='contact_detail'),
    path('contact/add/',ContactCreateView.as_view(), name='contact_create'),
    path('contact/<int:pk>/update/', ContactUpdateView.as_view(),name='contact_update'),
    path('contact/<int:pk>/delete/', ContactDeleteView.as_view(),name='contact_delete'),
]