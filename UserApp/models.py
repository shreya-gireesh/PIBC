from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.
class AdminModel(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_first_name = models.CharField(max_length=100)
    admin_last_name = models.CharField(max_length=100, null=True)
    admin_email = models.EmailField()
    admin_password = models.CharField(max_length=100)
    is_superadmin = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.admin_first_name} {self.admin_last_name}"


class UserModel(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_first_name = models.CharField(max_length=100)
    user_last_name = models.CharField(max_length=100)
    user_email = models.CharField(max_length=100)
    user_phoneno = models.CharField(max_length=100)



class LoanModel(models.Model):
    loan_id = models.AutoField(primary_key=True)
    loan_name = models.CharField(max_length=100)

    def __str__(self):
        return self.loan_name


class StatusModel(models.Model):
    status_id = models.AutoField(primary_key = True)
    status_name = models.CharField(max_length=100)

    def __str__(self):
        return self.status_name


class BankModel(models.Model):
    bank_id = models.AutoField(primary_key = True)
    bank_name = models.CharField(max_length=100)

    def __str__(self):
        return self.bank_name


class LoanApplicationModel(models.Model):
    Accept = 'Accept'
    Reject = 'Reject'
    STATUS_CHOICES = [
        (Accept, 'Accept'),
        (Reject, 'Reject'),
    ]
    form_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=15, null=True)
    loan_name = models.ForeignKey(LoanModel, on_delete=models.CASCADE)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    followup_date = models.DateField()
    description = models.TextField()
    status_name = models.ForeignKey(StatusModel, on_delete=models.CASCADE)
    application_description = models.TextField(null=True)
    bank_name = models.ForeignKey(BankModel, on_delete=models.CASCADE)

    executive_name = models.CharField(max_length=100)
    mobileno_1 = models.CharField(max_length=15)
    mobileno_2 = models.CharField(max_length=15, blank=True, null=True)
    assigned_to = models.ForeignKey(AdminModel, on_delete=models.CASCADE)
    work_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        null=True,
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.loan_name}"



class UploadedFile(models.Model):
    loan_application = models.ForeignKey(LoanApplicationModel, related_name='uploaded_files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/')