---
layout: default
title: SAML Integration
parent: Develop
nav_order: 5
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
pipenv run pip install git+https://github.com/nyudlts/ultraviolet-saml.git
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
-e SIMPLESAMLPHP_SP_ENTITY_ID=https://127.0.0.1:5000/saml/metadata/nyu \
-e SIMPLESAMLPHP_SP_ASSERTION_CONSUMER_SERVICE=https://127.0.0.1:5000/saml/authorized/nyu \
-e SIMPLESAMLPHP_SP_SINGLE_LOGOUT_SERVICE=https://127.0.0.1:5000/saml/sls/nyu \
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

SSO_SAML_IDP_NAME = os.getenv('IDP', 'nyu')

SSO_SAML_IDPS = {

    # name your authentication provider
    SSO_SAML_IDP_NAME: {

        # Basic info
        "title": "NYU Mock SAML",
        "description": "SAML Authentication Service for NYU Ultraviolet",
        "icon": "static/images/logo_ultraviolet_1word_white.svg",

        # path to the file i.e. "./saml/sp.crt"
        'sp_cert_file': os.getenv('SP_CERT','./sp.crt'),

        # path to the file i.e. "./saml/sp.key"
        'sp_key_file': os.getenv('SP_KEY','./sp.key'),

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
                'entityId': os.getenv("IDP_METADATA",'http://localhost:8080/simplesaml/saml2/idp/metadata.php'),

                # SSO endpoint info of the IdP. (Authentication Request protocol)
                'singleSignOnService': {

                    # URL Target of the IdP where the Authentication Request Message
                    # will be sent.
                    'url': os.getenv("IDP_SSO",'http://localhost:8080/simplesaml/saml2/idp/SSOService.php'),

                    # SAML protocol binding to be used when returning the <Response>
                    # message. OneLogin Toolkit supports the HTTP-Redirect binding
                    # only for this endpoint.
                    'binding':
                        'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect'
                },

                # SLO endpoint info of the IdP.
                'singleLogoutService': {
                    # URL Location where the <LogoutRequest> from the IdP will be sent (IdP-initiated logout)
                    "url": os.getenv("IDP_SLO","http://localhost:8080/simplesaml/saml2/idp/SingleLogoutService.php"),

                    # SAML protocol binding to be used when returning the <Response>
                    # message. OneLogin Toolkit supports the HTTP-Redirect binding
                    # only for this endpoint.
                    "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
                },
                # Public X.509 certificate of the IdP
                'x509cert': os.getenv('IDP_X509_CERT_SINGLE','')
            },

            # Security settings
            # more on https://github.com/onelogin/python-saml
            'security': {
                'allowRepeatAttributeName': True,
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
            "email": os.getenv("IDP_SAML_EMAIL", "urn:oid:1.3.6.1.7"),
            "name": os.getenv("IDP_SAML_NAME", "urn:oid:2.5.4.42"),
            "surname": os.getenv("IDP_SAML_SURNAME", "urn:oid:2.5.4.4"),
            "external_id": os.getenv("IDP_SAML_EXTERNALID", "urn:oid:0.9.2342.19200300.100.1.1")
        },

        # Default Affiliation to be assigned to all SAML logged in users - remove this if not required
        "default_affiliation": "New York University",

        # This is used to automatically set email and profile visibility to public to all SAML logged in users - remove this if not required
        "default_visibility": "public",

        # Inject your remote_app to handler
        # Note: keep in mind the string should match
        # given name for authentication provider
        'acs_handler': acs_handler_factory(SSO_SAML_IDP_NAME),

        # Auto confirms all SAML logged in users
        'auto_confirm': True
    }
}

if os.getenv('IDP_X509_CERT_SIGNING',''):
    SSO_SAML_IDPS[SSO_SAML_IDP_NAME]['settings']['idp']['x509certMulti'] = {
    'signing': [os.getenv('IDP_X509_CERT_SIGNING')],
    'encryption': [os.getenv('IDP_X509_CERT_ENCRYPTION')]
    }

SSO_SAML_ROLES = {
        # Default role to be assigned to all SAML logged in users - remove this if not required
        SSO_SAML_IDP_NAME: os.getenv("DEFAULT_SAML_ROLE", "defaultsamlrole"),
}

# The following is a hacky implementation. It should be False for a fresh invenio installation. After creating a community and adding the nyuusers role to the community, add the community ID as a list here
# For example: "auto_update_communities": ["c441b9c2-40e0-4035-96cc-8e13bd28d0f7"] where c441b9c2-40e0-4035-96cc-8e13bd28d0f7 is the community ID retrieved from the communities_metadata table. If one
# community is updated here, no need to update for subsequent communities, they add new group members automatically.
COMMUNITIES_AUTO_UPDATE = False
```


## Configure Environment

Environment needs to be configured for the above SAML setup to work since the sensitive keys and certificates cannot be
placed within cfg. A sample .env config could be as follows:

```
SP_CERT=/home/akshayhegde/ultraviolet/sp.crt
SP_KEY=/home/akshayhegde/ultraviolet/sp.key
IDP=nyu
IDP_X509_CERT_SINGLE=<idp-cert here>
IDP_METADATA=http://localhost:8080/simplesaml/saml2/idp/metadata.php
IDP_SSO=http://localhost:8080/simplesaml/saml2/idp/SSOService.php
IDP_SLO=http://localhost:8080/simplesaml/saml2/idp/SingleLogoutService.php
IDP_SAML_EMAIL=urn:oid:1.3.6.1.7
IDP_SAML_NAME=urn:oid:2.5.4.42
IDP_SAML_SURNAME=urn:oid:2.5.4.4
IDP_SAML_EXTERNALID=urn:oid:0.9.2342.19200300.100.1.1
DEFAULT_SAML_ROLE=nyuuser
```

For multi-cert IDP setup, replace `IDP_X509_CERT_SINGLE` with the following:

```
IDP_X509_CERT_SIGNING=<idp-signing-cert here>
IDP_X509_CERT_ENCRYPTION=<idp-encryption-cert here>
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