from django import forms


class JobForm(forms.Form):
    skill = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter Skills', 'class': 'form-control'})
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'Enter Job Description', 'class': 'form-control', 'rows': 5})
    )
    location = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter Location', 'class': 'form-control'})
    )
    salary = forms.IntegerField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter Prefered salary', 'class': 'form-control'})
    )
