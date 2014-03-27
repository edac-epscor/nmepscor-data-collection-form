nmepscor-data-collection-form
=============================

## NMEPSCoR data documentation tool -- angular-enterprise-seed/djangoized

Clone/fork of  https://github.com/robertjchristian/angular-enterprise-seed.git with lots of modifications to bring up a data collection form
that can auth to the nm epscor portal

# Usage

## As Django app.  No real database configured given expected load

## Known Stack

***

* See freezelog

# Known Issues

***

* This should be split into a few apps
  * Angular Enterprise Build
  * NM EPSCoR Remote Auth
  * NM EPSCoR form collection widget
  * `needs` a submission/email utility
  * `needs` a way to obtain the PI
* The enterprise seed should have angularjs brought forward
* There are some local script sources that should probably be brought in via CDN
* Should add django minifier to the css & js
* It is very unclear if the NM EPSCoR site is willing to run or provide remote services or keep them updated
  - Which has resulted in awkward session code in the builder module and to the user authentication system
  - And highly indirect best-effort proxied authentication
  - The builder code should be rewritten as a custom django authentication backend instead of what it is now
  - If the remote user name changes, we're in trouble.
* The /admin portion could be rebound to the native user application
  - And should probably have a few more fields locked.
* Error Messaging
* Testing
* Angular must have a better interstitial/overlay that can be bound to $http
  and jQuery with a timer and/or retry/error handler and/or event queue
* The django debug toolbar isn't very useful in the JSON views
* There's got to be a better django-crud-json framework available


# Next Steps

***
* Finish bowerizing CSS which has minor mismatch in versions.
  - Unpin versions and move closer to trunks/stable
* EMail
* Content/Dialog Updates
* Some way to obtain PI and/or account relationships
* More form validators


# To Run (not install)

***
* Setup and activate a python virtualenv
* git clone
* pip install -r requirements.txt
* Rename mdform/secret_settings.template.py to secret_settings.py and fill in for your app
  - Set SECRET_EPSCOR_SERVER (to the drupal install that we will authenticate against)
  - Set allowed hosts to your hostname
    - If debug is not set, and you are not accessing by hostname, you will get a security error from the django host validator
    - For testing, you could use * or '127.0.0.1' 
    - Basically, if "DEBUG=False", your browser needs to send a host header matching allowed hosts while testing.
  - Set your SECRET_KEY (this is used to cryptographically sign cookies)
    - http://www.miniwebtool.com/django-secret-key-generator/
    - Explanation at https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
* python manage.py syncdb (setup initial account/database via sqlite)
* python manage.py runserver 0.0.0.0:8000
* Test by visiting http://127.0.0.1:8000 (if debug is on)
  - Visit at host name if debug is off (http://example.com....)
  - This will redirect you to 127.0.0.1:8000/#/
  - This URL may be changed at a later date
  - If debug is off, you will need staticfiles served or will see a blank page.

# If in production environment

***
* See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/
  - Be sure debug is False
* python manage.py bower_install (Gather proper JS versions, choose bootstrap 3.0.0)
* python manage.py collectstatic (collect static files for serving outside of wsgi)
  - Add the folder this creates as an apache served folder
* I believe this entire app is now 'rooted' within whatever folder it lies in
  - Therefore it can be mod-rewritten into folders of Apache

