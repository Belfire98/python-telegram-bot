..
    Make sure to apply any changes to this file to README.rst as well!

.. image:: https://github.com/python-telegram-bot/logos/blob/master/logo-text/png/ptb-raw-logo-text_768.png?raw=true
   :align: center
   :target: https://python-telegram-bot.org
   :alt: python-telegram-bot-raw Logo

Resource Badges
--------------

.. list-table::
   :header-rows: 1

   * - Badge
     - Description
     - Link

   * - PyPi Package Version
     - The current version on PyPI
     - https://pypi.org/project/python-telegram-bot-raw/

   * - Supported Python versions
     - The Python versions that are supported
     - https://pypi.org/project/python-telegram-bot-raw/

   * - Supported Bot API versions
     - The Bot API versions that are supported
     - https://core.telegram.org/bots/api-changelog

   * - PyPi Package Monthly Download
     - The number of monthly downloads from PyPI
     - https://pypistats.org/packages/python-telegram-bot-raw

   * - Documentation Status
     - The status of the documentation
     - https://docs.python-telegram-bot.org/

   * - LGPLv3 License
     - The license under which the software is released
     - https://www.gnu.org/licenses/lgpl-3.0.html

   * - Github Actions workflow
     - The status of the Github Actions workflow
     - https://github.com/python-telegram-bot/python-telegram-bot/

   * - Code coverage
     - The code coverage report
     - https://app.codecov.io/gh/python-telegram-bot/python-telegram-bot

   * - Median time to resolve an issue
     - The median time to resolve an issue
     - https://isitmaintained.com/project/python-telegram-bot/python-telegram-bot

   * - Code quality: Codacy
     - The code quality report from Codacy
     - https://app.codacy.com/gh/python-telegram-bot/python-telegram-bot/dashboard

   * - pre-commit.ci status
     - The status of the pre-commit.ci checks
     - https://results.pre-commit.ci/latest/github/python-telegram-bot/python-telegram-bot/master

   * - Code Style: Black
     - The code style used in the project
     - https://github.com/psf/black

   * - Telegram Channel
     - The official Telegram channel for updates and news
     - https://t.me/pythontelegrambotchannel

   * - Telegram Group
     - The official Telegram group for discussions and support
     - https://telegram.me/pythontelegrambotgroup

Introduction
============

This library provides a pure Python, asynchronous interface for the
`Telegram Bot API <https://core.telegram.org/bots/api>`_.
It's compatible with Python versions **3.8+**.

``python-telegram-bot-raw`` is part of the `python-telegram-bot <https://python-telegram-bot.org>`_ ecosystem and provides the pure API functionality extracted from PTB. It therefore does not have independent release schedules, changelogs or documentation.

Note
----

Installing both ``python-telegram-bot`` and ``python-telegram-bot-raw`` in conjunction will result in undesired side-effects, so only install *one* of both.

Telegram API support
====================

All types and methods of the Telegram Bot API **7.1** are supported.

Installing
==========

You can install or upgrade ``python-telegram-bot-raw`` via

.. code:: shell

    $ pip install python-telegram-bot-raw --upgrade

To install a pre-release, use the ``--pre`` `flag <https://pip.pypa.io/en/stable/cli/pip_install/#cmdoption-pre>`_ in addition.

You can also install ``python-telegram-bot-raw`` from source, though this is usually not necessary.

.. code:: shell

    $ git clone https://github.com/python-telegram-bot/python-telegram-bot
    $ cd python-telegram-bot
    $ python setup_raw.py install

Note
----

Installing the ``.tar.gz`` archive available on PyPi directly via ``pip`` will *not* work as expected, as ``pip`` does not recognize that it should use ``setup_raw.py`` instead of ``setup.py``.

Verifying Releases
------------------

We sign all the releases with a GPG key.
The signatures are uploaded to both the `GitHub releases page <https://github.com/python-telegram-bot/python-telegram-bot/releases>`_ and the `PyPI project <https://pypi.org/project/python-telegram-bot/>`_ and end with a suffix ``.asc``.
Please find the public keys `here <https://github.com/python-telegram-bot/python-telegram-bot/tree/master/public_keys>`_.
The keys are named in the format ``<first_version>-<last_version>.gpg`` or ``<first_version>-current.gpg`` if the key is currently being used for new releases.

In addition, the GitHub release page also contains the sha1 hashes of the release files in the files with the suffix ``.sha1``.

This allows you to verify that a release file that you downloaded was indeed provided by the ``python-telegram-bot`` team.

Dependencies & Their Versions
-----------------------------

``python-telegram-bot`` tries to use as few 3rd party dependencies as possible.
However, for some features using a 3rd party library is more sane than implementing the functionality again.
As these features are *
