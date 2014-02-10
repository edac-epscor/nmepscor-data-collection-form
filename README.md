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


# Next Steps

***
* EMail
* Content/Dialog Updates
* Some way to obtain PI and/or account relationships

