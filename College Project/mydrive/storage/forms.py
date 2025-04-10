from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()
    password = forms.CharField(widget=forms.PasswordInput)
