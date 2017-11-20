from django.contrib.auth.models import User
from project.tickets.models import Ticket
from rest_framework import serializers, status


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

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


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

    def validate(self, data):
        """
        Check that assignee is not reporter
        """
        reporter = self.context['request'].user
        if reporter == data.get('assignee', None):
            raise serializers.ValidationError("Reporter cannot be the assignee")

        data['reporter'] = reporter
        return data

    def create(self, validated_data):
        ticket = Ticket.objects.create(**validated_data)
        ticket.save()
        return ticket
