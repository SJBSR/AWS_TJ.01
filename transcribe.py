import boto3
import time
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)

def start_job(
    job_name,
    media_uri,
    media_format,
    language_code,
    transcribe_client,
    vocabulary_name=None,
):
    """
    Starts a transcription hob. THis function returns as soon as the job is started.
    To get the current status of the job, call get_transcription_job. The job is successfully
    completed when the job status is 'COMPLETED'.

    :param job_name: The name of the transcription job.  This must be unifor for your AWS account.
    :param media_uri: The URI where the audio file is stored. This is typically in an Amazon S3 bucket.
    :param media_format: The format of the audio file. For example, mp3 or wav.
    :param language_code: The language code of the audio file. For example en-US or ja-JP
    :param transcribe_client: The Boto3 Transcribe client.
    :param vocabulary_name: The name of a custome vocabulary to use when transcribing the audio file.
    :return: Data about the job.
    """
    try:
        job_args = {
            "TranscriptionJobName": job_name,
            "Media": {"MediaFileUri": media_uri},
            "MediaFormat": media_format,
            "LanguageCode": language_code,
        }
        if vocabulary_name is not None:
            job_args["Settings"] = {"VocabularyName": vocabulary_name}
        response = transcribe_client.start_transcription_job(**job_args)
        job = response["TranscriptionJob"]
        logger.info("Started transcription job%s.", job_name)
        raise
    else:
        return job

def get_transcription_job(job_name, transcribe_client):
    """
    Get details about a transcription job.
    """
    try:
        response = transcribe_client.get_transcription_job(
            TranscriptionJobName=job_name
        )
        job = response["TranscriptionJob"]
        logger.info("Get job%s.", job_name)
    except ClientError:
        logger.exception("Couldn't get job %s.", job_name)