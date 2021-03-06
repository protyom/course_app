import uuid
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from rest_framework.exceptions import PermissionDenied


class BankAccount(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    public_number = models.CharField(max_length=257)

    factor_1 = models.CharField(max_length=257, blank=True, null=True)
    factor_2 = models.CharField(max_length=129, blank=True, null=True)
    beta = models.CharField(max_length=257, blank=True, null=True)

    users = models.ManyToManyField(
        get_user_model(),
        related_name='used_accounts'
    )
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='owned_accounts'
    )

    balance = models.PositiveIntegerField(default=0)

    def pay(self, user, to_account, funds, **kwargs):
        if self.balance < funds:
            raise PermissionDenied({'details': 'Insufficient funds'})
        self.balance -= funds
        to_account.balance += funds
        Transaction.objects.create(
            from_account=self,
            to_account=to_account,
            funds=funds,
            **kwargs
        )
        self.users.add(user)
        self.save()
        to_account.save()


class Transaction(models.Model):
    from_account = models.ForeignKey(
        BankAccount,
        on_delete=models.CASCADE,
        related_name='outcome_transactions'
    )
    to_account = models.ForeignKey(
        BankAccount,
        on_delete=models.CASCADE,
        related_name='income_transactions'
    )

    funds = models.PositiveIntegerField(validators=(MinValueValidator(1),))
    pay_code = models.CharField(max_length=257, blank=True, null=True)
    challenge = models.CharField(max_length=129, blank=True, null=True)
    evaluated = models.CharField(max_length=129, blank=True, null=True)
