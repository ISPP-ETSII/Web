from django import forms

class FlatForm(forms.Form):
    address = forms.CharField(label='Address', max_length=100)
    description = forms.CharField(label='Description', max_length=500)




    #class Meta:
     #   models = Flat
     #  fields = ['description','pictures','owner']