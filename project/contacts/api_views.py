from rest_framework.response import Response
from rest_framework import status
from .serializers import ContactModelSerializer, ContactAllFieldsModelSerializer
from .models import Contact
from rest_framework.decorators import api_view
import requests

@api_view(['POST','GET'])
def contacts(request):
    if request.method == 'GET':
        """
        This endpoint returns a list of contact record data.
        """
        contacts = Contact.objects.all()
        serializedContactsData = ContactModelSerializer(contacts, many=True).data
        return Response(serializedContactsData, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        """
        This endpoint accepts JSON data for a new contact data. In additional adding latitude and
        longitude to contact record. Data ich fetched form 'nominatim' API.
        """
        data = request.data
        serializedContactsData = ContactAllFieldsModelSerializer(data = data)
        if serializedContactsData.is_valid():
            city = serializedContactsData.validated_data.get('city')
            
            try:
                response = requests.get(f'https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1',
                                    headers={"User-Agent": "Mozilla/5.0"})
                response_data = response.json()
                if not response_data:
                    return Response({"error": f"{city} not found."}, status=status.HTTP_400_BAD_REQUEST)
                lat = round(float(response_data[0]["lat"]), 2)
                lon = round(float(response_data[0]["lon"]), 2)

                contact = serializedContactsData.save()
                contact.latitude = lat
                contact.longitude = lon
                contact.save()
                return Response(ContactAllFieldsModelSerializer(contact).data, status=status.HTTP_201_CREATED)

            except Exception as e:  
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(serializedContactsData.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT','DELETE'])
def change_contact(request, id):
    try:
        get_contact = Contact.objects.get(id = id)
    except Contact.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'DELETE':
        """
        This endpoint allow to delete data by id.
        """
        get_contact.delete()
        return Response(status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        """
        This endpoint accepts JSON data for updating contact data by id. In additional adding latitude and
        longitude to contact record. Data ich fetched form 'nominatim' API.
        """
        data = request.data
        serializedContactData = ContactAllFieldsModelSerializer(get_contact, data=data)
        if serializedContactData.is_valid():
            city = serializedContactData.validated_data.get('city')
            
            try:
                response = requests.get(f'https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1',
                                    headers={"User-Agent": "Mozilla/5.0"})
                response_data = response.json()
                if not response_data:
                    return Response({"error": f"{city} not found."}, status=status.HTTP_400_BAD_REQUEST)
                lat = round(float(response_data[0]["lat"]), 2)
                lon = round(float(response_data[0]["lon"]), 2)

                contact = serializedContactData.save()
                contact.latitude = lat
                contact.longitude = lon
                contact.save()
                return Response(ContactAllFieldsModelSerializer(contact).data, status=status.HTTP_201_CREATED)

            except Exception as e:  
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(serializedContactData.errors, status=status.HTTP_400_BAD_REQUEST)