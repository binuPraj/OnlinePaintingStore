from django import forms

class userForm(forms.Form):
    num3=forms.CharField(label='value1', required=False, widget=forms.Textarea(attrs={'class':'form-control'})) #form control le bootstrapko euta classlai apply type garne ho, textareako satta textinput ni garda hunxa for small ones
    num4=forms.CharField(label='value2')
    email=forms.EmailField()