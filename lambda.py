import boto3
import StringIO
import zipfile
import mimetypes

s3 = boto3.resource('s3')
#/*assigning bucket variables*/
resume_lohitdevana = s3.Bucket('resume.lohitdevana.info')
build_lohitdevana = s3.Bucket('resumebuild.lohitdevana.info')

#/*store the contents of the zip file in memory*/
resume_zip = StringIO.StringIO()
build_lohitdevana.download_fileobj('resumebuild.zip', resume_zip)

#/*opens each file and upload them to the
with zipfile.ZipFile(resume_zip) as myzip:
    for nm in myzip.namelist():
        obj=myzip.open(nm)
        resume_lohitdevana.upload_fileobj(obj, nm)
        resume_lohitdevana.Object(nm).Acl().put(ACL = 'public-read')
