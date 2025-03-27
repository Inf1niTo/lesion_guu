import pytest
from playwright.sync_api import sync_playwright

def test_page_load():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Запуск в headless режиме
        page = browser.new_page()
        page.goto("http://127.0.0.1:8050")  # Адрес твоего Dash-приложения
        assert page.title() == "My First App with Data"  # Пример проверки заголовка страницы
        browser.close()

def test_table_display():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://127.0.0.1:8050")
        
        # Проверка наличия таблицы
        table = page.locator('table')
        assert table.is_visible(), "Таблица не найдена на странице"
        
        # Проверка первой строки таблицы
        first_row = table.locator('tr:nth-child(1)')
        assert first_row.inner_text() != "", "Первая строка таблицы пуста"
        
        browser.close()
