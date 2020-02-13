#!/usr/bin/env python3

from aws_cdk import core

from sample_app.vpc_stack import SampleVPCStack
from sample_app.ec2_stack import SampleEC2Stack
#from sample_app.alb_stack import SampleALBStack

app = core.App()

vpc_stack = SampleVPCStack(app, "Network", env=core.Environment(region="ap-northeast-2",account="my_account")) #Network is named ~/*/* (firsted named), it works based on this name.
ec2_stack = SampleEC2Stack(app, "Service", vpc=vpc_stack.vpc, env=core.Environment(region="ap-northeast-2",account="my_account"))

app.synth()
