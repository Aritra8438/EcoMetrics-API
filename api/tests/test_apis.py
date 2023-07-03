def test_home(client):
    # test get method
    response = client.get("/")
    assert response.status_code == 200
    assert b"<title>Document</title>" in response.data
    # test other methods which are not allowed
    response = client.post("/")
    assert response.status_code == 405
    assert b'<title>405 Method Not Allowed</title>' in response.data
    response = client.put("/")
    assert response.status_code == 405
    assert b'<title>405 Method Not Allowed</title>' in response.data


def test_querybuilder(client):
    response = client.get("/querybuilder")
    assert response.status_code == 200
    assert b"<title>Query Builder</title>" in response.data
    response = client.post("/querybuilder")
    assert response.status_code == 405
    assert b'<title>405 Method Not Allowed</title>' in response.data
    response = client.put("/querybuilder")
    assert response.status_code == 405
    assert b'<title>405 Method Not Allowed</title>' in response.data


def test_json(client):
    response = client.get("/json?Region=[%22China%22]&Year=%222020,2020,1%22")
    assert response.status_code == 200
    assert (
        b'[{"country":"China","population":1424929800,"year":2020}]\n' in response.data
    )


def test_table(client):
    response = client.get("/table?Region=[%22China%22]&Year=%222020,2020,1%22")
    assert response.status_code == 200
    assert b"<title>Table</title>" in response.data
