from flask import url_for


def test_login_page_is_reached(client):
    """
    GIVEN a user surfing the web page
    WHEN tries to access login_page.login
    THEN makes sure that the right html is returned
    """
    with client.application.app_context():
        login_url = url_for('login_page.login')
    response = client.get(login_url)

    assert 200 == response.status_code
    assert b'<!--Login_form this comment is to check that it is reached on test-->' in response.data


def test_all_pages_are_protected_by_login_page(client):
    """
    GIVEN all routes in the web page
    WHEN the user is not authenticated
    THEN makes sure that the user cannot access the route and is sent back to login page
    """
    links = []
    with client.application.app_context():
        for _rule in client.application.url_map.iter_rules():
            if _rule:
                if '/' == _rule.endpoint[0]:
                    links.append(_rule.endpoint)
                elif 'STATIC' in _rule.endpoint.upper():
                    pass
                else:
                    links.append(url_for('%s' % _rule.endpoint))

    for url in links:
        response = client.get(url, follow_redirects=True)

        assert 200 == response.status_code
        assert b'<!--Login_form this comment is to check that it is reached on test-->' in response.data


def test_log_in_and_out(client):
    """
    GIVEN a user that navigates the web page
    WHEN he logs in or logs out
    THEN he should get to the landing page (log in) or should be redirected to log in page (log out)
    """
    response_login = client.login()
    response_logout = client.logout('login_page.logout')

    assert 200 == response_login.status_code
    assert b'<!--home this comment is to check that it is reached on test-->' in response_login.data
    assert 200 == response_logout.status_code
    assert b'<!--Login_form this comment is to check that it is reached on test-->' in response_logout.data


def test_log_in_with_wrong_credentials(client_wrong_credentials):
    """
    GIVEN a user trying to authenticate
    WHEN he uses wrong credentials
    THEN he should not be allowed to log in and should be redirected to login page
    """
    response = client_wrong_credentials.login()

    assert b'<!--Login_form this comment is to check that it is reached on test-->' in response.data


def test_login_page_when_field_required_no_provided(client_wrong_credentials):
    """
    GIVEN a user trying to authenticate
    WHEN he does not provide user_name or password
    THEN 'This field is required' message should be prompted
    """
    client_wrong_credentials.password = ''
    response_no_username = client_wrong_credentials.login()

    client_wrong_credentials.username = ''
    client_wrong_credentials.password = '123'
    response_username_empty_string = client_wrong_credentials.login()

    assert b'This field is required' in response_no_username.data
    assert b'This field is required' in response_username_empty_string.data
