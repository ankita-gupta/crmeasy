from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.views.generic import DetailView, View, FormView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Contact
from .forms import ContactForm
from crmapp.accounts.models import Account

class ContactDetail(DetailView):
     model = Contact
     template_name = 'contacts/contact_detail.html'
     context_object_name = 'contacts'

     def get_object(self):
         object = get_object_or_404(Contact, uuid=self.kwargs.get('uuid'))
         return object


class ContactCru(FormView):
    model = Contact
    template_name = 'contacts/contact_cru.html'
    form_class = ContactForm

    def dispatch(self, request, *args, **kwargs):
        if 'uuid' in self.kwargs:
            self.contact = get_object_or_404(Contact, uuid=self.kwargs['uuid'])
            if self.contact.owner != request.user:
                return HttpResponseForbidden()
        else:
            self.contact = Contact(owner=request.user)
        if request.GET.get('account', ''):
            self.account = Account.objects.get(id=request.GET.get('account', ''))

        return super(ContactCru, self).dispatch(request, *kwargs, **kwargs)

    def get(self, request, *args, **kwargs):
        self.form = self.form_class(instance=self.contact)
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.form = self.form_class(request.POST, instance=self.contact)
        if self.form.is_valid():
            self.account = self.form.cleaned_data['account']
            if self.account.owner != request.user:
                return HttpResponseForbidden()
            contact = self.form.save(commit=False)
            contact.owner = request.user
            contact.save()
            reverse_url = reverse('account_detail', args=(self.account.uuid,))
            return HttpResponseRedirect(reverse_url)
        else:
            self.account = self.form.cleaned_data['account']

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        ctx = super(ContactCru, self).get_context_data(**kwargs)
        ctx['account'] = self.account
        ctx['contact'] = self.contact
        ctx['form'] = self.form
        return ctx
