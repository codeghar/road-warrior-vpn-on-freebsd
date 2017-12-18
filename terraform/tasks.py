import datetime
import json
import os
# import sys

from invoke import task
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound
# import paramiko


@task
def sshkeys(ctx):
    os.makedirs(os.path.join("..", "ssh_keys"), exist_ok=True)
    private_key = os.path.join("..", "ssh_keys", "droplet-key")
    public_key = f"{private_key}.pub"
    if not os.path.exists(private_key):
        ctx.run(f"ssh-keygen -t rsa -b 4096 -f {private_key}")
        # key = paramiko.RSAKey.generate(4096)
        # print(key.get_base64())  # print public key
        # key.write_private_key(sys.stdout)  # print private key
    result = ctx.run(f"ssh-keygen -E md5 -lf {private_key}", hide="out")
    fingerprint_full = result.stdout.strip()
    md5_fingerprint = fingerprint_full.split()[1][4:]
    print(f"MD5 fingerprint of {private_key} - {md5_fingerprint}")
    try:
        cache = json.load(open("tasks.json"))
    except FileNotFoundError:
        cache = {"ssh_md5_fingerprint": md5_fingerprint,
                 "ssh_private_key": os.path.abspath(private_key),
                 "ssh_public_key": os.path.abspath(public_key)}
    else:
        cache["ssh_md5_fingerprint"] = md5_fingerprint
        cache["ssh_private_key"] = os.path.abspath(private_key)
        cache["ssh_public_key"] = os.path.abspath(public_key)
    finally:
        json.dump(cache, open("tasks.json", "w"), indent=2)


@task
def terraforminit(ctx):
    terraform_dir = os.path.join(".", ".terraform")
    if not os.path.exists(terraform_dir):
        ctx.run(f"terraform init")


@task
def doapitoken(ctx):
    if "TF_VAR_do_api_token" not in os.environ:
        print("Error: TF_VAR_do_api_token environment variable not set")
        exit(123)
    try:
        cache = json.load(open("tasks.json"))
    except FileNotFoundError:
        cache = {"do_api_token": os.environ["TF_VAR_do_api_token"]}
    else:
        cache["do_api_token"] = os.environ["TF_VAR_do_api_token"]
    finally:
        json.dump(cache, open("tasks.json", "w"), indent=2)


@task(pre=[terraforminit, doapitoken, sshkeys])
def provider(ctx):
    try:
        cache = json.load(open("tasks.json"))
    except FileNotFoundError:
        print("Error: tasks.json not found")
        exit(157)

    template_env = Environment(loader=FileSystemLoader("./"))
    template_name = "main.tf.j2"
    try:
        template = template_env.get_template(template_name)
    except TemplateNotFound:
        print(f"Error: Template {template_name} not found")
        exit(157)

    try:
        do_api_token = cache["do_api_token"]
    except KeyError:
        print("Error: do_api_token not found in tasks.json")
        exit(144)

    try:
        ssh_md5_fingerprint = cache["ssh_md5_fingerprint"]
    except KeyError:
        print("Error: ssh_md5_fingerprint not found in tasks.json")
        exit(144)

    try:
        ssh_private_key = cache["ssh_private_key"]
    except KeyError:
        print("Error: ssh_private_key not found in tasks.json")
        exit(145)

    try:
        ssh_public_key = cache["ssh_public_key"]
    except KeyError:
        print("Error: ssh_public_key not found in tasks.json")
        exit(145)

    with open("main.tf", "w") as fh:
        fh.write(template.render(do_api_token=do_api_token,
                                 ssh_md5_fingerprint=ssh_md5_fingerprint,
                                 ssh_private_key=ssh_private_key,
                                 ssh_public_key=ssh_public_key))
        fh.write("\n")


@task(pre=[provider])
def plan(ctx):
    plans_dir = os.path.join(".", "plans")
    os.makedirs(plans_dir, exist_ok=True)
    now = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
    plan = os.path.join(plans_dir, f"plan-{now}")

    try:
        cache = json.load(open("tasks.json"))
    except FileNotFoundError:
        cache = {"plan": plan}
    else:
        cache["plan"] = plan
    finally:
        json.dump(cache, open("tasks.json", "w"), indent=2)

    ctx.run(f"terraform plan -out {plan}")
