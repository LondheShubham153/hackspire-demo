from aws_cdk import (
    Stack,
    CfnOutput,
    Duration,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_iam as iam,
)
from constructs import Construct

class SentimentAnalysisStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Sentiment Analysis Lambda Function
        sentiment_lambda = _lambda.Function(
            self, "SentimentAnalysisFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="sentiment_analysis.lambda_handler",
            code=_lambda.Code.from_asset("../lambda"),
            function_name="SentimentAnalysisLambda",
            timeout=Duration.seconds(30)
        )
        
        # Add Bedrock permissions
        sentiment_lambda.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["bedrock:InvokeModel"],
                resources=[
                    "arn:aws:bedrock:*::foundation-model/anthropic.*",
                    "arn:aws:bedrock:*::foundation-model/amazon.*",
                    "arn:aws:bedrock:*::foundation-model/cohere.*",
                    "arn:aws:bedrock:*::foundation-model/meta.*",
                    "arn:aws:bedrock:*::foundation-model/mistral.*"
                ]
            )
        )

        # API Gateway
        api = apigateway.RestApi(
            self, "SentimentAnalysisApi",
            rest_api_name="Sentiment Analysis API"
        )

        # Lambda integration
        sentiment_integration = apigateway.LambdaIntegration(sentiment_lambda)
        
        # Add POST method for sentiment analysis
        api.root.add_method("POST", sentiment_integration)
        
        # Add health check endpoint
        health_resource = api.root.add_resource("health")
        health_resource.add_method("GET", sentiment_integration)
        
        # Output the API Gateway URL
        CfnOutput(
            self, "ApiUrl",
            value=api.url,
            description="Sentiment Analysis API Gateway URL"
        )