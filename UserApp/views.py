from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncYear
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
        loan_form = LoanApplicationModel.objects.filter(admin = user)
        today = datetime.now().date()
        loans = LoanApplicationModel.objects.filter(followup_date = today)
        loan_users = UserModel.objects.all().count()
        loan_app = LoanApplicationModel.objects.all().count()
        # Fetch loan data grouped by month for the area chart
        loans_per_month = LoanApplicationModel.objects.annotate(month=TruncMonth('followup_date')).values(
            'month').annotate(count=Count('form_id')).order_by('month')

        # Fetch loan data grouped by year for the bar chart
        loans_per_year = LoanApplicationModel.objects.annotate(year=TruncYear('followup_date')).values('year').annotate(
            count=Count('form_id')).order_by('year')

        # Preparing data for Chart.js
        months = [loan['month'].strftime('%b') for loan in loans_per_month]
        monthly_counts = [loan['count'] for loan in loans_per_month]

        years = [loan['year'].year for loan in loans_per_year]
        yearly_counts = [loan['count'] for loan in loans_per_year]

        context = {
            'username': admin_name,
            'forms': loan_form,
            'loans': loans,
            'months': months,
            'monthly_counts': monthly_counts,
            'years': years,
            'yearly_counts': yearly_counts,
            'total_users': loan_users,
            'loan_app': loan_app,
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
    return render(request, 'register.html', {'form': form})


def loanform(request):
    user = request.session.get('user', None)
    if user is None:
        return redirect('/login')
    else:
        loan = LoanModel.objects.all()
        status = StatusModel.objects.all()
        bank = BankModel.objects.all()
        if request.method == 'POST':
            form = LoanApplicationForm(request.POST)
            if form.is_valid():
                loan_application = form.save(commit=False)
                loan_application.admin = AdminModel.objects.get(admin_id = user)  # Set the admin field from the logged-in user
                loan_application.save()
                return redirect('/')
        else:
            form = LoanApplicationForm()
        return render(request, 'loan-form.html',{'loan':loan, 'status': status, 'bank': bank, 'form': form})



def loan_page(request, form_id):
    user = request.session.get('user', None)
    if user is None:
        return redirect('/login')
    else:
        # Get the specific form entry by ID
        form_instance = get_object_or_404(LoanApplicationModel, form_id=form_id)

        # Check if the form was submitted
        if request.method == 'POST':
            form = LoanApplicationForm(request.POST, instance=form_instance)
            if form.is_valid():
                form.save()  # Save the edited data
                return redirect('/')  # Redirect to a success page
            else:
                print('Form errors:', form.errors)
        else:
            form = LoanApplicationForm(instance=form_instance)

        return render(request, 'loan-page.html', {'form': form})


def logout(request):
    del request.session['user']
    return redirect('/')
