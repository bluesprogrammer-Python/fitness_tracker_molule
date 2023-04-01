from typing import Dict, Type


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str, duration: float,
                 distance: float, speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65
    MIN_IN_H = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
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
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    K_CAL_1 = 18
    K_CAL_2 = 20
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        time_min = self.duration * self.MIN_IN_H
        return ((self.K_CAL_1 * self.get_mean_speed() - self.K_CAL_2)
                * self.weight / self.M_IN_KM * time_min)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    K_CAL_1 = 0.035
    K_CAL_2 = 0.029
    K_SPEED = 2

    def __init__(self, action, duration,
                 weight, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        time_min = self.duration * self.MIN_IN_H
        walk_speed = self.get_mean_speed()
        return (self.K_CAL_1 * self.weight + (walk_speed**self.K_SPEED
                // self.height) * self.K_CAL_2 * self.weight) * time_min


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    K_CAL_1 = 1.1
    K_CAL_2 = 2

    def __init__(self, action, duration, weight,
                 length_pool: float, count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        time_h = self.duration
        return self.length_pool * self.count_pool / self.M_IN_KM / time_h

    def get_spent_calories(self) -> float:
        speed_km_h = self.get_mean_speed()
        return (speed_km_h + self.K_CAL_1) * self.K_CAL_2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    storage: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}
    if workout_type in storage and data:
        return storage[workout_type](*data)
    else:
        raise KeyError('Fail input')


def main(training: Training) -> None:
    """Главная функция."""
    return print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),

    ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
