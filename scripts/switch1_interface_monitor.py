Manifest = {
    "Name": "switch1_interface_monitor",
    "Description": "Physical Interface Tx/Rx statistics monitoring agent"
    " using multi-graph",
    "Version": "1.2",
    "TargetSoftwareVersion": "10.11",
    "Author": "Kobe Wijnants",
}

ParameterDefinitions = {
    "rx_packets_threshold": {
        "Name": "Threshold for Rx packets",
        "Description": "Threshold for number of Rx packets received",
        "Type": "integer",
        "Required": True,
    },
    "tx_packets_threshold": {
        "Name": "Threshold for Tx packets",
        "Description": "Threshold for number of Tx packets transmitted",
        "Type": "integer",
        "Required": True,
    },
}


class Agent(NAE):
    def __init__(self):
        # rx packets
        uri1 = (
            "/rest/v1/system/interfaces/*?attributes=statistics.rx_packets"
            + "&filter=type:system"
        )
        rate_m1 = Rate(uri1, "20 seconds")
        self.m1 = Monitor(rate_m1, "Rx Packets (packets per second)")
        self.r1 = Rule("Rule to Monitor Interface rx Packets")
        self.r1.condition("{} > {}", [self.m1, self.params["rx_packets_threshold"]])
        self.r1.clear_condition(
            "{} < {}", [self.m1, self.params["rx_packets_threshold"]]
        )
        self.r1.action("ALERT_LEVEL", AlertLevel.CRITICAL)
        self.r1.clear_action("ALERT_LEVEL", AlertLevel.NONE)

        # tx packets
        uri2 = (
            "/rest/v1/system/interfaces/*?attributes=statistics.tx_packets"
            + "&filter=type:system"
        )
        rate_m2 = Rate(uri2, "20 seconds")
        self.m2 = Monitor(rate_m2, "Tx Packets (packets per second)")
        self.r2 = Rule("Rule to Monitor Interface tx Packets")

        self.r2.condition("{} > {}", [self.m2, self.params["tx_packets_threshold"]])
        self.r2.clear_condition(
            "{} < {}", [self.m2, self.params["tx_packets_threshold"]]
        )
        self.r2.action("ALERT_LEVEL", AlertLevel.CRITICAL)
        self.r2.clear_action("ALERT_LEVEL", AlertLevel.NONE)

        # graph display for change of traffic and packets drop
        # self.graph_rx_packets = Graph(
        #     [self.m1],
        #     title=Title("Rate of change of Interface Rx packets (in seconds)"),
        #     dashboard_display=True,
        # )
        # self.graph_tx_packets = Graph(
        #     [self.m2],
        #     title=Title("Rate of change of Interface Tx packets (in seconds)"),
        #     dashboard_display=False,
        # )
