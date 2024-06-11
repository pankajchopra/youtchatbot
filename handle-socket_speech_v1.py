import asyncio
import base64
import websockets
import os
import sounddevice as sd
from getAudioBytes import  read_wav_using_pydub as rwup

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../service-account-key.json"
#C:\Users\panka\PycharmProjects\youtChatbot\service-account-key.json
from google.cloud import speech

#API-KEY=AIzaSyB5CrN6lXMVYohR7_GobAiJ8N1zdZr6TSI

# Initialize the Vertex AI Speech-to-Text client
speech_client = speech.SpeechClient()


async def handle_websocket(websocket):
    async for message in websocket:

        audio_data = message
        with open("audio.wav", 'wb') as f:
            while True:
                try:
                    # data = await websocket.recv()
                    if isinstance(audio_data, bytes):
                        f.write(audio_data)
                    else:
                        print("Received non-binary data: ", audio_data)
                except websockets.ConnectionClosed:
                    print("Connection closed")
                    break

        rwup("audio.wav")
        print(f"Received audio data: {audio_data[:20]}...")

        audio_file = speech.RecognitionAudio(content=audio_data)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code="en-US"


        )
        print(f"Pankaj- config is {config} ")
        # print("Pankaj- audio-data is {}".format(base64.b64decode(audio_data_base64)))
        response = speech_client.recognize(config=config, audio=audio_file)
        print(f"Pankaj- after sending audio file response is {response.results}")
        # Get the transcribed text from the API response

        for i, result in enumerate(response.results):
            alternative = result.alternatives[i]
            print("-" * 20)
            print(u"First alternative of result {}".format(i))
            transcribed_text = format(alternative.transcript)
            print(u"Transcript: {}".format(alternative.transcript))
            print(f'transcribed_text={transcribed_text}')
            # Send the transcribed text back to the front-end
            await websocket.send(transcribed_text)


async def main():
    # Create a new event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    start_server = websockets.serve(handle_websocket, "localhost", 8765)

    await start_server
    await asyncio.Future() # run forever

if __name__ == "__main__":
    asyncio.run(main())

# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()