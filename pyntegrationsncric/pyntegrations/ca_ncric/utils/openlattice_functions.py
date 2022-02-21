from auth0.v3.authentication import GetToken
import openlattice
import os

def get_jwt(username = None, password = None, client_id = None, base_url='https://api.mychildcare.dss.ca.gov'):
    """
    Gets the jwt token for a given usr/pw from a given url.
    """

    domain='dev-elp-ybhu.us.auth0.com'
    realm='Username-Password-Authentication'
    scope='openid email nickname roles user_id organizations'

    envvars = {
        'rundeck': {
            'user': os.environ.get("RD_OPTION_OL_USER"),
            "password": os.environ.get("RD_OPTION_OL_PASSWORD"),
            "client_id": os.environ.get("RD_OPTION_OL_CLIENT_ID")
        },
        'local_to_local': {
            'user': os.environ.get("ol_user"),
            "password": os.environ.get("ol_password"),
            "client_id": os.environ.get("ol_client_id_local")
        },
        'local_to_prod': {
            'user': os.environ.get("ol_user"),
            "password": os.environ.get("ol_password"),
            "client_id":  os.environ.get('ol_client_id')
        }
    }


    environment = os.environ
    if 'RD_JOB_ID' in environment:
        env = 'rundeck'
    else:
        env = 'local_to_prod' if 'https://api.mychildcare.dss.ca.gov' in base_url else 'local_to_local'
    env = envvars[env]

    if username:
        env['user'] = username
    if password:
        env['password'] = password
    if client_id:
        env['client_id'] = client_id
    if not 'https://api.mychildcare.dss.ca.gov' in base_url:
        base_url = 'https://openlattice.auth0.com/userinfo'

    if not (env['user'] and env['password'] and env['client_id']):
        raise ValueError("Not all necessary variables for authentication are present !")


    get_token = GetToken(domain)
    token = get_token.login(
        client_id=env['client_id'],
        client_secret="",
        username=env['user'],
        password=env['password'],
        scope=scope,
        realm=realm,
        audience=base_url,
        grant_type='http://auth0.com/oauth/grant-type/password-realm'
        )
    return token['id_token']

def get_config(jwt = None, base_url = "https://api.mychildcare.dss.ca.gov"):
    if not jwt:
        jwt = get_jwt(base_url = base_url)
    configuration = openlattice.Configuration()
    configuration.host = base_url
    configuration.access_token = jwt

    return configuration