import asyncio
import os

import websockets

from transcribe_file import transcribe_streaming_voice_activity_events

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../service-account-key.json"


async def receive_audio(uri, output_file):
    async with websockets.connect(uri) as websocket:
        with open(output_file, 'wb') as f:
            while True:
                try:
                    data = await websocket.recv()
                    if isinstance(data, bytes):
                        f.write(data)
                    else:
                        print("Received non-binary data: ", data)
                except websockets.ConnectionClosed:
                    print("Connection closed")
                    break


if __name__ == "__main__":
    uri = "ws://127.0.0.1:8765"  # Replace with your WebSocket server URI
    output_file = "received_audio.wav"  # File to save the received audio

    asyncio.get_event_loop().run_until_complete(receive_audio(uri, output_file))

    project_id = "voiceanalysisproject"
    # audio_file = "../audio/1ch-mono.wav"
    audio_file = output_file
    # "../audio/addf8-Alaw-GW16PCM.wav"
    # Read and chunk the audio file
    # Transcribe the audio chunks
    responses = transcribe_streaming_voice_activity_events(project_id, audio_file)

    # Print final transcripts
    for response in responses:
        for result in response.results:
            print(f"Final Transcript: {result.alternatives[0].transcript}")
