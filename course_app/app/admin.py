from django.contrib import admin

from course_app.app.models import BankAccount, Transaction, User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    pass


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass
