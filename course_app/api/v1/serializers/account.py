import hashlib

from rest_framework import serializers
from Crypto.Util import number
from Crypto.Random import random

from course_app.app.models import BankAccount, Transaction
from course_app.app.utils import fast_power

class ShortAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankAccount
        fields = ('uuid',)


def generate_primes():
    is_prime = False
    p, q, x = 0, 0, 0
    while not is_prime:
        q = number.getPrime(257)
        x = random.getrandbits(1791)

        p = q*x + 1

        is_prime = number.isPrime(p)
    return p, q, x


class FullAccountSerializer(serializers.ModelSerializer):

    users_count = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)
    public_number = serializers.CharField(read_only=True)

    class Meta:
        model = BankAccount
        fields = ('public_number', 'uuid', 'balance', 'owner', 'users_count', 'factor_1', 'factor_2', 'password', 'beta')

    def get_users_count(self, obj):
        return obj.users.count()

    def create(self, validated_data):
        factor_1, factor_2, x = generate_primes()
        f = random.randint(2, factor_1 - 1)
        beta = fast_power(f, x, factor_1)
        secret_key = int(hashlib.sha256(validated_data.pop('password').encode('utf-8')).hexdigest(), 16)
        public_number = fast_power(number.inverse(beta, factor_1), secret_key, factor_1)
        validated_data['public_number'] = hex(public_number)[2:]
        validated_data['factor_1'] = hex(factor_1)[2:]
        validated_data['factor_2'] = hex(factor_2)[2:]
        validated_data['beta'] = hex(beta)[2:]
        account = BankAccount.objects.create(**validated_data)
        return account


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'


class PaymentSerializer(serializers.Serializer):

    evaluated = serializers.CharField()
    funds = serializers.IntegerField(min_value=1)
    recipient = serializers.UUIDField()