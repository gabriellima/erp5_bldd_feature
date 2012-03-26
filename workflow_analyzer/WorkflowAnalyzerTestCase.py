##############################################################################
#
# Copyright (c) 2002-2012 Nexedi SA and Contributors. All Rights Reserved.
#                         Gabriel L. Oliveira <ciberglo@gmail.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
##############################################################################
import base64, errno, os, select, socket, sys, time
from threading import Thread
from UserDict import IterableUserDict
import Lifetime
import transaction
from Testing import ZopeTestCase
from ZODB.POSException import ConflictError
from zLOG import LOG, ERROR
from Products.CMFActivity.Activity.Queue import VALIDATION_ERROR_DELAY
from Products.ERP5Type.tests import backportUnittest
from Products.ERP5Type.tests.utils import createZServer

def patchPortalWorkflow():
  """Redefine several methods of portal_workflow for unit tests
  """
  from Products.DCWorkflow.DCWorkflow import DCWorkflowDefinition
  def patch(function):
    name = function.__name__
    orig_function = getattr(DCWorkflowDefinition, name)
    setattr(DCWorkflowDefinition, '_orig_' + name, orig_function)
    setattr(DCWorkflowDefinition, name, function)
    function.__doc__ = orig_function.__doc__
    # make life easier when inspecting the wrapper with ipython
    function._original = orig_function

  from Products.CMFCore.WorkflowTool import WorkflowTool
  setattr(WorkflowTool, 'analyzer_modified_objects', {})

  @patch
  def _executeTransition(self, ob, tdef=None, kwargs=None):
    # save action
    try:
      modified_objects = getattr(self.getParentNode(), 'analyzer_modified_objects')
      # get information
      portal_type = ob.getPortalType()
      portal_path = ob.getPath()
      workflow_id = self.getId()
      action = tdef and tdef.getId() or self.variables['action'].default_value
      old_state = self._getWorkflowStateOf(ob).getId()
      new_state = tdef and tdef.new_state_id or self.initial_state
      # save information to output
      modified_objects.setdefault(workflow_id, []).append({
        'portal_type': portal_type,
        'portal_path': portal_path,
        'action': action,
        'old_state': old_state,
        'new_state': new_state,
      })
      # persist information
      persistTransactions(self, modified_objects)
    except:
      pass
    self._orig__executeTransition(ob, tdef, kwargs)


def persistTransactions(self, modified_workflows):
  import inspect
  import os
  import shelve
  # introspection to get test_name and test_class
  ERP5TypeTestCase_frame = [call for call in inspect.stack() \
          if 'ERP5TypeTestCase' in call[1]][0][0] #call[1] is filename
  test_name = ERP5TypeTestCase_frame.f_locals['test_name']
  test_class = ERP5TypeTestCase_frame.f_locals['test_method'].im_class.__name__

  # persist data
  folder_path = os.path.dirname(os.path.abspath(__file__))
  db_path = os.path.join(folder_path, 'analyzer.db')

  db = shelve.open(db_path)
  for workflow in modified_workflows.keys():
    if workflow in db.keys():
      wf_dict = db[workflow]
    else:
      wf_dict = {}
    wf_dict.setdefault(test_class, {}).setdefault(test_name, [])
    wf_dict[test_class][test_name] = modified_workflows[workflow]

    db[workflow] = wf_dict
  db.close()

def rescueTestTransactions(workflow_id=None):
  import os
  import shelve
  folder_path = os.path.dirname(os.path.abspath(__file__))
  db_path = os.path.join(folder_path, 'analyzer.db')

  db_copy = {}
  db = shelve.open(db_path)
  db_copy.update(db)
  db.close()
  if workflow_id and not db_copy.has_key(workflow_id):
    raise KeyError("No tests have used workflow '%s' yet." % workflow_id)
  return workflow_id and db_copy[workflow_id] or db_copy

def patchERP5PortalWorkflow():
  """Redefine several methods of portal_workflow for unit tests
  """
  from Products.DCWorkflow.DCWorkflow import DCWorkflowDefinition
  def patch(function):
    name = function.__name__
    orig_function = getattr(DCWorkflowDefinition, name)
    setattr(DCWorkflowDefinition, '_orig_' + name, orig_function)
    setattr(DCWorkflowDefinition, name, function)
    function.__doc__ = orig_function.__doc__
    # make life easier when inspecting the wrapper with ipython
    function._original = orig_function

  # NOTE: This next 2 lines are VERY IMPORTANT!
  from Products.CMFCore.WorkflowTool import WorkflowTool
  setattr(WorkflowTool, 'analyzer_modified_objects', {})

  @patch
  def _executeTransition(self, ob, tdef=None, kwargs=None):
    # save action
    try:
      modified_objects = getattr(self.getParentNode(), 'analyzer_modified_objects', {})
      # get information
      portal_type = ob.getPortalType()
      workflow_id = self.getId()
      action = tdef and tdef.getId() or self.variables['action'].default_value
      old_state = self._getWorkflowStateOf(ob).getId()
      new_state = tdef and tdef.new_state_id or self.initial_state
      # save information to output
      modified_objects.setdefault(workflow_id, []).append({
        'portal_type': portal_type,
        'action': action,
        'old_state': old_state,
        'new_state': new_state,
      })
      #print modified_objects
    except:
      pass
    self._orig__executeTransition(ob, tdef, kwargs)

def unpatchERP5PortalWorkflow():
  from Products.DCWorkflow.DCWorkflow import DCWorkflowDefinition
  for name in ['_executeTransition']:
    orig_function = getattr(DCWorkflowDefinition, '_orig_' + name)
    delattr(DCWorkflowDefinition, '_orig_' + name)
    setattr(DCWorkflowDefinition, name, orig_function)

  from Products.CMFCore.WorkflowTool import WorkflowTool
  delattr(WorkflowTool, 'analyzer_modified_objects')
