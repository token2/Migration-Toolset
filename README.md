# Migration-Toolset
A collection of scripts and tools for migrating TOTP profiles from Google Authenticator to Token2 hardware tokens or other TOTP applications

Google Authenticator is still the most popular TOTP application used for 2FA. The accounts in Google Authenticator do not get synced via the cloud as it uses local storage only to save the seeds for TOTP profiles. For this reason, there was no simple way to transfer the accounts to a new device if your phone is running a regular (not rooted) operating system.  Around a year ago, Google has updated the app, and it is now possible to manually export the accounts and import them to another phone. 


In this project, we will publish tools and scripts allowing you can benefit from this feature and transfer the accounts to a hardware token. You can use this both for backing up your TOTP profiles and transferring them completely to a hardware token.

## Usage syntax

### Windows


extract_otp_secret_keys-win.py --fromimg *png file* --moltofile *txt file*   --htmlfile *html file*
  
  
  --fromimg : provide the path of the image file containing the screenshot of QR from Google Authenticator export
  
  --moltofile : save exctracted data in file compatible with Molto-2 format. If file does not exist a new file will be created
  
  --htmlfile : save exctracted data in html file with QR codes for enrolling TOTP profiles to other apps or single profile tokens 
  
