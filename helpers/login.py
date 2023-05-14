import grequests
from requests.cookies import merge_cookies
from .config import (
    LMS_URL,
    STAFF_EMAIL,
    STAFF_PASSWORD
)

LOGIN_URL = f"{LMS_URL}/login"
LOGIN_SESSION_URL = f"{LMS_URL}/api/user/v1/account/login_session/"

def _fetch_session_cookies_for_login():
    '''
    Fetch some cookies such as csrf token required for login_session call
    '''
    print("Fetching session cookies for login")
    reqs = [grequests.get(LOGIN_URL)]
    r = grequests.map(reqs)[0]
    return r.cookies

def login_to_lms():
    '''
    Create a user session in LMS using the user credentials

    Returns the session cookies to be used for API calls.
    '''
    cookie_jar = _fetch_session_cookies_for_login()
    
    auth_creds = {'email': STAFF_EMAIL, 'password': STAFF_PASSWORD}
    headers = {'Referer': LOGIN_URL, 'X-CSRFToken': cookie_jar['csrftoken'], 'X-Requested-With': 'XMLHttpRequest'}

    print("Logging in using staff credentials")
    reqs = [grequests.post(LOGIN_SESSION_URL, cookies=cookie_jar, data=auth_creds, headers=headers)]
    r = grequests.map(reqs)[0]
    cookie_jar = merge_cookies(cookie_jar, r.cookies)

    return cookie_jar
