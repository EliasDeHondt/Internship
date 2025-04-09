############################
# @author Elias De Hondt   #
# @since 01/01/2025        #
############################
# type: ignore[annotation-unchecked]

import math
from json import dumps

Manifest = {
    'Name': 'switch1_resource_monitor',
    'Description': 'This script monitors the CPU and memory utilization of the management module.',
    'Version': '1.0',
    'Tags': ['network', 'traffic'],
    'Author': 'Elias De Hondt'
}

ParameterDefinitions = {
    'short_term_high_threshold': {
        'Name': 'Average CPU/Memory utilization in percentage in a short period of offence to set Minor alert',
        'Description': 'Deprecated: when average CPU/Memory utilization exceeds this value, agent status will be set to Minor and agent will log all system daemons CPU/Memory utilization details with CoPP statistics',
        'Type': 'integer',
        'Default': 90
    },
    'short_term_normal_threshold': {
        'Name': 'Average CPU/Memory utilization in percentage in a short period of offence to unset Minor alert',
        'Description': 'Deprecated: when average CPU/Memory utilization is below this value, Minor status will be unset.',
        'Type': 'integer',
        'Default': 80
    },
    'short_term_time_period': {
        'Name': 'Time interval in minutes to consider average CPU/Memory utilization for Short Term thresholds',
        'Description': 'Deprecated: time interval to consider average CPU/Memory utilization for Short Term thresholds',
        'Type': 'integer',
        'Default': 5
    },
    'medium_term_high_threshold': {
        'Name': 'Average CPU/Memory utilization in percentage over a medium period of offence to set Major alert.',
        'Description': 'When average CPU/Memory utilization exceeds this value, agent status will be set to Major and agent will log all system daemons CPU/Memory utilization details with CoPP statistics.',
        'Type': 'integer',
        'Default': 80
    },
    'medium_term_normal_threshold': {
        'Name': 'Average CPU/Memory utilization in percentage over a medium period of offence to unset Major alert',
        'Description': 'When average CPU/Memory utilization is below this vlaue, Major status will be unset.',
        'Type': 'integer',
        'Default': 60
    },
    'medium_term_time_period': {
        'Name': 'Time interval in minutes to consider average CPU/Memory utilization for Medium Term thresholds',
        'Description': 'Time interval to consider average CPU/Memory utilization for Medium Term thresholds',
        'Type': 'integer',
        'Default': 120
    },
    'long_term_high_threshold': {
        'Name': 'Average CPU/Memory utilization in percentage for a sustained long period of offence to set Critical alert',
        'Description': 'Deprecated: when average CPU/Memory utilization exceeds this value, agent status will be set to Critical and agent will log all system daemons CPU/Memory utilization details with CoPP statistics.',
        'Type': 'integer',
        'Default': 70
    },
    'long_term_normal_threshold': {
        'Name': 'Average CPU/Memory utilization in percentage for a sustained long period of offence to unset Critical alert',
        'Description': 'Deprecated: when average CPU/Memory utilization is below this value, Critical status will be unset.',
        'Type': 'integer',
        'Default': 60
    },
    'long_term_time_period': {
        'Name': 'Time interval in minutes to consider average CPU/Memory utilization for Long Term thresholds',
        'Description': 'Deprecated: time interval to consider average CPU/Memory utilization for Long Term thresholds',
        'Type': 'integer',
        'Default': 480
    }
}

class Agent(NAE):
    def __init__(self):
        url = "{}/rest/v10.11/system?attributes=capabilities".format(
            HTTP_ADDRESS)
        data = self.get_rest_request_json(url)
        if 'vsf' in data['capabilities']:
            conductor_url = "{}/rest/v10.11/system/vsf_members?attributes=id&filter=role%3Aconductor".format(HTTP_ADDRESS)
            current_conductor = self.get_rest_request_json(conductor_url)
            conductor_id = list(current_conductor.keys())[0]
            param_list = []
            mm1_cpu_uri = '/rest/v1/system/subsystems/management_module/{}%2F1?attributes=resource_utilization.cpu'.format(conductor_id)
            mm1_mem_uri = '/rest/v1/system/subsystems/management_module/{}%2F1?attributes=resource_utilization.memory'.format(conductor_id)
        else:
            param_list = []
            mgmt_role_url = "{}/rest/v10.11/system/redundant_managements/Mgmt%20Module%201?attributes=mgmt_role".format(HTTP_ADDRESS)
            json_data = self.get_rest_request_json(mgmt_role_url)
            mgmt_role = json_data['mgmt_role']

            if mgmt_role == "Active":
                mm1_cpu_uri = '/rest/v1/system/subsystems/management_module/1%2F1?attributes=resource_utilization.cpu'
                mm1_mem_uri = '/rest/v1/system/subsystems/management_module/1%2F1?attributes=resource_utilization.memory'
            else:
                mm1_cpu_uri = '/rest/v1/system/subsystems/management_module/1%2F2?attributes=resource_utilization.cpu'
                mm1_mem_uri = '/rest/v1/system/subsystems/management_module/1%2F2?attributes=resource_utilization.memory'

        self.mm1_cpu_mon = Monitor(mm1_cpu_uri, 'CPU raw (CPU/Memory utilization in %)', param_list)

        medium_term_time_period = str(self.params['medium_term_time_period'].value) + ' minutes'

        self.r1 = Rule('Medium-Term High CPU')
        mm1_medium_term_cpu_uri = AverageOverTime(mm1_cpu_uri, medium_term_time_period, param_list)
        self.mm1_medium_term_cpu_mon = Monitor(mm1_medium_term_cpu_uri, 'Medium-Term CPU (CPU/Memory utilization in %)')
        self.r1.condition('{} > {}', [self.mm1_medium_term_cpu_mon, self.params['medium_term_high_threshold']])
        self.r1.action(self.action_major_cpu)

        self.r2 = Rule('Medium-Term Normal CPU')
        self.r2.condition('{} < {}', [self.mm1_medium_term_cpu_mon, self.params['medium_term_normal_threshold']])
        self.r2.action(self.action_cpu_normal_major)

        self.mm1_mem_mon = Monitor(mm1_mem_uri, 'Memory raw (CPU/Memory utilization in %)', param_list)

        self.r3 = Rule('Medium-Term High Memory')
        mm1_medium_term_mem_uri = AverageOverTime(mm1_mem_uri, medium_term_time_period, param_list)
        self.mm1_medium_term_mem_mon = Monitor(mm1_medium_term_mem_uri, 'Medium-Term Memory (CPU/Memory utilization in %)')
        self.r3.condition('{} > {}', [self.mm1_medium_term_mem_mon, self.params['medium_term_high_threshold']])
        self.r3.action(self.action_major_memory)

        self.r4 = Rule('Medium-Term Normal Memory')
        self.r4.condition('{} < {}', [self.mm1_medium_term_mem_mon, self.params['medium_term_normal_threshold']])
        self.r4.action(self.action_memory_normal_major)

        self.variables['cpu_minor'] = '0'
        self.variables['cpu_major'] = '0'
        self.variables['cpu_critical'] = '0'
        self.variables['memory_minor'] = '0'
        self.variables['memory_major'] = '0'
        self.variables['memory_critical'] = '0'
        self.variables['cpu_status'] = '0'
        self.variables['memory_status'] = '0'
        self.variables['overall_status'] = '0'

    def parse_utilization(self, event, method):
        rule_name = event['rule_description']
        utilization = str(method(float(event['value'])))
        subsystem = event['labels'].split(',')[0].split('=')[1]
        return rule_name, subsystem, utilization

    def action_major_cpu(self, event):
        self.variables['cpu_major'] = '1'
        cpu_status = int(self.variables['cpu_status'])
        overall_status = int(self.variables['overall_status'])
        if cpu_status < 2 and overall_status <= 2:
            self.variables['cpu_status'] = '2'
            self.action_cpu(event, self.params['medium_term_high_threshold'], self.params['medium_term_time_period'])
            self.set_agent_alert_level()

    def action_cpu(self, event, threshold, time_period):
        rule_name, subsystem, utilization = self.parse_utilization(event, math.ceil)
        mgmt_module = self.get_mgmt_module(event['labels'])
        trap_message = '{}. Subsystem {}. CPU utilization {}%.'.format(rule_name, subsystem, utilization)
        ActionSNMP(trap_message)
        ActionSyslog('Average ' + mgmt_module + ' CPU utilization over ' + 'last {} minute(s): [' + utilization + '], exceeded threshold: [{}]', [time_period, threshold], severity=SYSLOG_WARNING)
        ActionCLI('top cpu display-limit 30')
        ActionCLI('show system resource-utilization')
        ActionCLI('show copp-policy statistics')

    def action_cpu_normal_major(self, event):
        self.variables['cpu_major'] = '0'
        cpu_status = int(self.variables['cpu_status'])
        if cpu_status == 2:
            self.variables['cpu_status'] = '0'
            cpu_minor = int(self.variables['cpu_minor'])
            if cpu_minor:
                self.variables['cpu_status'] = '1'
            self.action_cpu_normal(event, self.params['medium_term_normal_threshold'], self.params['medium_term_time_period'])
            self.set_agent_alert_level()

    def action_cpu_normal(self, event, threshold, time_period):
        rule_name, subsystem, utilization = self.parse_utilization(event, math.floor)
        trap_message = '{}. Subsystem {}. CPU utilization {}%.'.format(rule_name, subsystem, utilization)
        ActionSNMP(trap_message)
        mgmt_module = self.get_mgmt_module(event['labels'])
        ActionSyslog('Average ' + mgmt_module + ' CPU utilization over ' + 'last {} minute(s): [' + utilization + '], is below normal threshold: [{}]', [time_period, threshold], severity=SYSLOG_WARNING)

    def set_agent_alert_level(self):
        cpu_status = int(self.variables['cpu_status'])
        memory_status = int(self.variables['memory_status'])
        overall_status = 0
        if cpu_status > memory_status:
            overall_status = cpu_status
        else:
            overall_status = memory_status
        self.variables['overall_status'] = str(overall_status)
        alert_actions = {
            3: lambda: self.set_alert_level(AlertLevel.CRITICAL),
            2: lambda: self.set_alert_level(AlertLevel.MAJOR),
            1: lambda: self.set_alert_level(AlertLevel.MINOR)
        }

        alert_actions.get(overall_status, lambda: self.remove_alert_level() if self.get_alert_level is not None else None)()

    def action_major_memory(self, event):
        self.variables['memory_major'] = '1'
        memory_status = int(self.variables['memory_status'])
        overall_status = int(self.variables['overall_status'])
        if memory_status < 2 and overall_status <= 2:
            self.variables['memory_status'] = '2'
            self.action_memory(event, self.params['medium_term_high_threshold'], self.params['medium_term_time_period'])
            self.set_agent_alert_level()

    def action_memory(self, event, threshold, time_period):
        rule_name, subsystem, utilization = self.parse_utilization(event, math.ceil)
        mgmt_module = self.get_mgmt_module(event['labels'])
        trap_message = '{}. Subsystem {}. Memory utilization {}%.'.format(rule_name, subsystem, utilization)
        ActionSNMP(trap_message)
        ActionSyslog('Average ' + mgmt_module + ' Memory utilization over last ' + '{} minute(s): [' + utilization + '], exceeded threshold: [{}]', [time_period, threshold], severity=SYSLOG_WARNING)
        ActionCLI('top memory display-limit 30')
        ActionCLI('show system resource-utilization')
        ActionCLI('show copp-policy statistics')

    def action_memory_normal_major(self, event):
        self.variables['memory_major'] = '0'
        memory_status = int(self.variables['memory_status'])
        if memory_status == 2:
            self.variables['memory_status'] = '0'
            memory_minor = int(self.variables['memory_minor'])
            if memory_minor:
                self.variables['memory_status'] = '1'
            self.action_memory_normal(event, self.params['medium_term_normal_threshold'], self.params['medium_term_time_period'])
            self.set_agent_alert_level()

    def action_memory_normal(self, event, threshold, time_period):
        rule_name, subsystem, utilization = self.parse_utilization(event, math.floor)
        mgmt_module = self.get_mgmt_module(event['labels'])
        trap_message = '{}. Subsystem {}. Memory utilization {}%.'.format(rule_name, subsystem, utilization)
        ActionSNMP(trap_message)
        ActionSyslog('Average ' + mgmt_module + 'Memory utilization over last {} ' + 'minute(s): [' + utilization + '], is below normal threshold: [{}]', [time_period, threshold], severity=SYSLOG_WARNING)

    def get_mgmt_module(self, event_label):
        _, mgmt_module = event_label.split(',')[0].split('=')
        ret_mgmt_module = ''
        if mgmt_module == 'management_module_1/1':
            ret_mgmt_module = 'MM1'
        else:
            ret_mgmt_module = 'MM2'
        return ret_mgmt_module