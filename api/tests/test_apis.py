def test_home_okay(client):
    """test get method"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"<title>Document</title>" in response.data


def test_home_method_not_allowed(client):
    """test other methods which are not allowed"""
    response = client.post("/")
    assert response.status_code == 405
    assert b"<title>405 Method Not Allowed</title>" in response.data
    response = client.put("/")
    assert response.status_code == 405
    assert b"<title>405 Method Not Allowed</title>" in response.data


def test_querybuilder_okay(client):
    """test get method"""
    response = client.get("/querybuilder")
    assert response.status_code == 200
    assert b"<title>Query Builder</title>" in response.data


def test_querybuilder_method_not_allowed(client):
    """test other methods which are not allowed"""
    response = client.post("/querybuilder")
    assert response.status_code == 405
    assert b"<title>405 Method Not Allowed</title>" in response.data
    response = client.put("/querybuilder")
    assert response.status_code == 405
    assert b"<title>405 Method Not Allowed</title>" in response.data


def test_json_okay(client):
    """test get method and possible param combinations"""
    response = client.get("/json?Region=[%22China%22]&Year=%222020,2020,1%22")
    assert response.status_code == 200
    assert (
        b'[{"country":"China","population":1424929800,"year":2020}]\n' in response.data
    )
    response = client.get('json?Region=["India"]&Year=["2000","2010","1"]')
    assert response.status_code == 200
    assert b'[{"country":"India","population":1059633660,"year":2000}' in response.data
    assert b'year":1' not in response.data
    response = client.get('json?Region="India"&Year=2000')
    assert response.status_code == 200
    assert b'[{"country":"India","population":1059633660,"year":2000}' in response.data
    response = client.get('json?Year=[2000]&Region="India"')
    assert response.status_code == 200
    assert b'[{"country":"India","population":1059633660,"year":2000}' in response.data


def test_json_method_not_allowed(client):
    """test other methods which are not allowed"""
    response = client.post("/json?Region=[%22China%22]&Year=%222020,2020,1%22")
    assert response.status_code == 405
    assert b"<title>405 Method Not Allowed</title>" in response.data


def test_json_missing_parameter(client):
    """test bad request missing parameters"""
    response = client.get("/json")
    assert response.status_code == 400
    assert b"<p>Region must be specified in the url</p>" in response.data
    response = client.get("/json?Region=[%22Germany%22,%22China%22,%22India%22]")
    assert response.status_code == 400
    assert b"<p>Year must be specified in the url</p>" in response.data
    response = client.get("/json?region=[%22Germany%22,%22China%22,%22India%22]")
    assert response.status_code == 400
    assert b"<p>Region must be specified in the url</p>" in response.data


def test_json_invalid_parameter(client):
    """test bad request missing parameters"""
    response = client.get('json?Region=["India"]&Year="2000,2010,1')
    assert response.status_code == 400
    assert (
        b"<p>The Year should either be a Number, array of number or a string of tuple"
        in response.data
    )
    response = client.get('json?Region=[India]&Year="2000,2010,1"')
    assert response.status_code == 400
    assert (
        b"<p>The Region should either be a string enclosed by quotation or an array"
        in response.data
    )
    response = client.get('json?Region=India&Year="2000,2010,1')
    assert response.status_code == 400
    assert (
        b"<p>The Region should either be a string enclosed by quotation or an array"
        in response.data
    )


def test_table_okay(client):
    """test get method and possible param combinations"""
    response = client.get("/table?Region=[%22Chin%22]&Year=%222020,2020,1%22")
    assert response.status_code == 200
    assert b"China" in response.data
    assert b"1424929800" in response.data


def test_table_method_not_allowed(client):
    """test other methods which are not allowed"""
    response = client.post("/table?Region=[%22China%22]&Year=%222020,2020,1%22")
    assert response.status_code == 405
    assert b"<title>405 Method Not Allowed</title>" in response.data


def test_table_missing_parameter(client):
    """test bad request missing parameters"""
    response = client.get("/table")
    assert response.status_code == 400
    assert b"<p>Region must be specified in the url</p>" in response.data
    response = client.get("/table?Region=[%22Germany%22,%22China%22,%22India%22]")
    assert response.status_code == 400
    assert b"<p>Year must be specified in the url</p>" in response.data
    response = client.get("/table?region=[%22Germany%22,%22China%22,%22India%22]")
    assert response.status_code == 400
    assert b"<p>Region must be specified in the url</p>" in response.data


def test_table_invalid_parameter(client):
    """test bad request missing parameters"""
    response = client.get('table?Region=["India"]&Year="2000,2010,1')
    assert response.status_code == 400
    assert (
        b"<p>The Year should either be a Number, array of number or a string of tuple"
        in response.data
    )
    response = client.get('table?Region=[India]&Year="2000,2010,1"')
    assert response.status_code == 400
    assert (
        b"<p>The Region should either be a string enclosed by quotation or an array"
        in response.data
    )
    response = client.get('table?Region=India&Year="2000,2010,1')
    assert response.status_code == 400
    assert (
        b"<p>The Region should either be a string enclosed by quotation or an array"
        in response.data
    )


def test_graph_okay(client):
    """test get method and possible param combinations"""
    response = client.get("/graph?Region=[%22Chin%22]&Year=%222020,2020,1%22")
    assert response.status_code == 200
    assert b"China" in response.data
    assert b"1424929800" in response.data


def test_graph_method_not_allowed(client):
    """test other methods which are not allowed"""
    response = client.post("/graph?Region=[%22China%22]&Year=%222020,2020,1%22")
    assert response.status_code == 405
    assert b"<title>405 Method Not Allowed</title>" in response.data


def test_graph_missing_parameter(client):
    """test bad request missing parameters"""
    response = client.get("/graph")
    assert response.status_code == 400
    assert b"<p>Region must be specified in the url</p>" in response.data
    response = client.get("/graph?Region=[%22Germany%22,%22China%22,%22India%22]")
    assert response.status_code == 400
    assert b"<p>Year must be specified in the url</p>" in response.data
    response = client.get("/graph?region=[%22Germany%22,%22China%22,%22India%22]")
    assert response.status_code == 400
    assert b"<p>Region must be specified in the url</p>" in response.data


def test_graph_invalid_parameter(client):
    """test bad request missing parameters"""
    response = client.get('graph?Region=["India"]&Year="2000,2010,1')
    assert response.status_code == 400
    assert (
        b"<p>The Year should either be a Number, array of number or a string of tuple"
        in response.data
    )
    response = client.get('graph?Region=[India]&Year="2000,2010,1"')
    assert response.status_code == 400
    assert (
        b"<p>The Region should either be a string enclosed by quotation or an array"
        in response.data
    )
    response = client.get('graph?Region=India&Year="2000,2010,1')
    assert response.status_code == 400
    assert (
        b"<p>The Region should either be a string enclosed by quotation or an array"
        in response.data
    )


def test_graph_themes(client):
    """test the themes"""
    response = client.get('graph?Region=["India"]&Year="2000,2010,1"')
    assert b"Population vs Year graph" in response.data
    assert b'"paper_bgcolor":"white"' in response.data
    response = client.get('graph?Region=["India"]&Year="2000,2010,1"&Theme=light')
    assert b'"paper_bgcolor":"#A6BEBE"' in response.data
    response = client.get('graph?Region=["India"]&Year="2000,2010,1"&Theme=dark')
    assert b'"paper_bgcolor":"black"' in response.data
    response = client.get('graph?Region=["India"]&Year="2000,2010,1"&Theme=aquamarine')
    assert b'"paper_bgcolor":"#1E4967"' in response.data
    response = client.get('graph?Region=["India"]&Year="2000,2010,1"&Theme=blackpink')
    assert b'"paper_bgcolor":"black"' in response.data
    response = client.get('graph?Region=["India"]&Year="2000,2010,1"&Theme=fluorescent')
    assert b'"paper_bgcolor":"#B2FF00"' in response.data
