from http import HTTPStatus

import pytest
from httpx import AsyncClient


API_PREFIX = '/api/v1'


async def _register_and_login(
    client: AsyncClient,
    student_payload: dict,
) -> tuple[str, dict]:
    register_response = await client.post(
        f'{API_PREFIX}/auth/register',
        json=student_payload,
    )
    assert register_response.status_code == HTTPStatus.CREATED

    login_response = await client.post(
        f'{API_PREFIX}/auth/login',
        json={
            'email': student_payload['email'],
            'password': student_payload['password'],
        },
    )
    assert login_response.status_code == HTTPStatus.OK

    token_data = login_response.json()
    assert token_data['token_type'] == 'bearer'
    assert token_data['access_token']

    me_response = await client.get(
        f'{API_PREFIX}/auth/me',
        headers={'Authorization': f'Bearer {token_data["access_token"]}'},
    )
    assert me_response.status_code == HTTPStatus.OK

    return token_data['access_token'], me_response.json()


@pytest.mark.asyncio
async def test_registration_login_and_current_user_flow(client, load_fixture):
    student_payload = load_fixture('students.json')['registered_student']

    _, current_user = await _register_and_login(client, student_payload)

    assert current_user['email'] == student_payload['email']
    assert current_user['first_name'] == student_payload['first_name']
    assert current_user['last_name'] == student_payload['last_name']
    assert current_user['role'] == 'user'


@pytest.mark.asyncio
async def test_authenticated_student_can_create_and_read_project(client, load_fixture):
    student_payload = load_fixture('students.json')['registered_student']
    project_payload = load_fixture('projects.json')['critical_project']
    access_token, current_user = await _register_and_login(client, student_payload)
    headers = {'Authorization': f'Bearer {access_token}'}

    create_response = await client.post(
        f'{API_PREFIX}/projects/',
        headers=headers,
        json={
            **project_payload,
            'owner_student_id': current_user['id'],
        },
    )
    assert create_response.status_code == HTTPStatus.CREATED, create_response.text

    created_project = create_response.json()
    assert created_project['name'] == project_payload['name']
    assert created_project['owner_student_id'] == current_user['id']

    list_response = await client.get(f'{API_PREFIX}/projects/', headers=headers)
    assert list_response.status_code == HTTPStatus.OK
    assert list_response.json()['info']['total'] == 1

    detail_response = await client.get(
        f'{API_PREFIX}/projects/{created_project["id"]}',
        headers=headers,
    )
    assert detail_response.status_code == HTTPStatus.OK
    assert detail_response.json()['id'] == created_project['id']
