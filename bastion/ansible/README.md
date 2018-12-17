# Ansible instructions
Either run with a packer template or run on an already existing EC2 instance. Currently setup for ubuntu 18.04

_**Requires ansible >= 2.4**_

to run on an instance
create a `host` file containing the following
```
[bastion]
bastion ansible_ssh_host=<instance host ip> ansible_python_interpreter=/usr/bin/python3
```

then run the playbook:
```
ansible-playbook -u ubuntu -i 'host' --private-key <your ec2 keypair> playbook.yml
```
## packer
To make a bastion AMI run:
```
packer build packer.json
```
