from django.db import models
from django.contrib.auth.models import AbstractUser


# Main user account
# Gives us username, email, password, login etc.
class User(AbstractUser):
    pass

# Extra profile only for users who want to work
class WorkerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #CASCADE = delete related data too.Connect each worker profile to exactly one registered user.if that User account is deleted, its WorkerProfile is also deleted

    speciality = models.CharField(max_length=100)
    device = models.CharField(max_length=100)
    price_per_hour = models.DecimalField(max_digits=8 , decimal_places=2)

    LOCATION_CHOICES = [
        ('Mumbai', 'Mumbai'),
        # database  , shown to user ('stored_value', 'display_name')
        ('Thane', 'Thane'),
        ('Navi Mumbai', 'Navi Mumbai'),
        ('Pune', 'Pune'),
    ]   
    location = models.CharField(
        max_length=50,
        choices=LOCATION_CHOICES
    )

    bio = models.TextField(blank = True)
    
    def __str__(self):
        return self.user.username
        # Whenever you show this WorkerProfile, show its user's username instead.
  
class Booking(models.Model):
    user = models.ForeignKey(User , on_delete= models.CASCADE)
    worker = models.ForeignKey(WorkerProfile, on_delete= models.CASCADE)
    event_type = models.CharField(max_length=100)
    event_date = models.DateField()
    start_time = models.TimeField()
    duration = models.IntegerField()
    location = models.CharField(max_length=200)
    message = models.TextField(blank=True)

    STATUS_CHOICES = [
    ("Pending", "Pending"),
    ("Accepted", "Accepted"),
    ("Rejected", "Rejected"),
    ("Completed", "Completed"),
]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.worker.user.username}"

class Review(models.Model):

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    worker = models.ForeignKey(
        WorkerProfile,
        on_delete=models.CASCADE
    )

    rating = models.IntegerField()
    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} → {self.worker.user.username}"
