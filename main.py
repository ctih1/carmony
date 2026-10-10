import time

import keyboard
import pygame

from audio_manager import AudioManager, CarStatus, Settings, keep_between_0_1

a = AudioManager(
    ["assets/bass.mp3", "assets/drums.mp3", "assets/other.mp3", "assets/vocals.mp3"]
)

# speed = 0
# rpm = 0
# rpm_velocity = 0

# pygame.display.init()
# pygame.joystick.init()
# joystick = pygame.joystick.Joystick(0)
# while True:
#     pygame.event.pump()
#     trigger_val = (joystick.get_axis(5) + 1) / 2
#     rpm += (trigger_val * 40) - 5
#     rpm = max(min(rpm, 6800), 0)
#     speed += (trigger_val * 4) - 0.5
#     speed = max(min(speed, 200), 0)

#     print(f"{round(trigger_val * 100)}%,{round(rpm)}rpm,{round(speed)}kmh")

#     a.process_audio(
#         CarStatus(
#             engine_rpm=round(rpm),
#             speed_kmh=round(speed),
#             throttle_percentage=trigger_val,
#             settings=Settings(engine_max_rpm=6500, max_speed=120),
#         )
#     )

#     time.sleep(1 / 60)

rpm = 6500
kmh = 0
throttle = 0.0


def set_stuff(rpm_=None, kmh_=None, throttle_=None):
    global rpm, kmh, throttle

    if rpm_ is not None:
        rpm = rpm_

    if kmh_ is not None:
        kmh = kmh_

    if throttle_ is not None:
        throttle = throttle_


keyboard.on_press_key("1", lambda _: set_stuff(rpm_=6500))
keyboard.on_press_key("q", lambda _: set_stuff(rpm_=4000))
keyboard.on_press_key("a", lambda _: set_stuff(rpm_=1800))
keyboard.on_press_key("z", lambda _: set_stuff(rpm_=900))

keyboard.on_press_key("2", lambda _: set_stuff(kmh_=120))
keyboard.on_press_key("w", lambda _: set_stuff(kmh_=70))
keyboard.on_press_key("s", lambda _: set_stuff(kmh_=40))
keyboard.on_press_key("x", lambda _: set_stuff(kmh_=0))

keyboard.on_press_key("3", lambda _: set_stuff(throttle_=1.0))
keyboard.on_press_key("e", lambda _: set_stuff(throttle_=0.7))
keyboard.on_press_key("d", lambda _: set_stuff(throttle_=0.4))
keyboard.on_press_key("c", lambda _: set_stuff(throttle_=0.0))

keyboard.on_press_key("4", lambda _: set_stuff(throttle_=1.0, kmh_=120, rpm_=6300))
keyboard.on_press_key("5", lambda _: set_stuff(throttle_=0.5, kmh_=110, rpm_=1900))
keyboard.on_press_key("6", lambda _: set_stuff(throttle_=1.0, kmh_=100, rpm_=3800))
keyboard.on_press_key("7", lambda _: set_stuff(throttle_=0.4, kmh_=90, rpm_=1500))
keyboard.on_press_key("8", lambda _: set_stuff(throttle_=0.4, kmh_=60, rpm_=1400))
keyboard.on_press_key("9", lambda _: set_stuff(throttle_=0.3, kmh_=30, rpm_=1800))
keyboard.on_press_key("0", lambda _: set_stuff(throttle_=0.0, kmh_=0, rpm_=0))


while True:
    a.process_audio(
        CarStatus(
            engine_rpm=rpm,
            speed_kmh=kmh,
            throttle_percentage=throttle,
            settings=Settings(engine_max_rpm=6500, engine_low_rpm=900, max_speed=120),
        )
    )

    time.sleep(1 / 60)
# import os
# import time

# import obd
# import pygame

# from AudioLoop import AudioLoop
# from OBDHandler import OBDHandler


# def main():
#     songname = input(
#         "Please enter the name of the folder containing the song you want to play:"
#     )
#     path = "wavs/" + songname + "/"
#     file_paths = os.listdir(path)
#     file_paths = [path + file for file in file_paths if file.lower().endswith(".wav")]
#     loop = AudioLoop(file_paths)
#     loop.start()
#     loop.adjust_volumes([0, 0, 0, 0])
#     handler = OBDHandler()

#     try:
#         while True:
#             time.sleep(0.1)
#             handler.refresh()
#             volume_list = handler.get_volumes()
#             print(volume_list)
#             loop.adjust_volumes(volume_list)

#     except KeyboardInterrupt:
#         pygame.mixer.stop()
#         pygame.quit()


# if __name__ == "__main__":
#     main()
