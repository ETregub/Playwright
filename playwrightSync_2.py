import pytest
from playwright.sync_api import sync_playwright

def test_google_search():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        print("Переход на сайт Google")
        page.goto("https://www.google.com")
        #print("Принимаем условия")
        #page.get_by_role("none").get_by_text("Принять все").click()
        print("Ожидание элемента поиска")
        page.wait_for_selector("textarea[name='q']")
        print("Вводим 'playwright' в строку поиска")
        page.fill("textarea[name='q']", "playwright")
        print("Отправка формы")
        page.press("textarea[name='q']", "Enter")
        print("Ожидание загрузки результатов")
        page.wait_for_selector("#search")
        title = page.title()
        assert "playwright" in title.lower(), f"Заголовок страницы не содержит 'playwright', а содержит: {title}"
        print(f"Заголовок страницы: {title}")
        content = page.content()
        assert "playwright" in content, "Результаты поиска не содержат 'playwright'"
        results = page.query_selector_all("h3")
        assert len(results) > 0, "Не найдено ни одного результата поиска"
        print(f"Найдено {len(results)} результатов поиска.")
        page.screenshot(path="search_results.png")
        print("Скриншот страницы результатов сохранен как 'search_results.png'.")
        print("Тест пройден успешно!")
        browser.close()