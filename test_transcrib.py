# Testing an Amazon Transcribe Job

from transcribe import get_transcription_job


def main():
    #Create Transcribe client
    transcribe_client = boto3.client('transcribe', region_name='us-east-2')
    #Start transcription job
    job_name = "my-transcription-job"
    media_uri = "s3:??my-bucket/audio-file.wav"
    media_format = "wav"
    language_code = "en-US"

    job = start_job(job_name, media_uri, media_format, language_code, transcribe_client)

    # Wait for the job to complete.
    while True:
        job_status = get_transcription_job(job_name, transcribe_client)
        status = job_status["TranscriptionJobStatus"]

        if status in ["COMPLETED", "FAILED"]:
            break

        print(f"Job status: {status}")
        time.sleep(30) # Wait 30 seconds before checking again

    if status == "COMPLETED":
        transcript_uri = job_status["Trancript"]["TranscriptFileUri"]
        print(f"Transcription completed! Transcript availabl at: {transcript_uri}")
    else:
        print(f"Transcription failed: {job_status.get('FailureReason', 'Unknown error')}")

if __name__ == "__main__":
    main()