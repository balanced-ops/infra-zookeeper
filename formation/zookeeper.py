#!/usr/bin/python
from confu import atlas
from troposphere import ( Template, FindInMap, GetAtt, Ref, Parameter, Join, Base64, Select, Output, ec2 as ec2 )
  
template = Template()

template.add_description('ZooKeeper')

atlas.infra_params(template)  ## ssh_key, Env, Silo

atlas.conf_params(template)   ## Conf Name, Conf Version, Conf tarball bucket

atlas.instance_params(
    template,
    roles_default=['zookeeper',],
    iam_default='zookeeper',
)

atlas.mappings(
    template,
    accounts=[atlas.poundpay],
)

kafka_secgrp = atlas.instance_secgrp(
	template,
	name="Kafka",
	## TODO: add Kafka SG roles later
)

zk_secgrp = atlas.instance_secgrp(
    template,
    name="ZooKeeper",
    SecurityGroupIngress=[
## not sure if it will work properly or not!    
    	ec2.SecurityGroupIngress(
    		"SecurityGroupIngress1",
	    	GroupId=Ref(zk_secgrp),
    		SourceSecurityGroupId=Ref(zk_secgrp),
    		FromPort="2888",
    		ToPort="2888",
    		IpProtocol="tcp",
		),
		ec2.SecurityGroupIngress(
    		"SecurityGroupIngress2",
	    	GroupId=Ref(zk_secgrp),
		    SourceSecurityGroupId=Ref(zk_secgrp),
		    FromPort="3888",
		    ToPort="3888",
		    IpProtocol="tcp",
		),
		ec2.SecurityGroupIngress(
		    "SecurityGroupIngress3",
    		GroupId=Ref(zk_secgrp),
    		SourceSecurityGroupId=Ref(kafka_secgrp),
    		FromPort="2181",
    		ToPort="2181",
    		IpProtocol="tcp",
		),
    ]
)

i_meta_data = {}
atlas.cfn_auth_metadata(i_meta_data)
atlas.cfn_init_metadata(i_meta_data)

for i in range(1,4):
	i_launchconf = atlas.instance_launchconf(
    	template,
    	"ZOOKEEPER-"+str(i),
    	Metadata=i_meta_data,
    	SecurityGroups=[Ref(zk_secgrp)],
	)
 
if __name__ == '__main__':
    print template.to_json(indent=4, sort_keys=True)
