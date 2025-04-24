############################
# @author Elias De Hondt   #
# @see https://eliasdh.com #
# @since 01/01/2025        #
############################
# ad.ps1

Import-Module ActiveDirectory

<#
.SYNOPSIS    
    /
.DESCRIPTION
    /
.EXAMPLE
    .\ad.ps1
#>

##################################################
# buckingham.ac.uk                               #
# ├── Domain Controllers                         #
# │   ├── DC1                                    #
# │   ├── DC2                                    #
# │   └── DC3                                    #
# ├── Server                                     #
# │   ├── DHCP                                   #
# │   ├── DNS                                    #
# │   ├── NAS                                    #
# │   ├── Web                                    #
# │   └── Database                               #
# ├── Staging                                    #
# │   ├── Test User                              #
# │   └── Test Server                            #
# ├── Computers                                  #
# │   ├── Hunter Street                          #
# │   │   ├── Room 1                             #
# │   │   ├── Room 2                             #
# │   │   └── ...                                #
# │   ├── Vinson Building                        #
# │   │   ├── Room 1                             #
# │   │   ├── Room 2                             #
# │   │   └── ...                                #
# │   ├── Franciscan Building                    #
# │   │   ├── Room 1                             #
# │   │   ├── Room 2                             #
# │   │   └── ...                                #
# │   ├── Chandos Road                           #
# │   │   ├── Room 1                             #
# │   │   ├── Room 2                             #
# │   │   └── ...                                #
# │   └── Mount Pleasant                         #
# │       ├── Computer Room 1                    #
# │       │   ├── PC 1                           #
# │       │   ├── PC 2                           #
# │       │   ├── PC 3                           #
# │       │   ├── PC 4                           #
# │       │   └── PC 5                           #
# │       └── Room 2                             #
# │           ├── PC 1                           #
# │           └── PC 2                           #
# └── Users                                      #
#     ├── External                               #
#     ├── Students                               #
#     └── Staff                                  #
#         ├── IT                                 #
#         │   ├── Manager                        #
#         │   ├── Admin                          #
#         │   ├── Intern                         #
#         │   └── Support                        #
#         ├── HR                                 #
#         ├── Finance                            #
#         ├── Marketing                          #
#         ├── Teaching                           #
#         └── ...                                #
##################################################

# Set the default policy for passwords and account lockout
Set-ADDefaultDomainPasswordPolicy `
    -Identity (Get-ADDomain).NetBIOSName `
    -MaxPasswordAge 180.00:00:00 ` # 180 days -> 6 months -> 0.5 years
    -LockoutDuration 00:20:00 ` # 20 minutes
    -LockoutObservationWindow 00:10:00 ` # 10 minutes
    -MinPasswordLength 12 `
    -PasswordHistoryCount 24 ` # 24 passwords remembered
    -ComplexityEnabled $True `
    -ReversibleEncryptionEnabled $True

# Disable the use of the CMD
Set-ItemProperty -Path "HKCU:\Software\Policies\Microsoft\Windows\System" `
    -Name "DisableCMD" -Value 2 -Force

# Disable the use of PowerShell scripts
Set-ItemProperty -Path "HKCU:\Software\Policies\Microsoft\Windows\PowerShell" `
    -Name "EnableScripts" -Value 0 -Force

# Disable the use of PowerShell
Set-ItemProperty -Path "HKCU:\Software\Policies\Microsoft\Windows\PowerShell" `
    -Name "DisablePowerShell" -Value 1 -Force





gpupdate /force