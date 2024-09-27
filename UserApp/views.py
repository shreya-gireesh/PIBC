from idlelib.iomenu import errors

from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncYear
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from UserApp.models import *
from UserApp.forms import *

# Create your views here.
def home(request):
    user = request.session.get('user', None)
    if user is None:
        return redirect('/login')
    else:
        admin = AdminModel.objects.get(admin_id = user)
        if admin.admin_last_name:
            admin_name = f"{admin.admin_first_name} {admin.admin_last_name}"
        else:
            admin_name = f"{admin.admin_first_name}"
        loan_form = LoanApplicationModel.objects.filter(
            assigned_to=user
        )
        #
        # # Loans assigned to the user where status is "Accept"
        accepted_loans = loan_form.filter(workstatus='Accept')
        new_loans = loan_form.filter(workstatus = 'Not selected')
        accepted_loans_count = accepted_loans.count()

        today = datetime.now().date()
        all_loans = LoanApplicationModel.objects.filter(followup_date = today, workstatus='Accept')
        loan_followup = all_loans.filter(assigned_to = user)
        all_users = AdminModel.objects.filter(is_superadmin = False)
        all_users_count = all_users.count()
        loan_app = LoanApplicationModel.objects.all()
        loan_app_count = loan_app.count()
        last_loan_app = loan_app.order_by('-form_id')[:10]

        if admin.is_superadmin :
            context = {
                'username': admin_name,
                'forms': last_loan_app,
                'loans': all_loans,
                'total_users_count': all_users_count,
                'loan_app_count': loan_app_count,
                'all_users': all_users,
                'admin': admin
            }
        else:
            if request.method == 'POST':
                # Check if the user is submitting an update for the status
                status = request.POST.get('status')

                if status in ['Accept', 'Reject']:
                    loan_form.workstatus = status
                    loan_form.save()
            context = {
                'username': admin_name,
                'forms': accepted_loans,
                'new_loans': new_loans,
                'loans': loan_followup,
                'total_users_count': all_users_count,
                'loan_app_count': accepted_loans_count,
                'admin': admin
            }
        return render(request, 'index.html', context)


def update_status(request, form_id):
    # Get the loan form by its ID
    loan_form = get_object_or_404(LoanApplicationModel, form_id=form_id)

    if request.method == 'POST':
        # Check if the user is submitting an update for the status
        status = request.POST.get('status')

        if status in ['Accept', 'Reject']:
            loan_form.workstatus = status
            loan_form.save()

        # After updating the status, redirect back to the home page
        return redirect('/')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            admin = AdminModel.objects.get(admin_email=email, admin_password=password)
            request.session['user'] = admin.admin_id
            request.session.set_expiry(3600)
            return redirect('/')
        except AdminModel.DoesNotExist:
            return render(request, 'login.html', {'error': "User not found"})
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        form = AdminForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = AdminForm()
    return render(request, 'login.html', {'form': form})


def loanform(request):
    user = request.session.get('user', None)
    if user is None:
        return redirect('/login')
    else:
        admin = AdminModel.objects.get(admin_id=user)
        if admin.admin_last_name:
            admin_name = f"{admin.admin_first_name} {admin.admin_last_name}"
        else:
            admin_name = f"{admin.admin_first_name}"
        loan = LoanModel.objects.all()
        status = StatusModel.objects.all()
        bank = BankModel.objects.all()
        if request.method == 'POST':
            files = request.FILES.getlist('files')
            form = LoanApplicationForm(request.POST, request.FILES)
            if form.is_valid():
                loan_form = form.save()
                for file in files:
                    UploadedFile.objects.create(
                        file = file,
                        loan_application=LoanApplicationModel.objects.get(form_id=loan_form.form_id )
                    )
                return redirect('/')
        else:
            form = LoanApplicationForm()
        return render(request, 'loan-form.html',{'username':admin_name,'admin':admin,'loan':loan, 'status': status, 'bank': bank, 'form': form})



def loan_page(request, form_id):
    user = request.session.get('user', None)
    if user is None:
        return redirect('/login')
    else:
        admin = AdminModel.objects.get(admin_id=user)
        if admin.admin_last_name:
            admin_name = f"{admin.admin_first_name} {admin.admin_last_name}"
        else:
            admin_name = f"{admin.admin_first_name}"
        # Get the specific form entry by ID
        form_instance = get_object_or_404(LoanApplicationModel, form_id=form_id)
        files = UploadedFile.objects.filter(loan_application=form_instance)

        #Check if the form was submitted
        if request.method == 'POST':

            form = LoanApplicationForm(request.POST, instance=form_instance)
            if admin.is_superadmin:
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                district = request.POST.get('district')
                place = request.POST.get('place')
                phone_no = request.POST.get('phone_no')
                loan_name = request.POST.get('loan_name')
                loan_amount = request.POST.get('loan_amount')
                bank_name = request.POST.get('bank_name')
                executive_name = request.POST.get('executive_name')
                mobileno_1 = request.POST.get('mobileno_1')
                mobileno_2 = request.POST.get('mobileno_2')
                followup_date = request.POST.get('followup_date')
                description = request.POST.get('description')
                status_name = request.POST.get('status_name')
                application_description = request.POST.get('application_description')
                assigned_to = request.POST.get('assigned_to')

                form_instance.first_name = first_name
                form_instance.last_name = last_name
                form_instance.district = district
                form_instance.place = place
                form_instance.phone_no = phone_no
                form_instance.loan_name = LoanModel.objects.get(loan_id=loan_name)
                form_instance.loan_amount = loan_amount
                form_instance.followup_date = followup_date
                form_instance.description = description
                form_instance.status_name = StatusModel.objects.get(status_id=status_name)
                form_instance.application_description = application_description
                form_instance.bank_name = BankModel.objects.get(bank_id=bank_name)
                form_instance.executive_name = executive_name
                form_instance.mobileno_1 = mobileno_1
                form_instance.mobileno_2 = mobileno_2
                if assigned_to:
                    form_instance.assigned_to = AdminModel.objects.get(admin_id=assigned_to)
                    form_instance.work_status = LoanApplicationModel.NOT_SELECTED

            else:
                followup_date = request.POST.get('followup_date')
                description = request.POST.get('description')
                status_name = request.POST.get('status_name')
                application_description = request.POST.get('application_description')

                form_instance.followup_date = followup_date
                form_instance.description = description
                form_instance.status_name = StatusModel.objects.get(status_id=status_name)
                form_instance.application_description = application_description


            form_instance.save()
            return redirect('/')  # Redirect to a success page

        else:
            form = LoanApplicationForm(instance=form_instance)
        return render(request, 'loan-page.html', {'username':admin_name,'admin':admin,'form': form, 'files': files})


def all_app(request):
    user = request.session.get('user', None)
    if user is None:
        return redirect('/login')
    else:
        loan_app = LoanApplicationModel.objects.all()
        admin = AdminModel.objects.get(admin_id=user)
        if admin.admin_last_name:
            admin_name = f"{admin.admin_first_name} {admin.admin_last_name}"
        else:
            admin_name = f"{admin.admin_first_name}"
        return render(request, 'all-files.html', {'username': admin_name, 'admin': admin, 'forms':loan_app})


def createuser(request):
    user = request.session.get('user', None)
    error = ''
    if user is None:
        return redirect('/login')

    else:
        admin = AdminModel.objects.get(admin_id=user)
        if admin.admin_last_name:
            admin_name = f"{admin.admin_first_name} {admin.admin_last_name}"
        else:
            admin_name = f"{admin.admin_first_name}"
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password')

            if AdminModel.objects.filter(admin_email=email).exists():
                error = "User with this email already exists"
            else:
                if len(password)<8:
                    error = "Password length must be 8"
                else:
                    AdminModel.objects.create(
                        admin_first_name = first_name,
                        admin_last_name =last_name,
                        admin_email = email,
                        admin_password = password
                    )
                    return redirect('/')

        return render(request, 'create-user.html', {'username':admin_name,'admin':admin,'error':error})


def addloan(request):
    user = request.session.get('user', None)
    if user is None:
        return redirect('/login')
    else:
        admin = AdminModel.objects.get(admin_id=user)
        if admin.admin_last_name:
            admin_name = f"{admin.admin_first_name} {admin.admin_last_name}"
        else:
            admin_name = f"{admin.admin_first_name}"
        all_loans = LoanModel.objects.all()
        if request.method == 'POST':
            form = LoanForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/')  # Redirect to login page after successful registration
        else:
            form = LoanForm()
        return render(request, 'add-loan.html', {'username':admin_name,'admin':admin,'form': form, 'allloans': all_loans})

def addstatus(request):
    user = request.session.get('user', None)
    if user is None:
        return redirect('/login')
    else:
        admin = AdminModel.objects.get(admin_id=user)
        if admin.admin_last_name:
            admin_name = f"{admin.admin_first_name} {admin.admin_last_name}"
        else:
            admin_name = f"{admin.admin_first_name}"

        all_status = StatusModel.objects.all()
        if request.method == 'POST':
            form = StatusForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/')  # Redirect to login page after successful registration
        else:
            form = StatusForm()
        return render(request, 'add-status.html', {'username':admin_name,'admin':admin,'form': form, 'allstatus':all_status})


def addbank(request):
    user = request.session.get('user', None)
    if user is None:
        return redirect('/login')
    else:
        admin = AdminModel.objects.get(admin_id=user)
        admin_name = f"{admin.admin_first_name} {admin.admin_last_name}"
        all_bank = BankModel.objects.all()
        if request.method == 'POST':
            form = BankForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('addbank')  # Redirect to login page after successful registration
        else:
            form = BankForm()
        return render(request, 'add-bank.html', {'username':admin_name,'admin':admin,'form': form, 'allbank': all_bank})



def delete_loan(request, loan_id):
    loan = get_object_or_404(LoanModel, pk=loan_id)
    if request.method == 'POST':
        loan.delete()
        return redirect('addloan')  # Adjust the redirect based on your URL name for the user list page
    return redirect('addloan')

def delete_status(request, status_id):
    status = get_object_or_404(StatusModel, pk=status_id)
    if request.method == 'POST':
        status.delete()
        return redirect('addstatus')  # Adjust the redirect based on your URL name for the user list page
    return redirect('addstatus')


def delete_bank(request, bank_id):
    bank = get_object_or_404(BankModel, pk=bank_id)
    if request.method == 'POST':
        bank.delete()
        return redirect('addbank')  # Adjust the redirect based on your URL name for the user list page
    return redirect('addbank')


def delete_user(request, admin_id):
    user = get_object_or_404(AdminModel, pk=admin_id)
    if request.method == 'POST':
        LoanApplicationModel.objects.filter(assigned_to=user).update(assigned_to=None)
        user.delete()
        return redirect('/')  # Adjust the redirect based on your URL name for the user list page
    return redirect('/')


def delete_loanpage(request, form_id):
    loan = get_object_or_404(LoanApplicationModel, pk=form_id)
    if request.method == 'POST':
        loan.delete()
        return redirect('/')  # Adjust the redirect based on your URL name for the user list page
    return redirect('/')


def logout(request):
    del request.session['user']
    return redirect('/')



# chart
def get_loan_data(request):
    loan_data = LoanApplicationModel.objects.annotate(month=TruncMonth('followup_date')) \
        .values('month') \
        .annotate(loan_count=Count('form_id')) \
        .order_by('month')

    # Format the data to be used in the chart
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    loan_counts = [0] * 12  # Initialize with 0s

    for data in loan_data:
        loan_counts[data['month'].month - 1] = data['loan_count']

    response_data = {
        'months': months,
        'loan_counts': loan_counts,
    }

    return JsonResponse(response_data)


def get_loan_totals(request):
    loan_data = LoanApplicationModel.objects.annotate(month=TruncMonth('followup_date')) \
        .values('month') \
        .annotate(total_loans=Count('form_id')) \
        .order_by('month')

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']
    total_loans = [0] * 12  # Initialize with 0s

    for data in loan_data:
        total_loans[data['month'].month - 1] = data['total_loans']

    response_data = {
        'months': months,
        'total_loans': total_loans,
    }

    return JsonResponse(response_data)
