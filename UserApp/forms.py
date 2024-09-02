from django import forms
from .models import  AdminModel, LoanApplicationModel


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

    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Repeat Password'}))

    def clean(self):
        cleaned_data = super().clean()
        password = self.cleaned_data.get("admin_password")
        repeat_password = self.cleaned_data.get("repeat_password")

        if password != repeat_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data



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
            'bank_name',
            'executive_name',
            'mobileno_1',
            'mobileno_2',
            ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Last Name'}),
            'district': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'District'}),
            'place': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Place'}),
            'phone_no': forms.TextInput(
                attrs={'class': 'form-control form-control-user', 'placeholder': 'Phone Number'}),
            'loan_name': forms.Select(attrs={'class': 'form-select form-control'}),
            'loan_amount': forms.NumberInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Amount'}),
            'followup_date': forms.DateInput(attrs={'class': 'form-control form-control-user', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-user', 'placeholder': 'Description', 'rows': 3}),
            'status_name': forms.Select(attrs={'class': 'form-select form-control'}),
            'bank_name': forms.Select(attrs={'class': 'form-select form-control'}),
            'executive_name': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Executive Name'}),
            'mobileno_1': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Mobile No 1'}),
            'mobileno_2': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Mobile No 2'}),
        }

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