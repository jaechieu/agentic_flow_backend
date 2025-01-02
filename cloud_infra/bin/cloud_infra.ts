#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { CloudInfraStack } from '../lib/cloud_infra_stack';

const app = new cdk.App();
new CloudInfraStack(app, 'CloudInfraStack');
