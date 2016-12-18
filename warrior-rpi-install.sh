# Tested on Raspberry Pi 1 & 2016-11-25-raspbian-jessie-lite
# run this script with sudo

# Warrior requirements
apt-get install -y python3-pip python-software-properties
update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
update-alternatives --install /usr/bin/python python /usr/bin/python3.4 2

# wget-lua compile requirements
apt-get install -y autoconf libgnutls-deb0-28 libgnutls28-dev flex lua5.1 liblua5.1-0 liblua5.1-0-dev

# wget-lua compilation and installation
curl -sSL https://github.com/ArchiveTeam/codebender-grab/raw/master/get-wget-lua.sh | sh
mv wget-lua /usr/bin

# 'warrior' user creation
useradd warrior
usermod -a -G sudo warrior
echo "warrior ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/011_warrior-nopasswd
mkdir /home/warrior && chown warrior: /home/warrior

# filesystem and directories requirements
mkdir /home/warrior/data
mkdir /home/warrior/data/data
chmod 777 /home/warrior/data /home/warrior/data/data
ln -s /home/warrior/data /data
mkdir /home/warrior/projects

# Warrior installation
cd /home/warrior && sudo -u warrior git clone https://github.com/ArchiveTeam/warrior-code2.git

# Login with 'warrior' user, run 'warrior-install.sh' and then 'warrior-runner.sh' to start
