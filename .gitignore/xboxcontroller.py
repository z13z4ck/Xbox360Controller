import inputs
import time
from inputs import devices
devices.gamepads
from inputs import get_gamepad


def mapFromTo(x,a,b,c,d):
    """
        x:input value; 
        a,b:input range
        c,d:output range
        y:return interger value
    """
    y=(x-a)/(b-a)*(d-c)+c
    return int(y)


class ControllerSocket:
    def __init__(self):
        self.host = '192.168.0.165'
        self.port = 5050
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def send_data(self, data):
        self.sock.send(data)

    def socket_close(self):
        self.sock.close()   

class JoyStick:
    def __init__(self):
        print(devices.gamepads)
        self._control = ControllerSocket()
        self.parseval = 0
        self.parsethrottle = 0
        self.parsestering = 0
    
    def runjoystick(self):
        while True:
            try:
                events = get_gamepad()
                for event in events:
                    # print(event.ev_type + '---' + event.code + '---' + str(event.state) + '\n')
                    
                    if event.code == 'ABS_X':
                        _val = mapFromTo(event.state,-32768,32768,-100,100)
                        self.parsestering = _val
                        
                        
                    if event.code == 'ABS_RZ':
                        _val = mapFromTo(event.state,-255,255,-100,100)
                        self.parsethrottle = _val
                    
                    # print ("Throttle = %d" % self.parsethrottle + "\tSteering = %d \n" % self.parsestering)
                    _control.send_data(b'collect, ' + str(int(self.parsethrottle)).encode() + b', ' + str(int(self.parsestering)).encode())
            except KeyboardInterrupt:
                print("[!] Exiting..!")
                _control.socket_close()
                exit()
        

if __name__ == "__main__":
    """
    Receive input from controller and send data to RPI/lattecar
    :return: None
    """
    joystick = JoyStick()
    joystick.runjoystick()