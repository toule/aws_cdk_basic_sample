# CDK(Cloud Development Kit) Python Sample Test



## 가정 사항

- 파이썬에 대한 기본적인 지식을 가지고 있음
- 언어 : Python 3.x 
- 환경 : Cloud9



## CDK(Cloud Development Kit) Deploy

*Directory PATH = `~/environment`*

### 1. Download Code

```bash
git clone https://github.com/toule/aws_cdk_basic_sample.git
```



### 2. Install CDK

```bash
npm install -g aws-cdk
```



### 3. Confirm Version

```bash
cdk --version
```



### 4. Install pip

```bash
curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user
pip3 --version
```



### 5. Install CDK requirement

*Directory PATH = `~/environment/aws_cdk_basic_sample`*

```bash
pip3 install -r requirements.txt
```



### 6. CDK Stack List

```bash
cdk ls
```

![list](./images/list.png)

### 7. Edit Account

*Directory File = `~/environment/aws_cdk_basic_sample/app.py`*

아래 스크립트의 경우 편의를 위해 최초 한번의 변수에 대해서 치환해주는 구문이므로 동작하지 않는 경우 my_account를 본인의 account id로 직접 변경 해야함

```bash
account=$(aws sts get-caller-identity | jq -r ".Account")
echo $account
sed -i `` "s/my_account/$account/g" app.py
```

 (* 여기에서 `은 **backtick**임)

```python
### Not Paste !!! ###
vpc_stack = SampleVPCStack(app, "Network", env=core.Environment(region="ap-northeast-2",account="my_account")) #Network is named ~/*/* (firsted named), it works based on this name.
ec2_stack = SampleEC2Stack(app, "Service", vpc=vpc_stack.vpc, env=core.Environment(region="ap-northeast-2",account="my_account"))
```



### 8. CDK Deploy

```bash
cdk deploy Network Service
```

Do you wish to deploy these changes (y/n)? y (enter)

![deploy](./images/cdk-deploy-1.png)

![deploy](./images/cdk-deploy-2.png)

### 8. 생성 완료

- 인프라가 제대로 생성되었는지 확인

![output](./images/output-1.png)

![output](./images/output-2.png)

![output](./images/output-3.png)

## Destroy

`cdk destroy Network Service`

Are you sure you want to delete: Service, Network (y/n)? y (enter)

![destroy](./images/destroy.png)