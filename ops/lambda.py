# -*- coding: utf-8 -* https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html
import json
import logging

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# TODO: find a way to get the params from a file
def handler(event, context):
    logger.info(event)
    logger.info(context)

    ecs = boto3.client('ecs')
    default_params = {
        "cluster": "",
        "service": ""
    }
    raw_user_params = event['CodePipeline.job']['data']['actionConfiguration']['configuration'].get('UserParameters',
                                                                                                    "{}")
    user_params = json.loads(raw_user_params)

    processed_params = {}
    for k, v in default_params.items():
        processed_params[k] = user_params.get(k, default_params[k])

    # TODO: don't register a new task everytime, check for existing task with params and reuse if existing create only if not
    # http://boto3.readthedocs.io/en/latest/reference/services/ecs.html#ECS.Client.list_task_definitions
    try:
       cluster = processed_params["cluster"]
        service = processed_params["service"]

        logger.info('Attempting to update service {0} in cluster {1}'.format(service, cluster))

        ecs.update_service(cluster=cluster,
                           service=service,
                           forceNewDeployment=True)
        pipeline = boto3.client('codepipeline')
        pipeline.put_job_success_result(jobId=event['CodePipeline.job']['id'])
    except Exception as e:
        logger.exception('Exception while update ecs task via lambda')
        pipeline = boto3.client('codepipeline')
        pipeline.put_job_failure_result(jobId=event['CodePipeline.job']['id'], failureDetails={'type':
                                                                                                   'JobFailed',
                                                                                               'message': str(e), })


if __name__ == "__main__":
    handler({}, {})