# infra-zookeeper

Installs and configures a zookeeper cluster

```bash
$ git clone --recursive git@github.com:balanced-cookbooks/infra-zookeeper.git
$ git submodule update --init --recursive
$ cd infra-zookeeper
$ mkvirtualenv infra-zookeeper
(infra-zookeeperg)$ pip install -r requirements.txt
```


## Testing

```
vagrant plugin install vagrant-hostmanager
vagrant up
ANSIBLE_HOST_KEY_CHECKING=False ansible zk1.vm -i .vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory --user vagrant -o -m shell -a 'echo create /test WORKS | /opt/zookeeper*/bin/zkCli.sh'
ANSIBLE_HOST_KEY_CHECKING=False ansible zk2.vm -i .vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory --user vagrant -o -m shell -a 'echo get /test | /opt/zookeeper*/bin/zkCli.sh'
```

## Building a stack

```bash
(infra-vault)$ pypi_username=user pypi_password=pass vagrant provision infra-zookeeper
(infra-vault)$ vagrant ssh infra-zookeeper -c "source ~/infra/bin/activate && cd ~/infra-zookeeper/ && confu pkg clean && confu pkg build"
(infra-vault)$ confu pkg pub
```
