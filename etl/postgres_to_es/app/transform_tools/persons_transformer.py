from pydantic import BaseModel


class Person(BaseModel):
    id: str
    full_name: str


class PersonsTransformer:
    def transform_persons(self, persons):
        transformed_persons = []
        for person in persons:
            transformed_person = Person(id=person['id'],
                                        full_name=person['full_name'])

            transformed_persons.append(transformed_person)

        return transformed_persons
