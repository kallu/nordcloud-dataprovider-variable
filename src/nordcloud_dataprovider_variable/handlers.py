import logging
import json
import boto3
from typing import Any, MutableMapping, Optional
from cloudformation_cli_python_lib import (
    Action,
    HandlerErrorCode,
    OperationStatus,
    ProgressEvent,
    Resource,
    SessionProxy,
    exceptions,
    identifier_utils,
)

from .models import ResourceHandlerRequest, ResourceModel

# Use this logger to forward log messages to CloudWatch Logs.
LOG = logging.getLogger(__name__)
TYPE_NAME = "Nordcloud::Dataprovider::Variable"

resource = Resource(TYPE_NAME, ResourceModel)
test_entrypoint = resource.test_entrypoint


@resource.handler(Action.CREATE)
def create_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    # Typicaly model is in request.desiredResourceState
    # model = request.desiredResourceState
    # Work-a-round to create a resource with no properties (and ignore any properties set)
    model = ResourceModel(ID='', Content='')
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=model,
    )
    try:
        # setting up random primary identifier compliant with cfn standard
        model.ID = identifier_utils.generate_resource_identifier(
            stack_id_or_name=request.stackId,
            logical_resource_id=request.logicalResourceIdentifier,
            client_request_token=request.clientRequestToken,
            max_length=255
        )
        # Setting Status to success will signal to cfn that the operation is complete
        # progress.status = OperationStatus.SUCCESS
    except TypeError as e:
        # exceptions module lets CloudFormation know the type of failure that occurred
        raise exceptions.InternalFailure(f"was not expecting type {e}")
        # this can also be done by returning a failed progress event
        #return ProgressEvent.failed(HandlerErrorCode.InternalFailure, f"was not expecting type {e}")
    
    return ProgressEvent(status=OperationStatus.SUCCESS, resourceModel=model)


@resource.handler(Action.UPDATE)
def update_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=model,
    )
    return create_handler(session, request, callback_context)


@resource.handler(Action.DELETE)
def delete_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModel=None,
    )
    return progress


@resource.handler(Action.READ)
def read_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState

    try:
        cfn = session.client('cloudformation')
        myself = cfn.describe_stack_resource(
            StackName=request.stackId.split(':')[5].split('/')[1],
            LogicalResourceId=request.logicalResourceIdentifier
            )["StackResourceDetail"]
        model.Content = json.loads(myself["Metadata"])['Content']
    except Exception as e:
        raise exceptions.InternalFailure(f"{e}")
    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModel=model,
    )

# @resource.handler(Action.LIST)
# def list_handler(
#     session: Optional[SessionProxy],
#     request: ResourceHandlerRequest,
#     callback_context: MutableMapping[str, Any],
# ) -> ProgressEvent:
#     return ProgressEvent(
#         status=OperationStatus.SUCCESS,
#         resourceModels=[],
#     )
