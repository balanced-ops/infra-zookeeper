infra-zookeeper
===============

Installs and configures a zookeeper cluster

Testing
======

```
vagrant plugin install vagrant-hostmanager
vagrant up
ansible zk1.vm -i .vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory --user vagrant -o -m shell -a 'echo create /test WORKS | /opt/zookeeper*/bin/zkCli.sh'
ansible zk2.vm -i .vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory --user vagrant -o -m shell -a 'echo get /test | /opt/zookeeper*/bin/zkCli.sh'
```
