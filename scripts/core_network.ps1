$locations = @{
    "Yeomanry House" = "10.255.0.1"
    "Franciscan" = "10.255.0.2"
    "Chandos Road" = "10.255.0.3"
    "Vinson Centre" = "10.255.0.4"
    "Mount Pleasant" = "10.255.0.5"
}

foreach ($location in $locations.GetEnumerator()) {
    $name = $location.Name
    $ip = $location.Value
    $sshCommand = "ssh -o StrictHostKeyChecking=accept-new -o KexAlgorithms=+diffie-hellman-group1-sha1 -o HostKeyAlgorithms=+ssh-rsa -o Ciphers=+aes128-cbc admin@$ip"
    Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "wt -w 0 nt --title '$name' powershell -NoExit -Command $sshCommand"
}

# ssh -v -o KexAlgorithms=+diffie-hellman-group1-sha1 -o HostKeyAlgorithms=+ssh-rsa -o Ciphers=+aes128-cbc -o MACs=+hmac-sha1-96,hmac-md5,hmac-sha1,hmac-md5-96 admin@10.255.0.3