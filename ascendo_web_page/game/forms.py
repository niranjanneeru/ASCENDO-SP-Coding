from django import forms

from .models import Response


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['answer']


class AnswerForm(forms.Form):
    answer = forms.CharField(max_length=1000)

    def clean(self):
        cleaned_data = super(AnswerForm, self).clean()
        answer = cleaned_data.get('answer')
        if not answer:
            raise forms.ValidationError('You have to write something!')
