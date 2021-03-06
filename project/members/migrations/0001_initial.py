# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-12 04:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import project.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('rolodex', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(unique=True)),
                ('name', models.CharField(blank=True, default='', max_length=200, verbose_name='Full Name')),
                ('sort_name', models.CharField(blank=True, default='', max_length=200, verbose_name='Surname')),
                ('ref_name', models.CharField(blank=True, default='', max_length=200, verbose_name='First Name')),
                ('title', models.CharField(blank=True, default='', max_length=64)),
                ('notes', models.TextField(blank=True, default='')),
                ('private_notes', models.TextField(blank=True, default='')),
                ('address', models.TextField(blank=True, default='')),
                ('postcode', models.CharField(blank=True, default='', max_length=16)),
                ('suburb', models.CharField(blank=True, default='', max_length=64)),
                ('state', models.CharField(blank=True, default='', max_length=64)),
                ('country', models.CharField(blank=True, default='Australia', max_length=16)),
                ('year', models.PositiveIntegerField(blank=True, null=True)),
                ('dob', models.DateField(blank=True, help_text='Kept private.', null=True, verbose_name='Birth date')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_current', models.BooleanField(db_index=True, default=True)),
                ('key', models.CharField(blank=True, default='', max_length=64)),
                ('legacy_source', models.CharField(blank=True, default='', max_length=64)),
                ('emails', models.ManyToManyField(blank=True, to='rolodex.Email')),
                ('phones', models.ManyToManyField(blank=True, to='rolodex.Phone')),
                ('site', models.ForeignKey(default=project.utils.get_current_site, on_delete=django.db.models.deletion.PROTECT, related_name='members_member', to='sites.Site')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_type', models.CharField(choices=[('standard', 'Guild Member'), ('family', 'Guild Member Family'), ('student', 'Guild Student Member'), ('special', 'other (please add reason at end)')], max_length=255)),
                ('special', models.CharField(blank=True, default='', max_length=255)),
                ('valid_from', models.DateField()),
                ('valid_until', models.DateField(help_text="As the first day of the month following expiry. Eg. Nov 2018 = '1-Dec-2018'", null=True)),
                ('note', models.CharField(blank=True, default='', max_length=512)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.Member')),
            ],
        ),
        migrations.CreateModel(
            name='MembershipTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('given_at', models.DateTimeField(auto_now_add=True)),
                ('given_tag', models.BooleanField()),
                ('given_card', models.BooleanField()),
                ('membership', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.Membership')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(choices=[('paypal', 'paypal'), ('in person', 'in person')], default='paypal', max_length=128)),
                ('payment_ref', models.CharField(blank=True, default='', max_length=1024)),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.Member')),
            ],
            options={
                'ordering': ['member__name', 'created_at'],
            },
        ),
        migrations.CreateModel(
            name='TemporaryMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_checked', models.BooleanField(default=False)),
                ('is_approved_paid', models.BooleanField(default=False)),
                ('approved_payment_method', models.CharField(blank=True, choices=[('paypal', 'paypal'), ('in person', 'in person')], default='', max_length=255)),
                ('approved_at', models.DateTimeField(blank=True, null=True)),
                ('payment_method', models.CharField(blank=True, choices=[('paypal', 'paypal'), ('in person', 'in person')], default='', max_length=255)),
                ('payment_source', models.CharField(blank=True, choices=[('paypal', 'paypal'), ('in person', 'in person')], default='', max_length=255)),
                ('member_type', models.CharField(blank=True, choices=[('family', 'Guild Member Family'), ('student', 'Guild Student Member'), ('special', 'other (please add reason at end)')], default='', max_length=255)),
                ('name', models.CharField(blank=True, default='', max_length=200, verbose_name='Full Name')),
                ('sort_name', models.CharField(blank=True, default='', max_length=200, verbose_name='Surname')),
                ('ref_name', models.CharField(blank=True, default='', max_length=200, verbose_name='First Name')),
                ('notes', models.TextField(blank=True, default='')),
                ('suburb', models.CharField(max_length=64)),
                ('postcode', models.CharField(max_length=16)),
                ('state', models.CharField(max_length=64)),
                ('country', models.CharField(default='Australia', max_length=32)),
                ('year', models.PositiveIntegerField(blank=True, null=True)),
                ('dob', models.DateField(blank=True, help_text='Kept private, necessary as licenced venue.', null=True, verbose_name='Birth date')),
                ('legacy_source', models.CharField(blank=True, default='', max_length=64)),
                ('survey_games', models.TextField(blank=True, help_text='List as many as you like.', null=True, verbose_name="What's your favourite game?")),
                ('survey_food', models.TextField(blank=True, help_text='Say as much as you want.', null=True, verbose_name='What food, drink or pizza would you like see on our menu?')),
                ('survey_hear', models.TextField(blank=True, help_text='Tell us a story.', null=True, verbose_name='How did you hear about us?')),
                ('survey_suggestions', models.TextField(blank=True, help_text="We're still pretty new and learning as we go!", null=True, verbose_name='Any suggestions you would have for us?')),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('email', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='rolodex.Email')),
                ('member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='members.Member')),
                ('phone', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='rolodex.Phone')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together=set([('member', 'member_type', 'valid_from')]),
        ),
    ]
