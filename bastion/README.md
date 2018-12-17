# Bless with a Bastion
See youtube [tutorial](https://www.youtube.com/watch?v=8w0KWB8Bjvs) on how to get started. 
These are just a few policies and scripts you can put onto your Bastion to ensure that users can only access instances with 2fa enabled. You can use the code in this folder to follow along with the tutorial video. Or yo could run the [ansible](ansible) script to provision the bastion.

#### Benefits 
* 2fa Greatly reduces the chance of an attacker gaining access to your instances, even if a dev computer has been compromised.
* EC2 instances can be built with minimal provisioning (they only require trust of the CA - a simple 2 step ansible process)
* User management can be automated on the bastion only. Rather than user management on every instance (the lyft client approach)
* Users can manage their own SSH public keys, rather than going through a sys admin

#### Drawbacks
* Over confidence in the security of your bastion could lead to actively ignoring security flaws in your instances
* Inconvenience of having to SSH to the bastion before you can SSH to any other instance (can be negated with local .ssh config)
* Security group restrictions may affect your provisioning software.

## Bless invoke role.
[bastion-permissions](bastion-permissions.json) contains the policy that can be attached to a role that your Bastion can assume. It will allow the Bastion to invoke the Bless lambda, list users and their SSH keys.

To simplify the process I have hardcoded the group "blessed" on the scripts, thus, this will only work for the iam group "blessed".

## iamsync
I have taken the python script from [this](https://www.tastycidr.net/a-practical-guide-to-deploying-netflixs-bless-certificate-authority/) guide and modified it so it will also search for a users' IAM SSH public key (meant for AWS CodeCommit) to sync with their bastion account. This will allow users (given the right permissions) to rotate their own ssh public keys without having to version control them or giving them to an sysadmin.

The timer is set to trigger every 10 seconds just for the tutorial, change it to you think is necessary for your setup.

## bless client
The bless client is simply a modified Netflix sample bless client with a few <b>hardcoded smells</b>. _The hardcoding was for brevity in the youtube tutorial and as such the tutorial/code is only relevant to eu-west-1. But changing to a different region is trivial_

## file breakdown
All files in this directory will be used by ansible.
* [sshd_config](sshd_config) - config for /etc/ssh/sshd_config - _ubuntu user doesnt require 2 factor here, this was only for simplicity in the tutorial. its a good idea to force the ubuntu user to use 2fa_
* [sshd](sshd) - config for google authenticator /etc/pam.d/sshd
* [mfa.sh](mfa.sh) - forces a user to enable 2fa on first loging /etc/profile.d/mfa.sh
* iamsync - systemd service to sync users from the blessed group. Copied and modified from [this](https://www.tastycidr.net/a-practical-guide-to-deploying-netflixs-bless-certificate-authority/) bless lyft guide
* [bless_client.py](bless_client.py) - allows a user to call the BLESS lambda function to generate a certificate, all users will have this in their home directory
* [bash_aliases](bash_aliases) - an alias, bless, is created for all users to allow them to ssh to another instance. `bless user_name instance_ip`
* [bastion_permissions.json](bastion_permissions.json) - iam policy that allows user/role to call the bless lambda function and list users/ssh_keys in the 'blessed' group
