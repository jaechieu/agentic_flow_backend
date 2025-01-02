import * as cdk from 'aws-cdk-lib';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as lambda from '@aws-cdk/aws-lambda-python-alpha';
import { Construct } from 'constructs';

export class MyStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Create API Gateway
    const api = new apigateway.RestApi(this, 'MyApi', {
      restApiName: 'My API Service',
      description: 'API Gateway for Python Lambdas',
    });

    // Define GET Lambda
    const getLambda = new lambda.PythonFunction(this, 'GetHandler', {
        entry: 'lambdas/get_handler', // Directory containing app.py and requirements.txt
        runtime:  cdk.aws_lambda.Runtime.PYTHON_3_11,
      });

    // Add GET endpoint under /get route
    const getIntegration = new apigateway.LambdaIntegration(getLambda);
    api.root.addResource('get').addMethod('GET', getIntegration);
    

    // Define POST Lambda
    const postLambda = new lambda.PythonFunction(this, 'PostHandler', {
        entry: 'lambdas/post_handler',
        runtime:  cdk.aws_lambda.Runtime.PYTHON_3_11,
      });
    // Add POST endpoint under /post route
    const postIntegration = new apigateway.LambdaIntegration(postLambda);
    api.root.addResource('post').addMethod('POST', postIntegration);
  }
}
