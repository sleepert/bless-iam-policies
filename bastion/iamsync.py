"""
iamsync.py
Fetches the members of the 'blessed' group and ensures that they match the members
in the matching local unix blessed group.
"""

import boto3, pwd, grp, logging, logging.handlers, subprocess, json

_LOGGER = logging.getLogger('pythonLogger')

def get_local_group_membership(groupname):
  try:
    return grp.getgrnam(groupname)[3]
  except KeyError:
    print('Group {} does not exist.'.format(groupname))
    exitcode = subprocess.call(
      ["groupadd", groupname]
    )
    _LOGGER.info(
      "Creating group {} exited with code {}".format(
        groupname, exitcode
      )
    )
    return grp.getgrnam(groupname)[3]
  except Exception as e:
    _LOGGER.error(e)

def remove_defunct_users(group):
  allusers = pwd.getpwall()
  defunct = []
  try:
    for u in allusers:
      delete = False
      # set delete to True if the user's comment is iamsync
      if pwd.getpwnam(u.pw_name).pw_gecos == "iamsync":
        delete = True

      # Check each group's membership for the user
      # If any group has that user as a member, set delete to False
      if u.pw_name in grp.getgrnam(group).gr_mem:
        delete = False

      # If delete is True, add to list of defunct users
      if delete:
        defunct.append(u.pw_name)
    if defunct:
      _LOGGER.info("Defunct Users: {}".format(defunct))

    for u in defunct:
      exitcode = subprocess.call(
        ["userdel", "--remove", u]
      )
      _LOGGER.info(
        "Removing user {} and home directory exited with code {}".format(
          u, exitcode
        )
      )
  except Exception as e:
    _LOGGER.error(e)

def create_user(username, group):
  try:
    homedir = "/home/{}".format(username)
    exitcode = subprocess.call(
      [
        "useradd", "-s", "/bin/bash",
        "-c", "iamsync", "-md", homedir,
        "-g", group, username
      ]
    )
    _LOGGER.info(
      "Creating user {} with primary group {} exited with code {}".format(
      username, group, exitcode
    ))
  except Exception as e:
    _LOGGER.error(e)

def check_if_user_exists(username):
  try:
    check = pwd.getpwnam(username)
    return True
  except KeyError:
    return False

def remove_user_from_group(username, groupname):
  try:
    subprocess.call(
      [
        "gpasswd", "-d", username, groupname
      ]
    )
  except Exception as e:
    _LOGGER.error(e)

def add_user_to_group(username, groupname):
  try:
    exitcode = subprocess.call(
      [
        "usermod", "-aG", groupname, username
      ]
    )
    _LOGGER.info("Adding user {} to group {} exited with code {}".format(
      username, groupname, exitcode
    ))
  except Exception as e:
      _LOGGER.error(e)

def get_iam_group_membership(groupname):
  try:
    users = []
    iam = boto3.resource('iam')
    group = iam.Group(groupname)
    for u in group.users.all():
      users.append(u.name)
    return users
  except Exception as e:
    _LOGGER.error(e)

def populate_authorized_keys(localusers):
  client = boto3.client('iam')
  for user in localusers:
    public_key_list = client.list_ssh_public_keys(
      UserName=user
    )['SSHPublicKeys']
    if not public_key_list:
      open("/home/" + user + "/.ssh/authorized_keys", "w").close()
      continue
    sshkey = client.get_ssh_public_key(
      UserName=user,
      SSHPublicKeyId=public_key_list[0]['SSHPublicKeyId'],
      Encoding='SSH'
    )['SSHPublicKey'] \
    ['SSHPublicKeyBody']
    authorized_key_file = open("/home/" + user + "/.ssh/authorized_keys", "w")
    authorized_key_file.write(sshkey)
    authorized_key_file.close()

if __name__ == '__main__':

  logpath = "/var/log/iamsync.log"

  _LOGGER.setLevel(logging.INFO)
  py_hdlr = logging.handlers.WatchedFileHandler(
    logpath, mode='a'
  )
  py_formatter = logging.Formatter(
    '%(asctime)s : %(levelname)s - %(message)s'
  )
  py_hdlr.setFormatter(py_formatter)
  _LOGGER.addHandler(py_hdlr)

  group = "blessed"

  # Determine memberships in IAM and locally
  iamusers = get_iam_group_membership(group)

  localusers = get_local_group_membership(group)

  # List of users we want to purge from the group
  subtract = []

  # If user exists locally but is not in IAM group
  # Add to subtract list
  for u in localusers:
    if u not in iamusers:
      subtract.append(u)

  # Perform subtraction
  if subtract:
    for u in subtract:
      remove_user_from_group(u, group)

  # If user exists in IAM but not locally, create and append to group
  for u in iamusers:
    if u not in localusers:
      if not check_if_user_exists(u):
        create_user(u, group)
        add_user_to_group(u, group)

  remove_defunct_users(group)

  populate_authorized_keys(localusers)
