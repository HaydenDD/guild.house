# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from .models import Booking
from datetime import date, timedelta
from django import forms
from tinymce.widgets import TinyMCE


class BookingAdminForm(forms.ModelForm):

    class Meta(object):
        fields = ['name', 'site', 'reserved_date', 'reserved_time']
        model = Booking
        widgets = {'notes': TinyMCE()}


class BookingForm(forms.ModelForm):

    class Meta(object):
        fields = ['reserved_time', 'reserved_date', 'name', 'party_size', 'email',
                  'phone', 'booking_method', 'notes']
        model = Booking
        widgets = {'notes': TinyMCE()}