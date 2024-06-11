import speech_recognition as sr
import zmq
import sys
import datetime


class SpeechToText:
    """
      Speech-to-text module class.
    """

    def __init__(self, port):
        """
          Constructor of the class.
          Args:
            port (int): port of the server
          Returns:
            None
        """

        self.socket = None
        self.port = port
        self.zmqctx = zmq.Context()
        self.run_server()
        self.r = sr.Recognizer()
        self.m = sr.Microphone()
        self.threshold = 110

    def run_server(self):
        """
          Runs the ZMQ server.
          Returns:  None
        """
        # bind the port
        self.socket = self.zmqctx.socket(zmq.REP)
        print(f"Going to listen at port:{port}!")
        self.socket.bind('tcp://127.0.0.1:{}'.format(port))
        print(f"Listening at port:{port}!")

    def listen(self):
        """
          Listens on the port.
          Returns:
            None
        """
        while True:
            # wait for request
            # message = self.socket.recv_json()

            # config = message['config']
            # data = message['data']
            # timestamp = message['timestamp']
            #
            # # save config
            # if bool(config):
            #     config_saved = self.saveConfig(config)
            # else:
            #     # no config send
            #     config_saved = True
            #
            # # do what is needed with the data
            # if bool(data):
            reply_data = self.application("message")
            # else:
            #     # no data send
            #     reply_data = {}

            # prepare data before send
            reply_timestamp = datetime.datetime.now().isoformat(' ')
            reply = {'timestamp': reply_timestamp, 'data': reply_data, 'config': {}}
            # if config_saved:
            reply['config']['state'] = 'accepted'
            # else:
            #     reply['config']['state'] = 'failed'

            # send back reply
            # self.socket.send_json(reply)

    def application(self, message):
        """
          Main application logic of the module.
          Args:
            message (dict): received data as a dictionary
          Returns:
            dict: data to send back as dictionary
        """

        self.r.energy_threshold = self.threshold
        print("Set minimum energy threshold to {}".format(self.r.energy_threshold))

        print("Say!")
        with self.m as source:
            audio = self.r.listen(source)
        print("Got it! Now to recognize it...")
        try:
            # recognize speech using Google Speech Recognition
            value = self.r.recognize_google(audio)

            # we need some special handling here to correctly print unicode characters to standard output
            if str is bytes:  # this version of Python uses bytes for strings (Python 2)
                message = u"{}".format(value).encode("utf-8")
            else:  # this version of Python uses unicode for strings (Python 3+)
                message = "{}".format(value)
        except sr.UnknownValueError:
            message = "Oops! Didn't catch that"
        except sr.RequestError as e:
            message = "Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e)
        print(message)
        # return result
        # return {'request': message}

    def save_config(self, config):
        """
          Saves config received from the kernel.
          Args:
            config (dict): received config
          Returns:
            bool: True if config successuflly saved, False is not
        """
        thresh = config['threshold']
        self.threshold = thresh
        return True


if __name__ == '__main__':
    # port = sys.argv[1]
    port = "5555"
    port = int(port)
    dm = SpeechToText(port)
    print("Say something!")
    dm.listen()
