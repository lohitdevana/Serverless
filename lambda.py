import json
import boto3
import StringIO
import zipfile


def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    sns = boto3.resource('sns')

     try:
        #assigning  variables
        resume_lohitdevana = s3.Bucket('resume.lohitdevana.info')
        build_lohitdevana = s3.Bucket('resumebuild.lohitdevana.info')
        topic = sns.Topic ('arn:aws:sns:us-east-1:993318415470:deploynotification')

        #store the contents of the zip file in memory
        resume_zip = StringIO.StringIO()
        build_lohitdevana.download_fileobj('resumebuild.zip', resume_zip)

        #opens each file and upload them to the
        with zipfile.ZipFile(resume_zip) as myzip:
            for nm in myzip.namelist():
                obj=myzip.open(nm)
                resume_lohitdevana.upload_fileobj(obj, nm)
                resume_lohitdevana.Object(nm).Acl().put(ACL = 'public-read')
        topic.publish(Subject="Deployment Notification- Success", Message="A new commit has been made and code is deployed succeffully")
    except:
        topic.publish(Subject="Deployment Notification- Failure", Message="A new commit has been made and code is deployment has failed")
        raise

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
