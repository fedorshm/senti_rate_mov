from django import forms

class TextInputForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label='Введите отзыв о фильме на английском языке для классификации')
