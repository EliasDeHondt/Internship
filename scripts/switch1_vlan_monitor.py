############################
# @author Elias De Hondt   #
# @since 07/04/2025        #
############################

from json import dumps
from aruba.nae import NAE, Monitor, Rule, ActionSyslog, ActionSNMP, ActionCLI, AlertLevel

Manifest = {
    'Name': 'switch1_vlan_monitor',
    'Description': 'Monitors all VLANs on the switch, including configuration and traffic statistics',
    'Version': '1.0',
    'Tags': ['vlan', 'network', 'traffic'],
    'Author': 'Elias De Hondt'
}

class Agent(NAE):
    def __init__(self):
        vlan_count_uri = '/rest/v1/system/vlans?attributes=count'
        self.vlan_count_mon = Monitor(vlan_count_uri, 'Total VLAN Count')

        self.r1 = Rule('High VLAN Count')
        self.r1.condition('{} > {}', [self.vlan_count_mon, self.params['vlan_count_high_threshold']])
        self.r1.action(self.action_high_vlan_count)

        self.vlan_traffic_monitors = {}
        self.vlan_names = {}
        self.update_vlan_list()

        self.variables['vlan_count_status'] = '0'
        self.variables['traffic_status'] = {}

    def update_vlan_list(self):
        vlan_list_uri = '/rest/v1/system/vlans'
        vlan_data = self.get_rest_request_json(vlan_list_uri)
        vlan_ids = [int(vlan_id.split('/')[-1]) for vlan_id in vlan_data.keys() if vlan_id.startswith('/system/vlans/')]

        traffic_time_period = str(self.params['traffic_time_period'].value) + ' minutes'

        for vlan_id in vlan_ids:
            if vlan_id not in self.vlan_traffic_monitors:
                # Store VLAN name
                vlan_info_uri = f'/rest/v1/system/vlans/{vlan_id}?attributes=name'
                vlan_info = self.get_rest_request_json(vlan_info_uri)
                self.vlan_names[vlan_id] = vlan_info.get('name', f'VLAN {vlan_id}')

                # Traffic monitor (bytes in + out)
                traffic_uri = f'/rest/v1/system/vlans/{vlan_id}?attributes=statistics.bytes_in,statistics.bytes_out'
                avg_traffic_uri = AverageOverTime(
                    lambda x: x['statistics.bytes_in'] + x['statistics.bytes_out'],
                    traffic_time_period,
                    traffic_uri
                )
                self.vlan_traffic_monitors[vlan_id] = Monitor(
                    avg_traffic_uri,
                    f'{self.vlan_names[vlan_id]} Traffic (bytes/sec)'
                )

                # Rules for traffic
                r_high = Rule(f'High Traffic {self.vlan_names[vlan_id]}')
                r_high.condition('{} > {}', [self.vlan_traffic_monitors[vlan_id], self.params['traffic_high_threshold']])
                r_high.action(self.action_high_traffic, vlan_id=vlan_id)

                r_normal = Rule(f'Normal Traffic {self.vlan_names[vlan_id]}')
                r_normal.condition('{} <= {}', [self.vlan_traffic_monitors[vlan_id], self.params['traffic_high_threshold']])
                r_normal.action(self.action_normal_traffic, vlan_id=vlan_id)

                # Initialize traffic status
                self.variables['traffic_status'][str(vlan_id)] = '0'  # 0=Normal, 1=Major

    def on_monitor_update(self, mon):
        # Re-check VLAN list periodically in case new VLANs are added
        if mon == self.vlan_count_mon:
            self.update_vlan_list()

    def action_high_vlan_count(self, event):
        vlan_count = int(event['value'])
        self.variables['vlan_count_status'] = '1'
        ActionSyslog(
            'Total VLAN count [{}] exceeded threshold [{}]', 
            [vlan_count, self.params['vlan_count_high_threshold']], 
            severity=SYSLOG_CRITICAL
        )
        ActionSNMP(f'High VLAN count detected: {vlan_count}')
        ActionCLI('show vlan')
        self.update_alert_level()

    def action_high_traffic(self, event, vlan_id):
        traffic = int(event['value'])
        vlan_name = self.vlan_names[vlan_id]
        self.variables['traffic_status'][str(vlan_id)] = '1'
        ActionSyslog(
            f'{vlan_name} traffic [{traffic} bytes/sec] exceeded threshold [{self.params["traffic_high_threshold"]}] over last {self.params["traffic_time_period"]} minute(s)', 
            severity=SYSLOG_WARNING
        )
        ActionSNMP(f'High traffic on {vlan_name}: {traffic} bytes/sec')
        ActionCLI(f'show vlan {vlan_id}')
        ActionCLI('show interface vlan all')
        self.update_alert_level()

    def action_normal_traffic(self, event, vlan_id):
        traffic = int(event['value'])
        vlan_name = self.vlan_names[vlan_id]
        if self.variables['traffic_status'][str(vlan_id)] != '0':
            self.variables['traffic_status'][str(vlan_id)] = '0'
            ActionSyslog(
                f'{vlan_name} traffic [{traffic} bytes/sec] is below threshold [{self.params["traffic_high_threshold"]}]', 
                severity=SYSLOG_INFO
            )
            ActionSNMP(f'Traffic normalized on {vlan_name}: {traffic} bytes/sec')
            self.update_alert_level()

    def update_alert_level(self):
        vlan_count_status = int(self.variables['vlan_count_status'])
        traffic_status_max = max([int(status) for status in self.variables['traffic_status'].values()])
        overall_status = max(vlan_count_status, traffic_status_max)

        if overall_status == 1 and vlan_count_status == 1:
            self.set_alert_level(AlertLevel.CRITICAL)
        elif overall_status == 1 and traffic_status_max == 1:
            self.set_alert_level(AlertLevel.MAJOR)
        elif self.get_alert_level() is not None:
            self.remove_alert_level()