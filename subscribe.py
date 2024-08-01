from connection import sns_client
import environtment as E

register_subscription = sns_client.subscribe(
    TopicArn=E.SNS_ARN_,
    Protocol="email",
    Endpoint="hdballestan@unal.edu.co",
    ReturnSubscription=True
)


