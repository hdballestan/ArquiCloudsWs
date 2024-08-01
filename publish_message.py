from connection import sns_client
import environment as E

message = sns_client.publish(
    TopicArn=E.SNS_ARN_,
    Message="This is a test",
    Subject="Hello"
)
