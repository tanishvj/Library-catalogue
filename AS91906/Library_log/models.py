from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from django.utils import timezone

class Book(models.Model):
    book_ddc = models.CharField(primary_key=True, max_length=100)
    book_name = models.CharField(max_length=100)
    book_img = models.ImageField(upload_to='Books/', default='Books/download.jpg', blank=True, null=True)
    book_author = models.CharField(max_length=100, null=False)  # Added max_length here
    book_publisher = models.CharField(blank=True, max_length=100)
    book_category = models.CharField(max_length=100)
    book_available = models.BooleanField(default=True)
    book_copies = models.PositiveIntegerField(null=False, 
                                      validators=[MaxValueValidator(100)],
                                      default=1)
    copies_available = models.PositiveIntegerField(null=False, default=1,
                                      validators=[MaxValueValidator(100)])
    book_isbn = models.CharField(max_length=13, validators=[MinLengthValidator(13)])

    def __str__(self):
        return f"{self.book_name} By {self.book_author}"
    
class User(models.Model):
    user_id = models.CharField(primary_key=True, max_length=100)
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField(max_length=254, unique=True)
    user_password = models.CharField(max_length=100)

    def __str__(self):
        return self.user_name
    
    def requested_books(self):
        return ", ".join(
            req.book.book_name for req in self.reserve_set.filter(request_type="reserve")
        )

    def borrowed_books(self):
        # Adjust status list here as needed
        return ", ".join(
            req.book.book_name for req in self.reserve_set.filter(request_type="borrow", status__in=["borrowed"])
        )

class IssueHistory(models.Model):
    loan_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.user_id} issued {self.book.book_name}"    


class Reserve(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Request Pending'),
        ('not returned', 'Not Returned by Previous User'),
        ('ready', 'Ready for Pickup'),
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
    ]
    reserve_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reserved_at = models.DateTimeField(default=timezone.now)
    request_status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='pending')
    
    class Meta:
        db_table = 'library_log_reserve'

    def __str__(self):
        return f"{self.user.user_id} reserved {self.book.book_name}"
