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
        admin_name = f"{admin.admin_first_name} {admin.admin_last_name}"
        loan_form = LoanApplicationModel.objects.filter(assigned_to = user)
        today = datetime.now().date()
        all_loans = LoanApplicationModel.objects.filter(followup_date = today)
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
            context = {
                'username': admin_name,
                'forms': loan_form,
                'loans': loan_followup,
                'total_users_count': all_users_count,
                'loan_app_count': loan_app_count,
                'admin': admin
            }

        return render(request, 'index.html', context)


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
        admin_name = f"{admin.admin_first_name} {admin.admin_last_name}"
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
        admin_name = f"{admin.admin_first_name} {admin.admin_last_name}"
        # Get the specific form entry by ID
        form_instance = get_object_or_404(LoanApplicationModel, form_id=form_id)
        files = UploadedFile.objects.filter(loan_application=form_instance)

        # Check if the form was submitted
        if request.method == 'POST':
            form = LoanApplicationForm(request.POST, instance=form_instance)
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
            # else:
            #     print(form.errors)
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
        admin_name = f"{admin.admin_first_name} {admin.admin_last_name}"
        return render(request, 'all-files.html', {'username': admin_name, 'admin': admin, 'forms':loan_app})


def createuser(request):
    user = request.session.get('user', None)
    if user is None:
        return redirect('/login')
    else:
        admin = AdminModel.objects.get(admin_id=user)
        admin_name = f"{admin.admin_first_name} {admin.admin_last_name}"
        if request.method == 'POST':
            form = AdminForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/')  # Redirect to login page after successful registration
        else:
            form = AdminForm()
        return render(request, 'create-user.html', {'username':admin_name,'admin':admin,'form': form})


def addloan(request):
    user = request.session.get('user', None)
    if user is None:
        return redirect('/login')
    else:
        admin = AdminModel.objects.get(admin_id=user)
        admin_name = f"{admin.admin_first_name} {admin.admin_last_name}"
        if request.method == 'POST':
            form = LoanForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/')  # Redirect to login page after successful registration
        else:
            form = LoanForm()
        return render(request, 'add-loan.html', {'username':admin_name,'admin':admin,'form': form})

def addstatus(request):
    user = request.session.get('user', None)
    if user is None:
        return redirect('/login')
    else:
        admin = AdminModel.objects.get(admin_id=user)
        admin_name = f"{admin.admin_first_name} {admin.admin_last_name}"
        if request.method == 'POST':
            form = StatusForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/')  # Redirect to login page after successful registration
        else:
            form = StatusForm()
        return render(request, 'add-status.html', {'username':admin_name,'admin':admin,'form': form})

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
