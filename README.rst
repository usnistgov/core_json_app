=============
Core JSON App
=============

Add JSON support to the curator core project.

Quick start
===========

1. Add "core_json_app" to your INSTALLED_APPS setting
-----------------------------------------------------

.. code:: python

    INSTALLED_APPS = [
      ...
      'core_json_app',
    ]

2. Include the core_json_app URLconf in your project urls.py
------------------------------------------------------------

.. code:: python

    url(r'^', include('core_json_app.urls')),
