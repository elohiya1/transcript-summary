import json
import boto3
import datetime
import time

# Initialize the AWS clients
transcribe = boto3.client('transcribe')
s3 = boto3.client('s3')
bedrock = boto3.client("bedrock-runtime")

# Define job parameters
job_name = "MyTranscriptionJob" + "-" + str(datetime.datetime.now().timestamp())
media_uri = "s3://esha-transcribe/input/test-transcribe.m4a"  # Replace with your file's S3 URL
output_bucket = "esha-transcribe"  # (Optional) If you want to store the result in an S3 bucket

# Start the transcription job
transcribe.start_transcription_job(
    TranscriptionJobName=job_name,
    Media={'MediaFileUri': media_uri},
    MediaFormat='mp3',  # Change to mp4, wav, flac, etc.
    LanguageCode='en-US',  # Change based on your file's language
    OutputBucketName=output_bucket  # Optional: Saves transcript to this bucket
)

# Wait for the job to complete
while True:
    job = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    status = job['TranscriptionJob']['TranscriptionJobStatus']
    if status in ['COMPLETED', 'FAILED']:
        break
    print("Waiting for transcription to complete...")
    time.sleep(10)

# Retrieve transcript URL
if status == "COMPLETED":
    transcript_url = job['TranscriptionJob']['Transcript']['TranscriptFileUri']
    print(f"Transcription completed. Download the transcript from: {transcript_url}")
    # Extract bucket name and object key from S3 URL
    s3_path = transcript_url.replace("https://", "").split("/")
    bucket_name = s3_path[1]
    print(bucket_name)
    object_key = s3_path[2]
    print(object_key)
    # Download transcript file
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    transcript_data = json.loads(response["Body"].read().decode("utf-8"))
    # Extract text
    transcript_text = transcript_data["results"]["transcripts"][0]["transcript"]
    print("Transcript Text:\n", transcript_text)

    # Call LLM Model (Anthropic Claude) in AWS Bedrock
    llm_input = "Summarize this transcript:\n{transcript_text}"
    response = bedrock.invoke_model(
        modelId="amazon.nova-micro-v1:0",
        contentType="application/json",
        accept="application/json",
        body=json.dumps({
            "inferenceConfig": {"max_new_tokens": 1000},
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"text": f"Summarize this transcript in three sentences:\n{transcript_text}"}
                    ]
                }
            ]
        })
    )

    summary = response["body"].read().decode("utf-8")
    summary_text = json.loads(summary)['output']['message']['content'][0]['text']
    print("Summary text:\n", summary_text)

else:
    print("Transcription failed.")


