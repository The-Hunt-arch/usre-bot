from django.db import models

# Create your models here.

from django.db import models

class JobApplication(models.Model):
    REVIEW_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    higher_degree = models.CharField(max_length=100)
    skills = models.TextField()
    years_of_experience = models.IntegerField()
    # New fields
    current_ctc = models.DecimalField(max_digits=10, decimal_places=2)  # Current CTC (Cost to Company)
    expected_ctc = models.DecimalField(max_digits=10, decimal_places=2)  # Expected CTC
    np = models.IntegerField()  # Notice period in days
    counter = models.IntegerField(default=0)  # Counter (default value: 0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')  # Status

    review_job_description = models.CharField(max_length=3, choices=REVIEW_CHOICES)
    resume = models.FileField(upload_to='resumes/')

    def __str__(self):
        return self.full_name
