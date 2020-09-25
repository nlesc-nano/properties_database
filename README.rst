.. image:: https://github.com/nlesc-nano/properties_database/workflows/build/badge.svg
   :target: https://github.com/nlesc-nano/properties_database/actions

################################################################################
properties_database
################################################################################

Database for the ligands molecular properties

Installation
************
1. Install `Docker <https://www.docker.com/>`_
2. Start the mongodb image:
::
   docker run -d -p 27017-27019:27017-27019 --name mongodb mongo:latest


Contributing
************

If you want to contribute to the development of properties_database,
have a look at the `contribution guidelines <CONTRIBUTING.rst>`_.

License
*******

Copyright (c) 2020, 

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.



Credits
*******

This package was created with `Cookiecutter <https://github.com/audreyr/cookiecutter>`_ and the `NLeSC/python-template <https://github.com/NLeSC/python-template>`_.
