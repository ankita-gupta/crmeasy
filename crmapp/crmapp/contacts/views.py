from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.views.generic import DetailView, View
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Contact
from .forms import ContactForm


class ContactDetail(DetailView):
     model = Contact
     template_name = 'contacts/contact_detail.html'
     context_object_name = 'contacts'

     def get_object(self):
         object = get_object_or_404(Contact, uuid=self.kwargs.get('uuid'))
         return object


class ContactCru(View):
    model = Contact
    template_name = 'contacts/contact_cru.html'
    form_class = ContactForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form' : form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            account = form.cleaned_data['account']
            if account.owner != request.user:
                return HttpResponseForbidden()
            contact = form.save(commit=False)
            contact.owner = request.user
            contact.save()
            reverse_url = reverse('account_detail', args=(account.uuid,))
            return HttpResponseRedirect(reverse_url)

        return render(request, self.template_name, {'form':form})

