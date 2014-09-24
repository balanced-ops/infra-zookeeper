#!/usr/bin/env python
from confu import atlas
from troposphere import (Template, FindInMap, GetAtt, Ref, Parameter, Join, Base64, Select, Output, ec2 as ec2 )

template = Template()

template.add_description('ZooKeeper')

atlas.infra_params(template)  ## ssh_key, Env, Silo

atlas.conf_params(template)   ## Conf Name, Conf Version, Conf tarball bucket

atlas.instance_params(
    template,
    roles_default=['zookeeper',],
    iam_default='zookeeper',
)

atlas.scaling_params(template)

atlas.mappings(
    template,
    accounts=[atlas.poundpay],
)

zk_secgrp = atlas.instance_secgrp(
    template,
    name="ZooKeeper",
    SecurityGroupIngress=[
        ec2.SecurityGroupRule(
            'ZKClients',
            IpProtocol='tcp',
            FromPort='2181',
            ToPort='2181',
            CidrIp=atlas.vpc_cidr,  ##TODO: open 2181 for Clients only.
        ),
    ]
)

template.add_resource(ec2.SecurityGroupIngress(
    "ZKFollowers",
    GroupId=Ref(zk_secgrp),
    SourceSecurityGroupId=Ref(zk_secgrp),
    FromPort="2888",
    ToPort="2888",
    IpProtocol="tcp",
))

template.add_resource(ec2.SecurityGroupIngress(
    "ZKServers",
    GroupId=Ref(zk_secgrp),
    SourceSecurityGroupId=Ref(zk_secgrp),
    FromPort="3888",
    ToPort="3888",
    IpProtocol="tcp",
))

i_meta_data = {}
atlas.cfn_auth_metadata(i_meta_data)
atlas.cfn_init_metadata(i_meta_data)

i_user_data = Join(
    '',
    atlas.user_data('ZKLaunchConfiguration') +
    atlas.user_data_signal_on_scaling_failure(),
)

i_launchconf = atlas.instance_launchconf(
    template,
    "ZK",
    UserData=Base64(i_user_data),
    Metadata=i_meta_data,
    SecurityGroups=[Ref(zk_secgrp)],
)

scaling_group = atlas.instance_scalegrp(
    template,
    'ZK',
    LaunchConfigurationName=Ref(i_launchconf),
    MinSize=Ref('MinSize'),
    MaxSize=Ref('MaxSize'),
    DesiredCapacity=Ref('DesiredCapacity'),
)

if __name__ == '__main__':
    print template.to_json(indent=4, sort_keys=True)
