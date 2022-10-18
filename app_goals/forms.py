from django import forms
from .models import Goal


class DateInput(forms.DateInput):
    input_type = 'date'


class GoalForm(forms.ModelForm):
    """Форма цели"""
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
    """Форма изменения цели"""
    title = forms.CharField(max_length=30, required=True)
    value = forms.IntegerField(max_value=999999, required=True)
    deadline = forms.DateField(widget=DateInput, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form_control'
