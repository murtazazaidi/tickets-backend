# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

SEVERITIES = (
    (1, 'minor'),
    (2, 'major'),
    (3, 'critical'),
    (4, 'blocker')
)

class Ticket(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    severity = models.CharField(choices=SEVERITIES, default='minor', max_length=100)
    description = models.TextField()
    penalty = models.TextField()
    assignee = models.ForeignKey('auth.User', related_name='assigned', on_delete=models.CASCADE)
    reporter = models.ForeignKey('auth.User', related_name='reported', on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)
    done_date = models.DateTimeField()

    class Meta:
        ordering = ('created',)
