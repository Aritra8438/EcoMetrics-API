def test_home_okay(client):
    """test get method"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"<title>Homepage</title>" in response.data
    assert b"Welcome to this API." in response.data


def test_home_method_not_allowed(client):
    """test other methods which are not allowed"""
    response = client.post("/")
    assert response.status_code == 405
    assert b"<title>405 Method Not Allowed</title>" in response.data
    response = client.put("/")
    assert response.status_code == 405
    assert b"<title>405 Method Not Allowed</title>" in response.data


def test_documentation_okay(client):
    """test get method"""
    response = client.get("/api-documentation")
    assert response.status_code == 200
    assert b"<title>API documentation</title>" in response.data


def test_documentation_method_not_allowed(client):
    """test other methods which are not allowed"""
    response = client.post("/api-documentation")
    assert response.status_code == 405
    assert b"<title>405 Method Not Allowed</title>" in response.data
    response = client.put("/api-documentation")
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
    assert b'[{"country":"China","value":1424929800,"year":2020}]\n' in response.data
    response = client.get(
        "/json?Region=[%22China%22]&Year=%222020,2020,1%22&Query_type=gdp_per_capita"
    )
    assert response.status_code == 400
    assert b"<p>We have GDP per capita data upto 2018</p>\n" in response.data
    response = client.get(
        "/json?Region=[%22China%22]&Year=%222014,2016,1%22&Query_type=gdp_per_capita"
    )
    assert response.status_code == 200
    assert b'{"country":"China","value":"12244","year":2015}' in response.data
    response = client.get(
        "/json?Region=[%22China%22]&Year=%222014,2016,1%22&Query_type=gdp_per_capita&Pivot=Region"
    )
    assert response.status_code == 200
    response = client.get(
        "/json?Region=[%22China%22]&Year=%222014,2016,1%22&Query_type=gdp_per_capita&Pivot=Year"
    )
    assert response.status_code == 200
    response = client.get('/json?Region=["India"]&Year=["2000","2010","1"]')
    assert response.status_code == 200
    assert b'[{"country":"India","value":1059633660,"year":2000}' in response.data
    assert b'year":1' not in response.data
    response = client.get('/json?Region="India"&Year=2000')
    assert response.status_code == 200
    assert b'[{"country":"India","value":1059633660,"year":2000}' in response.data
    response = client.get('/json?Year=[2000]&Region="India"')
    assert response.status_code == 200
    assert b'[{"country":"India","value":1059633660,"year":2000}' in response.data
    response = client.get('/json?Year=[2000]&Region="India"&Pivot=Year')
    assert response.status_code == 200
    assert b'[{"2000":[{"India":1059633660}]}]\n' in response.data
    response = client.get('/json?Year=[2000]&Region="India"&Pivot=Region')
    assert response.status_code == 200
    assert b'[{"India":[{"2000":1059633660}]}]\n' in response.data


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
    response = client.get('/json?Region=["India"]&Year="2000,2010,1')
    assert response.status_code == 400
    assert (
        b"<p>The Year should either be a Number, array of number or a string of tuple"
        in response.data
    )
    response = client.get('/json?Region=[India]&Year="2000,2010,1"')
    assert response.status_code == 400
    assert (
        b"<p>The Region should either be a string enclosed by quotation or an array"
        in response.data
    )
    response = client.get('/json?Region=India&Year="2000,2010,1')
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
    response = client.get(
        "/table?Region=[%22Chin%22]&Year=%222020,2020,1%22&Pivot=Region"
    )
    assert response.status_code == 200
    assert b"China" in response.data
    assert b"1424929800" in response.data
    response = client.get(
        "/table?Region=[%22China%22]&Year=%222014,2016,1%22&Query_type=gdp_per_capita&Pivot=Region"
    )
    assert response.status_code == 200
    response = client.get(
        "/table?Region=[%22China%22]&Year=%222014,2016,1%22&Query_type=gdp_per_capita&Pivot=Year"
    )
    assert response.status_code == 200


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
    response = client.get('/table?Region=["India"]&Year="2000,2010,1')
    assert response.status_code == 400
    assert (
        b"<p>The Year should either be a Number, array of number or a string of tuple"
        in response.data
    )
    response = client.get('/table?Region=[India]&Year="2000,2010,1"')
    assert response.status_code == 400
    assert (
        b"<p>The Region should either be a string enclosed by quotation or an array"
        in response.data
    )
    response = client.get('/table?Region=India&Year="2000,2010,1')
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
    response = client.get(
        "/graph?Region=[%22China%22]&Year=%222014,2016,1%22&Query_type=gdp_per_capita"
    )
    assert response.status_code == 200
    response = client.get(
        "/graph?Region=[%22China%22]&Year=%222014,2016,1%22&Query_type=gdp_per_capita"
    )
    assert b"China" in response.data
    assert b"GDP per capita vs Year graph" in response.data
    assert response.status_code == 200


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
    response = client.get('/graph?Region=["India"]&Year="2000,2010,1')
    assert response.status_code == 400
    assert (
        b"<p>The Year should either be a Number, array of number or a string of tuple"
        in response.data
    )
    response = client.get('/graph?Region=[India]&Year="2000,2010,1"')
    assert response.status_code == 400
    assert (
        b"<p>The Region should either be a string enclosed by quotation or an array"
        in response.data
    )
    response = client.get('/graph?Region=India&Year="2000,2010,1')
    assert response.status_code == 400
    assert (
        b"<p>The Region should either be a string enclosed by quotation or an array"
        in response.data
    )


def test_graph_themes(client):
    """test the themes"""
    response = client.get('/graph?Region=["India"]&Year="2000,2010,1"')
    assert b"Population vs Year graph" in response.data
    assert b'"paper_bgcolor":"white"' in response.data
    response = client.get('/graph?Region=["India"]&Year="2000,2010,1"&Theme=light')
    assert b'"paper_bgcolor":"#A6BEBE"' in response.data
    response = client.get('/graph?Region=["India"]&Year="2000,2010,1"&Theme=dark')
    assert b'"paper_bgcolor":"black"' in response.data
    response = client.get('/graph?Region=["India"]&Year="2000,2010,1"&Theme=aquamarine')
    assert b'"paper_bgcolor":"#1E4967"' in response.data
    response = client.get('/graph?Region=["India"]&Year="2000,2010,1"&Theme=blackpink')
    assert b'"paper_bgcolor":"black"' in response.data
    response = client.get(
        '/graph?Region=["India"]&Year="2000,2010,1"&Theme=fluorescent'
    )
    assert b'"paper_bgcolor":"#B2FF00"' in response.data
    response = client.get(
        '/graph?Region=["China"]&Year=2014&Query_type=gdp_per_capita&Theme=blackpink'
    )
    assert b'"paper_bgcolor":"black"' in response.data


def test_graph_bar(client):
    response = client.get('/graph?Region=["India"]&Year="2000,2010,1"&Plot=bar')
    assert b"Population vs Year bar plot" in response.data
    response = client.get(
        '/graph?Region=["India"]&Year="2000,2010,1"&Plot=bar&Query_type=gdp_per_capita'
    )
    assert b"GDP per capita vs Year bar plot" in response.data


def test_stats_okay(client):
    """test get method and possible param combinations"""
    response = client.get("/stats?Number=5&Year=2000")
    assert response.status_code == 200
    assert b"India" in response.data
    assert b"Tuvalu" in response.data
    assert b"Stats pie charts" in response.data
    response = client.get("/stats?Year=2001&Query_type=gdp_per_capita&Number=5")
    assert b"Norway" in response.data
    assert b"Afghanistan" in response.data
    assert b"Stats pie charts for GDP per capita" in response.data


def test_stats_method_not_allowed(client):
    """test other methods which are not allowed"""
    response = client.post("/stats")
    assert response.status_code == 405
    assert b"<title>405 Method Not Allowed</title>" in response.data


def test_compare_okay(client):
    """test get method and possible param combinations"""
    response = client.get('/compare?Year=[2000,2001]&Region=["India","China"]')
    assert response.status_code == 200
    assert b"China" in response.data
    assert b"India" in response.data
    assert b"3d plot for country, population and GDP per capita" in response.data
    response = client.get('/compare?Year=[2000,2001]&Region=["India"]&Type=2d')
    assert response.status_code == 200
    assert b"Population" in response.data
    assert b"GDP per capita" in response.data
    assert b"Population vs GDP per capita visualization" in response.data


def test_compare_method_not_allowed(client):
    """test other methods which are not allowed"""
    response = client.post("/compare")
    assert response.status_code == 405
    assert b"<title>405 Method Not Allowed</title>" in response.data


def test_compare_missing_parameter(client):
    """test bad request missing parameters"""
    response = client.get("/compare")
    assert response.status_code == 400
    assert b"<p>Region must be specified in the url</p>" in response.data
    response = client.get("/compare?Region=[%22Germany%22,%22China%22,%22India%22]")
    assert response.status_code == 400
    assert b"<p>Year must be specified in the url</p>" in response.data
    response = client.get("/compare?region=[%22Germany%22,%22China%22,%22India%22]")
    assert response.status_code == 400
    assert b"<p>Region must be specified in the url</p>" in response.data


def test_compare_invalid_parameter(client):
    """test bad request missing parameters"""
    response = client.get('/compare?Region=["India"]&Year="2000,2010,1')
    assert response.status_code == 400
    assert (
        b"<p>The Year should either be a Number, array of number or a string of tuple"
        in response.data
    )
    response = client.get('/compare?Region=[India]&Year="2000,2010,1"')
    assert response.status_code == 400
    assert (
        b"The Region should either be a string enclosed by quotation or an array"
        in response.data
    )
    response = client.get('/compare?Region=India&Year="2000,2010,1')
    assert response.status_code == 400
    assert b"The Year should either be a Number" in response.data in response.data

def test_compare_3d_themes(client):
    """test the themes for compare plot(3d)"""
    response = client.get('/compare?Region=["India"]&Year="2000,2010,1"')
    assert b"3d plot for country, population and GDP per capita" in response.data
    assert b'"paper_bgcolor":"white"' in response.data
    response = client.get('/graph?Region=["India"]&Year="2000,2010,1"&Theme=light')
    assert b'"paper_bgcolor":"#A6BEBE"' in response.data
    response = client.get('/graph?Region=["India"]&Year="2000,2010,1"&Theme=dark')
    assert b'"paper_bgcolor":"black"' in response.data
    response = client.get('/graph?Region=["India"]&Year="2000,2010,1"&Theme=aquamarine')
    assert b'"paper_bgcolor":"#1E4967"' in response.data
    response = client.get('/graph?Region=["India"]&Year="2000,2010,1"&Theme=blackpink')
    assert b'"paper_bgcolor":"black"' in response.data
    response = client.get(
        '/graph?Region=["India"]&Year="2000,2010,1"&Theme=fluorescent'
    )
    assert b'"paper_bgcolor":"#B2FF00"' in response.data
    response = client.get(
        '/graph?Region=["China"]&Year=2014&Query_type=gdp_per_capita&Theme=blackpink'
    )
    assert b'"paper_bgcolor":"black"' in response.data

def test_compare_2d_themes(client):
    """test the themes for compare plot(2d)"""
    response = client.get('/compare?Region=["India"]&Year="2000,2010,1"&Type=2d')
    assert b"Population vs GDP per capita visualization" in response.data
    assert b'"paper_bgcolor":"white"' in response.data
    response = client.get('/graph?Region=["India"]&Year="2000,2010,1"&Theme=light')
    assert b'"paper_bgcolor":"#A6BEBE"' in response.data
    response = client.get('/graph?Region=["India"]&Year="2000,2010,1"&Theme=dark')
    assert b'"paper_bgcolor":"black"' in response.data
    response = client.get('/graph?Region=["India"]&Year="2000,2010,1"&Theme=aquamarine')
    assert b'"paper_bgcolor":"#1E4967"' in response.data
    response = client.get('/graph?Region=["India"]&Year="2000,2010,1"&Theme=blackpink')
    assert b'"paper_bgcolor":"black"' in response.data
    response = client.get(
        '/graph?Region=["India"]&Year="2000,2010,1"&Theme=fluorescent'
    )
    assert b'"paper_bgcolor":"#B2FF00"' in response.data
    response = client.get(
        '/graph?Region=["China"]&Year=2014&Query_type=gdp_per_capita&Theme=blackpink'
    )
    assert b'"paper_bgcolor":"black"' in response.data
