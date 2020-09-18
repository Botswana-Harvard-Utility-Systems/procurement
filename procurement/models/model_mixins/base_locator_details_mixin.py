from django.db import models

from ..address import Address


class BaseLocatorDetailsMixin(models.Model):

    name = models.CharField(max_length=150)

    description = models.CharField(max_length=200)

    address = models.ForeignKey(
        Address, on_delete=models.PROTECT)

    contact_person = models.CharField(
        max_length=100,
        help_text='First and Last Name')

    class Meta:
        abstract = True
