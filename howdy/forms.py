from django import forms

class HomeForm(forms.Form):
    symbol = forms.CharField(max_length = 100)

