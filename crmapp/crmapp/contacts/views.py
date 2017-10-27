from django.shortcuts import render
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from .models import Contact

class ContactDetail(DetailView):
     model = Contact
     template_name = 'contacts/contact_detail.html'
     context_object_name = 'contacts'

     def get_object(self):
         object = get_object_or_404(Contact, uuid=self.kwargs.get('uuid'))
         return object
