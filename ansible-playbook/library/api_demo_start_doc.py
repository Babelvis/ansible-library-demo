#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Ansible module that has only documentation."""

# Bas Magré <bas.magre@babelvis.nl>
# The MIT License (MIT) (see https://opensource.org/license/mit)

# See documentation:
# - https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html
# - https://docs.ansible.com/ansible/latest/dev_guide/developing_locally.html
# - https://docs.ansible.com/ansible/latest/dev_guide/developing_program_flow_modules.html
# - https://github.com/ansible-collections/community.general/tree/main/plugins/modules
# - https://docs.ansible.com/ansible/latest/collections_guide/collections_installing.html

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = r'''
---
module: api_demo
author:
    - Bas Magré (@opvolger)
short_description: The ability to create, remove and manage a list of characters that have numbers
version_added: 0.0.1
description: "The ability to create, remove and manage a list of characters that have numbers. This is just a demo!"

options:
    endpoint:
        description: The uri of the API
        type: str
        required: true
        sample: 'http://localhost:5041/'
    username:
        description: Username to get a token
        type: str
        required: false
        sample: 'user'
    password:
        description: Password to get a token
        type: str
        required: false
        sample: 'password'
    token:
        description: Use a token direct (without username/password)
        type: str
        required: false
        sample: 'secret'
    character:
        description: Character (key)
        type: str
        required: false
        sample: 'A'
    number:
        description: Number (value)
        type: int
        required: false
        sample: 5
    action:
        description: The action to perform
        type: str
        required: true
        default: get
        choices: [ get, set, clear ]
        sample: 'set'
'''

EXAMPLES = r'''
- name: Clear all set character and numbers with a token
  api_demo:
    endpoint: http://localhost:5041/
    token: secret
    action: clear
  delegate_to: localhost

- name: Set number on a character with username and password
  api_demo:
    endpoint: http://localhost:5041/
    username: user
    password: password
    character: "A"
    number: 4
    action: set
  delegate_to: localhost

- name: Get number from set character with a token
  api_demo:
    endpoint: http://localhost:5041/
    token: secret
    character: "A"
    action: get
  delegate_to: localhost
'''

RETURN = r'''
exists:
    description: if the character is set
    returned: success
    type: bool
    sample: True
number:
    description: The number that is set or get
    type: int
    sample: 5
'''

def run_module() -> None:
    """The Ansible module."""

    # define the available arguments/parameters that a user can pass to the module
    module_args = {
        'endpoint': {'type': 'str', 'required': True},
        'username': {'type': 'str', 'required': False},
        'password': {'type': 'str', 'required': False, 'no_log': True},
        'token': {'type': 'str', 'required': False, 'no_log': True},
        'character': {'type': 'str', 'required': False},
        'number': {'type': 'int', 'required': False},
        'action': {'type': 'str', 'required': True, 'choices': ['get', 'set', 'clear']}
    }

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = {
        'changed': False,
        'rc': 1,
        'stdout': None,
        'stderr': None
    }

    result['rc'] = 0  # we are at the end, no errors occurred
    module.exit_json(**result)

def main() -> None:
    """Main function to run Ansible Module."""
    run_module()

if __name__ == '__main__':
    main()
