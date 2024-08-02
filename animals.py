from datetime import datetime
from typing import Optional

animal_data = [
    ('Lion', 'yellow', '01-01-2000'),
    ('Eagle', 'grey', '05-12-2010'),
    ('Snake', 'red', '23-09-2015')
]


class MyAnimal:
    def __init__(self, name, color, birth_date):
        self.name = name
        self.color = color
        self.birth_date = datetime.strptime(birth_date, '%d-%m-%Y').date()

    @classmethod
    def create_animals(cls, animal_data: Optional[list] = None):
        data = animal_data or []
        return [MyAnimal(*animal_tuple) for animal_tuple in data]


def print_animals_data(animals_data):
    for animal in animals_data:
        print(f"Name: {animal.name} Color: {animal.color} Birth: {animal.birth_date}")


def main():
    animals = MyAnimal.create_animals(animal_data)
    print_animals_data(animals)


if __name__ == "__main__":
    main()
