# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import re
import datetime
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.db import models, IntegrityError
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from taggit.managers import TaggableManager

from project import utils
from . import querysets, settings

def get_current_site():
    try:
        return Site.objects.get_current().pk
    except Site.DoesNotExist:
        pass

@python_2_unicode_compatible
class Booking(models.Model):

    code = models.CharField(max_length=8, blank=True, default='')

    name = models.CharField(max_length=200)

    party_size = models.PositiveIntegerField()

    status = models.CharField(max_length=50, choices=settings.STATUS_CHOICE,
                              default=settings.STATUS_CHOICE[0][0])

    area = models.CharField(max_length=50, choices=settings.AREA_CHOICE,
                            default=settings.AREA_CHOICE[0][0])

    notes = models.TextField(blank=True, default='')

    private_notes = models.TextField(blank=True, default='')

    email = models.EmailField(max_length=150, blank=True, default='')

    phone = models.CharField(max_length=100,
                             help_text="One phone number only. Put additional numbers in 'notes' if necessary. We may need to confirm details so be sure to provide a good number."
                             )

    postcode = models.CharField(max_length=16, blank=True, default='')

    booking_method = models.CharField(max_length=50, choices=settings.METHOD_CHOICE,
                                      default=settings.METHOD_CHOICE[0][0],
                                      help_text="Only logged in people can see booking method."
    )

    user = models.ForeignKey(User, blank=True, null=True)

    site = models.ForeignKey('sites.Site', default=get_current_site,
                             related_name='bookings_booking',
                             on_delete=models.PROTECT)

    reserved_date = models.DateField(db_index=True)
    reserved_time = models.TimeField(db_index=True, default=timezone.now)

    booking_duration = models.DurationField(blank=True, null=True)

    service = models.CharField(max_length=50, choices=settings.SERVICE_CHOICE,
                               blank=True, default=''
                               )

    busy_night = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    updated_at = models.DateTimeField(auto_now=True, editable=False)

    updated_by = models.ForeignKey(User, blank=True, null=True,
                                   related_name="booking_updated_by"
                                   )

    hear_choices = models.CharField(max_length=56, blank=True, default='',
                                    choices=settings.HEAR_CHOICE,
                                    verbose_name="Choices",
                                    help_text="How did you hear about us?"
                                    )
    hear_other = models.TextField(blank=True, default='',
                                  verbose_name="Other",
                                  help_text="Tell us a story about how you heard about us ..."
                                  )

    legacy_code = models.CharField(max_length=256, blank=True, null=True)

    objects = querysets.QuerySet.as_manager()

    class Meta(object):
        ordering = ['reserved_date', 'reserved_time', 'name']
        verbose_name_plural = 'bookings'

    def __str__(self):
        desc = "{date} {start} {pax}pax {name}".format(
            name=self.name,
            pax=self.party_size,
            date=self.reserved_date.strftime("%d-%b-%Y"),
            start=self.reserved_time.strftime("%H:%M")
        )

        if self.booking_duration:
            desc = "{date} {start} {pax}pax {name}".format(
                name=self.name,
                pax=self.party_size,
                date=self.reserved_date.strftime("%d-%b-%Y"),
                start=self.reserved_time.strftime("%H:%M")
            )
        return desc

    def get_absolute_url(self):
        return reverse('bookings:booking_update', kwargs={'code': self.code})

    def get_next(self):
        queryset = self.__class__.objects.exclude(pk=self.pk).filter(
            site=self.site, reserved_date__gte=self.reserved_date
        ).active().order_by('reserved_date', 'reserved_time')
        return queryset.first()

    def get_previous(self):
        queryset = self.__class__.objects.exclude(pk=self.pk).filter(
            site=self.site, reserved_date__lte=self.reserved_date
        ).active().order_by('-reserved_date', 'reserved_time')
        return queryset.first()

    def is_active(self):
        return self in self.__class__.objects.filter(pk=self.pk).active()
    is_active.boolean = True
    is_active.short_description = 'active'

    def save(self, *args, **kwargs):
        self.clean()

        if self.legacy_code and Booking.objects.filter(
                legacy_code=self.legacy_code):
            return False

        # Automatically make code if doesn't already have one.
        if not self.code:
            self.code = utils.generate_unique_hex(
                queryset=Booking.objects.all())

            # adding on first creation. Messy, but works.
            # @@TODO make this less crap
            if "full" in self.private_notes:
                self.busy_night = True
                for booking in Booking.objects.filter(
                        reserved_date=self.reserved_date):
                    booking.busy_night = True
                    booking.save()

        # Automatically set `service` (eg. lunch) based upon `reserved_time`.
        for service_time, service in reversed(settings.SERVICE_TIMES):
            if self.reserved_time >= service_time:
                this_service = service
                break
        self.service = this_service

        # Create a user whose username is their phone number.
        """ This was a tough decision to use phone number as username.

        This is legacy from the original system where only phone number was
        required.
        """
        if not self.user:
            if not self.phone:
                username = password = self.email
            else:
                username = password = self.phone
            try:
                user = User.objects.create_user(username=username)
                user.first_name = self.name
                if self.email:
                    ## @@TODO: add multiple emails to user check if variant email
                    user.email = self.email
                user.save()
            except IntegrityError:
                user = User.objects.get(username=username)
                self.user = user
            except ValueError:
                ## @@TODO fallback "Unknown" user done this way feels like potential blackhole
                user = User.objects.get(username="unknown")
            if self.email:
                user.email = self.email
                user.save()
            self.user = user

        super(Booking, self).save(*args, **kwargs)
