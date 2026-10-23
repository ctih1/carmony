import obd
import time


class OBDHandler:
    def __init__(self):
        self.connection = obd.OBD("COM6")  # auto-connects to USB or RF port
        self.speed = 0
        self.rpm = 0
        self.throttle = 0

    def get_speed(self):
        cmd = obd.commands.SPEED  # select an OBD command (sensor)
        response = self.connection.query(
            cmd
        )  # send the command, and parse the response
        if response.is_null():
            return self.speed
        a = response.value.magnitude  # user-friendly unit conversions
        self.speed = a
        return a

    def get_rpm(self):
        cmd = obd.commands.RPM  # select an OBD command (sensor)
        response = self.connection.query(
            cmd
        )  # send the command, and parse the response
        if response.is_null():
            return self.rpm
        a = response.value.magnitude
        self.rpm = a
        return a

    def get_throttle(self, min: float, max: float):
        cmd = obd.commands.THROTTLE_ACTUATOR
        response = self.connection.query(cmd)
        if response.is_null():
            return self.throttle
        self.throttle = response.value.magnitude
        return self.throttle / 100
