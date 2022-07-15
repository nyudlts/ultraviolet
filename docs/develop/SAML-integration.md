---
layout: default
title: SAML Integration
parent: Develop
nav_order: 4
---
# {{ page.title }}

## Prerequisites

SAML Integration requires the installation of the `invenio-saml` package, which in turn requires `libxml2-dev` and `libxmlsec1-dev` to be installed on your system.

```
cd ultraviolet
pipenv install invenio-saml
```

This is different from the command given to install `invenio-saml` in the invenio documentation:
```
cd ultraviolet
pipenv run pip install invenio-saml
```
The above command runs successfully, but doesn't create saml endpoints and doesn't show the package inside the `pipfile`.

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

### Usage
```
docker run --name=testsamlidp_idp \
-p 8080:8080 \
-p 8443:8443 \
-e SIMPLESAMLPHP_SP_ENTITY_ID=https://archivefda.dlib.nyu.edu/shibboleth-sp \
-e SIMPLESAMLPHP_SP_ASSERTION_CONSUMER_SERVICE=<UV SP ACS ROUTE> \
-e SIMPLESAMLPHP_SP_SINGLE_LOGOUT_SERVICE=<UV SP SLO ROUTE> \
-d kristophjunge/test-saml-idp
```

## Configuration

In your `invenio.cfg`:

```
from invenio_saml.handlers import acs_handler_factory

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
    'simplesaml': {

        # Basic info
        "title": "SAML",
        "description": "SAML Authentication Service",
        "icon": "",

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
                'NameIDFormat': 'urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified',
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
                    'url': 'http://localhost:8080/simplesaml/saml2/idp/SingleLogoutService.php',

                    # SAML protocol binding to be used when returning the <Response>
                    # message. OneLogin Toolkit supports the HTTP-Redirect binding
                    # only for this endpoint.
                    'binding':
                        'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect'
                },
                # Public X.509 certificate of the IdP
                'x509cert': '119b9e027959cdb7c662cfd075d9e2ef384e445f'
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

        # Account Mapping
        "mappings": {
            "email": "<attribute_email>",
            "name": "<attribute_name>",
            "surname": "<attribute_surname>",
            "external_id": "<attribute_external_id>",
        },

        # Inject your simplesaml idp app to handler
        # Note: keep in mind the string should match
        # given name for authentication provider
        'acs_handler': acs_handler_factory('simplesaml'),
    }
}
```

## Show the Login Button

The last step is to enable the login template, provided by the SAML module, to display the new button `Login with SAML`. In your `invenio.cfg`:

```
OAUTHCLIENT_LOGIN_USER_TEMPLATE = "invenio_saml/login_user.html"
```