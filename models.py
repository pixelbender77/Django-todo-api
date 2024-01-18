from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    task = models.TextField()
    completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField( auto_now= True)
    updated = models.DateTimeField(auto_now=True )
    user = models.ForeignKey(User , on_delete=models.CASCADE , blank=True , null= True)
    #don't forget there's an id field created automatically along with django models

    def __str__(self):
        return self.task


#timestamp = models.DateTimeField(auto_now_add= True, auto_now= True , blank= True)
    

# Create your models here.
