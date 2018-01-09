# Import the base64 encoding library.
import base64

# Pass the audio data to an encoding function.
def encode_audio(audio):
  audio_content = audio.read()
  return base64.b64encode(audio_content)

if __name__ == '__main__':
    f = open('/home/pi/robodex/human_comment.wav')
    print(encode_audio(f))
