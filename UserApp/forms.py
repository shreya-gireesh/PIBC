from django import forms
from django.core.exceptions import ValidationError

from .models import AdminModel, LoanApplicationModel, UserModel, LoanModel, StatusModel


class AdminForm(forms.ModelForm):
    class Meta:
        model = AdminModel
        fields = ['admin_first_name', 'admin_last_name', 'admin_email', 'admin_password']
        widgets = {
            'admin_first_name': forms.TextInput(
                attrs={'class': 'form-control form-control-user', 'placeholder': 'First Name'}),
            'admin_last_name': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Last Name'}),
            'admin_email': forms.EmailInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Email Address'}),
            'admin_password': forms.PasswordInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Password'}),
        }


    def clean_admin_email(self):
        email = self.cleaned_data.get('admin_email')
        if AdminModel.objects.filter(admin_email=email).exists():
            raise ValidationError("An admin with this email already exists.")
        return email

    def clean_admin_password(self):
        password = self.cleaned_data.get('admin_password')
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        # Add more password validations if needed (e.g., complexity)
        return password


class LoanApplicationForm(forms.ModelForm):

    class Meta:
        model = LoanApplicationModel
        fields = [
            'first_name',
            'last_name',
            'district',
            'place',
            'phone_no',
            'loan_name',
            'loan_amount',
            'followup_date',
            'description',
            'status_name',
            'application_description',
            'bank_name',
            'executive_name',
            'mobileno_1',
            'mobileno_2',
            'assigned_to'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Last Name'}),
            'district': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'District'}),
            'place': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Place'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Phone Number'}),
            'loan_name': forms.Select(attrs={'class': 'form-select form-control'}),
            'loan_amount': forms.NumberInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Amount'}),
            'followup_date': forms.DateInput(attrs={'class': 'form-control form-control-user', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-user', 'placeholder': 'Description', 'rows': 3}),
            'status_name': forms.Select(attrs={'class': 'form-select form-control'}),
            'application_description': forms.Textarea(
                attrs={'class': 'form-control form-control-user', 'placeholder': 'Description', 'rows': 3}),
            'bank_name': forms.Select(attrs={'class': 'form-select form-control'}),
            'executive_name': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Executive Name'}),
            'mobileno_1': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Mobile No 1'}),
            'mobileno_2': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Mobile No 2'}),
            'assigned_to':forms.Select(attrs={'class': 'form-select form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(LoanApplicationForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = AdminModel.objects.filter(is_superadmin=False)
    # def clean_phone_no(self):
    #     phone_no = self.cleaned_data.get('phone_no')
    #
    #     # Exclude the current instance from the query if it's an update
    #     if self.instance.pk:
    #         if LoanApplicationModel.objects.exclude(pk=self.instance.pk).filter(phone_no=phone_no).exists():
    #             raise forms.ValidationError('A loan application with this phone number already exists.')
    #     else:
    #         if LoanApplicationModel.objects.filter(phone_no=phone_no).exists():
    #             raise forms.ValidationError('A loan application with this phone number already exists.')
    #
    #     return phone_no

class LoanForm(forms.ModelForm):
    class Meta:
        model =LoanModel
        fields = ['loan_name']
        widgets = {
            'loan_name': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Loan Name'})
        }

class StatusForm(forms.ModelForm):
    class Meta:
        model = StatusModel
        fields = ['status_name']
        widgets = {
            'status_name': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Status Type'})
        }