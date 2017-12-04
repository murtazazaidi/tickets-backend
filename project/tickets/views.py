# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib.auth.models import User

from rest_framework import viewsets, status, permissions, serializers
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from project.tickets.models import Ticket
from project.tickets.permissions import IsReporter, IsReporterOrAssignee, IsSameUser
from project.tickets.serializers import CreateUserSerializer, UserSerializer, TicketSerializer, CreateTicketSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method not in permissions.SAFE_METHODS:
            serializer_class = CreateUserSerializer

        return serializer_class

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.AllowAny()]

        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]

        return [IsSameUser()]


class TicketViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tickets to be viewed or edited.
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'POST':
            return CreateTicketSerializer

        return serializer_class

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]

        if self.request.method in permissions.SAFE_METHODS:
            return [IsReporterOrAssignee()]

        return [IsReporter()]

    @detail_route(methods=['PUT'])
    def mark_done(self, request, pk=None):
        ticket = self.get_object()
        if ticket.is_done:
            raise serializers.ValidationError('Ticket is already marked done.')

        ticket.is_done = True
        ticket.done_date = datetime.now()
        ticket.save()
        return Response(status=status.HTTP_200_OK)

    @detail_route(methods=['PUT'])
    def mark_undone(self, request, pk=None):
        ticket = self.get_object()
        if not ticket.is_done:
            raise serializers.ValidationError('Ticket is not marked done.')

        ticket.is_done = False
        ticket.save()
        return Response(status=status.HTTP_200_OK)
