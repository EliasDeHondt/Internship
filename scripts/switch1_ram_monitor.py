############################
# @author Elias De Hondt   #
# @since 07/04/2025        #
############################
# type: ignore[annotation-unchecked]

import math
from json import dumps

Manifest = {
    'Name': 'switch1_ram_monitor',
    'Description': 'This script monitors the RAM utilization of the management module.',
    'Version': '1.0',
    'Tags': ['network', 'traffic'],
    'Author': 'Elias De Hondt'
}

ParameterDefinitions = {
    'medium_term_high_threshold': {
        'Name': 'Average RAM utilization in percentage over a medium period of offence to set Major alert.',
        'Description': 'When average RAM utilization exceeds this value, agent status will be set to Major.',
        'Type': 'integer',
        'Default': 80
    },
    'medium_term_normal_threshold': {
        'Name': 'Average RAM utilization in percentage over a medium period of offence to unset Major alert',
        'Description': 'When average RAM utilization is below this value, Major status will be unset.',
        'Type': 'integer',
        'Default': 60
    },
    'medium_term_time_period': {
        'Name': 'Time interval in minutes to consider average RAM utilization for Medium Term thresholds',
        'Description': 'Time interval to consider average RAM utilization for Medium Term thresholds',
        'Type': 'integer',
        'Default': 120
    }
}

class Agent(NAE):
    def __init__(self):
        url = "{}/rest/v10.11/system?attributes=capabilities".format(HTTP_ADDRESS)
        data = self.get_rest_request_json(url)
        if 'vsf' in data['capabilities']:
            conductor_url = "{}/rest/v10.11/system/vsf_members?attributes=id&filter=role%3Aconductor".format(HTTP_ADDRESS)
            current_conductor = self.get_rest_request_json(conductor_url)
            conductor_id = list(current_conductor.keys())[0]
            mm1_ram_uri = '/rest/v1/system/subsystems/management_module/{}%2F1?attributes=resource_utilization.memory'.format(conductor_id)
        else:
            mgmt_role_url = "{}/rest/v10.11/system/redundant_managements/Mgmt%20Module%201?attributes=mgmt_role".format(HTTP_ADDRESS)
            json_data = self.get_rest_request_json(mgmt_role_url)
            mgmt_role = json_data['mgmt_role']

            if mgmt_role == "Active":
                mm1_ram_uri = '/rest/v1/system/subsystems/management_module/1%2F1?attributes=resource_utilization.memory'
            else:
                mm1_ram_uri = '/rest/v1/system/subsystems/management_module/1%2F2?attributes=resource_utilization.memory'

        self.mm1_ram_mon = Monitor(mm1_ram_uri, 'RAM raw (RAM utilization in %)', [])

        medium_term_time_period = str(self.params['medium_term_time_period'].value) + ' minutes'

        self.r1 = Rule('Medium-Term High RAM')
        mm1_medium_term_ram_uri = AverageOverTime(mm1_ram_uri, medium_term_time_period, [])
        self.mm1_medium_term_ram_mon = Monitor(mm1_medium_term_ram_uri, 'Medium-Term RAM (RAM utilization in %)')
        self.r1.condition('{} > {}', [self.mm1_medium_term_ram_mon, self.params['medium_term_high_threshold']])
        self.r1.action(self.action_major_ram)

        self.r2 = Rule('Medium-Term Normal RAM')
        self.r2.condition('{} < {}', [self.mm1_medium_term_ram_mon, self.params['medium_term_normal_threshold']])
        self.r2.action(self.action_ram_normal_major)

        self.variables['ram_major'] = '0'
        self.variables['ram_status'] = '0'
        self.variables['overall_status'] = '0'

    def parse_utilization(self, event, method):
        rule_name = event['rule_description']
        utilization = str(method(float(event['value'])))
        subsystem = event['labels'].split(',')[0].split('=')[1]
        return rule_name, subsystem, utilization

    def action_major_ram(self, event):
        self.variables['ram_major'] = '1'
        ram_status = int(self.variables['ram_status'])
        overall_status = int(self.variables['overall_status'])
        if ram_status < 2 and overall_status <= 2:
            self.variables['ram_status'] = '2'
            self.action_ram(event, self.params['medium_term_high_threshold'], self.params['medium_term_time_period'])
            self.set_agent_alert_level()

    def action_ram(self, event, threshold, time_period):
        rule_name, subsystem, utilization = self.parse_utilization(event, math.ceil)
        mgmt_module = self.get_mgmt_module(event['labels'])
        trap_message = '{}. Subsystem {}. RAM utilization {}%.'.format(rule_name, subsystem, utilization)
        ActionSNMP(trap_message)
        ActionSyslog('Average ' + mgmt_module + ' RAM utilization over last {} minute(s): [' + utilization + '], exceeded threshold: [{}]', [time_period, threshold], severity=SYSLOG_WARNING)
        ActionCLI('show system resource-utilization')

    def action_ram_normal_major(self, event):
        self.variables['ram_major'] = '0'
        ram_status = int(self.variables['ram_status'])
        if ram_status == 2:
            self.variables['ram_status'] = '0'
            self.action_ram_normal(event, self.params['medium_term_normal_threshold'], self.params['medium_term_time_period'])
            self.set_agent_alert_level()

    def action_ram_normal(self, event, threshold, time_period):
        rule_name, subsystem, utilization = self.parse_utilization(event, math.floor)
        trap_message = '{}. Subsystem {}. RAM utilization {}%.'.format(rule_name, subsystem, utilization)
        ActionSNMP(trap_message)
        mgmt_module = self.get_mgmt_module(event['labels'])
        ActionSyslog('Average ' + mgmt_module + ' RAM utilization over last {} minute(s): [' + utilization + '], is below normal threshold: [{}]', [time_period, threshold], severity=SYSLOG_WARNING)

    def set_agent_alert_level(self):
        ram_status = int(self.variables['ram_status'])
        overall_status = ram_status
        self.variables['overall_status'] = str(overall_status)
        alert_actions = {
            3: lambda: self.set_alert_level(AlertLevel.CRITICAL),
            2: lambda: self.set_alert_level(AlertLevel.MAJOR),
            1: lambda: self.set_alert_level(AlertLevel.MINOR)
        }

        alert_actions.get(overall_status, lambda: self.remove_alert_level() if self.get_alert_level is not None else None)()

    def get_mgmt_module(self, event_label):
        _, mgmt_module = event_label.split(',')[0].split('=')
        return 'MM1' if mgmt_module == 'management_module_1/1' else 'MM2'