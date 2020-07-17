from django import forms
from . import models

class CreateAssistant(forms.ModelForm):
    '''Creates an Assistant from form data'''
    class Meta:
        model = models.Assistant
        fields = ['sid']
        labels = {
                'sid': 'Assistant SID: ',
            }

class CreateTask(forms.ModelForm):
    '''Creates a Task from form data'''
    class Meta:
        model = models.Task
        fields = ['sid', 'unique_name']
        labels = {
                'sid': 'Task SID: ',
            }
