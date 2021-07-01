import random

import pytest
import requests

from conftest import JSON_PH_URL


def test_json_ph_status_code():
    assert requests.get(JSON_PH_URL).status_code == 200


@pytest.mark.parametrize("post_number", ("1", f"{random.randint(2, 99)}", "100"))
def test_post_theme(post_number):
    r = requests.get(JSON_PH_URL + 'posts/' + post_number)
    assert r.status_code == 200 and r.json()["title"], f"Пост с id={r.json()['id']}недоступен или не имеет темы"


@pytest.mark.parametrize("user_number", [i for i in range(1, 11)])
@pytest.mark.parametrize("user_info", ("name",
                                       "username",
                                       "email",
                                       "address",
                                       "phone",
                                       "website",
                                       "company",))
def test_user_info(user_number, user_info):
    r = requests.get(JSON_PH_URL + 'users/' + str(user_number))
    assert r.json()[user_info], f"Для пользователя с id={user_number} не заполнены сведения в поле {user_info}"


@pytest.mark.parametrize("service, result", (
        ["posts", 100],
        ["comments", 500],
        ["albums", 100],
        ["photos", 5000],
        ["todos", 200],
        ["users", 10],
))
def test_count_results(service, result):
    r = requests.get(JSON_PH_URL + service)
    assert r.status_code == 200 and len(r.json()) == result, f"Некорректное количество записей в спике '{service}'"


@pytest.mark.parametrize("post_number", [i for i in range(1, 101)])
def test_post_comments(post_number):
    r = requests.get(JSON_PH_URL + f'posts/{post_number}/comments')
    assert r.status_code == 200 and len(r.json()) > 0, f"Пост с id='{post_number}' недоступен или не имеет комментария"


def test_post_req_status_code():
    r = requests.post(url=JSON_PH_URL + f'posts',
                      headers={'Content-type': 'application/json; charset=UTF-8'},
                      json={"title": "title", "body": "text", "userId": 1})
    assert r.status_code == 201
