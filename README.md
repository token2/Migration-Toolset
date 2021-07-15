# Migration-Toolset
A collection of scripts and tools for migrating TOTP profiles from Google Authenticator to Token2 hardware tokens or other TOTP applications

Google Authenticator is still the most popular TOTP application used for 2FA. The accounts in Google Authenticator do not get synced via the cloud as it uses local storage only to save the seeds for TOTP profiles. For this reason, there was no simple way to transfer the accounts to a new device if your phone is running a regular (not rooted) operating system.  Around a year ago, Google has updated the app, and it is now possible to manually export the accounts and import them to another phone. 


In this project, we will publish tools and scripts allowing you can benefit from this feature and transfer the accounts to a hardware token. You can use this both for backing up your TOTP profiles and transferring them completely to a hardware token. The main script is forked from https://github.com/scito/extract_otp_secret_keys 

## Packages used
The protobuf package of Google for proto3 is required for running this script. protobuf >= 3.14 is recommended.

    pip install protobuf

## Usage syntax

### Windows

extract_otp_secret_keys-win.py --fromimg *png file* --moltofile *txt file*   --htmlfile *html file*

### Linux

extract_otp_secret_keys-linux.py --fromimg *png file* --moltofile *txt file*   --htmlfile *html file*

  
### Command line parameters
  
  --fromimg : provide the path of the image file containing the screenshot of QR from Google Authenticator export
  
  --moltofile : save exctracted data in file compatible with Molto-2 format. If file does not exist a new file will be created
  
  --htmlfile : save exctracted data in html file with QR codes for enrolling TOTP profiles to other apps or single profile tokens 
  
#### Note: the  toolset uses the following third-party executables:
**Windows**

*qrdecode.exe* - used to decode the contents of the QR code to text. This is a part of Zbar Code Reader project (http://zbar.sourceforge.net/)

*SimpleCodeGenerator.exe* - used to create a QR code from text.  Created by  Nir Sofer (https://www.nirsoft.net/utils/qr_code_generator.html)

**Linux

*zbarimg* - used to decode the contents of the QR code to text. This is a part of Zbar Code Reader project (http://zbar.sourceforge.net/). Installation using the following command:

     sudo apt-get install zbar-tools

*qrencode* - a tool used to create a QR code from text  by Kentaro Fukuchi ( http://fukuchi.org/works/qrencode/ ).  Installation using the following command:

    sudo apt-get install qrencode



 
