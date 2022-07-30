from flask import url_for


def test_login_page_is_reached(client):
    with client.application.app_context():
        login_url = url_for('login_page.login')
    response = client.get(login_url)

    assert 200 == response.status_code
    assert b'<!--Login_form this comment is to check that it is reached on test-->' in response.data


def test_all_pages_are_protected_by_login_page(client):
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
    response = client.login()

    assert 200 == response.status_code
    assert b'<!--home this comment is to check that it is reached on test-->' in response.data

    response = client.logout('login_page.logout')

    assert 200 == response.status_code
    assert b'<!--Login_form this comment is to check that it is reached on test-->' in response.data


def test_log_in_with_wrong_credentials(client_wrong_credentials):
    response = client_wrong_credentials.login()

    assert b'<!--Login_form this comment is to check that it is reached on test-->' in response.data


def test_login_page_when_field_required_no_provided(client_wrong_credentials):
    client_wrong_credentials.password = ''
    response = client_wrong_credentials.login()

    assert b'This field is required' in response.data

    client_wrong_credentials.username = ''
    client_wrong_credentials.password = 123
    response = client_wrong_credentials.login()

    assert b'This field is required' in response.data
