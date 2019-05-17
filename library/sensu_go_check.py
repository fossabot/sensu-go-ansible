#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Jared Ledvina <jaredledvina@gmail.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
author:
  - "Jared Ledvina (@jaredledvina)"
description:
  - "Create/Delete Sensu Go checks"
module: sensu_go_check
options:
  check_hooks:
    description:
      - "An array of check response types with respective arrays of Sensu hook names."
      - "Sensu hooks are commands run by the Sensu agent in response to the result of the check command execution."
      - "Hooks are executed, in order of precedence, based on their severity type 1 to 255, ok, warning, critical, unknown, and finally non-zero."
    type: list
  command:
    description:
      - "The check command to be executed."
    type: str
  cron:
    description:
      - "When the check should be executed, using cron syntax or these predefined schedules."
      - Required if interval is not set.
    type: str
  env_vars:
    description:
      - "An array of environment variables to use with command execution."
    type: list
  handlers:
    description:
      - "An array of Sensu event handlers (names) to use for events created by the check."
    type: list
  high_flap_threshold:
    description:
      - "The flap detection high threshold (% state change) for the check. Sensu uses the same flap detection algorithm as Nagios."
    type: int
  host:
    description:
      - "The host to query, needs to be running the sensu-backend for API access."
      - "Required if environmental variable C(ANSIBLE_SENSU_GO_HOST) is not set."
    required: true
    type: str
  http_agent:
    default: ansible-httpget
    description:
      - "The user agent to configure when accessing the Sensu Go API."
  interval:
    description:
      - "How often the check is executed, in seconds."
      - Required if cron is not set.
    type: int
  low_flap_threshold:
    description:
      - "The flap detection low threshold (% state change) for the check. Sensu uses the same flap detection algorithm as Nagios."
    type: int
  name:
    description:
      - "A unique string used to identify the check."
      - 'Check names cannot contain special characters or spaces (validated with Go regex \A[\w\.\-]+\z).'
      - "Each check must have a unique name within its namespace."
    required: true
    type: str
  namespace:
    default: default
    description:
      - "The Sensu RBAC namespace that this check belongs to."
    type: str
  output_metric_format:
    choices:
      - ''
      - nagios_perfdata
      - graphite_plaintext
      - influxdb_line
      - opentsdb_line
    description:
      - "The metric format generated by the check command."
    type: str
  output_metric_handlers:
    description:
      - "An array of Sensu handlers to use for events created by the check."
      - "Each array item must be a string."
      - "output_metric_handlers should be used in place of the handlers attribute if output_metric_format is configured."
    type: list
  password:
    aliases:
      - url_password
    default: P@ssword!
    description:
      - "Password to use when initially authenticating to the Sensu Go API."
      - "Can be overriden with the environmental variable C(ANSIBLE_SENSU_GO_PASSWORD)"
    type: str
  port:
    default: 8080
    description:
      - "The port that the Sensu Go API is listening on."
      - "Can be overriden with the environmental variable C(ANSIBLE_SENSU_GO_PORT)"
    type: int
  protocol:
    choices:
      - http
      - https
    default: http
    description:
      - "The protocol to use when accessing the Sensu Go API."
      - "Can be overriden with the environmental variable C(ANSIBLE_SENSU_GO_PROTOCOL)"
    type: str
  proxy_entity_name:
    description:
      - "The entity name, used to create a proxy entity for an external resource (i.e., a network switch)."
      - 'Must match the regex \A[\w\.\-]+\z'
    type: str
  proxy_requests:
    description:
      - "Sensu proxy request attributes allow you to assign the check to run for multiple entities according to their entity_attributes."
    type: dict
  publish:
    description:
      - "If check requests are published for the check."
    type: bool
    default: True
  round_robin:
    description:
      - "When set to true, Sensu executes the check once per interval, cycling through each subscribing agent in turn."
    type: bool
  runtime_assets:
    description:
      - "An array of Sensu assets (names), required at runtime for the execution of the command."
    type: list
  state:
    choices:
      - present
      - absent
    default: present
    description:
      - "Whether we are ensuring the check exists or is removed from Sensu Go."
    type: str
  stdin:
    description:
      - "If the Sensu agent writes JSON serialized Sensu entity and check data to the command process STDIN."
      - "The command must expect the JSON data via STDIN, read it, and close STDIN."
    type: bool
  subdue:
    description:
      - "Check subdues are not yet implemented in Sensu Go."
      - "Although the subdue attribute appears in check definitions by default, it is a placeholder and should not be modified."
      - "It is included here for future compatibility."
    type: bool
  subscriptions:
    description:
      - "An array of Sensu entity subscriptions that check requests will be sent to."
      - "The array cannot be empty and its items must each be a string."
    type: list
  timeout:
    description:
      - "The check execution duration timeout in seconds (hard stop)."
    type: int
  ttl:
    description:
      - "The time to live (TTL) in seconds until check results are considered stale."
      - "If an agent stops publishing results for the check, and the TTL expires, an event will be created for the agents entity."
      - "The check ttl must be greater than the check interval, and should accommodate time for the check execution and result processing to complete."
    type: int
  use_proxy:
    default: "yes"
    description:
      - "Configures Ansible to use or ignore an http_proxy."
    type: bool
  username:
    aliases:
      - url_username
    default: admin
    description:
      - "Username to use when initially authenticating to the Sensu Go API."
      - "Can be overriden with the environment variable C(ANSIBLE_SENSU_GO_USERNAME)"
    type: str
  validate_certs:
    default: "yes"
    description:
      - "Whether or not Ansible should validate Sensu Go's certs."
    type: bool
short_description: "Manage Sensu Go checks"
version_added: "2.8"
'''

EXAMPLES = r'''
- name: Create a new check
  sensu_go_check:
    state: present
    host: sensu.example.com
    port: 8080
    user: admin
    password: P@ssw0rd!
    namespace: default
    name: check_example
    interval: 60

- name: Delete an existing check
  sensu_go_check:
    state: absent
    host: sensu.example.com
    port: 8080
    user: admin
    password: P@ssw0rd!
    namespace: default
    name: check_example
    interval: 60
'''

RETURN = r'''
message:
    description: Humanized description of the changes performed
    type: str
    returned: always
    sample: Updated existing Sensu Go check check_example
check_definition:
    description: The final check definition generated from the module inputs
    type: dict
    returned: always
    sample: |
      "check_definition": {
        "interval": 120,
        "command": "systemctl is-system-running",
        "metadata": {
          "namespace": "default",
          "name": "check_failed_units"
        },
        "subscriptions": [
          "all"
        ]
      }
diff:
    description: A dict before & after, with the attributes and vaules changed.
    returned: When a check has been modified
    type: dict
    sample: |
        "diff": {
            "after": {"interval": 120}
            "before": {"interval": 60}
           }
         }
'''

import json

from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible.module_utils.urls import fetch_url, url_argument_spec
from ansible.module_utils._text import to_native
from ansible.module_utils.sensu_go import SensuGo, recursive_diff


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = url_argument_spec()
    # Sensu Go doesn't support client cert/key auth to the API nor will it let
    # basic auth work outside of the initial auth flow, disable them.
    for argument in ['client_cert', 'client_key', 'force_basic_auth', 'force']:
        del module_args[argument]
    module_args.update(dict(state=dict(type='str', default='present', choices=['present', 'absent'])))
    sensu_go_check_spec = dict(
        check_hooks=dict(type='list', elements='str'),
        command=dict(type='str'),
        cron=dict(type='str'),
        env_vars=dict(type='list', elements='str'),
        handlers=dict(type='list', elements='str', default=[]),
        high_flap_threshold=dict(type='int', default=0),
        interval=dict(type='int'),
        low_flap_threshold=dict(type='int', default=0),
        metadata=dict(
            type='dict',
            elements='dict',
            options=dict(
                annotations=dict(type='dict', elements='str'),
                labels=dict(type='dict', elements='str')
            )
        ),
        output_metric_format=dict(type='str', default='', choices=['', 'nagios_perfdata', 'graphite_plaintext', 'influxdb_line', 'opentsdb_line']),
        output_metric_handlers=dict(type='list', elements='str'),
        proxy_entity_name=dict(type='str', default=''),
        proxy_requests=dict(
            type='dict',
            elements='dict',
            options=dict(
                entity_attributes=dict(type='list', elements='tr'),
                splay=dict(type='bool', default=False),
                splay_coverage=dict(type='int')
            )
        ),
        publish=dict(type='bool', default=True),
        round_robin=dict(type='bool', default=False),
        runtime_assets=dict(type='list', elements='str'),
        stdin=dict(type='bool', default=False),
        subdue=dict(type='bool'),
        subscriptions=dict(type='list', elements='str', default=[]),
        timeout=dict(type='int', default=0),
        ttl=dict(type='int', default=0),
    )
    module_args.update(sensu_go_check_spec)
    required_if = [
        ('state', 'present', ['command', 'subscriptions']),
        ('state', 'present', ['interval', 'cron'], True)
    ]
    mutually_exclusive = [['interval', 'cron']]

    result = dict(
        changed=False,
        message='',
    )

    module = SensuGo(
        argument_spec=module_args,
        attributes=sorted(sensu_go_check_spec.keys()),
        resource='checks',
        supports_check_mode=True,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive
    )
    module.auth()
    if module.params['state'] == 'present':
        response, info = module.get_resource()
        check_def = module.create_check_definition()
        result['check_definition'] = check_def
        if info['status'] == 404:
            if module.check_mode:
                result['message'] = 'Would have created new Sensu Go check: {0}'.format(module.params['name'])
                result['changed'] = True
            else:
                module.post_resource(check_def)
                result['changed'] = True
                result['message'] = 'Created new Sensu Go check: {0}'.format(module.params['name'])
        elif info['status'] == 200:
            for attribute in check_def.keys():
                # We've configured the default value for the module
                if check_def[attribute] is None:
                    # The API hasn't returned this attribute
                    if attribute not in response:
                        # TODO: This logic is shitty, figure out a way to drop it
                        # Remove it, this prevents diffs from showing attributes
                        # that the module has but, that the checks api doesn't
                        # return unless set. Currently, that's interval/cron
                        # (depending on which is set in the check), and proxy_requests.
                        check_def.pop(attribute)
            difference = recursive_diff(response, check_def)
            if difference:
                result['diff'] = {'before': '', 'after': ''}
                result['diff']['before'] = difference[0]
                result['diff']['after'] = difference[1]
                if module.check_mode:
                    result['message'] = 'Would have updated Sensu Go check: {0}'.format(module.params['name'])
                    result['changed'] = True
                else:
                    response, info = module.put_resource(check_def)
                    result['message'] = 'Updated existing Sensu Go check: {0}'.format(module.params['name'])
                    result['changed'] = True
            else:
                result['message'] = 'Sensu Go check already exists and doesn\'t need to be updated: {0}'.format(module.params['name'])
    elif module.params['state'] == 'absent':
        response, info = module.get_resource()
        if info['status'] == 404:
            result['message'] = 'Sensu Go check does not exist: {0}'.format(module.params['name'])
        elif info['status'] == 200:
            if module.check_mode:
                result['message'] = 'Would have deleted Sensu Go check: {0}'.format(module.params['name'])
                result['changed'] = True
            else:
                reponse, info = module.delete_resource()
                result['message'] = 'Deleted Sensu Go check: {0}'.format(module.params['name'])
                result['changed'] = True
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
