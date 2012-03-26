BLDD Features
=============

This is my final work of BS in Computer Science at UENF (Universidade Estadual do Norte Fluminense - RJ / Brazil)

Preparing environment
++++++++++++++++++++++

- You'll need a developing instance of `ERP5 <http://www.erp5.com>`_ (I'd recommend `installing it through SlapOS <http://www.erp5.com/download/linux>`_)
- Download ``erp5_bldd_feature`` and install it as a `bt5 <http://www.erp5.org/HowToInstallBusinessTemplates>`_ , first taking out ``README.rst``, ``ERP5TypeTestCase.py``, ``license.txt`` and ``workflow_analyzer`` files/folders (not related directly to the bt5)
- Place  ``workflow_analyzer`` folder at ``ERP5Type/tests`` product folder, so that python will find ``Products.ERP5Type.tests.workflow_analyzer`` to import
- Patch ``Products.ERP5Type.tests.ERP5TypeTestCase`` like shown in ``ERP5TypeTestCase.py`` available here

Using
++++++

- Run any ERP5 test, and the manipuled ``workflows`` of each ``test method`` will be stored under ``workflow_analyzer/analyzer.db`` file, using `shelve <http://docs.python.org/library/shelve.html>`_.
- With an ERP5 instance running, add some features and then some scenarios.
- Each scenario contains an "Execute Steps" action, that will parse the scenario's steps. The ones that will be recognized (via regex) are:

  - ``create_object_step = re.match("(Given|And) that I have a \'([^\']+)\'", step)``
  - ``fire_transaction_step = re.match("(When|And) I trigger \'([^\']+)\'", step)``
  - ``check_state_step = re.match("(Then|And) it should be in \'([^\']+)\'", step)``

- Any other step that does not match the regular expressions defined will be ignored.
- Also, during the execution, handled ``workflows`` will be kept so that after the execution, tests related to the same ``workflows`` will be shown.
- Further, during execution, handled workflows are kept so that, after execution, tests related to them are displayed.

---------------------------------------

This project is licensed under `GNU General Public License <http://www.gnu.org/licenses/gpl-2.0.html>`_. For more information, read ``license.txt``.
