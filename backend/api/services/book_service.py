from uuid import UUID
from api.models.Book import Book, BookForCreate
from api.models.Page import Page
from typing import List


def get_book(id_book: UUID) -> Book:
    return None


def create_book(book: BookForCreate) -> Page:
    return None


def get_books(id_user: UUID) -> List[Book]:
    return None


def get_pages(id_book: UUID) -> Book:
    return None


def add_page(id_book: UUID) -> Page:
    return None


def send_message(page_id, message):
    return None
