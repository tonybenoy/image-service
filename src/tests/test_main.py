from src.tests.utils import client


def test_read_main():
    response = client.get("/test")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["result"] == "success"
    assert response_json["msg"] == "It works!"


def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert b"Upload an image" in response.content


def test_upload_image():
    response = client.post(
        "/upload",
        files={"image": open("src/tests/a.txt", "rb")},
    )
    assert response.status_code == 200
    assert b"Invalid file type" in response.content
