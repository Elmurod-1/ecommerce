from urllib import request

def test_get_all_category(c_client):
    endpoint = '/ninja/inventory/category/all/'
    response = c_client().get(endpoint)
    assert response.status_code == 200