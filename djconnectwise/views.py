# -*- coding: utf-8 -*-
import json
import logging

from braces import views

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django import forms
from django.views.generic import View

from . import models
from .models import CallBackEntry
from djconnectwise import sync

logger = logging.getLogger(__name__)


CALLBACK_DELETED = 'deleted'
CALLBACK_UPDATED = 'updated'

CALLBACK_ACTIONS = (
    (CALLBACK_DELETED, CALLBACK_DELETED),
    (CALLBACK_UPDATED, CALLBACK_UPDATED)
)


class CallBackView(views.CsrfExemptMixin,
                   views.JsonRequestResponseMixin, View):

    CALLBACK_TYPES = {
        CallBackEntry.TICKET: (sync.TicketSynchronizer, models.Ticket),
        CallBackEntry.PROJECT: (sync.ProjectSynchronizer, models.Project),
        CallBackEntry.COMPANY: (sync.CompanySynchronizer, models.Company),
    }

    def validate(self, request_body):
        params = ['Action', 'Type', 'Entity']

        errors = {}
        for param in params:
            msg = 'The {} parameter is required.'.format(param)
            if param not in request_body:
                errors['param'] = msg

        return errors

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body.decode(encoding='utf-8'))
        required_fields = {
            'action': body['Action'],
            'entity': body['Entity'],
            'callback_type': body['Type']
        }
        form = CallBackForm(required_fields)

        if not form.is_valid():
            fields = ', '.join(form.errors.keys())
            msg = 'Received callback with missing parameters: {}.'.format(
                fields)
            logger.warning(msg)
            return HttpResponseBadRequest(json.dumps(form.errors))

        self.action = form.cleaned_data['action']
        self.callback_type = body.get('Type')
        sync_class, self.model_class = \
            self.CALLBACK_TYPES[self.callback_type]
        self.synchronizer = sync_class()
        entity = json.loads(body.get('Entity'))

        logger.debug('{} {}: {}'.format(self.action.upper(), entity, body))

        if self.action == CALLBACK_DELETED:
            self.delete(entity)
        else:
            self.update(entity)

        # we need not return anything to connectwise
        return HttpResponse(status=204)

    def update(self, entity):
        self.model_class.objects.filter(id=entity['id'])
        logger.info('Update CallBack: {}'.format(entity))

        if self.callback_type == 'ticket':
            self.synchronizer.sync_ticket(entity)
        else:
            self.synchronizer.update_or_create_instance(entity)

    def delete(self, object_id):
        self.model_class.objects.filter(id=object_id).delete()
        logger.info('{} Deleted CallBack: {}'.format(object_id))


class CallBackForm(forms.Form):
    entity = forms.CharField()
    action = forms.ChoiceField(choices=CALLBACK_ACTIONS)

    callback_type = forms.ChoiceField(
        choices=[(c, c) for c in CallBackView.CALLBACK_TYPES.keys()]
    )
