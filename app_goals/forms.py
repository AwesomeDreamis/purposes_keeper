from django import forms
from .models import Goal, Operation


class DateInput(forms.DateInput):
    input_type = 'date'


class GoalForm(forms.ModelForm):
    title = forms.CharField(max_length=30, required=True)
    value = forms.IntegerField(max_value=999999, required=True)
    deadline = forms.DateField(widget=DateInput, required=True)

    class Meta:
        model = Goal
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form_control'


class GoalUpdateForm(forms.Form):
    title = forms.CharField(max_length=30, required=True)
    value = forms.IntegerField(max_value=999999, required=True)
    deadline = forms.DateField(widget=DateInput, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form_control'
