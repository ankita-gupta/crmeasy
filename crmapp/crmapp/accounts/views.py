from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from .models import Account


class AccountList(ListView):
    model = Account
    template_name = 'accounts/account_list.html'
    context_object_name = 'accounts'
    paginate_by = 12

    def get_queryset(self):
        try:
            a = self.request.GET.get('account',)
        except KeyError:
            a = None
        if a:
            account_list = Account.objects.filter(name__icontains=a, owner = self.request.user)
        else:
            account_list = Account.objects.filter(owner = self.request.user)
        return account_list

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AccountList, self).dispatch(*args, **kwargs)

class AccountDetail(DetailView):
     model = Account
     template_name = 'accounts/account_detail.html'
     context_object_name = 'account'

     def get_object(self):
        object = get_object_or_404(Account,uuid=self.kwargs.get('uuid'))
        return object

     # @method_decorator(login_required)
     # def dispatch(self, *args, **kwargs):
     #    return super(AccountDetail, self).dispatch(*args, **kwargs)


