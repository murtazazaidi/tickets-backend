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

class TicketSerializer(serializers.HyperlinkedModelSerializer):
    reporter = serializers.ReadOnlyField(source='reporter.username')
    assignee = serializers.ReadOnlyField(source='assignee.username')
    class Meta:
        model = Ticket
        fields = '__all__'

class CreateTicketSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ticket
        fields = ('severity', 'description', 'penalty', 'assignee')

    def create(self, validated_data):
        reporter = self.context['request'].user
        validated_data['reporter'] = reporter
        ticket = Ticket.objects.create(**validated_data)
        ticket.save()
        return ticket
