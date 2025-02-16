# Esha Lohiya - Call Transcript Summarizer

## Overview
The Call Transcript Summarizer is a project that transcribes  audio files and generates concise summaries using AWS services and language models. It automates the extraction of insights from conversations, reducing manual effort.

## Features
- **Automated Transcription**: Uses AWS Transcribe to convert speech to text.
- **Summarization with LLM**: Leverages AWS Bedrock (Anthropic Claude) to summarize transcripts.
- **S3 Integration**: Retrieves and processes transcript files from AWS S3.
- **Real-time Processing**: Continuously checks job status for efficient transcription.

## Technology Stack
- **AWS Services**: Transcribe, S3, Bedrock
- **Programming Language**: Python
- **Libraries**: Boto3, JSON

## Installation & Usage
### Prerequisites
- AWS Account with permissions for Transcribe, S3, and Bedrock
- Python 3.x installed
- AWS CLI configured with appropriate credentials
- Dependencies installed using:
   ```sh
   pip install boto3
  
### Running the Project
1. Upload your audio file to an S3 bucket.
2. Update media_uri in the script with your S3 file path.
3. Run the script:
   ```sh
   python main.py
4. Retrieve the generated summary from the console output.

## Modifications
- The script allows customization for different audio formats (mp3, wav, etc.). 
- The summary generation can be fine-tuned using different AWS Bedrock models. 
- Users can modify inference configurations to adjust summarization length and detail.