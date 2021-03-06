from django.conf import settings
from django.db.models import Q
from django.core.cache import cache

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from Crypto.Random import random

from course_app.api.v1.serializers import ShortAccountSerializer, \
    TransactionSerializer, PaymentSerializer, FullAccountSerializer
from course_app.app.models import BankAccount, Transaction
from course_app.app.utils import fast_power


class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = ShortAccountSerializer

    @action(methods=['get'], detail=False)
    def parameters(self, request):
        response = {
            'factor1': settings.FACTOR_1,
            'factor2': settings.FACTOR_2,
            'beta': settings.BETA,
        }
        return Response(response, status=status.HTTP_200_OK)


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class DetailAccountViewSet(viewsets.ModelViewSet):

    serializer_class = FullAccountSerializer
    queryset = BankAccount.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return BankAccount.objects.filter(
            Q(owner_id=user.pk) | Q(users__in=[user.pk])
        )

    def create(self, request, *args, **kwargs):
        request.data['owner'] = request.user.id
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    def transactions(self, request, pk=None):
        account = self.get_object()
        transactions = Transaction.objects.filter(
            Q(from_account=account) | Q(to_account=account)
        )
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        account = self.get_object()
        if not cache.get(f'{account.uuid}_pay_code') or not cache.get(f'{account.uuid}_evaluation_parameter'):
            return Response({'details': 'You must start process first'}, status=status.HTTP_400_BAD_REQUEST)

        evaluation_parameter = int(cache.get(f'{account.uuid}_evaluation_parameter'), 16)
        pay_code = int(cache.get(f'{account.uuid}_pay_code'), 16)

        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            to_account = BankAccount.objects.get(uuid=serializer.validated_data['recipient'])
        except BankAccount.DoesNotExist as exc:
            return Response({'details': 'Recipient account does not exist'},
                            status=status.HTTP_400_BAD_REQUEST)

        beta = int(account.beta, 16)
        evaluated = int(serializer.validated_data['evaluated'], 16)
        factor1 = int(account.factor_1, 16)
        public_key = int(account.public_number, 16)
        print(factor1, beta, public_key)
        result = (fast_power(beta, evaluated, factor1)
                  * fast_power(public_key, evaluation_parameter, factor1)) % factor1
        print(result)
        if result != pay_code:
            return Response({'details': 'Payment was not verified'},
                            status=status.HTTP_403_FORBIDDEN)
        account.pay(
            request.user,
            to_account,
            serializer.validated_data['funds'],
            challenge=hex(evaluation_parameter)[2:],
            pay_code=hex(pay_code)[2:],
            evaluated=serializer.validated_data['evaluated']
        )
        cache.delete(f'{account.uuid}_pay_code')
        cache.delete(f'{account.uuid}_evaluation_parameter')
        return Response({'details': 'Ok'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def start_pay(self, request, pk=None):
        account = self.get_object()
        try:
            pay_parameter = self.request.data['pay_code']
        except KeyError as exc:
            return Response(
                {'details': 'pay_code is mandatory'},
                status=status.HTTP_400_BAD_REQUEST
            )
        cache.set(f'{account.uuid}_pay_code', pay_parameter)
        evaluation_parameter = hex(random.getrandbits(settings.SECURITY_PARAMETER))[2:]
        cache.set(f'{account.uuid}_evaluation_parameter', evaluation_parameter)
        return Response({'evaluation_parameter': evaluation_parameter}, status=status.HTTP_200_OK)