# Based on the original script from : Scito (https://scito.ch)
# Changes in this script:
# 1. Changed the QR code generation method to SimpleCodeGenerator from  Nir Sofer
# 2. Changed export format to have HTML and Molto-2 compatible import file
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import base64
import fileinput
import sys
from urllib.parse import parse_qs, urlencode, urlparse, quote
from os import path, mkdir, system, remove
from re import sub, compile as rcompile
import generated_python.google_auth_pb2
from tkinter import filedialog
from tkinter import *
from tkinter.ttk import *
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--verbose', '-v', help='verbose output', action='store_true')
arg_parser.add_argument('--saveqr', '-s', help='save QR code(s) as images to the "qr" subfolder', action='store_true')
arg_parser.add_argument('--printqr', '-p', help='print QR code(s) as text to the terminal', action='store_true')
arg_parser.add_argument('--infile', help='file or - for stdin (default: -) with "otpauth-migration://..." URLs separated by newlines, lines starting with # are ignored')
arg_parser.add_argument('--moltofile', help='save exctracted data in file compatible with Molto-2 format. If file does not exist a new file will be created.')
arg_parser.add_argument('--htmlfile', help='save exctracted data in html file with QR codes for enrolling TOTP profiles to other apps or single profile tokens')
arg_parser.add_argument('--fromimg', help='read otpauth-migration strings from a screenshot')
args = arg_parser.parse_args()

verbose = args.verbose

# https://stackoverflow.com/questions/40226049/find-enums-listed-in-python-descriptor-for-protobuf
def get_enum_name_by_number(parent, field_name):
    field_value = getattr(parent, field_name)
    return parent.DESCRIPTOR.fields_by_name[field_name].enum_type.values_by_number.get(field_value).name

def convert_secret_from_bytes_to_base32_str(bytes):
    return str(base64.b32encode(otp.secret), 'utf-8').replace('=', '')

#decode from image to text file
if  args.fromimg:
    system("qrdecode.exe --raw "+args.fromimg+" > input_qr.txt ")
    args.infile = "input_qr.txt"

i = j = 0
print('Starting the process')
for line in (line.strip() for line in fileinput.input(args.infile)):
    if verbose: print(line)
    if line.startswith('#') or line == '': continue
    if not line.startswith('otpauth-migration://'): print('\nWARN: line is not a otpauth-migration:// URL\ninput file: {}\nline "{}"\nProbably a wrong file was given'.format(args.infile, line))
    parsed_url = urlparse(line)
    params = parse_qs(parsed_url.query)
    if not 'data' in params:
        print('\nERROR: no data query parameter in input URL\ninput file: {}\nline "{}"\nProbably a wrong file was given'.format(args.infile, line))
        sys.exit(1)
    data_encoded = params['data'][0]
    data = base64.b64decode(data_encoded)
    payload = generated_python.google_auth_pb2.MigrationPayload()
    payload.ParseFromString(data)
    i += 1
    if verbose: print('\n{}. Payload Line'.format(i), payload, sep='\n')
    line_count = -1
    #Count lines  in Molto2-export.txt
    if   args.moltofile:
     if  path.exists(args.moltofile):

      file = open(args.moltofile, "r")
     
      for line in file:
       if line != "\n":
        line_count += 1
      file.close()
		
    # pylint: disable=no-member
    for otp in payload.otp_parameters:
        j += 1
		
        if verbose: print('\n{}. Secret Key'.format(j))
        else: print()
        print('Name:   {}'.format(otp.name))
        secret = convert_secret_from_bytes_to_base32_str(otp.secret)
        #print('Secret: {}'.format(secret))
        if otp.issuer: print('Issuer: {}'.format(otp.issuer))
        print('Type:   {}'.format(get_enum_name_by_number(otp, 'type')))
        url_params = { 'secret': secret }
        if otp.type == 1: url_params['counter'] = otp.counter
        if otp.issuer: url_params['issuer'] = otp.issuer
        otp_url = 'otpauth://{}/{}?'.format('totp' if otp.type == 2 else 'hotp', quote(otp.name)) + urlencode(url_params)
        if   args.moltofile:
         with open(args.moltofile, 'a') as f:
		#Create text file with seed info
             f.write(str(line_count+j)+'\t'+secret+'\tsha1\t6\t30\tyes\tyes\t'+otp.issuer+'\n')
        if   args.htmlfile:
         with open(args.htmlfile, 'a') as f2:
		#Create html file with seed info in QR format
             keyURI="otpauth://totp/"+otp.name+"?secret="+secret#+"?issuer="+otp.issuer 
             #Generate QR code image			 
             system ("SimpleCodeGenerator.exe /Save "+ keyURI + " img/"+str(line_count+j)+".png")
             encoded = base64.b64encode(open("img/"+str(line_count+j)+".png", "rb").read())
             encoded2=encoded.decode('utf-8')
             remove("img/"+str(line_count+j)+".png")
             f2.write('TOTP Profile '+str(line_count+j)+':'+otp.name+"<br><img width=250  src='data:image/png;base64,"+encoded2+"'><pre>"+secret+"</pre><hr><br><br>")			 
#empty input_qr.txt
f = open('input_qr.txt', 'r+')
f.truncate(0) # need '0' when using r+

print(' ')			 
print('Files have been generated:')
print (args.htmlfile)			 
print (args.moltofile)
