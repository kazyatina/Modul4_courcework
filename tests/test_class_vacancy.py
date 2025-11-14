import unittest

from src.class_vacancy import BaseVacancy, Vacancy


def test_vacancy(init_vacancy: Vacancy, vacancy_data: dict) -> None:
    """Тест на инициализацию по фикстуре"""
    assert str(init_vacancy) == (
        "119602010 Тестировщик (QA-инженер) "
        "https://api.hh.ru/vacancies/119602010?host=hh.ru 1 - 10000 Знакомство с "
        "Postman и умение составлять API запросы. Знание основ HTML, CSS, JS, "
        "<highlighttext>Python</highlighttext>. Опыт написания тестовой документации "
        "(тест-кейсы..."
    )

    assert isinstance(Vacancy.create_vacancies([vacancy_data]), list)


class TestVacancy(unittest.TestCase):

    def test_inheritance(self) -> None:
        """Проверка, что Vacancy наследуется от BaseVacancy."""
        self.assertTrue(issubclass(Vacancy, BaseVacancy))

    def test_abstract_methods(self) -> None:
        """Проверяем наличие абстрактных методов в BaseVacancy и их наличие."""

        self.assertTrue(hasattr(BaseVacancy, "create_vacancies"))
        self.assertTrue(hasattr(BaseVacancy, "to_dict"))
        self.assertTrue(callable(BaseVacancy.create_vacancies))
        self.assertTrue(callable(BaseVacancy.to_dict))

    def test_init_valid_data(self) -> None:
        """Проверка инициализации объекта Vacancy с валидными данными."""
        vacancy = Vacancy("123", "Python Developer", "http://example.com", 100000, 150000, "Python, Django")
        self.assertEqual(vacancy.id_vacancy, "123")
        self.assertEqual(vacancy.name, "Python Developer")
        self.assertEqual(vacancy.url, "http://example.com")
        self.assertEqual(vacancy.salary_from, 100000)
        self.assertEqual(vacancy.salary_to, 150000)
        self.assertEqual(vacancy.requirement, "Python, Django")

    def test_init_invalid_data(self) -> None:
        """Проверка инициализации объекта Vacancy с невалидными данными."""
        vacancy = Vacancy(123, "", 123, "abc", -100, None)
        self.assertEqual(vacancy.id_vacancy, "ID не указан")
        self.assertEqual(vacancy.name, "Название не указано")
        self.assertEqual(vacancy.url, "URL не указан")
        self.assertEqual(vacancy.salary_from, 0)
        self.assertEqual(vacancy.salary_to, 0)
        self.assertEqual(vacancy.requirement, "Краткое описание не указано")

    def test_str(self) -> None:
        """Проверка магического метода __str__."""
        vacancy = Vacancy("123", "Python Developer", "http://example.com", 100000, 150000, "Python, Django")
        expected_string = "123 Python Developer http://example.com 100000 - 150000 Python, Django"
        self.assertEqual(str(vacancy), expected_string)

    def test_lt_valid(self) -> None:
        """Проверка магического метода __lt__ (меньше), валидные данные."""
        vacancy1 = Vacancy("1", "Dev1", "http://example.com", 100000, 150000, "req1")
        vacancy2 = Vacancy("2", "Dev2", "http://example.com", 120000, 180000, "req2")
        self.assertTrue(vacancy1 < vacancy2)
        self.assertFalse(vacancy2 < vacancy1)

    def test_lt_invalid(self) -> None:
        """Проверка магического метода __lt__ (меньше), невалидные данные."""
        vacancy = Vacancy("1", "Dev1", "http://example.com", 100000, 150000, "req1")
        other = "string"
        self.assertEqual(vacancy.__lt__(other), NotImplemented)

    def test_validate_id_vacancy(self) -> None:
        """Проверка метода validate_id_vacancy."""
        vacancy = Vacancy("123", "Python Developer", "http://example.com", 100000, 150000, "Python, Django")
        self.assertEqual(vacancy._Vacancy__validate_id_vacancy("456"), "456")
        self.assertEqual(vacancy._Vacancy__validate_id_vacancy(""), "ID не указан")
        self.assertEqual(vacancy._Vacancy__validate_id_vacancy(123), "ID не указан")  # Проверка типа

    def test_validate_name(self) -> None:
        """Проверка метода validate_name."""
        vacancy = Vacancy("123", "Python Developer", "http://example.com", 100000, 150000, "Python, Django")
        self.assertEqual(vacancy._Vacancy__validate_name("Software Engineer"), "Software Engineer")
        self.assertEqual(vacancy._Vacancy__validate_name(""), "Название не указано")
        self.assertEqual(vacancy._Vacancy__validate_name(123), "Название не указано")  # Проверка типа

    def test_validate_requirement(self) -> None:
        """Проверка метода validate_requirement."""
        vacancy = Vacancy("123", "Python Developer", "http://example.com", 100000, 150000, "Python, Django")
        self.assertEqual(vacancy._Vacancy__validate_requirement("Experience required"), "Experience required")
        self.assertEqual(vacancy._Vacancy__validate_requirement(""), "Краткое описание не указано")
        self.assertEqual(vacancy._Vacancy__validate_requirement(123), "Краткое описание не указано")  # Проверка типа

    def test_validate_salary_from(self) -> None:
        """Проверка метода validate_salary_from."""
        vacancy = Vacancy("123", "Python Developer", "http://example.com", 100000, 150000, "Python, Django")
        self.assertEqual(vacancy._Vacancy__validate_salary_from(50000), 50000)
        self.assertEqual(vacancy._Vacancy__validate_salary_from(0), 0)
        self.assertEqual(vacancy._Vacancy__validate_salary_from(-100), 0)
        self.assertEqual(vacancy._Vacancy__validate_salary_from("abc"), 0)  # Проверка типа

    def test_validate_salary_to(self) -> None:
        """Проверка метода validate_salary_to."""
        vacancy = Vacancy("123", "Python Developer", "http://example.com", 100000, 150000, "Python, Django")
        self.assertEqual(vacancy._Vacancy__validate_salary_to(200000), 200000)
        self.assertEqual(vacancy._Vacancy__validate_salary_to(0), 0)
        self.assertEqual(vacancy._Vacancy__validate_salary_to(-100), 0)
        self.assertEqual(vacancy._Vacancy__validate_salary_to("abc"), 0)  # Проверка типа

    def test_validate_site_url(self) -> None:
        """Проверка метода validate_site_url."""
        vacancy = Vacancy("123", "Python Developer", "http://example.com", 100000, 150000, "Python, Django")
        self.assertEqual(vacancy._Vacancy__validate_site_url("https://google.com"), "https://google.com")
        self.assertEqual(vacancy._Vacancy__validate_site_url("http://example.com"), "http://example.com")
        self.assertEqual(vacancy._Vacancy__validate_site_url(""), "URL не указан")
        self.assertEqual(vacancy._Vacancy__validate_site_url("example.com"), "URL не указан")
        self.assertEqual(vacancy._Vacancy__validate_site_url(123), "URL не указан")  # Проверка типа

    def test_create_vacancies(self) -> None:
        """Проверка метода create_vacancies."""
        list_hh_vacancy = [
            {
                "id": "1",
                "name": "Python Dev",
                "url": "http://example.com",
                "snippet": {"requirement": "Django"},
                "salary": {"from": 100000, "to": 150000},
            },
            {
                "id": "2",
                "name": "Java Dev",
                "url": "http://example.com",
                "snippet": {"requirement": "Spring"},
                "salary": {"from": 120000, "to": 180000},
            },
        ]
        vacancies = Vacancy.create_vacancies(list_hh_vacancy)
        self.assertEqual(len(vacancies), 2)
        self.assertIsInstance(vacancies[0], Vacancy)
        self.assertEqual(vacancies[0].id_vacancy, "1")
        self.assertEqual(vacancies[0].name, "Python Dev")
        self.assertEqual(vacancies[0].requirement, "Django")
        self.assertEqual(vacancies[0].salary_from, 100000)
        self.assertEqual(vacancies[0].salary_to, 150000)

    def test_create_vacancies_missing_fields(self) -> None:
        """Проверка метода create_vacancies с отсутствующими полями."""
        list_hh_vacancy = [
            {"id": "1", "url": "http://example.com", "snippet": {}, "salary": None}  # salary намеренно убран
        ]
        vacancies = Vacancy.create_vacancies(list_hh_vacancy)
        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0].name, "Нет названия")
        self.assertEqual(vacancies[0].requirement, "Нет requirement")  # Проверяем значение по умолчанию
        self.assertEqual(vacancies[0].salary_from, 0)
        self.assertEqual(vacancies[0].salary_to, 0)

    def test_to_dict(self) -> None:
        """Проверка метода to_dict."""
        vacancy = Vacancy("123", "Python Developer", "http://example.com", 100000, 150000, "Python, Django")
        expected_dict = {
            "id_vacancy": "123",
            "name": "Python Developer",
            "url": "http://example.com",
            "salary_from": 100000,
            "salary_to": 150000,
            "requirement": "Python, Django",
        }
        self.assertEqual(vacancy.to_dict(), expected_dict)

    def test_create_vacancies_empty_snippet(self) -> None:
        """Проверка create_vacancies с пустым snippet."""
        list_hh_vacancy = [
            {
                "id": "1",
                "name": "Python Dev",
                "url": "http://example.com",
                "snippet": None,
                "salary": {"from": 100000, "to": 150000},
            }
        ]
        vacancies = Vacancy.create_vacancies(list_hh_vacancy)
        self.assertEqual(vacancies[0].requirement, "Нет requirement")

    def test_create_vacancies_missing_salary_fields(self) -> None:
        """Проверка create_vacancies с отсутствующими полями from/to в salary."""
        list_hh_vacancy = [
            {
                "id": "1",
                "name": "Python Dev",
                "url": "http://example.com",
                "snippet": {"requirement": "Django"},
                "salary": {},  # from and to are missing
            }
        ]
        vacancies = Vacancy.create_vacancies(list_hh_vacancy)
        self.assertEqual(vacancies[0].salary_from, 0)
        self.assertEqual(vacancies[0].salary_to, 0)


if __name__ == "__main__":
    unittest.main()
