import asyncio
from playwright.async_api import async_playwright

async def run(playwright):
    browser = await playwright.chromium.launch(headless=False)
    page = await browser.new_page()
    print("Переход на сайт Google")
    await page.goto("https://www.google.com")
    print("Принимаем условия")
    #await page.get_by_text("Принять все").click()
    await page.get_by_role("none").get_by_text("Принять все").click()
    print("Ожидание элемента поиска")
    await page.wait_for_selector("textarea[name='q']")
    print("Вводим 'playwright' в строку поиска")
    await page.fill("textarea[name='q']", "playwright")
    await asyncio.sleep(1)
    print("Отправка формы")
    await page.press("textarea[name='q']", "Enter")
    await asyncio.sleep(2)
    print("Ожидание загрузки результатов")
    await page.wait_for_selector("#search")
    title = await page.title()
    assert "playwright" in title.lower(), f"Заголовок страницы не содержит 'playwright', а содержит: {title}"
    print(f"Заголовок страницы: {title}")
    content = await page.content()
    assert "playwright" in content, "Результаты поиска не содержат 'playwright'"
    results = await page.query_selector_all("h3")
    assert len(results) > 0, "Не найдено ни одного результата поиска"
    print(f"Найдено {len(results)} результатов поиска.")
    await page.screenshot(path="search_results.png")
    print("Скриншот страницы результатов сохранен как 'search_results.png'.")
    print("Тест пройден успешно!")
    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)

asyncio.run(main())