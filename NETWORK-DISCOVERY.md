# Network Discovery

How did we find the devices on the network?

## Ping scan on subnet

By pinging a whole subnet we could find devices that live on the subnet, this helps us with the discovery and documentation of the network.

```bash
nmap -sn 10.18.71.0/24
```

## TCP connect scan on device

By doing a deeper nmap scan on a specific device we can identify the device and what it does on the network.

```bash
nmap -sC -sV -O -Pn 10.18.71.1
```

## Mac address table of switch

By logging in to a switch we can have a look at the mac address table

For aruba this would be

```aruba
show mac-address-table port 1/1/1
```

This way we can see all the devices that the switch knows of on a certain port.

After this we can fill in the mac on a website like: <https://dnschecker.org/mac-lookup.php> to find out which brand the NIC is from. This could identify a device.
