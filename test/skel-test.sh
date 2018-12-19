#!/bin/bash

set -e

USER="testuser"
HOME_DIR="/home/$USER"
useradd -md $HOME_DIR $USER

echo "Testing .ssh directory"
if [ ! -d "$HOME_DIR/.ssh" ]; then
  echo "Missing .ssh"
  exit 1
fi

echo "test authorized_keys exists..."
if [ ! -f "$HOME_DIR/.ssh/authorized_keys" ]; then
  echo "missing authorized_keys"
  exit 1
fi

echo "test empty authorized_keys"
if [ -s "$HOME_DIR/.ssh/authorized_keys" ]; then
  echo "authorized_keys contains data it shouldnt"
  exit 1
fi

echo "test bless_client exits"
if [ ! -f "$HOME_DIR/bless_client.py" ]; then
  echo "bless_client missing from home directory"
  exit 1
fi

echo "test temporary key exists"
if [ ! -f "$HOME_DIR/.ssh/blessid" ]; then
  echo "private key missing"
  exit 1
fi

echo "test temporary cert exists"
if [ ! -f "$HOME_DIR/.ssh/blessid-cert" ]; then
  echo "temp cert missing"
  exit 1
fi

echo "Switch user to launch google_authenticator"
sudo -i -u $USER bash << EOF
exit
EOF

echo "test .google_authenticator exists in home directory"
if [ ! -f "$HOME_DIR/.google_authenticator" ]; then
  echo "new user switched and .google_authenticator not in home path"
  exit 1
fi
