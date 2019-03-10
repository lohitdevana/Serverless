import json
import boto3
from botocore.client import Config
import StringIO
import zipfile
import mimetypes


def lambda_handler(event, context):
    s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))
    sns = boto3.resource('sns')
    topic = sns.Topic ('arn:aws:sns:us-east-1:993318415470:deploynotification')

    location = {
        "bucketName":'resumebuild.lohitdevana.info',
        "objectKey": 'resumebuild.zip'
    }

    try:
        job = event.get("codepipeline.job")

        if job:
            for artifact in job["data"]["inputArtifacts"]:
                if artifact["name"] == "BuildApp":
                     location = artifact ["location"]["s3location"]

        print "building the code " + str(location)
        #assigning  variables
        resume_lohitdevana = s3.Bucket('resume.lohitdevana.info')
        build_lohitdevana = s3.Bucket('resumebuild.lohitdevana.info')


        #store the contents of the zip file in memory
        resume_zip = StringIO.StringIO()
        build_lohitdevana.download_fileobj(location["objectKey"], resume_zip)

        build_lohitdevana.download_fileobj('resumebuild.zip', resume_zip)
        #opens each file and upload them to the
        with zipfile.ZipFile(resume_zip) as myzip:
            for nm in myzip.namelist():
                obj=myzip.open(nm)
                resume_lohitdevana.upload_fileobj(obj, nm, ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                resume_lohitdevana.Object(nm).Acl().put(ACL = 'public-read')
        topic.publish(Subject="Deployment Notification- Success", Message="A new commit has been made and code is deployed succeffully")
        if job:
            codepipeline = boto3.client('codepipeline')
            codepipeline.put_job_success_result(jobId=job["id"])
    except:
        topic.publish(Subject="Deployment Notification- Failure", Message="A new commit has been made and code is deployment has failed")
        raise

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
