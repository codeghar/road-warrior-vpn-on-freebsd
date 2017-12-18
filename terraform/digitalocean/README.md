# Module: digitalocean

Upload ssh public key that will be inserted into the droplet after creation.

Create a droplet with FreeBSD 11.1 installed. This is not a variable because
this entire repo is meant to showcase how to automate a just-in-time VPN server
on FreeBSD.

## Variables

**ssh_private_key** - Path to the ssh private key to be used for ssh'ing into
the droplet for provisioning.

**ssh_public_key** - Path to the ssh public key to be uploaded to Digital Ocean.

**ssh_fingerprint** - md5 fingerprint of ssh key to identify the key to be 
inserted into the droplet after creation.

**region** - The region in Digital Ocean where the droplet is to be created. 
Refer to Digital Ocean's documentation for more information.

**droplet_size** - The size of the droplet to create. Refer to Digital Ocean's 
documentation for more information. 

**droplet_name** - Name of the droplet. Refer to Digital Ocean's documentation 
for more information. 

## Outputs

Module has no outputs.
