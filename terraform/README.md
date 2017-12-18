# Terraform

Create infrastructure on Digital Ocean to host the VPN server.

``tasks.py`` is used as a wrapper to make working with ``terraform`` easier.

## Environment Variables

Export these environment variables:

**TF_VAR_do_api_token** - Create an API token by logging in to Digital Ocean 
web interface. Export it as an environment variable.

## Steps

Create a ``terraform`` plan.

        $ pipenv run inv plan

The plan is created in the *terraform/plans* directory and its name is provided
on stdout. Review it to ensure it's right.

Apply the ``terraform`` plan.

        $ terraform apply ${NAME_OF_PLAN_IN_PREVIOUS_STEP}

## Details

The ``tasks.py`` script creates ssh keys specifically for the VM(s) created 
with this process. The files are named *droplet-key* and *droplet-key.pub*. If 
you want to use other keys and do not want ``tasks.py`` to create them,
simply create them elsewhere and copy them in the *ssh_keys* directory with the
names *droplet-key* and *droplet-key.pub*. One the *ssh_keys* directory has 
these files, ``tasks.py`` does not recreate keys and instead uses what's
already available.

``tasks.py`` creates a temporary file called ``tasks.json``, which stores
information shared between various steps. This file contains sensitive 
information so keep it safe.

``tasks.py`` creates *main.tf* from *main.tf.j2*, which is a Jinja 2 template 
file. Since *main.tf* contains sensitive information, it is not to be stored 
with ``git`` and must be kept safe. The reason for using a template file was
that ``tasks.py`` can create or gather sensitive information and fill in
the template for security reasons. ``terraform`` will use *main.tf* not 
*main.tf.j2*. If you want your *main.tf* to be customized, 

* Edit *main.tf.j2* and ``tasks.py`` as needed
* Run ``pipenv run inv plan`` to regenerate *main.tf*

``install_python.sh`` is copied to the droplet to bootstrap a Python 2.7 
install in preparation of using ``ansible``.
