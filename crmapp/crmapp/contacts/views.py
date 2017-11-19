from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, View, FormView
from django.views.generic.edit import DeleteView
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
        if request.is_ajax():
            template = 'contacts/contact_item_form.html'
        else:
            template = 'contacts/contact_cru.html'
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
            # reverse_url = reverse('account_detail', args=(self.account.uuid,))
            # return HttpResponseRedirect(reverse_url)
            if request.is_ajax():
                return render(request,
                              'contacts/contact_item_view.html',
                              {'account':self.account, 'contact':contact}
                )
            else:
                reverse_url = reverse(
                    'account_detail',
                    args=(self.account.uuid,)
                )
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

class ContactMixin(object):
    model = Contact

    def get_context_data(self, **kwargs):
        kwargs.update({'object_name':'Contact'})
        return kwargs

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ContactMixin, self).dispatch(*args, **kwargs)


class ContactDelete(ContactMixin, DeleteView):

    template_name = 'object_confirm_delete.html'

    def get_object(self, queryset=None):
        obj = super(ContactDelete, self).get_object()
        if not obj.owner == self.request.user:
            raise Http404
        account = Account.objects.get(id=obj.account.id)
        self.account = account
        return obj

    def get_success_url(self):
        return reverse(
            'account_detail',
            args=(self.account.uuid,)
        )