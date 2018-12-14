if [ ! -e ~/.google_authenticator ]  &&  [ $USER != "root" ]; then
google-authenticator --time-based --disallow-reuse --force --rate-limit=3 --rate-time=30 --window-size=3
echo
echo "Save the generated emergency scratch codes and use secret key or scan the QR code to
register your device for multifactor authentication."
echo
echo "Login again using your ssh key pair and the generated One-Time Password on your registered
device."
echo
logout
fi
