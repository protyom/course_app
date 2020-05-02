from rest_framework import serializers

from course_app.app.models import BankAccount, Transaction


class ShortAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankAccount
        fields = ('uuid',)


class FullAccountSerializer(serializers.ModelSerializer):

    users_count = serializers.SerializerMethodField()

    class Meta:
        model = BankAccount
        fields = ('public_number', 'uuid', 'balance', 'owner', 'users_count')

    def get_users_count(self, obj):
        return obj.users.count()


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'


class PaymentSerializer(serializers.Serializer):

    evaluated = serializers.CharField()
    funds = serializers.IntegerField(min_value=1)
    recipient = serializers.UUIDField()