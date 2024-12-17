# Migration-Toolset
A collection of scripts and tools for migrating TOTP profiles from Google Authenticator to Token2 hardware tokens or other TOTP applications

Google Authenticator is still the most popular TOTP application used for 2FA. The accounts in Google Authenticator do not get synced via the cloud as it uses local storage only to save the seeds for TOTP profiles. For this reason, there was no simple way to transfer the accounts to a new device if your phone is running a regular (not rooted) operating system.  Around a year ago, Google has updated the app, and it is now possible to manually export the accounts and import them to another phone. 


In this project, we will publish tools and scripts allowing you to benefit from this feature and transfer the accounts to a hardware token. You can use this both for backing up your TOTP profiles and transferring them completely to a hardware token. The main script is forked from https://github.com/scito/extract_otp_secret_keys 

More information is available here https://www.token2.swiss/site/page/how-to-transfer-totp-profiles-from-google-authenticator-to-a-token2-hardware-token 

## Packages used
### Python 
The protobuf package of Google for proto3 is required for running this script. protobuf >= 3.14 < 3.21 is recommended.

    pip install "protobuf<3.21"

### Other packages 
#### Note: the  toolset uses the following third-party executables:
**Windows and Linux**

*qrscan.exe* - used to decode the contents of the QR code to text and to convert QR to svg. This is a part qrscan project (https://github.com/sayanarijit/qrscan). For linux, use `pip install qrcode` to add the qrcode module

## Usage syntax

extract_otp_secret_keys.py --fromimg *png file* --moltofile *txt file*   --htmlfile *html file*
  
### Command line parameters
  
  --fromimg : provide the path of the image file containing the screenshot of QR from Google Authenticator export
  
  --moltofile : save extracted data in file compatible with Molto-2 format. If file does not exist a new file will be created
  
  --htmlfile : save extracted data in html file with QR codes for enrolling TOTP profiles to other apps or single profile tokens 

### Examples

Windows - decode GA-QR.png contents to format for Molto2 bulk import

    python3 extract_otp_secret_keys.py --fromimg C:\Temp\GA-QR.png  --moltofile C:\Temp\Molto2-import-totp.txt
    
Linux - decode GA-QR.png contents to html (list of QR codes ready for migration)

    python3 extract_otp_secret_keys.py --fromimg /tmp/GA-QR.png  --htmlfile /tmp/totp.html

### Troubleshooting

- If Molto-2 USB Config Tool doesn't like the image use the moltofile output. Format is "Slot Seed Algorithm OTPLength TimeStep yes yes Title". Just copy it by hand over.
 
