# illumio-create-pairing-profile

Script to create a pairing profile for one-time use using user-supplied labels.
The script will output a file to the current directory with the content being the pairing key.

## Usage

```
usage: illumio-create-pairing-profile.py [-h] [--pce_host PCE_HOST] [--pce_port PCE_PORT] [--org_id ORG_ID] [--api_user API_USER]
                                         [--api_key API_KEY] [--labels LABELS] [--allowed_uses_per_key ALLOWED_USES_PER_KEY] [--verbose]
                                         [--keyfile-base KEYFILE_BASE] [--pp_name PP_NAME]

PCE Demo Host Credentials

options:
  -h, --help            show this help message and exit
  --pce_host PCE_HOST   Integer for the PCE demo host
  --pce_port PCE_PORT   TCP port for the PCE connection
  --org_id ORG_ID       Organization ID for the PCE
  --api_user API_USER   Optional username (default: demo@illumio.com)
  --api_key API_KEY     Optional password (default: password)
  --labels LABELS       Optional labels in the form of key-value pairs separated by commas
  --allowed_uses_per_key ALLOWED_USES_PER_KEY
                        Key can be used this often (default: 1))
  --verbose             Be more verbose (logging)
  --keyfile-base KEYFILE_BASE
                        Use this as the basename for the keyfile generated. Rest will be the pairing profile name.
  --pp_name PP_NAME     Pairing Profile Name

```
