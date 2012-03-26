from Products.ERP5Type.tests.workflow_analyzer.WorkflowAnalyzerTestCase import patchERP5PortalWorkflow, unpatchERP5PortalWorkflow, rescueTestTransactions

def patchPortalWorkflow(self):
  patchERP5PortalWorkflow()
  print "\nALERT: PortalWorkflow patched!!!\n"

def unpatchPortalWorkflow(self):
  unpatchERP5PortalWorkflow()
  print "\nALERT: PortalWorkflow unpatched!!!\n"

def rescueTransactions(self, workflow_id=None):
  result = rescueTestTransactions(workflow_id)
  #from pprint import pprint, _StringIO
  #output = _StringIO()
  #pprint(result, output)
  #output.seek(0)
  #return output.read()
  return result
#  return rescueTestTransactions(workflow_id)
