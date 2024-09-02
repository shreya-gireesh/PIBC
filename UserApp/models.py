from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.
class AdminModel(models.Model):
    admin_id = models.CharField(primary_key=True, max_length=20, unique=True)
    admin_first_name = models.CharField(max_length=100)
    admin_last_name = models.CharField(max_length=100, null=True)
    admin_email = models.EmailField()
    admin_password = models.CharField(max_length=100)

@receiver(pre_save, sender=AdminModel)
def generate_unique_id(sender, instance, **kwargs):
    if not instance.admin_id:
        last_admin = AdminModel.objects.all().order_by('admin_id').last()
        if last_admin:
            new_id = int(last_admin.admin_id.split('ADM')[-1]) + 1
        else:
            new_id = 1
        instance.admin_id = f"ADM{new_id:05d}"


class UserModel(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_first_name = models.CharField(max_length=100)
    user_last_name = models.CharField(max_length=100)
    user_email = models.CharField(max_length=100)
    user_password = models.CharField(max_length=100)


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
    form_id = models.CharField(primary_key=True, max_length=100)
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
    bank_name = models.ForeignKey(BankModel, on_delete=models.CASCADE)

    executive_name = models.CharField(max_length=100)
    mobileno_1 = models.CharField(max_length=15)
    mobileno_2 = models.CharField(max_length=15, blank=True, null=True)
    admin = models.ForeignKey(AdminModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.loan_name}"


@receiver(pre_save, sender=LoanApplicationModel)
def generate_unique_id(sender, instance, **kwargs):
    if not instance.form_id:
        last_loan = LoanApplicationModel.objects.all().order_by('form_id').last()
        if last_loan:
            new_id = int(last_loan.form_id.split('FORM')[-1]) + 1
        else:
            new_id = 1
        instance.form_id = f"FORM{new_id:05d}"