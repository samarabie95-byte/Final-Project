from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    CATEGORY_CHOICES = [
        ('Backend', 'Backend'),
        ('Frontend', 'Frontend'),
        ('Design', 'Design'),
        ('Writing', 'Writing'),
        ('Other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('Open', 'Open'), 
        ('Assigned', 'Assigned'), 
        ('Completed', 'Completed')
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='Backend')
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    
    risk_assessment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class Bid(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='bids')
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid by {self.freelancer.username} on {self.task.title}"