# -*- coding: utf-8 -*-
from serializers import UserSerializer

def jwt_response_payload_handler(token, user=None, request=None):
    """ JWT response for obtain and refresh """
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }
