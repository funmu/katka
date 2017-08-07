
## Get Mongo on this server
echo ------------------------ ------------------------ ------------------------
echo Mongo setup on EC2 as per: https://docs.mongodb.com/ecosystem/platforms/amazon-ec2/#deploy-mongodb-ec2
echo ------------------------ ------------------------ ------------------------

echo "[mongodb-org-3.2]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/amazon/2013.03/mongodb-org/3.2/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-3.2.asc" | sudo tee -a /etc/yum.repos.d/mongodb-org-3.2.repo


sudo yum install -y mongodb-org-server \
    mongodb-org-shell mongodb-org-tools


## For now I am using existing / for hosting Mongo on a single EBS 
##  ... Later consider moving the log, journal and data to different EBS
sudo mkdir /data
sudo mkdir /data/log.mongo
sudo mkdir /data/journal.mongo
sudo mkdir /data/data.mongo

sudo chown mongod:mongod /data/log.mongo /data/journal.mongo /data/data.mongo

sudo ln -s /data/journal.mongo /data/data.mongo/journal

dbpath=/data/data.mongo
logpath=/data/log.mongo/mongod.log

## If we do not want Mongo to start at boot, then do the following
# sudo chkconfig mongod off

echo '* soft nofile 64000
* hard nofile 64000
* soft nproc 64000
* hard nproc 64000' | sudo tee /etc/security/limits.d/90-mongodb.conf

# Optimize AWS EC2 read-ahead to be 32 blocks (or 16KB)
sudo blockdev --setra 32 /dev/xvda

# Make changes persistent across reoot.
# echo 'ACTION=="add|change", KERNEL=="xvdf", ATTR{bdi/read_ahead_kb}="16"' | sudo tee -a /etc/udev/rules.d/85-ebs.rules

## -----------
# Start the service
sudo service mongod start

# To automatically start at reboot
sudo chkconfig mongod on
