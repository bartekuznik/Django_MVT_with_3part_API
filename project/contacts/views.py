from django.shortcuts import render
from .models import Contact
from django.views import View
import requests
from django.core.cache import cache
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .utils import get_contact_data
from django.core.cache import cache
from .forms import ContactForm
    
class ContactListView(View):
    def get(self, request, order=None):
        """
        Handles displaying the contact list and sorting order. When 
        data is retrieved form database they get unique cache key based on id.
        If weather data is in cache, it is retrieved from there, else it is 
        called get_contact_data function.

        Args:
            request: The HTTP request object.
            order: An optional argument for sorting contacts.

        """

        order_choice = {
            'name': 'last_name',
            'name_desc': '-last_name',
            'created': 'created_at',
            'created_desc': '-created_at'
        }

        if not order:
            contacts_db = Contact.objects.all()
        else:
            if order in order_choice:
                contacts_db = Contact.objects.all().order_by(order_choice[order])
            else:
                contacts_db = Contact.objects.all()

        for contact in contacts_db:
            cache_key = f'weather_data_contact_{contact.id}'
            cached_weather = cache.get(cache_key)
            if cached_weather:
                weather = cached_weather
            else:
                try:
                    weather = get_contact_data(cache_key, contact.latitude, contact.longitude)
                except requests.RequestException:
                    weather ={
                        'temperature': "N/A",
                        'humidity': 'N/A',
                        'windspeed': 'N/A',
                        'is_day': 'N/A',
                        'rain': 'N/A',
                        'cloud_cover': 'N/A',
                        }

            contact.weather = weather

        context = {'contacts':contacts_db, "order_choice":order_choice}
        return render(request, 'contacts/contact_list.html', context)

class ContactDetailView(View):
    def get(self, request, id):
        """
        Handles displaying the contact detail

        Args:
            request: The HTTP request object.
            id: The contact id of contact being viewed

        """
        contact = Contact.objects.get(id = id)
        context = {'contact': contact}
        return render(request, 'contacts/contact_detail.html', context)
    
class ContactCreateView(CreateView):
    """
    View for creating a new contact.
        
    Methods:
        form_valid(): Customizes the form submission by adding latitude and
                      longitude to contact record. Data ich fetched form 
                      'nominatim' API.

    """

    model = Contact
    form_class = ContactForm
    template_name = 'contacts/create_contact.html'
    success_url = reverse_lazy('contact_list')

    
    def form_valid(self, form):
        contact = form.save(commit=False)
        city = form.cleaned_data.get("city")

        try:
            response = requests.get(f'https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1',
                headers={"User-Agent": "Mozilla/5.0"}
            )
            response.raise_for_status()
            response_data = response.json()

            if response_data:
                contact.latitude = round(float(response_data[0]["lat"]), 2)
                contact.longitude = round(float(response_data[0]["lon"]), 2)
        except requests.RequestException:
            contact.latitude = None
            contact.longitude = None
        
        contact.save()
        return super().form_valid(form)
    
class ContactUpdateView(UpdateView):
    """
    View for updating a contact.
        
    Methods:
        form_valid(): Customizes the form submission by adding latitude and
                      longitude to contact record. Data ich fetched form 
                      'nominatim' API. Existing cache data is also updated.

    """
    model = Contact
    form_class = ContactForm
    template_name = 'contacts/edit_contact.html'
    success_url = reverse_lazy('contact_list')
    
    def form_valid(self, form):
        contact = form.save(commit=False)
        city = form.cleaned_data.get("city")

        try:
            response = requests.get(f'https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1',
                headers={"User-Agent": "Mozilla/5.0"}
            )
            response.raise_for_status()
            response_data = response.json()

            if response_data:
                contact.latitude = round(float(response_data[0]["lat"]), 2)
                contact.longitude = round(float(response_data[0]["lon"]), 2)

                cache_key = f'weather_data_contact_{contact.id}'
                get_contact_data(cache_key, contact.latitude, contact.longitude)
        except requests.RequestException:
            contact.latitude = None
            contact.longitude = None
        
        contact.save()
        return super().form_valid(form)
    

class ContactDeleteView(DeleteView):
    """
    View for deleting a contact.
    """
    model = Contact
    template_name = 'contacts/delete_contact.html'
    success_url = reverse_lazy('contact_list')