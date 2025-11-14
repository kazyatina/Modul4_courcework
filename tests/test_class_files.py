import json
import os
import unittest

from src.class_files import FileHandlerBase, FileHandlerJob  # Замените на правильный путь
from src.class_vacancy import Vacancy  # Замените на правильный путь


class TestFileHandlerJob(unittest.TestCase):
    """Тесты для класса FileHandlerJob."""

    TEST_FILENAME = "test_job_hh.json"
    TEST_DIR = "./data/"
    FULL_TEST_FILENAME = os.path.join(TEST_DIR, TEST_FILENAME)

    def setUp(self) -> None:
        """Подготовка к каждому тесту: создание экземпляра класса и очистка тестового файла."""
        # Создаем каталог, если его нет
        if not os.path.exists(self.TEST_DIR):
            os.makedirs(self.TEST_DIR)

        self.file_handler = FileHandlerJob(self.TEST_FILENAME)
        # Убедимся, что файл существует и пуст перед каждым тестом
        with open(self.FULL_TEST_FILENAME, "w", encoding="utf-8") as f:
            f.write("[]")  # Записываем пустой список, чтобы избежать ошибок JSONDecodeError

    def tearDown(self) -> None:
        """Удаление тестового файла после каждого теста."""
        if os.path.exists(self.FULL_TEST_FILENAME):
            os.remove(self.FULL_TEST_FILENAME)

    def test_inheritance(self) -> None:
        """Проверяем, что FileHandlerJob наследуется от FileHandlerBase."""
        self.assertTrue(issubclass(FileHandlerJob, FileHandlerBase))

    def test_abstract_methods(self) -> None:
        """Проверяем наличие абстрактных методов в FileHandlerBase."""
        self.assertTrue(hasattr(FileHandlerBase, "write"))
        self.assertTrue(hasattr(FileHandlerBase, "open_file"))
        self.assertTrue(hasattr(FileHandlerBase, "add_vacancy"))
        self.assertTrue(hasattr(FileHandlerBase, "delete_vacancy"))

        self.assertTrue(callable(FileHandlerBase.write))
        self.assertTrue(callable(FileHandlerBase.open_file))
        self.assertTrue(callable(FileHandlerBase.add_vacancy))
        self.assertTrue(callable(FileHandlerBase.delete_vacancy))

    def test_init(self) -> None:
        """Проверяем инициализацию объекта FileHandlerJob."""
        self.assertEqual(
            self.file_handler._FileHandlerJob__filename, self.FULL_TEST_FILENAME
        )  # Проверяем приватный атрибут
        self.assertEqual(self.file_handler.data_file, [])

    def test_open_file_existing(self) -> None:
        """Проверяем открытие существующего файла."""
        #Создаем файл с данными
        test_data = [{"id_vacancy": "123", "requirement": "test"}]
        with open(self.FULL_TEST_FILENAME, "w", encoding="utf-8") as f:
            json.dump(test_data, f)

        # Создаем новый экземпляр FileHandlerJob, который должен прочитать данные из файла
        file_handler = FileHandlerJob(self.TEST_FILENAME)

        # Проверяем, что данные были прочитаны правильно
        self.assertEqual(file_handler.data_file, test_data)

    def test_open_file_not_existing(self) -> None:
        """Проверяем создание нового файла, если он не существует."""
        # Удаляем файл, чтобы убедиться, что он не существует
        if os.path.exists(self.FULL_TEST_FILENAME):
            os.remove(self.FULL_TEST_FILENAME)

        # Создаем экземпляр FileHandlerJob, который должен создать файл
        file_handler = FileHandlerJob(self.TEST_FILENAME)

        # Проверяем, что файл был создан и его data_file пуст
        self.assertTrue(os.path.exists(self.FULL_TEST_FILENAME))
        self.assertEqual(file_handler.data_file, [])

    def test_write(self) -> None:
        """Проверяем запись данных в файл."""
        test_data = [{"id_vacancy": "456", "requirement": "test2"}]
        self.file_handler.write(test_data, "w")

        with open(self.FULL_TEST_FILENAME, "r", encoding="utf-8") as f:
            file_content = json.load(f)

        self.assertEqual(file_content, test_data)
        self.assertEqual(self.file_handler.data_file, test_data)

    def test_add_vacancy(self) -> None:
        """Проверяем добавление вакансии в файл."""

        vacancy1 = Vacancy("1", "req1", "desc1", 76543, 76543, "salary1")
        vacancy2 = Vacancy("2", "req2", "desc2", 45678, 45678, "salary2")
        self.file_handler.data_file = [
            {"id_vacancy": "1", "requirement": "req1"}
        ]  # Имитируем, что в файле уже есть вакансия с id = 1

        self.file_handler.add_vacancy([vacancy2, vacancy1])  # Пытаемся добавить vacancy2 (новая) и vacancy1 (уже есть)

        with open(self.FULL_TEST_FILENAME, "r", encoding="utf-8") as f:
            file_content = json.load(f)

        self.assertEqual(len(file_content), 2)  # Убеждаемся, что добавилась только vacancy2
        self.assertEqual(file_content[0]["id_vacancy"], "2")
        self.assertEqual(file_content[0]["requirement"], "salary2")

    def test_delete_vacancy(self) -> None:
        """Проверяем удаление вакансии из файла."""

        vacancy1 = Vacancy("1", "req1", "desc1", 76543, 76543, "salary1")
        vacancy2 = Vacancy("2", "req2", "desc2", 23456, 23456, "salary2")
        self.file_handler.data_file = [vacancy1.to_dict(), vacancy2.to_dict()]
        self.file_handler.write(self.file_handler.data_file, "w")  # Записываем данные в файл

        self.file_handler.delete_vacancy(vacancy1)

        with open(self.FULL_TEST_FILENAME, "r", encoding="utf-8") as f:
            file_content = json.load(f)

        self.assertEqual(len(file_content), 1)
        self.assertEqual(file_content[0]["id_vacancy"], "2")  # Убеждаемся, что осталась только vacancy2

    def test_delete_vacancy_not_found(self) -> None:
        """Проверяем, что происходит, если вакансия для удаления не найдена."""

        vacancy1 = Vacancy("1", "req1", "desc1", 567354, 567354, "salary1")
        vacancy2 = Vacancy("2", "req2", "desc2", 23456, 23456, "salary2")
        self.file_handler.data_file = [vacancy1.to_dict()]
        self.file_handler.write(self.file_handler.data_file, "w")

        self.file_handler.delete_vacancy(vacancy2)  # Пытаемся удалить vacancy2, которой нет в файле

        with open(self.FULL_TEST_FILENAME, "r", encoding="utf-8") as f:
            file_content = json.load(f)

        self.assertEqual(len(file_content), 1)  # Убеждаемся, что vacancy1 осталась в файле
        self.assertEqual(file_content[0]["id_vacancy"], "1")


if __name__ == "__main__":
    unittest.main()
