import time

from src.app import Example
import panel as pn


# https://panel.holoviz.org/how_to/test/uitests.html
def test_example_frontend(page, port):
    component = Example()
    url = f"http://localhost:{port}"

    server = pn.serve(component, port=port, threaded=True, show=False)
    time.sleep(0.2)

    page.goto(url)

    page.goto("http://localhost:5006/app")
    page.get_by_role("button", name="SVK").click()
    page.get_by_role("gridcell", name="SVK").locator("div").click()

    server.stop()
