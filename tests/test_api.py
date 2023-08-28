import os
import json
import requests
from jsonschema.validators import validate


def test_list_users_schema():
    path_to_schema = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            'resources/list_users_schema.json'
        )
    )
    with open(path_to_schema) as file:
        schema = json.loads(file.read())

    response = requests.get('https://reqres.in/api/users')
    validate(response.json(), schema)


def test_single_user_schema():
    path_to_schema = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            'resources/single_user_schema.json'
        )
    )
    with open(path_to_schema) as file:
        schema = json.loads(file.read())

    response = requests.get('https://reqres.in/api/users/1')
    validate(response.json(), schema)


def test_list_users_status_code():
    response = requests.get(
        url='https://reqres.in/api/users')

    assert response.status_code == 200


def test_count_of_elements_on_page():
    page = 1
    per_page = 2

    response = requests.get(url='https://reqres.in/api/users',
                            params={'page': page, 'per_page': per_page})

    assert response.json()['per_page'] == per_page
    assert len(response.json()['data']) == per_page


def test_first_user_have_id_1():
    page = 1

    response = requests.get(url='https://reqres.in/api/users',
                            params={'page': page})

    assert response.json()['data'][0]['id'] == 1


def test_last_user_have_id_12():
    page = 2

    response = requests.get(url='https://reqres.in/api/users',
                            params={'page': page})

    assert response.json()['data'][5]['id'] == 12


def test_page_2_per_page_3():
    page = 2
    per_page = 3

    response = requests.get(url='https://reqres.in/api/users',
                            params={'page': page, 'per_page': per_page})
    data = response.json()

    assert data['page'] == 2
    assert len(data['data']) == 3
    assert data['per_page'] == 3


def test_creating_user():
    name = 'morpheus'
    job = 'leader'
    response = requests.post(url='https://reqres.in/api/users/1',
                             data={'name': name, 'job': job})

    data = response.json()

    assert data['name'] == 'morpheus'
    assert data['job'] == 'leader'


def test_updating_user():
    name = 'morpheus'
    job = 'zion resident'

    response = requests.put(url='https://reqres.in/api/users/2',
                            data={'name': name, 'job': job})

    data = response.json()

    assert data['name'] == 'morpheus'
    assert data['job'] == 'zion resident'


def test_deleting_user():
    response = requests.delete(url='https://reqres.in/api/users/2')

    assert response.status_code == 204
