import pytest
import requests

from conftest import DOG_URL


def test_dog_status_code():
    assert requests.get(DOG_URL).status_code == 200


@pytest.mark.parametrize("id", (0, -1, 'q'))
def test_negative(id):
    assert requests.get(f"{DOG_URL}breed/{id}/images/random").status_code == 404


def test_get_list_all_breeds():
    r = requests.get(f"{DOG_URL}breeds/list/all").json()
    assert r["status"] == "success" and len(r["message"]) >= 1, f"Список пород пуст или недоступен"
    return (r["message"])


@pytest.mark.parametrize("breed", [breed for breed in test_get_list_all_breeds()])
def test_check_all_breeds_photos(breed):
    r = requests.get(f"{DOG_URL}breed/{breed}/images")
    assert r.json()["status"] == "success" and len(r.json()["message"]) >= 1, f"Отсутствует фото для породы {breed}"


@pytest.mark.parametrize("breed", [breed for breed in test_get_list_all_breeds()])
def test_get_image_file_by_breed(breed):
    r = requests.get(f"{DOG_URL}breed/{breed}/images/random").json()
    assert r["status"] == "success", "Поиск фото по породе недоступен"
    r = r["message"].split("/")
    image_breed = r[4].split("-")[0]
    image_format = r[-1].split(".")[1]
    assert image_breed == breed, f"Некорректная порода на фото для породы {breed}"
    assert image_format in ("jpg", "jpeg", "png"), f"Некорректный формат фото для породы {breed}"
