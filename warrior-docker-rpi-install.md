### [ArchiveTeam Warrior](http://www.archiveteam.org/index.php?title=ArchiveTeam_Warrior) installation on Raspberry Pi 2 & 3 with Raspbian Jessie (using Docker)

* Docker installation
```bash
curl -sSL get.docker.com | sh
sudo usermod -aG docker pi
```

* Scripts download and preparation
```bash
git clone https://github.com/ArchiveTeam/warrior-dockerfile.git
cd warrior-dockerfile
chmod 755 wget-lua.raspberry
```

* Build image
```bash
sudo docker build -f Dockerfile.raspberry .
```

* Get the new image id from the output of the previous script: `Successfully built <id>`, and run it:
```bash
docker run -d -p 8001:8001 <id>
```

* Wait a while for initial configuration, point your browser to the 8001 port of your Raspberry Pi and start using the Warrior.

* You can stop and resume the Warrior with `docker stop` and `docker start`.
