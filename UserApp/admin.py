from django.contrib import admin
from UserApp.models import *

# Register your models here.
admin.site.register(UserModel)
admin.site.register(LoanModel)
admin.site.register(StatusModel)
admin.site.register(BankModel)
admin.site.register(AdminModel)
admin.site.register(LoanApplicationModel)