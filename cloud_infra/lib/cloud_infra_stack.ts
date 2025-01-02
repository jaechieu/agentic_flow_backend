import * as cdk from 'aws-cdk-lib';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as path from 'path';
import { PythonFunction } from '@aws-cdk/aws-lambda-python-alpha';
import { RestApi, LambdaIntegration, Cors } from 'aws-cdk-lib/aws-apigateway';
import { Construct } from 'constructs';

export class CloudInfraStack extends cdk.Stack {
    constructor(scope: Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        // Define the Lambda function for node types
        const nodeTypesLambda = new PythonFunction(this, 'NodeTypesLambda', {
            runtime: cdk.aws_lambda.Runtime.PYTHON_3_11,
            entry: path.join(__dirname, 'llm_lambda'),
            index: 'index.py',
            handler: 'lambda_handler',
            environment: {
                ENV: process.env.ENV || 'production',
            },
        });

        // Create API Gateway
        const api = new RestApi(this, 'NodeTypesApi', {
            restApiName: 'Node Types API',
            defaultCorsPreflightOptions: {
                allowOrigins: Cors.ALL_ORIGINS,
                allowMethods: Cors.ALL_METHODS,
                allowHeaders: ['Content-Type'],
            }
        });

        // Create /node-types endpoint
        const nodeTypes = api.root.addResource('node-types');
        nodeTypes.addMethod('GET', new LambdaIntegration(nodeTypesLambda));

        // Add CloudFormation output for the API URL
        new cdk.CfnOutput(this, 'ApiUrl', {
            value: api.url,
            description: 'API Gateway URL',
        });
    }
}
