from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.
class AdminModel(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_first_name = models.CharField(max_length=100)
    admin_last_name = models.CharField(max_length=100,blank=True, null=True)
    admin_email = models.EmailField()
    admin_password = models.CharField(max_length=100)
    is_superadmin = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.admin_first_name} {self.admin_last_name}"


class UserModel(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_first_name = models.CharField(max_length=100)
    user_last_name = models.CharField(max_length=100, null=True, blank=True)
    user_phoneno = models.CharField(max_length=100)
    user_password = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.user_first_name


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

class StaffSelectionModel(models.Model):
    selection_id = models.AutoField(primary_key = True)
    selection = models.CharField(max_length=100)

    def __str__(self):
        return self.selection

class YearModel(models.Model):
    year_id = models.AutoField(primary_key = True)
    year_range = models.CharField(max_length=100)

    def __str__(self):
        return self.year_range


class LoanApplicationModel(models.Model):
    ACCEPT = 'Accept'
    REJECT = 'Reject'
    NOT_SELECTED = 'Not selected'

    STATUS_CHOICES = [
        (ACCEPT, 'Accept'),
        (REJECT, 'Reject'),
        (NOT_SELECTED, 'Not selected'),
    ]

    form_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    place = models.CharField(max_length=100, null=True, blank=True)
    phone_no = models.CharField(max_length=15, null=True, blank=True)

    guaranter_name = models.CharField(max_length=100, null=True, blank=True)
    guaranter_phoneno = models.CharField(max_length=50, null=True, blank=True)
    guaranter_job = models.CharField(max_length=100, null=True, blank=True)
    guaranter_cibil_score = models.CharField(max_length=50, null=True, blank=True)
    guaranter_cibil_issue = models.TextField(null=True, blank=True)
    guaranter_it_payable = models.BooleanField(default=False)
    guaranter_years = models.ForeignKey(YearModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='guaranter_year')

    job = models.CharField(max_length=100, null=True, blank=True)
    cibil_score = models.CharField(max_length=100, null=True, blank=True)
    cibil_issue = models.TextField(null=True, blank=True)
    it_payable = models.BooleanField(default=False)
    years = models.ForeignKey(YearModel, on_delete=models.SET_NULL, null=True,blank=True, related_name='customer_year')

    loan_name = models.ForeignKey(LoanModel, on_delete=models.SET_NULL, null=True, blank=True)
    loan_amount = models.DecimalField(max_digits=10,default=0, decimal_places=2, null=True, blank=True)
    followup_date = models.DateField()
    description = models.TextField(null=True, blank=True)
    status_name = models.ForeignKey(StatusModel, on_delete=models.SET_NULL, null=True, blank=True)
    application_description = models.TextField(null=True, blank=True)
    bank_name = models.ForeignKey(BankModel, on_delete=models.SET_NULL, null=True, blank=True)

    executive_name = models.CharField(max_length=100, null=True, blank=True)
    mobileno_1 = models.CharField(max_length=15,null=True, blank=True)
    mobileno_2 = models.CharField(max_length=15, blank=True, null=True)
    assigned_to = models.ManyToManyField(AdminModel, blank=True)
    document_description = models.TextField(null=True, blank=True)
    workstatus = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=NOT_SELECTED,  # Set default value to "Not selected"
        null=True,
    )
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.loan_name}"




class UploadedFile(models.Model):

    loan_application = models.ForeignKey(LoanApplicationModel, related_name='uploaded_files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/')