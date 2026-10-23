import obd
import time


conn = obd.OBD()
while True:
    commands = [obd.commands.THROTTLE_POS, obd.commands.RELATIVE_THROTTLE_POS, obd.commands.THROTTLE_POS_B, obd.commands.THROTTLE_POS_C, obd.commands.ACCELERATOR_POS_D, obd.commands.ACCELERATOR_POS_E, obd.commands.ACCELERATOR_POS_F, obd.commands.THROTTLE_ACTUATOR]
    for i, command in enumerate(commands):
        try:
            response = conn.query(command)

            print(response.value.magnitude)
        except Exception as _:
            continue

    time.sleep(0.10)
