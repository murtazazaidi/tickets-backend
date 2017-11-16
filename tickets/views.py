from django.contrib.auth.models import User
from project.tickets.models import Ticket
from rest_framework import viewsets
from project.tickets.serializers import CreateUserSerializer, UserSerializer, TicketSerializer, CreateTicketSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'POST':
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
            serializer_class = CreateTicketSerializer

        return serializer_class
