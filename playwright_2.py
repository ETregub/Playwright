from playwright.sync_api import sync_playwright

def test_google_search():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        #context = browser.new_context()
        page = browser.new_page()
        page.goto("https://www.google.com")
        page.get_by_role("none").get_by_text("Принять все").click()
        page.fill("textarea[name='q']", "playwright")
        page.get_by_text('Поиск в Google').first.click()
        page.wait_for_selector("div.g")
        results = page.query_selector_all("div.g")
        assert len(results) > 0, "Результаты поиска не найдены"
        for result in results:
            title = result.query_selector("h3").text_content()
            assert "playwright" in title.lower(), f"Результат '{title}' не содержит слово 'playwright'"
        browser.close()

test_google_search()