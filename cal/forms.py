from django import forms

class EventForm(forms.Form):
    start_time = forms.DateTimeField
    end_time = forms.DateTimeField
    name = forms.CharField(max_length=50)
    desc = forms.CharField(max_length=200)
