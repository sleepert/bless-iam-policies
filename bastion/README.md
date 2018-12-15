# Bless with a Bastion
See youtube [tutorial](https://www.youtube.com/watch?v=8w0KWB8Bjvs) on how to get started. 
These are just a few policies and scripts you can put onto your Bastion to ensure that users can only access instances with 2fa enabled.

## Bless invoke role.
[bastion-permissions](bastion-permissions.json) contains the policy that can be attached to a role that your Bastion can assume. It will allow the Bastion to invoke the Bless lambda, list users and their SSH keys.

To simplify the process I have hardcoded the group "blessed" on the scripts, thus, this will only work for the iam group "blessed".

## iamsync
I have taken the python script from [this](https://www.tastycidr.net/a-practical-guide-to-deploying-netflixs-bless-certificate-authority/) guide and modified it so it will also search for a users' IAM SSH public key (meant for AWS CodeCommit) to sync with their bastion account. This will allow users (given the right permissions) to rotate their own ssh public keys without having to version control them or giving them to an sysadmin.

The timer is set to trigger every 10 seconds just for the tutorial, change it to you think is necessary for your setup.

## bless client
The bless client is simply a modified Netflix sample bless client with a few <b>hardcoded smells</b>. _The hardcoding was for berevity in the youtube tutorial and as such the tutorial/code is only relevant to eu-west-1. But changing to a different region is trivial_
