def test_home_page_is_reached(client):
    response = client.get_with_login('home_page.home')

    assert 200 == response.status_code
    assert b'<!--home this comment is to check that it is reached on test-->' in response.data


def test_error_page_is_reached(client):
    response = client.get_with_login('home_page.error_page')

    assert 200 == response.status_code
    assert b'<!--error_page this comment is to check that it is reached on test-->' in response.data


def test_successful_page_is_reached(client):
    response = client.get_with_login('home_page.successful',
                                     query_string=dict(go_back_to='new_record', blueprint='accounting'))

    assert 200 == response.status_code
    assert b'<!--successful this comment is to check that it is reached on test-->' in response.data


def test_error_page_shows_message_provided(client):
    message = 'This is a message to test the app'
    response = client.get_with_login('home_page.error_page',
                                     query_string=dict(message=message))

    assert 200 == response.status_code
    assert b'<!--error_page this comment is to check that it is reached on test-->' in response.data
    assert bytearray(message, "UTF-8") in response.data


def test_successful_builds_url_to_route_provided(client):
    response = client.get_with_login('home_page.successful',
                                     query_string=dict(go_back_to='new_record', blueprint='accounting'))

    assert 200 == response.status_code
    assert b'<!--successful this comment is to check that it is reached on test-->' in response.data
    assert b'/accounting/record_to_insert' in response.data
