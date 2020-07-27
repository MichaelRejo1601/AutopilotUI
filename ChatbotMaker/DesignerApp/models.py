from django.db import models

# Create your models here.
class Assistant(models.Model):
    '''A Chatbot a User Makes'''
    sid = models.CharField(max_length=256)
    def __str__(self):
        return str(self.sid)

class Task(models.Model):
    '''Autopilot Task for Chatbot'''
    assistant = models.ForeignKey('Assistant', on_delete=models.CASCADE, related_name='tasks')
    sid = models.CharField(max_length=256)
    unique_name = models.CharField(max_length=256)
    def __str__(self):
        return self.unique_name

class Relationship(models.Model):
    '''Every relationship between tasks'''
    parent = models.CharField(max_length=256)
    child = models.CharField(max_length=256)
    assistant = models.ForeignKey('Assistant', on_delete=models.CASCADE, related_name='relationships')
    def __str__(self):
        return self.parent + "->" + self.child
