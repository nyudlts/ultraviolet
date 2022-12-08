---
layout: default
title: SAML Integration
parent: Develop
nav_order: 4
---
# {{ page.title }}

## Prerequisites

SAML Integration requires the installation of the :code:`ultraviolet-saml` package, which in turn requires :code:`libxml2-dev` and :code:`libxmlsec1-dev` to be installed on your system. If you're running Ubuntu, run:

```
apt-get install libxml2-dev libxmlsec1-dev libxmlsec1-openssl
```

On the other hand, if you're running CentOS/RHEL:

```
yum install libxml2-devel xmlsec1-devel xmlsec1-openssl-devel libtool-ltdl-devel
```

Currently, the automatic-role-assignment branch needs to be used to obtain the required behaviour. Use the following commands to install:

```
cd ultraviolet
pipenv run pip install git+https://github.com/nyudlts/ultraviolet-saml.git@automatic-role-assignment
```

The above command runs successfully, but doesn't create saml endpoints and doesn't show the package inside the `pipfile`.

NOTE: Please note that Invenio v10.0 is required for communities related features. SAML-configured ultraviolet with v10 is available at 

## Server Information

List of information required to configure the InvenioRDM instance.

- SAML requires a x.509 cert to sign and encrypt elements like NameID, Message, Assertion, Metadata.
  - **sp.crt** or **sp.pem**: The public cert of the SP.
  - **sp.key** or **key.pem**: The private key of the SP.
- **EntityID**: Identifier of the IdP entity (must be a URI).
- **SSO(singleSignOnService)**: URL Target of the IdP where the Authentication Request Message will be sent.
- **SLO(singleLogoutService)**: URL Location where the from the IdP will be sent (IdP-initiated logout).
- **x509cert**: Public X.509 certificate of the IdP.
- **Attributes mapping**: IDP in Assertion of the SAML Response provides a dict with all the user data:

## IdP Setup

For testing, we have used the [Docker Test SAML 2.0 Identity Provider](https://hub.docker.com/r/kristophjunge/test-saml-idp/), which is built using SimpleSAMLphp. 
We are also using a custom authsources.php which helps us configure the SAML IdP to reflect NYU's IdP, this is currently placed under app_data of the v10-SAML branch of ultraviolet available [here](https://github.com/nyudlts/ultraviolet/blob/v10-SAML/app_data/authsources.php).
Run the following command to instantiate the docker container:

```
docker run --name=nyu_mock_idp \
-p 8080:8080 \
-p 8443:8443 \
-e SIMPLESAMLPHP_SP_ENTITY_ID=https://127.0.0.1:5000/saml/metadata/nyu_mock \
-e SIMPLESAMLPHP_SP_ASSERTION_CONSUMER_SERVICE=https://127.0.0.1:5000/saml/authorized/nyu_mock \
-e SIMPLESAMLPHP_SP_SINGLE_LOGOUT_SERVICE=https://127.0.0.1:5000/saml/sls/nyu_mock \
-v <Absolute path to your copy of authsources.php, currently placed under app_data/authsources.php>:/var/www/simplesamlphp/config/authsources.php \
-d kristophjunge/test-saml-idp
```

## Configuration

Add this to your imports in :code:`invenio.cfg`::

```
from ultraviolet_saml.handlers import acs_handler_factory
```

In your `invenio.cfg`, add the following:

```
# Invenio-SAML Configuration
# ==========================
# See https://inveniordm.docs.cern.ch/customize/authentication/#saml-integration

SSO_SAML_DEFAULT_BLUEPRINT_PREFIX = '/saml'
"""Base URL for the extensions endpoint."""

SSO_SAML_DEFAULT_METADATA_ROUTE = '/metadata/<idp>'
"""URL route for the metadata request."""

SSO_SAML_DEFAULT_SSO_ROUTE = '/login/<idp>'
"""URL route for the SP login."""

SSO_SAML_DEFAULT_ACS_ROUTE = '/authorized/<idp>'
"""URL route to handle the IdP login request."""

SSO_SAML_DEFAULT_SLO_ROUTE = '/slo/<idp>'
"""URL route for the SP logout."""

SSO_SAML_DEFAULT_SLS_ROUTE = '/sls/<idp>'
"""URL route to handle the IdP logout request."""

SSO_SAML_IDPS = {

# name your authentication provider
'nyu_mock': {

    # Basic info
    "title": "NYU Mock SAML",
    "description": "SAML Authentication Service for Ultraviolet",
    "icon": "static/images/logo_ultraviolet_1word_white.svg",

    # path to the file i.e. "./saml/sp.crt"
    'sp_cert_file': './certificate.pem',

    # path to the file i.e. "./saml/sp.key"
    'sp_key_file': './sp.pem',

    'settings': {
        # If strict is True, then the Python Toolkit will reject unsigned
        # or unencrypted messages if it expects them to be signed or encrypted.
        # Also it will reject the messages if the SAML standard is not strictly
        # followed. Destination, NameId, Conditions ... are validated too.
        'strict': True,

        # Enable debug mode (outputs errors).
        'debug': True,

        # Service Provider Data that we are deploying.
        'sp': {

            # Specifies the constraints on the name identifier to be used to
            # represent the requested subject.
            # Take a look on https://github.com/onelogin/python-saml/blob/master/src/onelogin/saml2/constants.py
            # to see the NameIdFormat that are supported.
            'NameIDFormat': 'urn:oasis:names:tc:SAML:2.0:nameid-format:transient'
        },

        # Identity Provider Data that we want connected with our SP.
        'idp': {

            # Identifier of the IdP entity  (must be a URI)
            'entityId': 'http://localhost:8080/simplesaml/saml2/idp/metadata.php',

            # SSO endpoint info of the IdP. (Authentication Request protocol)
            'singleSignOnService': {

                # URL Target of the IdP where the Authentication Request Message
                # will be sent.
                'url': 'http://localhost:8080/simplesaml/saml2/idp/SSOService.php',

                # SAML protocol binding to be used when returning the <Response>
                # message. OneLogin Toolkit supports the HTTP-Redirect binding
                # only for this endpoint.
                'binding':
                    'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect'
            },

            # SLO endpoint info of the IdP.
            'singleLogoutService': {
                # URL Location where the <LogoutRequest> from the IdP will be sent (IdP-initiated logout)
                "url": "http://localhost:8080/simplesaml/saml2/idp/SingleLogoutService.php",

                # SAML protocol binding to be used when returning the <Response>
                # message. OneLogin Toolkit supports the HTTP-Redirect binding
                # only for this endpoint.
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
            },
            # Public X.509 certificate of the IdP
            'x509cert': 'MIIDXTCCAkWgAwIBAgIJALmVVuDWu4NYMA0GCSqGSIb3DQEBCwUAMEUxCzAJBgNVBAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEwHwYDVQQKDBhJbnRlcm5ldCBXaWRnaXRzIFB0eSBMdGQwHhcNMTYxMjMxMTQzNDQ3WhcNNDgwNjI1MTQzNDQ3WjBFMQswCQYDVQQGEwJBVTETMBEGA1UECAwKU29tZS1TdGF0ZTEhMB8GA1UECgwYSW50ZXJuZXQgV2lkZ2l0cyBQdHkgTHRkMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzUCFozgNb1h1M0jzNRSCjhOBnR+uVbVpaWfXYIR+AhWDdEe5ryY+CgavOg8bfLybyzFdehlYdDRgkedEB/GjG8aJw06l0qF4jDOAw0kEygWCu2mcH7XOxRt+YAH3TVHa/Hu1W3WjzkobqqqLQ8gkKWWM27fOgAZ6GieaJBN6VBSMMcPey3HWLBmc+TYJmv1dbaO2jHhKh8pfKw0W12VM8P1PIO8gv4Phu/uuJYieBWKixBEyy0lHjyixYFCR12xdh4CA47q958ZRGnnDUGFVE1QhgRacJCOZ9bd5t9mr8KLaVBYTCJo5ERE8jymab5dPqe5qKfJsCZiqWglbjUo9twIDAQABo1AwTjAdBgNVHQ4EFgQUxpuwcs/CYQOyui+r1G+3KxBNhxkwHwYDVR0jBBgwFoAUxpuwcs/CYQOyui+r1G+3KxBNhxkwDAYDVR0TBAUwAwEB/zANBgkqhkiG9w0BAQsFAAOCAQEAAiWUKs/2x/viNCKi3Y6blEuCtAGhzOOZ9EjrvJ8+COH3Rag3tVBWrcBZ3/uhhPq5gy9lqw4OkvEws99/5jFsX1FJ6MKBgqfuy7yh5s1YfM0ANHYczMmYpZeAcQf2CGAaVfwTTfSlzNLsF2lW/ly7yapFzlYSJLGoVE+OHEu8g5SlNACUEfkXw+5Eghh+KzlIN7R6Q7r2ixWNFBC/jWf7NKUfJyX8qIG5md1YUeT6GBW9Bm2/1/RiO24JTaYlfLdKK9TYb8sG5B+OLab2DImG99CJ25RkAcSobWNF5zD0O6lgOo3cEdB/ksCq3hmtlC/DlLZ/D8CJ+7VuZnS1rR2naQ=='
        },

        # Security settings
        # more on https://github.com/onelogin/python-saml
        'security': {
            'authnRequestsSigned': False,
            'failOnAuthnContextMismatch': False,
            'logoutRequestSigned': False,
            'logoutResponseSigned': False,
            'metadataCacheDuration': None,
            'metadataValidUntil': None,
            'nameIdEncrypted': False,
            'requestedAuthnContext': False,
            'requestedAuthnContextComparison': 'exact',
            'signMetadata': False,
            'signatureAlgorithm':
                'http://www.w3.org/2001/04/xmldsig-more#rsa-sha256',
            'wantAssertionsEncrypted': False,
            'wantAssertionsSigned': False,
            'wantAttributeStatement': False,
            'wantMessagesSigned': False,
            'wantNameId': True,
            'wantNameIdEncrypted': False,
            'digestAlgorithm':
                'http://www.w3.org/2001/04/xmlenc#sha256'
        },
    },

    # Account Mapping as per NYU's available mappings. Please take a look here https://wikis.nyu.edu/download/attachments/40274104/SAMLShibbolethIntegrationGuidev2.1.pdf?version=1&modificationDate=1517176083918&api=v2
    "mappings": {
        "email": "eduPersonPrincipleName",
        "name": "givenName",
        "surname": "surname",
        "external_id": "uid"
    },

    # Default Affiliation to be assigned to all SAML logged in users - remove this if not required
    "default_affiliation": "New York University",

    # This is used to automatically set email and profile visibility to public to all SAML logged in users - remove this if not required
    "default_visibility": "public",

    # Inject your remote_app to handler
    # Note: keep in mind the string should match
    # given name for authentication provider
    'acs_handler': acs_handler_factory('nyu_mock'),

    # Auto confirms all SAML logged in users
    'auto_confirm': True
    }
}

# The following is a hacky implementation. It should be False for a fresh ultraviolet installation. After creating a community and adding the nyuusers role to the community using ultraviolet-cli, add the community ID as a list here
# For example: COMMUNITIES_AUTO_UPDATE = ["c441b9c2-40e0-4035-96cc-8e13bd28d0f7"] where c441b9c2-40e0-4035-96cc-8e13bd28d0f7 is the community ID retrieved from the ultraviolet-cli communities_create command. If one
# community is updated here, no need to update for subsequent communities, they add new group members automatically.
COMMUNITIES_AUTO_UPDATE = False

SSO_SAML_ROLES = {
        # Default role to be assigned to all SAML logged in users - remove this if not required
        # Unique role for each added SAML configuration needs to be specified here
        "nyu_mock": "nyuusers",
}
```

## Show the Login Button

Next, enable the login template, provided by the SAML module, to display the new button `Login with SAML`. In your `invenio.cfg`:

```
OAUTHCLIENT_LOGIN_USER_TEMPLATE = "ultraviolet_saml/login_user.html"
```

## Create Role

For SAML to work properly, the nyuusers role needs to be created and available. This step needs to be performed once. In your ultraviolet folder,

```
cd ultraviolet
pipenv run invenio roles create nyuusers -d "Group of all users logged in from NYU's Shibboleth SAML system"
```

## Production Deployment Notes

Note that to deploy into production, in your `invenio.cfg`, all SAML references to `localhost:8080` needs to be replaced by NYU's SAML IdP and all references to `127.0.0.1:5000` needs to be pointing to Ultraviolet's web domain. 
Replace the SAML configuration name from nyu_mock to nyu as you see fit as well.

## Points to Note

1. If after login, you encounter a 'Page Not Found' screen, check your invenio.cfg configuration, especially for the `default_role`, `default_visibility`, `auto_update_communities` fields.
2. It is important to create the nyuusers role before running SAML login, since the login tries to assign the role to the user without a clear error message.