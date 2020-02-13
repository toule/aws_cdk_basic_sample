from aws_cdk import core
from aws_cdk.aws_iam import (Role, ServicePrincipal, ManagedPolicy)
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as elb
import aws_cdk.aws_autoscaling as autoscaling


ec2_type = "t2.micro"
#key_name = "keypair" #EC2 keyname
linux_ami = ec2.GenericLinuxImage({	"ap-northeast-2": "ami-0bea7fd38fabe821a" })
with open("./userdata/userdata.sh") as f:
	userdata=f.read()

class SampleEC2Stack(core.Stack):
	def __init__(self, scope: core.Construct, id: str, vpc, **kwargs) -> None:
		super().__init__(scope, id, **kwargs)
	
		alb = elb.ApplicationLoadBalancer(self, "myALB",
                                          vpc=vpc,
                                          internet_facing=True,
                                          load_balancer_name="myALB"
                                          )
		alb.connections.allow_from_any_ipv4(
            ec2.Port.tcp(80), "Internet access ALB 80")
		listener = alb.add_listener("my80",
                                    port=80,
                                    open=True)
		self.asg = autoscaling.AutoScalingGroup(self, "myASG",
                                                vpc=vpc,
                                                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE),
                                                instance_type=ec2.InstanceType(instance_type_identifier=ec2_type),
                                                machine_image=linux_ami,
#                                                key_name=key_name,
                                                user_data=ec2.UserData.custom(userdata),
                                                desired_capacity=1,
                                                min_capacity=1,
                                                max_capacity=2,)
		self.asg.connections.allow_from_any_ipv4(ec2.Port.tcp(22), "Access SSH port of EC2 in Autoscaling Instance")                                        
		self.asg.connections.allow_from(alb, ec2.Port.tcp(80), "ALB access 80 port of EC2 in Autoscaling Group")
		listener.add_targets("addTargetGroup", port=80, targets=[self.asg])
		core.CfnOutput(self, "OUTPUT_ALB_DNS", value=alb.load_balancer_dns_name)
