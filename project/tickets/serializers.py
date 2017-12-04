# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from project.tickets.models import Ticket
from rest_framework import serializers, status
from rest_framework_jwt.settings import api_settings


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """ User Serializer Class """
    assigned = serializers.PrimaryKeyRelatedField(many=True, queryset=Ticket.objects.all())
    reported = serializers.PrimaryKeyRelatedField(many=True, queryset=Ticket.objects.all())
    class Meta:
        """ Meta Class """
        model = User
        fields = ('url', 'id', 'first_name', 'last_name', 'email', 'username', 'assigned', 'reported')


class CreateUserSerializer(serializers.HyperlinkedModelSerializer):
    """ CreateUser Serializer Class """
    token = serializers.SerializerMethodField()

    class Meta:
        """ Meta Class """
        model = User
        fields = ('url', 'id', 'first_name', 'last_name', 'email', 'username', 'token', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_token(self, user):
        """ Serializer Method for token """
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def update(self, instance, validated_data):
        """ Update Method for User """
        # Fields allowed to be updated
        whitelisted_keys = ['first_name', 'last_name', 'email', 'username']
        for key in whitelisted_keys:
            instance[key] = validated_data.get(key, instance[key])

        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class TicketSerializer(serializers.HyperlinkedModelSerializer):
    """ Ticket Serializer Class """
    reporter = serializers.ReadOnlyField(source='reporter.username')
    assignee = serializers.ReadOnlyField(source='assignee.username')
    class Meta:
        """ Meta Class """
        model = Ticket
        fields = '__all__'


class CreateTicketSerializer(serializers.HyperlinkedModelSerializer):
    """ CreateTicket Serializer Class """
    class Meta:
        """ Meta Class """
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
