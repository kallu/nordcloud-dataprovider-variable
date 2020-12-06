# Nordcloud::Dataprovider::Variable

## Dependencies

* Docker
* Python 3.7
* AWS CLI
* AWS SAM CLI
* CFN CLI
* CFN CLI Python plugin

See https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/what-is-cloudformation-cli.html

## Initialize a project 

```
% cfn init
Initializing new project
What's the name of your resource type?
(Organization::Service::Resource)
>> Nordcloud::Dataprovider::Variable
Select a language for code generation:
[1] go
[2] java
[3] python36
[4] python37
(enter an integer): 
>> 4
Use docker for platform-independent packaging (Y/n)?
This is highly recommended unless you are experienced 
with cross-platform Python packaging.
>> Y
Initialized a new project in nordcloud-dataprovider-variable
```

Update ```cloudformation-cli-python-lib``` to ```2.1.5```<br>
( see https://github.com/aws-cloudformation/cloudformation-cli-python-plugin/issues/140 )

## Congratulations on starting development! Next steps:

1. Write the JSON schema describing your resource, `nordcloud-dataprovider-variable.json`
2. Implement your resource handlers in `nordcloud_dataprovider_variable/handlers.py`

> Don't modify `models.py` by hand, any modifications will be overwritten when the `generate` or `package` commands are run.

Implement CloudFormation resource here. Each function must always return a ProgressEvent.

```python
ProgressEvent(
    # Required
    # Must be one of OperationStatus.IN_PROGRESS, OperationStatus.FAILED, OperationStatus.SUCCESS
    status=OperationStatus.IN_PROGRESS,
    # Required on SUCCESS (except for LIST where resourceModels is required)
    # The current resource model after the operation; instance of ResourceModel class
    resourceModel=model,
    resourceModels=None,
    # Required on FAILED
    # Customer-facing message, displayed in e.g. CloudFormation stack events
    message="",
    # Required on FAILED: a HandlerErrorCode
    errorCode=HandlerErrorCode.InternalFailure,
    # Optional
    # Use to store any state between re-invocation via IN_PROGRESS
    callbackContext={},
    # Required on IN_PROGRESS
    # The number of seconds to delay before re-invocation
    callbackDelaySeconds=0,
)
```

Failures can be passed back to CloudFormation by either raising an exception from `cloudformation_cli_python_lib.exceptions`, or setting the ProgressEvent's `status` to `OperationStatus.FAILED` and `errorCode` to one of `cloudformation_cli_python_lib.HandlerErrorCode`. There is a static helper function, `ProgressEvent.failed`, for this common case.

## What's with the type hints?

We hope they'll be useful for getting started quicker with an IDE that support type hints. Type hints are optional - if your code doesn't use them, it will still work.

## Deployment

```
cfn generate
cfn validate
cfn submit --set-default
```

First deployment will take a bit longer as it will not only create a new resource type version, but also 2 stacks with supporting resources

```
[
    [
        "CloudFormationManagedUploadInfrastructure",
        "This CloudFormation template provisions all the infrastructure that is required to upload artifacts to CloudFormation's managed experience."
    ],
    [
        "nordcloud-dataprovider-variable-role-stack",
        "This CloudFormation template creates a role assumed by CloudFormation during CRUDL operations to mutate resources on behalf of the customer."
    ]
]

```

Everything is ready to test Nordcloud::Dataprovider::Variable resource type.

```
aws cloudformation create-stack --stack-name Hello --template-body file://cloudformation.yaml
```

## Deregistering resource type versions

Each deployment will create a new version of resource type. To deregister all but the default version do

```
aws cloudformation list-type-versions --arn arn:aws:cloudformation:REGION:ACCOUNT_ID:type/resource/RESOURCE_TYPE_NAME \
 --query 'TypeVersionSummaries[?IsDefaultVersion==`false`].[Arn]' --output text | \
while read ARN
do
  aws cloudformation deregister-type --arn $ARN
done
```

Default version can not be deregistered but you should reregisted the type instead

```
aws cloudformation deregister-type --arn arn:aws:cloudformation:REGION:ACCOUNT_ID:type/resource/RESOURCE_TYPE_NAME
```

There is also deployment package stored in S3 bucket ```cloudformationmanageduploadinfrast-artifactbucket-xxxxxxxxxxxx```
for each version of resource type you have deployed. Note that bucket has versioning enabled so delete won't really delete
the objects unless you remove version(s) too, or disable object versioning for the bucket.
