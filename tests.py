import pytest
from main import BooksCollector

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    @pytest.fixture
    def collector(self):
        return BooksCollector()

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self, collector):
        # создаем экземпляр (объект) класса BooksCollector
        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
        assert len(collector.get_books_genre()) == 2

    # проверяем, что метод add_new_book повторно не добавляет книгу
    def test_add_book_with_duplicates(self, collector):
        collector.add_new_book('Гарри Поттер')
        collector.add_new_book('Гарри Поттер')
        assert len(collector.get_books_genre()) == 1

     # проверяем, что метод add_new_book добавляет книгу. Название книги может содержать максимум 40 символов.
    @pytest.mark.parametrize( "book_name, expected_length",
        [
            ("К", 1),
            ("Кн", 2),
            ("Книга с названием тридцать восемь симв", 38),
            ("Книга с названием тридцать девять симво", 39),
            ("Книга с названием в сорок символов книга", 40),
        ]
    )
    def test_add_valid_books(self, collector, book_name, expected_length):
        assert len(book_name) == expected_length
        collector.add_new_book(book_name)
        assert book_name in collector.books_genre

    # проверяем, что метод add_new_book не добавляет книгу, название которой содержит больше 40 символов.
    @pytest.mark.parametrize(
        "book_name, expected_length",
        [
            ("Слишком длинное название которое превышает сорок символов", 57),
            ("", 0),
            ("Книга с названием в сорок один символ кни", 41),
        ]
    )
    def test_add_invalid_books(self, collector, book_name, expected_length):
        assert len(book_name) == expected_length
        collector.add_new_book(book_name)
        assert book_name not in collector.books_genre

    # проверяем что метод устанавливает жанр книги, если книга есть в books_genreи её жанр входит в списокgenre
    def test_set_existing_book_existing_genre(self, collector):
        collector.add_new_book('Автостопом по галактике')
        collector.set_book_genre('Автостопом по галактике', 'Детективы')
        assert collector.get_book_genre('Автостопом по галактике') == 'Детективы'

    # проверяем, что метод get_books_with_specific_genre— выводит список книг с определённым жанром.
    def test_books_with_specific_genre_comedy(self, collector):
        collector.add_new_book('Двенадцать стульев')
        collector.set_book_genre('Двенадцать стульев', 'Комедии')
        assert collector.get_book_genre('Двенадцать стульев') == 'Комедии'
        assert 'Двенадцать стульев' in collector.get_books_with_specific_genre('Комедии')

    # проверяем, что метод get_books_genre— выводит текущий словарь books_genre
    @pytest.mark.parametrize("books",
                            [
                                [
                                    ("Паровозик из Ромашково", "Мультфильмы"),
                                    ("Двенадцать стульев", "Комедии"),
                                    ("Кэрри", "Ужасы"),
                                ]
                            ])
    def test_get_books_genre_multiple_books(self, collector, books):
        expected = dict(books)
        for book_name, genre in books:
            collector.add_new_book(book_name)
            collector.set_book_genre(book_name, genre)
        assert collector.get_books_genre() == expected

    # проверяем, что метод get_books_for_children — возвращает книги, которые подходят детям. У жанра книги не должно быть возрастного рейтинга.
    @pytest.mark.parametrize("book_name, genre, for_children",
                            [
                                ("Паровозик из Ромашково", "Мультфильмы", True),
                                ("Двенадцать стульев", "Комедии", True),
                                ("Кэрри", "Ужасы", False),
                            ])
    def test_get_books_for_children(self, collector, book_name, genre, for_children):
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        children_books = collector.get_books_for_children()
        assert (book_name in children_books) == for_children

    # проверяем, что метод add_book_in_favorites — добавляет книгу в избранное. Книга должна находиться в словаре books_genre
    def test_add_existing_book_to_favorites(self, collector):
        collector.add_new_book('Война и мир')
        collector.add_book_in_favorites('Война и мир')
        assert 'Война и мир' in collector.get_list_of_favorites_books()

    # проверяем, что метод add_book_in_favorites — не добавляет книгу в избранное, если книга не находится в коллекции.
    def test_add_nonexistent_book_to_favorites(self, collector):
        book_name = "Книга, которой нет в коллекции"
        assert book_name not in collector.books_genre
        collector.add_book_in_favorites(book_name)
        assert book_name not in collector.get_list_of_favorites_books()
        assert collector.get_list_of_favorites_books() == []

    # проверяем, что невозможно добавить повторно одну и ту же книгу в избранное
    def test_add_duplicate_book_to_favorites(self, collector):
        collector.add_new_book('Вино из одуванчиков')
        collector.add_book_in_favorites('Вино из одуванчиков')
        collector.add_book_in_favorites('Вино из одуванчиков')
        assert collector.get_list_of_favorites_books() == ['Вино из одуванчиков']

     # проверяем, что метод delete_book_from_favorites — удаляет книгу из избранного, если она там есть.
    def test_delete_existing_favorite(self, collector):
        collector.add_new_book('Анна Каренина')
        collector.add_book_in_favorites('Анна Каренина')
        collector.delete_book_from_favorites('Анна Каренина')
        assert 'Анна Каренина' not in collector.get_list_of_favorites_books()

    # проверяем, что невозможно удалить книгу из избранного, если её там нет.
    def test_delete_nonexistent_favorite(self, collector):
        non_existent_book = "Неизвестная книга"
        assert non_existent_book not in collector.books_genre
        collector.add_book_in_favorites(non_existent_book)
        assert collector.get_list_of_favorites_books() == []
        collector.delete_book_from_favorites(non_existent_book)
        assert collector.get_list_of_favorites_books() == []

    # проверяем, что метод get_list_of_favorites_books — получает список избранных книг.
    @pytest.mark.parametrize( "books_to_add, favorites_to_add, expected_result",
        [
            (
                    ["Вино из одуванчиков", "Автостопом по галактике", "Кэрри"],
                    ["Вино из одуванчиков", "Кэрри"],
                    ["Вино из одуванчиков", "Кэрри"]
            )
        ]
    )
    def test_get_list_of_favorites_books(self, collector, books_to_add, favorites_to_add, expected_result):
        for book in books_to_add:
            collector.add_new_book(book)
        for favorite in favorites_to_add:
            collector.add_book_in_favorites(favorite)
        assert collector.get_list_of_favorites_books() == expected_result
