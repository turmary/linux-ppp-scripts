#!/bin/bash

TARGET=/etc/ppp

_apt_updated=false
function apt_install() {
	local pkg=$1 status _pkg

	status=$(dpkg -l $pkg | tail -1)
	_pkg=$(  echo "$status" | awk '{ printf "%s", $2; }')
	status=$(echo "$status" | awk '{ printf "%s", $1; }')
	# echo $status $_pkg $pkg

	if [ "X$status" == "Xii" -a "X$_pkg" == "X$pkg" ]; then
		echo "debian package $pkg already installed."
		return 1
	fi

	# install the debian package
	if [ "X$_apt_updated" == "Xfalse" ]; then
		apt-get -y update
		_apt_updated=true
	fi
	apt-get -y install $pkg
	return 0
}


# 1. Install ppp package
apt_install ppp
#apt_install openresolv
apt_install resolvconf
#dpkg --purge resolvconf
dpkg --purge openresolv
dpkg --purge pppconfig

# 2. Copy ppp peers files
cp quectel-chat-connect $TARGET/peers
cp quectel-chat-disconnect $TARGET/peers
cp quectel $TARGET/peers
cp 000routeup $TARGET/ip-up.d/
cp 000routedown $TARGET/ip-down.d/
# disable resolvconf for PPP
# sed -i '9,9c exit 0' /etc/ppp/ip-up.d/000resolvconf
# cp ip-up $TARGET/
# chmod a+x $TARGET/ip-up
cp quectel-onoff.sh /usr/bin/
chmod a+x /usr/bin/quectel-onoff.sh

# 3. Remove service ModemManager
# Modem Manager will cause ppp unstable
killall ModemManager
systemctl stop ModemManager
systemctl disable ModemManager

echo
echo "############################"
echo "PPP scripts install complete"
echo "############################"
exit 0

