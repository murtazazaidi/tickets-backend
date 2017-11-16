from datetime import datetime

from django.contrib.auth.models import User

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from project.tickets.models import Ticket
from project.tickets.serializers import CreateUserSerializer, UserSerializer, TicketSerializer, CreateTicketSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method in ['POST', 'PUT']:
            serializer_class = CreateUserSerializer

        return serializer_class

    # def get_permissions(self):
    #     if self.request.method == 'DELETE':
    #         return [IsAdminUser()]
    #     elif self.request.method == 'POST':
    #         return [AllowAny()]
    #     else:
    #         return [IsStaffOrTargetUser()]


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

    @detail_route(methods=['POST'])
    def mark_done(self, request, pk=None):
        ticket = self.get_object()
        ticket.is_done = True
        ticket.done_date = datetime.now()
        ticket.save()
        return Response(status=status.HTTP_200_OK)
