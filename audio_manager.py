import os
from dataclasses import dataclass

import pygame
from pygame.mixer import Channel, Sound


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
    settings: Settings


def keep_between_0_1(val: float) -> float:
    return max(min(val, 1), 0)


class AudioManager:
    def __init__(self, paths_alph_order: list[str]):
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

        speed_percentage: float = car_status.speed_kmh / car_status.settings.max_speed
        added_throttle_sound: float = (
            keep_between_0_1(car_status.throttle_percentage) / 10
        )
        rpm_percentag: float = (
            car_status.engine_rpm - car_status.settings.engine_low_rpm
        ) / (car_status.settings.engine_max_rpm - car_status.settings.engine_low_rpm)
        added_rpm_sound: float = (keep_between_0_1(rpm_percentag)) / 10

        self.audios.bass.channel.set_volume(
            keep_between_0_1(rpm_percentag + 0.3 + added_throttle_sound)
        )
        self.audios.drums.channel.set_volume(
            keep_between_0_1(speed_percentage + added_throttle_sound * 2 - 0.4)
        )

        self.audios.misc.channel.set_volume(
            keep_between_0_1(
                (speed_percentage * 0.3 + car_status.throttle_percentage * 0.7)
                - ((1 - speed_percentage) / 2)
            )
        )

        self.audios.vocals.channel.set_volume(
            keep_between_0_1(
                speed_percentage * 0.3 + car_status.throttle_percentage * 0.7
            )
            + added_rpm_sound
        )

        print(
            f"Ba:{self.audios.bass.channel.get_volume()};Dr:{self.audios.drums.channel.get_volume()};Ms:{self.audios.misc.channel.get_volume()};Vc:{self.audios.vocals.channel.get_volume()}"
        )
