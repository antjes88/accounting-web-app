import pytest

@pytest.mark.parametrize(
    "route, expected_response, expected_status_code",
    [
        ("home", b'<!--home this comment is to check that it is reached on test-->', 200),
        ("error_page", b'<!--error_page this comment is to check that it is reached on test-->', 200)
    ]
)
def test_home_pages_are_reached(client, route, expected_response, expected_status_code):
    """
    GIVEN a user surfing the web page
    WHEN tries to access home_page routes
    THEN makes sure that the right html is returned
    """
    response = client.get_with_login('home_page.' + route)

    assert expected_status_code == response.status_code
    assert expected_response in response.data


def test_successful_page_is_reached(client):
    """
    GIVEN a user surfing the web page
    WHEN tries to access home_page.successful
    THEN makes sure that the right html is returned
    """
    response = client.get_with_login('home_page.successful',
                                     query_string=dict(go_back_to='home', blueprint='home_page'))

    assert 200 == response.status_code
    assert b'<!--successful this comment is to check that it is reached on test-->' in response.data


def test_error_page_shows_message_provided(client):
    """
    GIVEN that an error message in pass as argument to home_page.error_page
    WHEN home_page.error_page is rendered
    THEN makes sure that the right html is returned with the error message
    """
    message = 'This is a message to test the app'
    response = client.get_with_login('home_page.error_page',
                                     query_string=dict(message=message))

    assert 200 == response.status_code
    assert b'<!--error_page this comment is to check that it is reached on test-->' in response.data
    assert bytearray(message, "UTF-8") in response.data


def test_successful_builds_url_to_route_provided(client):
    """
    GIVEN that a Web App is provided to redirect back to is passed as argument to home_page.successful
    WHEN home_page.successful is rendered
    THEN makes sure that the right html is returned with the redirection link button
    """
    response = client.get_with_login('home_page.successful',
                                     query_string=dict(blueprint='accounting', go_back_to='new_record'))

    assert 200 == response.status_code
    assert b'<!--successful this comment is to check that it is reached on test-->' in response.data
    assert b'accounting/new_record' in response.data
