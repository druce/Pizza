# How To Deploy Container To AWS Elastic Container Service

Based on AWS document here: [Tutorial: Creating a Cluster with a Fargate Task Using the Amazon ECS CLI](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-cli-tutorial-fargate.html)

1) [Install and configure AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-environment.html)

2) [Install ECS CLI](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_CLI_installation.html)

3) Assume IAM task execution role if needed:

- Create the file `task-execution-assume-role.json` (see [example](task-execution-assume-role.json). Update region as necessary.) 

```aws iam --region us-east-1 create-role --role-name ecsTaskExecutionRole --assume-role-policy-document file://task-execution-assume-role.json```

- Attach role policy

  ```aws iam --region us-east-1 attach-role-policy --role-name ecsTaskExecutionRole --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy```

4) Configure credentials, default cluster
```
ecs-cli configure profile --access-key <access-key> --secret-key <secret-key> --profile-name pizza-profile
ecs-cli configure --cluster pizza --default-launch-type FARGATE --config-name pizza --region us-east-1
ecs-cli up --cluster-config pizza --ecs-profile pizza-profile```

Note that this doesn't create your own personal cluster but takes advantage of the Fargate container service.

Take note of info on cluster,  vpc and subnets:

```VPC created: vpc-123456789012e1234
VPC created: vpc-123456789012e1234
Subnet created: subnet-1234567890abcdef
Subnet created: subnet-fedcba0987654321```

Take note of security group
```aws ec2 describe-security-groups --filters Name=vpc-id,Values=vpc-123456789012e1234 --region us-east-1```

5) Configure security group to allow inbound on the desired port, using the security group-id reported (and correct port and region).
`aws ec2 authorize-security-group-ingress --group-id <group-id> --protocol tcp --port 8181 --cidr 0.0.0.0/0 --region us-east-1`

6) Create repository (not sure if this is created by default)

```aws ecr create-repository --repository-name pizza
aws ecr describe-repositories```


7) Push Docker image to ECS
```docker login -u AWS -p $(aws ecr get-login-password --region us-east-1) 123412341234.dkr.ecr.us-east-1.amazonaws.com
docker build . -t pizza
docker tag pizza:latest 123412341234.dkr.ecr.us-east-1.amazonaws.com/pizza:latest
docker push 123412341234.dkr.ecr.us-east-1.amazonaws.com/pizza:latest
```

8) Start the container 

- Make docker-compose.yml file (see [example](docker-compose.yml). Specify correct ECR image and region)
- Make ecs-params.yml file (see [example](ecs-params.yml). Specify correct subnets and security group)
p
```ecs-cli compose --project-name pizza service up --create-log-groups --cluster-config pizza --ecs-profile pizza-profile```

This will take a minute and show some log messages. Go to AWS ECS console and you should see your cluster running.


9) Get info on your container

```ecs-cli compose --project-name pizza service ps --cluster-config pizza --ecs-profile pizza-profile
Name                                              State    Ports                        Task          Definition  Healthpizza/0fec210e48734bf1bfca123a88e3a2f1/web  RUNNING  3.237.198.63:8181->8181/tcp  pizza:1       UNKNOWN
```

Note the IP address and port, access the service on IP:port

Note the task id and view logs
`ecs-cli logs --task-id 0fec210e48734bf1bfca123a88e3a2f1 --follow --cluster-config pizza --ecs-profile pizza-profile`

10) Shut it down

`ecs-cli compose --project-name tutorial service down --cluster-config tutorial --ecs-profile tutorial-profile`




