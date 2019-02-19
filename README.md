# Wordpress Ecs fargate Template
> this is ready for deploy Aws ecs fargate template

## Dependencies

1. AWS account.

2. aws cli installed.

## Optional

1. Installing [ecs cli](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_CLI_installation.html)

### Folders Structure

```javascript

config // nginx and php-fpm configuration

ops // json definitions for aws roles and processes

site // app files

.gitignore //ready to use with bedrock from roots.io

buidspec.yml // code build instructions

*.Dockerfile // both of the dockers that will be build at the process. YOU SHOULD CHANGE THEIR FROM SECTION. 

README.md // here i am
```

## How to use this repo

```shell
mkdir ${name-of-your-project}
cd ${name-of-your-project}

git clone https://github.com/amitrahav/wordpress-ecs-template.git ./

```

### ECR - if not exsits

1. create two ECR repositories: one for php-app and one for nginx: `create-repository --repository-name ${applicationName}-${environment}-fpm && create-repository --repository-name ${applicationName}-${environment}-nginx`.

### CodePipline

1. change all `{}` content at ops/codePipelineServiceRole.json create codePipeline service role by `aws iam create-role --role-name ${applicationName}-${environment} --assume-role-policy-document file://ops/codePipelineServiceRole.json`
2. modify ops/codePipeline.json with the correct name for your app. create new codePipeline using aws cli `aws codepipeline create-pipeline --cli-input-json file://ops/codePipeline.json` or manually.

### Lambda function - if not exists

1. change all `{}` content at ops/lambdaServiceRole.json create service role by `aws iam create-role --role-name arn:aws:iam::${accountId}:role/updateECSImage-service-role --assume-role-policy-document file://ops/codePiplineServiceRole.json`
2. zip lambda file `zip ops/lambda.zip ops/lambda.py`
3. deploy lambda function `aws lambda create-function --function-name updateECSImage --zip-file fileb://ops/lambda.zip --handler lambda.handler --runtime python2,7 --role arn:aws:iam::${accountId}:role/updateECSImage-service-role`

### ECS Task

1. change all `{}` content at ops/ecsTaskExecutionRole.json create service role by `aws iam create-role --role-name arn:aws:iam::${accountId}:role/ecsTaskExecutionRole file://ops/ecsTaskExecutionRole.json`.
2. change all `{}` content at ops/task-definition.json and register the task `aws ecs register-task-definition --cli-input-json file://ops/task-definition.json`

### ECS Service

1. create cluster if doesn't exists `aws ecs create-cluster --cluster-name "${application-name}"`
2. create service `aws ecs create-service --service-name ${app name}-${environment}-service --task-definition {task-definition family name} --desired-count 1` (you can use any other desired count)

### ToDo

1. add declarative loadBalancer security groups, target group and https configuration.

## App files

It's recommended to use [bedrock](https://roots.io/bedrock/).

```shell
cd site
composer create-project roots/bedrock ./
```

before initial commit you Should add php-fpm docker image path  to fpm.Dockerfile (line 1). I Use [Wp-Engine](https://github.com/amitrahav/WP-Slim-Container) as php-fpm container.

## How Does It work

1. dockerBuild install dependencies and create 2 docker image and push them into ECR repo.

2. Nginx and PHP-FPM configuration (from config/ folder) being copied to the containers.

3. With the help of a simple lambda function (ops/lambda.py), i updated ECS service, and reDeployed it.