#!/usr/bin/python
# -*- coding: utf-8 -*-

# Bas Magré <bas.magre@babelvis.nl>
# The MIT License (MIT) (see https://opensource.org/license/mit)

# See documentation:
# - https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html
# - https://docs.ansible.com/ansible/latest/dev_guide/developing_locally.html
# - https://docs.ansible.com/ansible/latest/dev_guide/developing_program_flow_modules.html
# - https://github.com/ansible-collections/community.general/tree/main/plugins/modules
# - https://docs.ansible.com/ansible/latest/collections_guide/collections_installing.html

import re
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

def run_module():
    # define the available arguments/parameters that a user can pass to the module
    module_args = dict(
        endpoint=dict(type='str', required=True),
        username=dict(type='str', required=False),
        password=dict(type='str', required=False, no_log=True),
        token=dict(type='str', required=False, no_log=True),
        character=dict(type='str', required=False),
        number=dict(type='int', required=False),
        action=dict(type='str', required=True, choices=['get', 'set', 'clear'])
    )

    # use username with password
    check_required_together = [
        ('username', 'password')
    ]

    # use username/password or token is needed
    check_required_one_of = [ ('username', 'token')]

    # use username/password or token, only one
    check_mutually_exclusive = [ ('username', 'token')]

    # if action == get, we need the character argument
    # if action == set, we need the character and number arguments
    check_required_if = [
         ('action', 'get', ['character']),
         ('action', 'set', ['character','number'])
    ]

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=check_required_if,
        required_together=check_required_together,
        required_one_of=check_required_one_of,
        mutually_exclusive=check_mutually_exclusive
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        rc=1,
        stdout=None,
        stderr=None
    )

    character = module.params['character']
    number = module.params['number']
    action = module.params['action']

    # input checks
    if character != None and not (re.fullmatch(r"[A-Z]", character)):
        module.fail_json(msg=f'character: "{character}" must be an alpha letter and in upper case', **result)
    if number != None and not (1 <= number <= 255):
        module.fail_json(msg='number must be between 1 and 255', **result)

    # actions
    if action == 'get':
        result['number'] = 4
        result['exists'] = True
    elif action == 'set':
        result['changed'] = True
        result['number'] = number
        result['exists'] = True
    elif action == 'clear':
        result['changed'] = True
        result['exists'] = False

    result['rc'] = 0  # we are at the end, no errors occurred
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
