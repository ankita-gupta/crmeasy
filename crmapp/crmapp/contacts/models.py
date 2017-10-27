from django.db import models
from django.contrib.auth.models import User

from crmapp.accounts.models import Account

from shortuuidfield import ShortUUIDField


class Contact(models.Model):
    uuid = ShortUUIDField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    role = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    account = models.ForeignKey(Account)
    owner = models.ForeignKey(User)
    created_on = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "contacts"

    def __unicode__(self):
        return u'%s' %self.full_name

    @property
    def full_name(self):
        return u'%s %s' %(self.first_name,self.last_name)