from src.class_files import FileHandlerJob
from src.class_Api_HH import HH
from src.class_vacancy import Vacancy
from src.add_func import (
    filter_vacancies,
    get_top_vacancies,
    get_vacancies_by_salary,
    print_vacancies,
    sort_vacancies,
)

hh_api = HH()
file_handler = FileHandlerJob()


def user_interaction() -> None:
    """Функция для взаимодействия с пользователем"""
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input("Введите диапазон зарплат: ")  # Пример: 100000 - 150000

    hh_vacancies = hh_api.load_vacancies(search_query)
    vacancies_list = Vacancy.create_vacancies(hh_vacancies)
    file_handler.add_vacancy(vacancies_list)

    file_handler.delete_vacancy(vacancies_list[0])
    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)

    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)

    sorted_vacancies = sort_vacancies(ranged_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()
