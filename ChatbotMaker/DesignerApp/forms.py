from django import forms
from . import models

class AssistantForm(forms.ModelForm):
    '''Creates an Assistant from form data'''
    class Meta:
        model = models.Assistant
        fields = ['sid']
        labels = {
                'sid': 'Assistant SID',
            }

class TaskForm(forms.ModelForm):
    '''Creates a Task from form data'''
    class Meta:
        model = models.Task
        fields = ['sid', 'unique_name', 'assistant']
        labels = {
                'sid': 'Task SID',
                'unique_name': 'Unique Name',
            }
        widgets = {
            'assistant': forms.HiddenInput(),
            'sid': forms.HiddenInput()

        }
