from decouple import config

AWS_ACCESS_KEY_ID_ = config('AWS_ACCESS_KEY_ID', default='')
AWS_SECRET_ACCESS_KEY_ = config('AWS_SECRET_ACCESS_KEY', default='')
REGION_ = config('AWS_REGION', default='')
SNS_ARN_ = config('SNS_ARN', default='')
