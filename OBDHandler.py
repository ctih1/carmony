import obd
import time


class OBDHandler:
    def __init__(self):
        self.connection = obd.OBD("COM6")  # auto-connects to USB or RF port
        self.speed = 0
        self.rpm = 0

    def get_speed(self):
        cmd = obd.commands.SPEED  # select an OBD command (sensor)
        response = self.connection.query(
            cmd
        )  # send the command, and parse the response
        return response.value.magnitude  # user-friendly unit conversions

    def get_rpm(self):
        cmd = obd.commands.RPM  # select an OBD command (sensor)
        response = self.connection.query(
            cmd
        )  # send the command, and parse the response
        return response.value.magnitude  # user-friendly unit conversions

    def get_throttle(self, min: int, max: int):
        cmd = obd.commands.THROTTLE_POS
        response = self.connection.query(cmd)
        current_val = response.value.magnitude
        return (current_val - min) / (max - min)
