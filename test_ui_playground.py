from playwright.async_api import async_playwright, expect, Error, TimeoutError
from playwright.sync_api._generated import Page
import pytest, pytest_asyncio
import pyperclip
import os

@pytest_asyncio.fixture(scope="function")
async def page():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        page.set_default_timeout(6000)
        yield page
        await page.close()
        await context.close()
        await browser.close()

@pytest.mark.asyncio
async def test_uiplay_landing(page: Page):
    await page.goto("http://uitestingplayground.com/", timeout=60000)
    await expect(page).to_have_title("UI Test Automation Playground")
    await expect(page.locator('img[alt="Responsive image"]')).to_be_visible()
    await expect(page.locator('section[id="description"]')).to_be_visible()
    await expect(page.locator('section[id="overview"]')).to_be_visible()

@pytest.mark.asyncio
async def test_uiplay_navbar(page: Page):
    await page.goto("http://uitestingplayground.com/", timeout=6000)
    navbar = page.locator('nav[class="navbar navbar-expand-lg navbar-light bg-light"]')
    await expect(navbar).to_be_visible()
    await expect(navbar.locator('a[class="navbar-brand"]')).to_have_text("UITAP")

@pytest.mark.asyncio
async def test_uiplay_overview(page: Page):
    await page.goto("http://uitestingplayground.com/", timeout=60000)
    overview = page.locator('section[id="overview"]')
    await expect(overview).to_be_visible()
    container = overview.locator("div")
    await expect(container.first.locator(":scope > *")).to_have_count(6)
    await expect(container.locator(":scope > div div").nth(0).locator("h3")).to_have_text("Dynamic ID")
    await expect(container.locator(":scope > div div").nth(1).locator("h3")).to_have_text("Class Attribute")
    await expect(container.locator(":scope > div div").nth(2).locator("h3")).to_have_text("Hidden Layers")
    await expect(container.locator(":scope > div div").nth(3).locator("h3")).to_have_text("Load Delay")
    await expect(container.locator(":scope > div div").nth(4).locator("h3")).to_have_text("AJAX Data")
    await expect(container.locator(":scope > div div").nth(5).locator("h3")).to_have_text("Client Side Delay")
    await expect(container.locator(":scope > div div").nth(6).locator("h3")).to_have_text("Click")
    await expect(container.locator(":scope > div div").nth(7).locator("h3")).to_have_text("Text Input")
    await expect(container.locator(":scope > div div").nth(8).locator("h3")).to_have_text("Scrollbars")
    await expect(container.locator(":scope > div div").nth(9).locator("h3")).to_have_text("Dynamic Table")
    await expect(container.locator(":scope > div div").nth(10).locator("h3")).to_have_text("Verify Text")
    await expect(container.locator(":scope > div div").nth(11).locator("h3")).to_have_text("Progress Bar")
    await expect(container.locator(":scope > div div").nth(12).locator("h3")).to_have_text("Visibility")
    await expect(container.locator(":scope > div div").nth(13).locator("h3")).to_have_text("Sample App")
    await expect(container.locator(":scope > div div").nth(14).locator("h3")).to_have_text("Mouse Over")
    await expect(container.locator(":scope > div div").nth(15).locator("h3")).to_have_text("Non-Breaking Space")
    await expect(container.locator(":scope > div div").nth(16).locator("h3")).to_have_text("Overlapped Element")
    await expect(container.locator(":scope > div div").nth(17).locator("h3")).to_have_text("Shadow DOM")
    await expect(container.locator(":scope > div div").nth(18).locator("h3")).to_have_text("Alerts")
    await expect(container.locator(":scope > div div").nth(19).locator("h3")).to_have_text("File Upload")
    await expect(container.locator(":scope > div div").nth(20).locator("h3")).to_have_text("Animated Button")
    await expect(container.locator(":scope > div div").nth(21).locator("h3")).to_have_text("Disabled Input")
    await expect(container.locator(":scope > div div").nth(22).locator("h3")).to_have_text("Auto Wait")

@pytest.mark.asyncio
async def test_uiplay_dynamic_id(page: Page):
    # ### Test for testing button with Dynamic ID.
    await page.goto("http://uitestingplayground.com/dynamicid", timeout=60000)
    await page.get_by_role("heading", name="Dynamic ID").click()
    await expect(page).to_have_title("Dynamic ID")
    dynamic_button = page.get_by_text("Button with Dynamic ID")
    dynamic_button_id1 = await dynamic_button.get_attribute("id")
    await page.reload()
    dynamic_button_id2 = await dynamic_button.get_attribute("id")
    assert dynamic_button_id1 != dynamic_button_id2

@pytest.mark.asyncio
async def test_uiplay_class_attribute(page: Page):
    # ### Test for testing button with Class Attribute.
    await page.goto("http://uitestingplayground.com/classattr", timeout=60000)
    await page.get_by_role("heading", name="Class Attribute").click()

    dialog_message = {}

    async def handle_dialog(dialog):
        dialog_message["text"] = dialog.message
        print("Dialog message:", dialog.message)
        await dialog.accept()
    page.once("dialog", handle_dialog)

    await page.locator('xpath=//button[contains(@class, "btn-primary")]').click()
    await page.wait_for_timeout(1000)
    assert dialog_message.get("text") == "Primary button pressed"

@pytest.mark.asyncio
async def test_uiplay_hidden_layers(page: Page):
    await page.goto("http://uitestingplayground.com/", timeout=60000)
    await page.get_by_role("heading", name="Hidden Layers").click()
    await expect(page).to_have_title("Hidden Layers")
    green_button = page.locator('button[id="greenButton"]')
    await expect(green_button).to_be_visible()
    await green_button.click()
    blue_button = page.locator('button[id="blueButton"]')
    await expect(blue_button).to_be_visible()
    
    try:
        await green_button.click(timeout=2000)
        assert False, "Element should not be clickable due to overlap"
    except Error as e:
        print("Element not clickable as expected due to overlap.")

@pytest.mark.asyncio
async def test_uiplay_load_delay(page: Page):
    await page.goto("http://uitestingplayground.com/", timeout=60000)
    await page.get_by_role("heading", name="Load Delay").click()
    await expect(page).to_have_title("Load Delays")
    await page.go_back()
    await page.get_by_role("heading", name="Load Delay").click()
    await page.wait_for_load_state("domcontentloaded")
    await expect(page).to_have_title("Load Delays")
    await page.get_by_text("Button Appearing After Delay").click()
    
@pytest.mark.asyncio
async def test_uiplay_ajax_data(page: Page):
    await page.goto("http://uitestingplayground.com/", timeout=60000)
    await page.get_by_role("heading", name="AJAX Data").click()
    await expect(page).to_have_title("AJAX Data")
    await page.get_by_text("Button Triggering AJAX Request").click()
    await expect(page.locator('p', has_text="Data loaded with AJAX get request.")).to_be_visible(timeout=16000)


@pytest.mark.asyncio
async def test_uiplay_client_side_delay(page: Page):
    await page.goto("http://uitestingplayground.com/", timeout=60000)
    await page.get_by_role("heading", name="Client Side Delay").click()
    await expect(page).to_have_title("Client Side Delay")
    await page.locator("button", has_text="Button Triggering Client Side Logic").click()
    await expect(page.locator("p", has_text="Data calculated on the client side.")).to_be_visible(timeout=16000)
    await page.locator("p", has_text="Data calculated on the client side.").click()

@pytest.mark.asyncio
async def test_uiplay_click(page: Page):
    await page.goto("http://uitestingplayground.com/", timeout=60000)
    click_link = page.locator('a', has_text="Click")
    await click_link.scroll_into_view_if_needed()
    box1 = await click_link.bounding_box()
    assert box1 is not None, "Bounding box for the link is None"
    x1 = box1['x'] + box1['width']/2
    y1 = box1['y'] + box1['height']/2
    await page.mouse.click(x1, y1)
    await expect(page).to_have_title("Click", timeout=5000)
    click_button = page.locator('button', has_text="Button That Ignores DOM Click Event")
    await expect(click_button).to_be_visible()
    await expect(click_button).to_have_css("background-color", "rgb(0, 123, 255)")
    box2 = await click_button.bounding_box()
    assert box2 is not None, "Bounding box for the button is None"
    x2 = box2['x'] + box2['width']/2
    y2 = box2['y'] + box2['height']/2
    await page.mouse.click(x2, y2)
    await expect(click_button).not_to_have_css("background-color", "rgb(0, 123, 255)", timeout=5000)

@pytest.mark.asyncio
async def test_uiplay_text_input(page: Page):
    await page.goto("http://uitestingplayground.com/", timeout=60000)
    await page.locator('a[href="/textinput"]').click(timeout=2000)
    await expect(page).to_have_title("Text Input")
    text_input_field = page.locator('input[id="newButtonName"]')
    updating_button = page.locator('button[id="updatingButton"]')
    await expect(text_input_field).to_be_visible()
    await expect(text_input_field).to_have_attribute("placeholder", "MyButton")
    await expect(updating_button).to_be_visible()
    await expect(updating_button).to_have_text("Button That Should Change it's Name Based on Input Value")
    await text_input_field.fill("Text Input for Button updatingButton Test")
    await updating_button.click()
    await expect(updating_button).to_have_text("Text Input for Button updatingButton Test", timeout=1000)

@pytest.mark.asyncio
async def test_uiplay_scrollbars(page: Page):
    await page.goto("http://uitestingplayground.com/", timeout=60000)
    await page.locator('a[href="/scrollbars"]').click(timeout=2000)
    hiding_button = page.locator('button[id="hidingButton"]')
    await hiding_button.scroll_into_view_if_needed()
    await expect(hiding_button).to_be_visible()
    await hiding_button.click()

@pytest.mark.asyncio
async def test_uiplay_dynamic_table(page: Page):
    await page.goto("http://uitestingplayground.com/dynamictable", timeout=60000)
    await expect(page).to_have_title("Dynamic Table")
    chrome_cpu_value = page.locator('p', has_text="Chrome CPU:")
    first_row = page.locator(':scope > div > div[role="row"]').nth(0)
    first_row_headers_count = await first_row.locator('span[role="columnheader"]').count()
    for i1 in range(first_row_headers_count):
        column_text = await first_row.locator('span[role="columnheader"]').nth(i1).text_content()
        if column_text == "CPU":
            cpu_index = i1
            break
    table_rows = page.locator(':scope > div[role="rowgroup"] > div[role="row"]')
    table_rows_count = await table_rows.count()
    table_content_row = table_rows.locator('scope > div > span[role="cell"]')
    for i2 in range(table_rows_count):
        table_content_rows = table_rows.nth(i2).locator('span[role="cell"]')
        name = await table_content_rows.nth(0).text_content()
        if name =="Chrome":
            chrome_index = i2
            break
        chrome_cpu = await table_content_rows.nth(cpu_index).text_content()
        chrome_cpu_string = str("Chrome CPU: " + chrome_cpu)
        assert chrome_cpu_string == await chrome_cpu_value.text_content(), "Chrome CPU value does not match"


@pytest.mark.asyncio
async def test_uiplay_verify_text(page: Page):
    await page.goto("http://uitestingplayground.com/", timeout=60000)
    await page.locator('a[href="/verifytext"]').click()
    await expect(page).to_have_title("Verify Text", timeout=1000)
    text_in_element = page.locator('div[class="bg-primary"]', has_text="Welcome Username!")
    await expect(text_in_element).to_be_visible(timeout=1000)

@pytest.mark.asyncio
async def test_uiplay_progress_bar(page: Page):
    await page.goto("http://uitestingplayground.com/", timeout=60000)
    await page.locator('a[href="/progressbar"]').click()
    await expect(page).to_have_title("Progress Bar")
    start_button = page.locator('button[id="startButton"]')
    stop_button = page.locator('button[id="stopButton"]')
    progress_bar = page.locator('div[id="progressBar"]')
    progress_bar_inner_text = await progress_bar.inner_text()
    progress_bar_value = int(progress_bar_inner_text.strip("%"))                        
    result = page.locator('p[id="result"]')
    await start_button.click()
    while progress_bar_value < 100:
        if await progress_bar.inner_text() >= "75%":
            await stop_button.click()
            break
        elif await progress_bar.inner_text() == "100%":
            break
    await expect(progress_bar).to_have_attribute("style", "width: 75%")

@pytest.mark.asyncio
async def test_uiplay_visibility(page: Page):
    await page.goto("http://uitestingplayground.com/", timeout=60000)
    await page.locator('a[href="/visibility"]').click()
    await expect(page).to_have_title("Visibility")
    hide_button = page.locator('button[id="hideButton"]')
    removed_button = page.locator('button[id="removeButton"]')
    zero_button = page.locator('button[id="zeroWidthButton"]')
    overlapped_button = page.locator('button[id="overlappedButton"]')
    opacity_button = page.locator('button[id="transparentButton"]')
    visibility_button = page.locator('button[id="invisibleButton"]')
    display_button = page.locator('button[id="notdisplayedButton"]')
    offscreen_button = page.locator('button[id="offscreenButton"]')
    await hide_button.click()
    await expect(removed_button).not_to_be_visible()
    await expect(zero_button).not_to_be_visible()
    try:
        await overlapped_button.click(timeout=2000)
        assert False, "Element should not be clickable due to overlap"
    except Error as e:
        print("Element not clickable as expected due to overlap.")

    await expect(opacity_button).to_have_css("opacity", "0")
    await expect(visibility_button).not_to_be_visible()
    await expect(display_button).not_to_be_visible()
    await expect(offscreen_button).not_to_be_in_viewport()


@pytest.mark.asyncio
async def test_uiplay_sample_app(page: Page):
### Positive test for sample app login functionality
    await page.goto("http://uitestingplayground.com")
    await page.locator('a[href="/sampleapp"]').click(timeout=2000)
    await expect(page).to_have_title("Sample App")
    await page.locator('input[name="UserName"]').fill("testuser")
    await page.locator('input[name="Password"]').fill("pwd")
    await page.locator('button[id="login"]').click()
    await expect(page.locator('label[id="loginstatus"]')).to_have_text("Welcome, testuser!", timeout=1000)

@pytest.mark.asyncio
async def test_uiplay_mouse_over(page: Page):
    await page.goto("http://uitestingplayground.com")
    await page.locator('a[href="/mouseover"]').click(timeout=2000)
    await expect(page).to_have_title("Mouse Over")
    await expect(page.locator('span[id="clickCount"]')).to_have_text("0", timeout=500)      #### Click Count
    await expect(page.locator('span[id="clickButtonCount"]')).to_have_text("0", timeout=500)   #### Click Button Count
    #### Mouse Hover Changes DOM Element properties Click Button
    await expect(page.get_by_text("Click Me")).to_have_attribute("class", "text-primary")
    await expect(page.get_by_text("Click Me")).to_have_attribute("title", "Click me")
    await page.get_by_text("Click Me").hover()
    await expect(page.get_by_text("Click Me")).not_to_have_attribute("class", "text-primary")
    await expect(page.get_by_text("Click Me")).not_to_have_attribute("title", "Click me")
    await page.get_by_text("Click Me").click() #### Way to find locator by inner text works regardless of dynamic CSS elements. Text Unchanged on hover
    await expect(page.locator('span[id="clickCount"]')).to_have_text("1", timeout=500)     
    await page.get_by_text("Click Me").click()
    await expect(page.locator('span[id="clickCount"]')).to_have_text("2", timeout=500)
    #### Mouse Hover Changes DOM element properties Link Button to identical ones
    await expect(page.get_by_text("Link Button")).to_have_attribute("class", "text-primary")
    await expect(page.get_by_text("Link Button")).to_have_attribute("title", "Link Button")
    await page.get_by_text("Link Button").hover()
    await expect(page.get_by_text("Link Button")).not_to_have_attribute("class", "text-primary")
    await page.get_by_text("Link Button").click()
    await expect(page.locator('span[id="clickButtonCount"]')).to_have_text("1", timeout=500)
    await page.get_by_text("Link Button").click()
    await expect(page.locator('span[id="clickButtonCount"]')).to_have_text("2", timeout=500)


@pytest.mark.asyncio
async def test_uiplay_non_breaking_space(page: Page):
    await page.goto("http://uitestingplayground.com")
    await page.locator('a[href="/nbsp"]').click(timeout=2000)
    await expect(page).to_have_title("Non-Breaking Space")
    await expect(page.locator('button', has_text="My Button")).to_be_visible(timeout=1000)      #### Playwright handles spaces in text automatically.
    await expect(page.get_by_text("My\u00a0Button", exact=True)).to_be_visible(timeout=1000)  #### to find exact match which includes non-breaking space
    await page.locator('//button[text()="My\u00a0Button"]').click()       #### using xpath to locate element and click


@pytest.mark.asyncio
async def test_uiplay_overlapped_element(page: Page):
    await page.goto("http://uitestingplayground.com")
    await page.locator('a[href="/overlapped"]').click(timeout=2000)
    await expect(page).to_have_title('Overlapped Element')
    await page.locator('input[id="id"]').fill("ID input")
    await expect(page.locator('input[id="id"]')).to_have_value("ID input")
    await page.locator('div[style="overflow-y: scroll; height:100px;"]').hover()
    await page.mouse.wheel(0, 100)
    await expect(page.locator('div[style="overflow-y: scroll; height:100px;"]')).to_be_visible(timeout=1000)
    await page.locator('input[id="name"]').focus()
    await page.locator('input[id="name"]').click(force=True)
    await page.wait_for_timeout(500)    
    await page.locator('input[id="name"]').type("Name Input")
    await page.wait_for_timeout(500)
    value = await page.locator('input[id="name"]').input_value()
    print(f"input value: {value}")
    await expect(page.locator('input[id="name"]')).to_have_value("Name Input", timeout=5000)

@pytest.mark.skip(reason="unable to verify if clipboard content matches input field value. HTTP server security limitation")
@pytest.mark.asyncio
async def test_uiplay_shadow_dom(page: Page):
    async def console_error_handle(msg):
        if msg.type == "error":
            print(f"[Console Error] {msg.text}")
    await page.goto("http://uitestingplayground.com")
    await page.locator('a[href="/shadowdom"]').click(timeout=2000)
    guid_generate_button = page.locator('button[id="buttonGenerate"]')
    guid_input_field = page.locator('input[id="editField"]')
    await guid_generate_button.click()
    guid = await guid_input_field.input_value()
    print('Generated GUID: ' + str(guid))
    guid_copy_button = page.locator('button[id="buttonCopy"]')
    await guid_copy_button.click(force=True)
    page.on("console", console_error_handle)
    await page.wait_for_timeout(2000)
    guid_copied = page.evaluate('navigator.clipboard.readText()')
    print(str(guid_copied))
    assert str(guid) == str(guid_copied)



@pytest.mark.asyncio
async def test_uiplay_alerts(page: Page):
#### will need to break this up into separate tests for each of the alert buttons.
    await page.goto("http://uitestingplayground.com")
    await page.locator('a[href="/alerts"]').click(timeout=2000)
    await expect(page).to_have_title("Alerts")
    
    dialog_message = {}

    async def handle_dialog(dialog):
        dialog_message["text"] = dialog.message
        print("Dialog message:", dialog.message)
        await dialog.accept()
    page.once("dialog", handle_dialog)

    await page.locator('button[id="alertButton"]').click()
    await page.locator('button[id="confirmButton"]').click()
    await page.locator('button[id="promptButton"]').click()


@pytest.mark.asyncio
async def test_uiplay_file_upload(page: Page):
    await page.goto("http://uitestingplayground.com")
    await page.locator('a[href="/upload"]').click(timeout=2000)
    await expect(page).to_have_title("File Upload")
    # print(os.getcwd())
    page.frame_locator("iframe")
    browse_file_input = page.frame_locator("iframe").locator('input[id="browse"]')
    await browse_file_input.set_input_files("./file_upload_test_file.txt")
    await page.wait_for_timeout(500)
    await expect(page.frame_locator("iframe").locator('div[class="file-info"]')).to_have_text("file_upload_test_file.txt")
    await expect(page.frame_locator("iframe").locator('div[class=success-file]')).to_have_text("1 file(s) selected")


@pytest.mark.asyncio
async def test_uiplay_animated_button(page: Page):
    await page.goto("http://uitestingplayground.com")
    await page.locator('a[href="/animation"]').click(timeout=2000)
    await expect(page).to_have_title("Animated Button")
    await expect(page.locator('button[id="movingTarget"]')).to_have_attribute("class", "btn btn-primary")
    await page.locator('button[id="animationButton"]').click()
    await expect(page.locator('div[id="opstatus"]')).to_have_text("Animating the button...")
    await expect(page.locator('button[id="movingTarget"]')).to_have_attribute("class", "btn btn-primary spin")
    await expect(page.locator('button[id="movingTarget"]')).to_have_attribute("class", "btn btn-primary", timeout=10000)
    await expect(page.locator('button[id="movingTarget"]')).not_to_have_attribute("class", "btn btn-primary spin")
    await expect(page.locator('div[id="opstatus"]')).to_have_text("Animation done")


@pytest.mark.asyncio
async def test_uiplay_disabled_input(page: Page):
        await page.goto("http://uitestingplayground.com")
        await page.locator('a[href="/disabledinput"]').click(timeout=2000)
        await expect(page).to_have_title("Disabled Input")
        enable_edit_button = page.locator('button[id="enableButton"]')
        input_field = page.locator('input[id="inputField"]')
        await enable_edit_button.click()
        await expect(input_field).to_be_disabled()
        await page.wait_for_timeout(5500)
        await expect(input_field).not_to_be_disabled() ### 5 second delay
        await expect(input_field).to_be_enabled()
        await input_field.fill("Text Input Test 123")
        await input_field.press("Enter")
        await expect(input_field).to_have_value("Text Input Test 123")
        await expect(page.locator('div[id="opstatus"]')).to_have_text("Value changed to: Text Input Test 123")
        

@pytest.mark.asyncio
async def test_uiplay_auto_wait_button(page: Page):
    await page.goto("http://uitestingplayground.com")
    await page.locator('a[href="/autowait"]').click(timeout=2000)
    await expect(page).to_have_title("Auto Wait")
    await page.get_by_label("Choose an element type:\u00a0").select_option("Button")
    await page.get_by_label("Visible").set_checked(False)
    await expect(page.get_by_label("Visible")).not_to_be_checked()
    await page.get_by_label("Enabled").set_checked(False)
    await expect(page.get_by_label("Enabled")).not_to_be_checked()
    await page.get_by_label("Editable").set_checked(False)
    await expect(page.get_by_label("Editable")).not_to_be_checked()
    await page.get_by_label("On Top").set_checked(False)
    await expect(page.get_by_label("On Top")).not_to_be_checked()
    await page.get_by_label("Non Zero Size").set_checked(False)
    await expect(page.get_by_label("Non Zero Size")).not_to_be_checked()
    # #apply_10
    # #apply_5
    apply_3 = page.locator('button[id="applyButton3"]')
    await apply_3.click()
    button_button = page.locator('button[id="target"]')
    await expect(page.locator('div[id=opstatus]')).to_have_text("Target element settings applied for 3 seconds.")
    await button_button.click()
    await expect(page.locator('div[id="opstatus"]')).to_have_text("Target clicked.")


@pytest.mark.asyncio
async def test_uiplay_auto_wait_input(page: Page):
    await page.goto("http://uitestingplayground.com")
    await page.locator('a[href="/autowait"]').click(timeout=2000)
    await expect(page).to_have_title("Auto Wait")
    await page.get_by_label("Choose an element type:\u00a0").select_option("Input")
    await page.get_by_label("Visible").set_checked(False)
    await expect(page.get_by_label("Visible")).not_to_be_checked()
    await page.get_by_label("Enabled").set_checked(False)
    await expect(page.get_by_label("Enabled")).not_to_be_checked()
    await page.get_by_label("Editable").set_checked(False)
    await expect(page.get_by_label("Editable")).not_to_be_checked()
    await page.get_by_label("On Top").set_checked(False)
    await expect(page.get_by_label("On Top")).not_to_be_checked()
    await page.get_by_label("Non Zero Size").set_checked(False)
    await expect(page.get_by_label("Non Zero Size")).not_to_be_checked()
    input_input = page.locator('input[id="target"]')
    apply_3 = page.locator('button[id="applyButton3"]')
    ##apply_5 = page.locator('button[id="applyButton5"]')
    #apply_10 = page.locator('button[id="applyButton10"]')
    await apply_3.click()
    await expect(page.locator('div[id="opstatus"]')).to_have_text("Target element settings applied for 3 seconds.")
    await input_input.fill("Input Area input test 12345")
    await input_input.press("Enter")
    await expect(page.locator('div[id="opstatus"]')).to_have_text("Text: Input Area input test 12345")



@pytest.mark.asyncio
async def test_uiplay_auto_wait_textarea(page: Page):
    await page.goto("http://uitestingplayground.com")
    await page.locator('a[href="/autowait"]').click(timeout=2000)
    await expect(page).to_have_title("Auto Wait")
    await page.get_by_label("Choose an element type:\u00a0").select_option("Textarea")
    await page.get_by_label("Visible").set_checked(False)
    await expect(page.get_by_label("Visible")).not_to_be_checked()
    await page.get_by_label("Enabled").set_checked(False)
    await expect(page.get_by_label("Enabled")).not_to_be_checked()
    await page.get_by_label("Editable").set_checked(False)
    await expect(page.get_by_label("Editable")).not_to_be_checked()
    await page.get_by_label("On Top").set_checked(False)
    await expect(page.get_by_label("On Top")).not_to_be_checked()
    await page.get_by_label("Non Zero Size").set_checked(False)
    await expect(page.get_by_label("Non Zero Size")).not_to_be_checked()
    textarea_area = page.locator('textarea[id="target"]')
    apply_3 = page.locator('button[id="applyButton3"]')
    ##apply_5 = page.locator('button[id="applyButton5"]')
    #apply_10 = page.locator('button[id="applyButton10"]')
    await apply_3.click()
    await expect(page.locator('div[id="opstatus"]')).to_have_text("Target element settings applied for 3 seconds.")
    await textarea_area.click()
    await textarea_area.fill("Textarea input test 12345")
    await expect(page.locator('div[id="opstatus"]')).to_have_text("Target clicked.")
    await expect(textarea_area).to_have_value("Textarea input test 12345")


@pytest.mark.asyncio
async def test_uiplay_auto_wait_select(page: Page):
    await page.goto("http://uitestingplayground.com")
    await page.locator('a[href="/autowait"]').click(timeout=2000)
    await expect(page).to_have_title("Auto Wait")
    await page.get_by_label("Choose an element type:\u00a0").select_option("Select")
    await page.get_by_label("Visible").set_checked(False)
    await expect(page.get_by_label("Visible")).not_to_be_checked()
    await page.get_by_label("Enabled").set_checked(False)
    await expect(page.get_by_label("Enabled")).not_to_be_checked()
    await page.get_by_label("Editable").set_checked(False)
    await expect(page.get_by_label("Editable")).not_to_be_checked()
    await page.get_by_label("On Top").set_checked(False)
    await expect(page.get_by_label("On Top")).not_to_be_checked()
    await page.get_by_label("Non Zero Size").set_checked(False)
    await expect(page.get_by_label("Non Zero Size")).not_to_be_checked()
    target_select_dropdown_box = page.locator('select[id="target"]')
    apply_3 = page.locator('button[id="applyButton3"]')
    await apply_3.click()
    await target_select_dropdown_box.select_option("Item 3")
    # #await target_select_dropdown_box.select_option("Item 1")
    # #await target_select_dropdown_box.select_option("Item 2")
    await expect(page.locator('div[id="opstatus"]')).to_have_text("Selected: Item 3")


@pytest.mark.asyncio
async def test_uiplay_auto_wait_label(page: Page):
    await page.goto("http://uitestingplayground.com")
    await page.locator('a[href="/autowait"]').click(timeout=2000)
    await expect(page).to_have_title("Auto Wait")
    await page.get_by_label("Choose an element type:\u00a0").select_option("Label")
    await page.get_by_label("Visible").set_checked(False)
    await expect(page.get_by_label("Visible")).not_to_be_checked()
    await page.get_by_label("Enabled").set_checked(False)
    await expect(page.get_by_label("Enabled")).not_to_be_checked()
    await page.get_by_label("Editable").set_checked(False)
    await expect(page.get_by_label("Editable")).not_to_be_checked()
    await page.get_by_label("On Top").set_checked(False)
    await expect(page.get_by_label("On Top")).not_to_be_checked()
    await page.get_by_label("Non Zero Size").set_checked(False)
    await expect(page.get_by_label("Non Zero Size")).not_to_be_checked()
    ##apply_10
    ##apply_5
    apply_3 = page.locator('button[id="applyButton3"]')
    await apply_3.click()
    label_label = page.locator('label', has_text="This is a Label")
    await expect(page.locator('div[id=opstatus]')).to_have_text("Target element settings applied for 3 seconds.")
    await label_label.click()
    await expect(page.locator('div[id="opstatus"]')).to_have_text("Target clicked.")

