import os
from mock import patch

import json
import responses

from . import fixtures

CW_MEMBER_IMAGE_FILENAME = 'AnonymousMember.png'


def create_mock_call(method_name, return_value, side_effect=None):
    """Utility function for mocking the specified function or method"""
    _patch = patch(method_name, side_effect=side_effect)
    mock_get_call = _patch.start()

    if not side_effect:
        mock_get_call.return_value = return_value

    return mock_get_call, _patch


def company_api_by_id_call(return_value):
    method_name = 'djconnectwise.api.CompanyAPIClient.by_id'
    return create_mock_call(method_name, return_value)


def company_api_get_call(return_value):
    method_name = 'djconnectwise.api.CompanyAPIClient.get'
    return create_mock_call(method_name, return_value)


def _service_api_tickets_call(page=0, page_size=25):
    return_value = []
    if page == 0:
        return_value = [fixtures.API_SERVICE_TICKET]
    return return_value


def service_api_tickets_call():
    method_name = 'djconnectwise.api.ServiceAPIClient.get_tickets'
    mock_call, _patch = create_mock_call(
        method_name,
        None,
        side_effect=_service_api_tickets_call)
    return mock_call, _patch


def _service_api_get_ticket_call(ticket_id):
    return fixtures.API_SERVICE_TICKET_MAP.get(ticket_id)


def service_api_get_ticket_call():
    method_name = 'djconnectwise.api.ServiceAPIClient.get_ticket'
    mock_call, _patch = create_mock_call(
        method_name,
        None,
        side_effect=_service_api_get_ticket_call)
    return mock_call, _patch


def service_api_get_boards_call(return_value):
    method_name = 'djconnectwise.api.ServiceAPIClient.get_boards'
    return create_mock_call(method_name, return_value)


def service_api_update_ticket_call(return_value):
    method_name = 'djconnectwise.api.ServiceAPIClient.update_ticket'
    return create_mock_call(method_name, return_value)


def service_api_get_statuses_call(return_value):
    method_name = 'djconnectwise.api.ServiceAPIClient.get_statuses'
    return create_mock_call(method_name, return_value)


def service_api_get_priorities_call(return_value):
    method_name = 'djconnectwise.api.ServiceAPIClient.get_priorities'
    return create_mock_call(method_name, return_value)


def service_api_get_teams_call(return_value):
    method_name = 'djconnectwise.api.ServiceAPIClient.get_teams'
    return create_mock_call(method_name, return_value)


def system_api_get_connectwise_version_call(return_value):
    method_name = 'djconnectwise.api.SystemAPIClient.get_connectwise_version'
    return create_mock_call(method_name, return_value)


def system_api_get_members_call(return_value):
    method_name = 'djconnectwise.api.SystemAPIClient.get_members'
    return create_mock_call(method_name, return_value)


def system_api_get_member_image_by_identifier_call(return_value):
    method_name = 'djconnectwise.api.SystemAPIClient.' \
                  + 'get_member_image_by_identifier'

    return create_mock_call(method_name, return_value)


def system_api_get_member_count_call(return_value):
    method_name = 'djconnectwise.api.SystemAPIClient.get_members'
    return create_mock_call(method_name, return_value)


def cw_api_fetch_resource_call(return_value):
    method_name = 'djconnectwise.api.ConnectWiseAPIClient.fetch_resource'
    return create_mock_call(method_name, return_value)


def get(url, data, headers=None):
    """Set up requests mock for given URL and JSON-serializable data."""
    get_raw(url, json.dumps(data), "application/json", headers)


def get_raw(url, data, content_type="application/octet-stream", headers=None):
    """Set up requests mock for given URL."""
    responses.add(
        responses.GET,
        url,
        body=data,
        content_type=content_type,
        adding_headers=headers,
    )


def get_member_avatar():
    """Return the avatar image data in the tests directory."""
    cw_member_image_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        CW_MEMBER_IMAGE_FILENAME
    )
    with open(cw_member_image_path, 'rb') as anonymous_image_file:
        return anonymous_image_file.read()
