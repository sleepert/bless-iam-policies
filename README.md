# bless-iam-policies
Basic iam policies for getting Netflix Bless up and running.
Full youtube tutorial [here](https://youtu.be/j-ks2MBeUWw).<br>
The tutorial aims to further break down the very useful [guide](https://www.tastycidr.net/a-practical-guide-to-deploying-netflixs-bless-certificate-authority/) written by Connor Reilly.

## Creating an iam role for Bless
Bless requires access to your kms key for decrypting your private key password, it also requires access to kms to generate random byte strings.
This policy is in the [bless-lambda](bless-lambda-policy.json) json, you simply need to supply your kms arn.

## Permission to invoke Bless
To generate a certificate using Bless, your iam user will need permission to invoke the Bless lambda.
This policy is in the [bless-invoke](bless-invoke-permissions.json) json, you will need to supply the arn for your Bless lambda function.

For ease of use, a temporary key should be generated before your first Bless request attempt:
```
ssh-keygen -f ~/.ssh/blessid -b 4096 -t rsa -C 'Temporary key for BLESS certificate' -N ''
ssh-keygen -y -f ~/.ssh/blessid > ~/.ssh/blessid.pub
touch ~/.ssh/blessid-cert.pub
ln -s ~/.ssh/blessid-cert.pub ~/.ssh/blessid-cert
```
More information on that can be found in the [lyft-blessclient](https://github.com/lyft/python-blessclient) readme.
