from dataclasses import dataclass, asdict
from typing import Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE = ('Тип тренировки: {training_type};'
               ' Длительность: {duration:0.3f} ч.;'
               ' Дистанция: {distance:0.3f} км;'
               ' Ср. скорость: {speed:0.3f} км/ч;' 
               ' Потрачено ккал: {calories:0.3f}.')

    def get_message(self):
        return (self.MESSAGE.format(**asdict(self)))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MINUTES_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определите get_spent_calories в %s.' %
                                  (self.__class__.__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * self.duration * self.MINUTES_IN_HOUR)


class SportsWalking(Training):
    CALORIES_MEAN_SPEED_SPORTS_WALKING: float = 0.035
    CALORIES_MEAN_SPEED_SPORTS_WALKING_2: float = 0.029
    KMH_IN_MS: float = 0.278
    SM_IN_M: int = 100

    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((
                self.CALORIES_MEAN_SPEED_SPORTS_WALKING
                * self.weight
                + (self.get_mean_speed() * self.KMH_IN_MS)**2
                / self.height * self.SM_IN_M
                * self.CALORIES_MEAN_SPEED_SPORTS_WALKING_2
                * self.weight)
                * self.duration
                * self.MINUTES_IN_HOUR)


class Swimming(Training):
    LEN_STEP: float = 1.38
    COEF_1: float = 1.1
    COEF_2: int = 2
    """Тренировка: плавание."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.COEF_1) * self.COEF_2
                * self.weight * self.duration)


def read_package(workout_type: Type[Training],
                 data: Type[Training]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return workout[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        if (workout_type != 'SWM'
           and workout_type != 'RUN' and workout_type != 'WLK'):
            print('Неверный тип тренировки')
            break

        main(training)
