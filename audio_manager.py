import os
from dataclasses import dataclass
from collections import deque
import time

import pygame
from pygame.mixer import Channel, Sound

try:
    import ctypes

    kernel32 = ctypes.windll.kernel32
    h_out = kernel32.GetStdHandle(-11)

    dw_mode = ctypes.c_ulong()
    kernel32.GetConsoleMode(h_out, ctypes.byref(dw_mode))

    dw_mode.value |= 0x0004
    kernel32.SetConsoleMode(h_out, dw_mode)

except Exception as _:
    pass


@dataclass
class Settings:
    engine_max_rpm: int
    engine_low_rpm: int
    max_speed: int


@dataclass
class AudioType:
    sound: Sound
    channel: Channel


@dataclass
class Audios:
    bass: AudioType
    drums: AudioType
    vocals: AudioType
    misc: AudioType


@dataclass
class CarStatus:
    speed_kmh: int
    engine_rpm: int
    throttle_percentage: float
    brake_percentage: float
    clutch_depression_percentage: float
    settings: Settings


def keep_between_0_1(val: float) -> float:
    return max(min(val, 1), 0)


class AudioManager:
    def __init__(self, paths_alph_order: list[str]):
        os.system("cls")
        pygame.mixer.init()
        pygame.mixer.set_num_channels(4)

        p = paths_alph_order
        self.audios = Audios(
            bass=AudioType(
                channel=pygame.mixer.Channel(0), sound=pygame.mixer.Sound(p[0])
            ),
            drums=AudioType(
                channel=pygame.mixer.Channel(1), sound=pygame.mixer.Sound(p[1])
            ),
            misc=AudioType(
                channel=pygame.mixer.Channel(2), sound=pygame.mixer.Sound(p[2])
            ),
            vocals=AudioType(
                channel=pygame.mixer.Channel(3), sound=pygame.mixer.Sound(p[3])
            ),
        )

        self.audio_started: bool = False
        self.speeds: deque[tuple[float, float]] = deque(maxlen=10)
        self.last_call_time = time.time()

    def process_audio(self, car_status: CarStatus):
        if not self.audio_started:
            for audio in [
                self.audios.bass,
                self.audios.drums,
                self.audios.misc,
                self.audios.vocals,
            ]:
                audio.channel.play(audio.sound, loops=-1)
                self.audio_started = True

        self.speeds.append((time.time(), car_status.speed_kmh))

        acceleration = 0

        if len(self.speeds) == self.speeds.maxlen:
            first_point = self.speeds[0]
            recent_point = self.speeds[1]

            acceleration = (
                (recent_point[1] - first_point[1])
                / (recent_point[0] - first_point[0])
                / 3.6
            )

        speed_percentage: float = car_status.speed_kmh / car_status.settings.max_speed
        added_throttle_sound: float = (
            keep_between_0_1(car_status.throttle_percentage) / 10
        )
        rpm_percentage: float = (
            car_status.engine_rpm - car_status.settings.engine_low_rpm
        ) / (car_status.settings.engine_max_rpm - car_status.settings.engine_low_rpm)

        added_rpm_sound: float = (keep_between_0_1(rpm_percentage)) / 5

        self.audios.misc.channel.set_volume(
            keep_between_0_1(
                keep_between_0_1(rpm_percentage + 0.3 + added_throttle_sound)
            )
        )
        self.audios.vocals.channel.set_volume(
            keep_between_0_1(
                keep_between_0_1(speed_percentage + rpm_percentage * 0.6 - 0.3)
            )
        )

        self.audios.drums.channel.set_volume(
            keep_between_0_1(
                (speed_percentage + car_status.throttle_percentage * 0.1)
                + (keep_between_0_1(acceleration - speed_percentage) * 0.2)
                - ((1 - speed_percentage) / 2)
            )
        )

        self.audios.bass.channel.set_volume(
            keep_between_0_1(
                keep_between_0_1(
                    speed_percentage
                    + (car_status.throttle_percentage**2) * 0.1
                    + added_rpm_sound * 2
                    + (acceleration / 10) ** 2
                )
                - ((1 - speed_percentage**2))
            )
        )

        self.print_status(car_status, acceleration)

    def print_status(self, status: CarStatus, accel: float):
        print("\033[6A\033[2K", end="")
        print(
            f"Bass: {self.audios.bass.channel.get_volume()}\nDrums: {self.audios.drums.channel.get_volume()}\nMisc: {self.audios.misc.channel.get_volume()}\nVoice: {self.audios.vocals.channel.get_volume()}"
        )
        print(
            f"\nThrottle: {round(status.throttle_percentage*100)}%, speed: {round(status.speed_kmh)}kmh, Acceleration: {round(accel)}mss, Engine RPM: {round(status.engine_rpm)}rpm, clutch: {round(status.clutch_depression_percentage*100)}, brake: {round(status.brake_percentage)}"
        )
