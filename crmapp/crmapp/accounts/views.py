from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from .models import Account
from .forms import AccountForm

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

login_required()
def account_cru(request):
    if request.POST:
        form = AccountForm(request.post)
        if form.is_valid():
            account = form.save(commit=False)
            account.owner = request.user
            account.save()
            redirect_url = reverse('account_detail', args=(account.uuid))
            return HttpResponseRedirect(redirect_url)
    else:
        form = AccountForm()

    context = {
        'form': form,
    }
    template = 'accounts/account_cru.html'
    return render(request, template, context)
