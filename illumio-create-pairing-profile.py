import argparse
from illumio import *
import sys
import os
import json
import argparse
import uuid
import logging

def write_to_file(keyfile, content):
    file_name = keyfile 
    with open(file_name, 'w') as outfile:
        outfile.write(content)
    logging.info(f"Content written to {file_name} successfully!")

def parse_arguments():
    parser = argparse.ArgumentParser(description='PCE Demo Host Credentials')
    parser.add_argument('--pce_host', default=os.environ.get('PCE_HOST', 'poc1.illum.io'), help='Integer for the PCE demo host')
    parser.add_argument('--pce_port', default=os.environ.get('PCE_PORT', 443), help='TCP port for the PCE connection')
    parser.add_argument('--org_id', default=os.environ.get('PCE_ORG', 1), help='Organization ID for the PCE')
    parser.add_argument('--api_user', default=os.environ.get('PCE_API_USER'), help='Optional username (default: demo@illumio.com)')
    parser.add_argument('--api_key', default=os.environ.get('PCE_API_KEY'), help='Optional password (default: password)')
    parser.add_argument('--labels', help='Optional labels in the form of key-value pairs separated by commas')
    parser.add_argument('--allowed_uses_per_key', default=1, help='Key can be used this often (default: 1))')
    parser.add_argument('--verbose', action='store_true', help='Be more verbose (logging)')
    parser.add_argument('--keyfile-base', default='pairing-key', help='Use this as the basename for the keyfile generated. Rest will be the pairing profile name.')
    parser.add_argument('--pp_name', default='Cloud-Provisioning-{}'.format(uuid.uuid4().hex[:6].upper()), help='Pairing Profile Name')
    return parser.parse_args()

# Parsing the arguments
args = parse_arguments()

# Accessing the values
pce_host = args.pce_host
pce_port = args.pce_port
org_id = args.org_id
username = args.api_user
password = args.api_key
labels = args.labels.split(',') if args.labels else []
verbose = args.verbose
allowed_uses_per_key = args.allowed_uses_per_key
keyfile_base = args.keyfile_base
pp_name = args.pp_name

if not pce_host:
    exit("PCE Host (--pce_host or environemnt variable PCE_HOST) is required")

if not username:
    exit("API User (--api_user or environment variable PCE_API_USER) is required")

if not password:
    exit("API Key (--api_key or environment variable PCE_API_KEY) is required")

if verbose:
    print("Verbose logging enabled")
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


# Printing the values
logging.debug(f"PCE Host: {pce_host}")
logging.debug(f"PCE Port: {pce_port}")
logging.debug(f"Organization ID: {org_id}")
logging.debug(f"Username: {username}")
logging.debug(f"Labels: {labels}")
logging.debug(f"Allowed uses per key: {allowed_uses_per_key}")
logging.debug(f"Keyfile base: {keyfile_base}")
logging.debug(f"Pairing Profile Name: {pp_name}")

pce = PolicyComputeEngine(pce_host, port=pce_port, org_id=org_id)
pce.set_credentials(username, password)
pce.check_connection()

# fill label dict, this reads all labels and puts the object into a value of a dict. The dict key is the label name.
label_href_map = {}
value_href_map = {}
for l in pce.labels.get():
    label_href_map[l.href] = { "key": l.key, "value": l.value }
    value_href_map["{}={}".format(l.key, l.value)] = l.href
 
pairing_labels = []

for l in labels:
    if l in value_href_map:
        logging.debug("Label exists: {}".format(l))
        pce_label = pce.labels.get_by_reference(value_href_map[l])
        pairing_labels.append(pce_label)
    else:
        # create label
        k,v = l.split('=')
        create_label = Label(key=k, value=v)
        create_label = pce.labels.create(create_label)
        pairing_labels.append(create_label)
        value_href_map["{}={}".format(create_label.key, create_label.value)] = create_label.href

        
for item in pairing_labels:
    logging.debug("Item: {} = {}".format(item.key, item.value))

if not pp_name:
    pp_name = "Cloud-Provisioning-{}".format(uuid.uuid4().hex[:6].upper())

logging.debug("Pairing Profile Name: {}".format(pp_name))

pairing_profile = PairingProfile(
    name=pp_name,
    enabled=True,
    enforcement_mode='visibility_only',
    labels = pairing_labels,
    allowed_uses_per_key = allowed_uses_per_key
)

logging.debug("Pairing Profile: {}".format(pairing_profile))
pairing_profile = pce.pairing_profiles.create(pairing_profile)
logging.debug("Provisioned profile: {}".format(pairing_profile))
key = pce.generate_pairing_key(pairing_profile.href)
logging.debug("Pairing key: {}".format(key))

write_to_file(keyfile_base + "-{}.txt".format(pp_name), key)
