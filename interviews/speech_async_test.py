# [START speech_transcribe_async]
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
import io
from IPython import embed

 
def recognize(local_file_path):

    client = speech_v1.SpeechClient()

    # The language of the supplied audio
    language_code = "ko-KR"

    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 8000

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    audio_channel_count=1
    encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    config = {
        "language_code": language_code,
        "sample_rate_hertz": sample_rate_hertz,
        "encoding": encoding,
        "audio_channel_count":audio_channel_count,
    }
    with io.open(local_file_path, "rb") as f:
        content = f.read()
    audio = {"content": content}

    operation = client.long_running_recognize(config, audio)

    print(u"Waiting for operation to complete...")
    response = operation.result()
    for result in response.results:
        alternatives = result.alternatives
        for alternative in alternatives:
            # alternative = result.alternatives[0]
            print(u"Transcript: {}".format(alternative.transcript))
            print(u"Confidence: {}".format(alternative.confidence))

# [END speech_transcribe_async]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        # default = 음성 파일 경로 
        "--local_file_path", type=str, default="resources/speech.wav"
    )
    args = parser.parse_args()

    recognize(args.local_file_path)


if __name__ == "__main__":
    main()