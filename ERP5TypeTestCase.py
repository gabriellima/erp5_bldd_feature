# Somewhere around the beginning of this file available
# at https://svn.erp5.org/repos/public/erp5/trunk/products/ERP5Type/tests/ERP5TypeTestCase.py
# ........................................................
from Products.ERP5Type.tests.ProcessingNodeTestCase import \
  ProcessingNodeTestCase, patchActivityTool
onsetup(patchActivityTool)()

# NOTE: this is what you need to add right after !!!
from Products.ERP5Type.tests.workflow_analyzer.WorkflowAnalyzerTestCase import patchPortalWorkflow
onsetup(patchPortalWorkflow)()


# NOTE: And the above line must be placed before the line below:
ZopeTestCase.installProduct('DCWorkflow', quiet=install_product_quiet)
