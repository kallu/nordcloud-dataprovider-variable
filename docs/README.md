# Nordcloud::Dataprovider::Variable

Pseudo resource for storing a value of complex function for future reference(s).

## Syntax

To declare Nordcloud::Dataprovider::Variable in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "Type" : "Nordcloud::Dataprovider::Variable",
    "Metadata": {
        "Content": String
    }
}
</pre>

### YAML

<pre>
Type: Nordcloud::Dataprovider::Variable
Metadata:
  Content: String
</pre>

## Properties

This resource type has no properties

## Return Values

### Ref

When you pass the logical ID of this resource to the intrinsic `Ref` function, Ref returns the ID.

### Fn::GetAtt

The `Fn::GetAtt` intrinsic function returns a value for a specified attribute of this type. The following are the available attributes and sample return values.

For more information about using the `Fn::GetAtt` intrinsic function, see [Fn::GetAtt](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html).

#### ID

ID is automatically generated on creation and assigned as the unique identifier.

#### Content

Variable content

## Examples


### JSON

<pre>
"Resources" : {
    "MyVar" : {
        "Type" : "Nordcloud::Dataprovider::Variable"
        "Metadata": {
            "Content": "Value is stored in Metadata Content attribute. No Properties are set."
        }
    }
},

"Outputs": {
    "Output": {
        "Description": "Content of MyVar",
        "Value": { "Fn::GetAtt" : [ "MyVar", "Content" ] }
    }
}
</pre>

### YAML

<pre>
Resources:
  MyVar:
    Type: Nordcloud::Dataprovider::Variable
    Metadata:
      Content: Value is stored in Metadata Content attribute. No Properties are set.

Outputs:
  Output:
    Description: Content of MyVar
    Value: !GetAtt MyVar.Content
</pre>