from django import forms

class FlatForm(forms.Form):
    address = forms.CharField(label='Address', max_length=100)
    description = forms.CharField(label='Description', max_length=500)

class ProfileForm(forms.Form):
    avatar = forms.ImageField()
    owner = forms.CharField(label='Owner',max_length=50)
    code = forms.CharField(label='Code',max_length=16)
    cvv = forms.CharField(label='CVV',max_length=3)