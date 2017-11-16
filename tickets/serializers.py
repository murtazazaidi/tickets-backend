from django.contrib.auth.models import User
from project.tickets.models import Ticket
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    assigned = serializers.PrimaryKeyRelatedField(many=True, queryset=Ticket.objects.all())
    reported = serializers.PrimaryKeyRelatedField(many=True, queryset=Ticket.objects.all())
    class Meta:
        model = User
        fields = ('url', 'id', 'first_name', 'last_name', 'email', 'username', 'assigned', 'reported')

class CreateUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'first_name', 'last_name', 'email', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(user.password)
        user.save()
        return user


class TicketSerializer(serializers.ModelSerializer):
    assignee = serializers.ReadOnlyField(source='assignee.username')
    reporter = serializers.ReadOnlyField(source='reporter.username')
    class Meta:
        model = Ticket
        fields = '__all__'
