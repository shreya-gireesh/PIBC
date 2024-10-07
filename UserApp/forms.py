from django import forms
from django.core.exceptions import ValidationError

from .models import AdminModel, LoanApplicationModel, UserModel, LoanModel, StatusModel, BankModel


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
            'guaranter_name',
            'guaranter_phoneno',
            'guaranter_job',
            'guaranter_cibil_score',
            'guaranter_cibil_issue',
            'guaranter_it_payable',
            'guaranter_years',
            'job',
            'cibil_score',
            'cibil_issue',
            'it_payable',
            'years',

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
            'assigned_to',
            'document_description'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Last Name', 'required': False}),
            'district': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'District', 'required': False}),
            'place': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Place', 'required': False}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Phone Number', 'required': False}),

            'guaranter_name':forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Name', 'required': False}),
            'guaranter_phoneno':forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Phone Number','required': False}),
            'guaranter_job':forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Job', 'required': False}),
            'guaranter_cibil_score':forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Cibil Score', 'required': False}),
            'guaranter_cibil_issue':forms.Textarea(attrs={'class': 'form-control form-control-user', 'placeholder': 'Cibil Issue', 'rows': 3,'required': False}),
            'guaranter_years': forms.Select(attrs={'class': 'form-select form-control', 'required': False}),

            'job': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Job', 'required': False}),
            'cibil_score': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Cibil Score', 'required': False}),
            'cibil_issue': forms.Textarea(attrs={'class': 'form-control form-control-user', 'placeholder': 'Cibil Issue','rows':3,'required': False}),
            'years': forms.Select(attrs={'class': 'form-select form-control', 'required': False}),

            'loan_name': forms.Select(attrs={'class': 'form-select form-control', 'required': False}),
            'loan_amount': forms.NumberInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Amount', 'required': False}),
            'followup_date': forms.DateInput(attrs={'class': 'form-control form-control-user', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-user', 'placeholder': 'Description', 'rows': 3,'required': False}),
            'status_name': forms.Select(attrs={'class': 'form-select form-control', 'required': False}),
            'application_description': forms.Textarea(
                attrs={'class': 'form-control form-control-user', 'placeholder': 'Description', 'rows': 3, 'required': False}),
            'bank_name': forms.Select(attrs={'class': 'form-select form-control', 'required': False}),
            'executive_name': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Executive Name', 'required': False}),
            'mobileno_1': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Mobile No 1', 'required': False}),
            'mobileno_2': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Mobile No 2', 'required': False}),
            'assigned_to': forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'assigned_to'}),
            'document_description': forms.Textarea(attrs={'class': 'form-control form-control-user', 'placeholder': 'Description', 'rows': 3,'required': False}),

        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(LoanApplicationForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = AdminModel.objects.filter(is_superadmin=False)


        non_editable_fields = [
            'first_name',
            'last_name',
            'district',
            'place',
            'phone_no',
            'loan_name',
            'loan_amount',
            'bank_name',
            'executive_name',
            'mobileno_1',
            'mobileno_2',
            'assigned_to'
        ]

        # If the user is not super_admin, disable the fields
        if user and not user.is_superadmin:  # Or user.is_super_admin if you have a custom super_admin attribute
            for field in non_editable_fields:
                self.fields[field].disabled = True  # Disable the field

    def clean_phone_no(self):
        phone_no = self.cleaned_data.get('phone_no')
        if phone_no and len(phone_no) != 10:
            raise ValidationError("Phone number must be exactly 10 digits.")
        return phone_no

    def clean_mobileno_1(self):
        mobileno_1 = self.cleaned_data.get('mobileno_1')
        if mobileno_1 and len(mobileno_1) != 10:
            raise ValidationError("Mobile number must be exactly 10 digits.")
        return mobileno_1

    def clean_mobileno_2(self):
        mobileno_2 = self.cleaned_data.get('mobileno_2')
        if mobileno_2 and len(mobileno_2) != 10:
            raise ValidationError("Mobile number must be exactly 10 digits.")
        return mobileno_2
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


class BankForm(forms.ModelForm):
    class Meta:
        model = BankModel
        fields = ['bank_name']
        widgets = {
            'bank_name': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Bank Name'})
        }

class UserForm(forms.ModelForm):
    repeat_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-control-user', 'placeholder': 'Repeat Password'}
        ),
        label="Repeat Password"
    )

    class Meta:
        model = UserModel
        fields = ['user_first_name', 'user_last_name', 'user_phoneno', 'user_password']
        widgets = {
            'user_first_name': forms.TextInput(
                attrs={'class': 'form-control form-control-user', 'placeholder': 'First Name'}),
            'user_last_name': forms.TextInput(
                attrs={'class': 'form-control form-control-user', 'placeholder': 'Last Name'}),
            'user_phoneno': forms.TextInput(
                attrs={'class': 'form-control form-control-user', 'placeholder': 'Phone Number'}),
            'user_password': forms.PasswordInput(
                attrs={'class': 'form-control form-control-user', 'placeholder': 'Password'}),
        }
    def clean_user_phoneno(self):
        phoneno = self.cleaned_data.get('user_phoneno')
        if UserModel.objects.filter(user_phoneno=phoneno).exists():
            raise ValidationError("An admin with this phone number already exists.")
        if len(phoneno) != 10 or not phoneno.isdigit():
            raise ValidationError("Phone Number must be exactly 10 digits and contain only numbers.")
        return phoneno

    def clean_user_password(self):
        password = self.cleaned_data.get('user_password')
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        # Add more password validations if needed (e.g., complexity)
        return password

    def clean_repeat_password(self):
        repeat_password = self.cleaned_data.get('repeat_password')
        password = self.cleaned_data.get('user_password')

        if password and repeat_password and password != repeat_password:
            raise ValidationError("Passwords do not match.")

        return repeat_password