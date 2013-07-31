# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import Registration

class EventRegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event')
        self.language_code = kwargs.pop('language_code')
        super(EventRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget = forms.Textarea(attrs={'rows': 2})

    def clean(self):
        if self.event.is_registration_deadline_passed:
            raise ValidationError(_('the registration deadline for this event has already passed'))
        return self.cleaned_data

    def save(self, commit=True):
        r = super(EventRegistrationForm, self).save(commit=False)
        r.event = self.event
        r.language_code = self.language_code
        if commit:
            r.save()
        return r

    class Meta:
        model = Registration
        fields = (
            'salutation',
            'company',
            'first_name', 'last_name',
            'address',
            'address_zip', 'address_city',
            'phone',
            'mobile',
            'email',
            'message'
        )