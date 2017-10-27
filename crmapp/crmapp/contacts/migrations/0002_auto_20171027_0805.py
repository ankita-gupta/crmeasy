# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='account',
            field=models.ForeignKey(related_name='contact_account', to='accounts.Account'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='owner',
            field=models.ForeignKey(related_name='contact_owner', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
