from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../service-account-key.json"


def transcribe_streaming_voice_activity_events(project_id: str, audio_file: str) -> cloud_speech.StreamingRecognizeResponse:
    """Transcribes audio from a file into text.

    Args:
        project_id: The GCP project ID to use.
        audio_file: The path to the audio file to transcribe.

    Returns:
        The streaming response containing the transcript.
    """
    # Instantiates a client
    client = SpeechClient()

    # Reads a file as bytes
    with open(audio_file, "rb") as f:
        content = f.read()

    # In practice, stream should be a generator yielding chunks of audio data
    chunk_length = len(content) // 5
    stream = [
        content[start: start + chunk_length]
        for start in range(0, len(content), chunk_length)
    ]
    audio_requests = (
        cloud_speech.StreamingRecognizeRequest(audio=audio) for audio in stream
    )

    recognition_config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=["en-US"],
        model="long",
    )

    # Sets the flag to enable voice activity events
    streaming_features = cloud_speech.StreamingRecognitionFeatures(
        enable_voice_activity_events=True
    )
    streaming_config = cloud_speech.StreamingRecognitionConfig(
        config=recognition_config, streaming_features=streaming_features
    )

    config_request = cloud_speech.StreamingRecognizeRequest(
        recognizer=f"projects/{project_id}/locations/global/recognizers/_",
        streaming_config=streaming_config,
    )

    def requests(config: cloud_speech.RecognitionConfig, audio: list) -> list:
        yield config
        yield from audio

    # Transcribes the audio into text
    responses_iterator = client.streaming_recognize(
        requests=requests(config_request, audio_requests)
    )
    responses = []
    for response in responses_iterator:
        responses.append(response)
        if (
                response.speech_event_type
                == cloud_speech.StreamingRecognizeResponse.SpeechEventType.SPEECH_ACTIVITY_BEGIN
        ):
            print("Speech started.")
        if (
                response.speech_event_type
                == cloud_speech.StreamingRecognizeResponse.SpeechEventType.SPEECH_ACTIVITY_END
        ):
            print("Speech ended.")
        for result in response.results:
            print(f"Transcript: {result.alternatives[0].transcript}")

    return responses




if __name__ == "__main__":
    project_id = "voiceanalysisproject"
    # audio_file = "../audio/1ch-mono.wav"
    audio_file = "../audio/addf8-Alaw-GW16PCM.wav"
    responses = transcribe_streaming_voice_activity_events(project_id, audio_file)

    # Print the final transcripts
    for response in responses:
        for result in response.results:
            print(f"Final Transcript: {result.alternatives[0].transcript}")
