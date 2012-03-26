BLDD Features
=============

This is my final work of BS in Computer Science at UENF (Universidade Estadual do Norte Fluminense - RJ / Brazil)

Preparing environment
++++++++++++++++++++++

- You'll need a developing instance of `ERP5 <http://www.erp5.com>`_ (I'd recommend `installing it through SlapOS <http://www.erp5.com/download/linux>`_)
- Clone this project and install the inner `erp5_bldd_feature <https://github.com/gabriellima/erp5_bldd_feature/tree/master/erp5_bldd_feature>`_ folder as a `bt5 <http://www.erp5.org/HowToInstallBusinessTemplates>`_
- Place  `workflow_analyzer <https://github.com/gabriellima/erp5_bldd_feature/tree/master/workflow_analyzer>`_ folder at ``ERP5Type/tests`` product folder, so that python will find ``Products.ERP5Type.tests.workflow_analyzer`` to import
- Patch ``Products.ERP5Type.tests.ERP5TypeTestCase`` like shown in `ERP5TypeTestCase.py <https://github.com/gabriellima/erp5_bldd_feature/blob/master/ERP5TypeTestCase.py>`_

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

This project is licensed under `GNU General Public License <http://www.gnu.org/licenses/gpl-2.0.html>`_. For more information, read `license.txt <https://github.com/gabriellima/erp5_bldd_feature/blob/master/license.txt>`_.
