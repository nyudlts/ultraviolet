# -*- coding: utf-8 -*-
#
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 NYU.
#
# ultraviolet is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""E2E test for files page download related elements."""


import os
import random
import string
import subprocess
from time import sleep

import pytest
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

code_text = None

def login(browser):
    """
    Logs a user into the application by navigating to the login page, filling credentials, and submitting form.
    """
    try:
        browser.get("https://127.0.0.1:5000/")
        login_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.ui.button[href='/login/?next=%2F']"))
        )
        login_button.click()
        assert "Log in to account" == browser.find_element(By.TAG_NAME, "h3").text

        # Login
        browser.find_element(By.NAME, "email").send_keys('adminUV@test.com')
        browser.find_element(By.NAME, "password").send_keys('adminUV')
        login_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ui.fluid.large.submit.primary.button"))
        )
        login_button.click()
    except Exception as e:
        if not os.path.exists("screenshots"):
            os.mkdir("screenshots")
        browser.save_screenshot(f'screenshots/test_login{".".join(random.choices(string.ascii_lowercase + string.digits, k=10))}.png')
        print(str(e))
        raise e

def upload_file(code_text, size):
    """
    Handles the upload process of a file to InvenioRDM.

    Args:
    code_text (str): The bearer token used for authorization.
    size (int): The size of the file to generate and upload in mb.

    Raises:
    Exception: If any step in the file upload process fails.
    """
    try:
        # 1. Create a Draft Upload
        url = "https://127.0.0.1:5000/api/records"
        headers = {
            "Authorization": f"Bearer {code_text}",
            "Content-Type": "application/json",
            "Referer": "https://127.0.0.1:5000"
        }
        data = {
            "metadata": {
                "title": "Test file",
                "creators": [
                    {
                        "person_or_org": {
                            "given_name": "Josiah",
                            "family_name": "Carberry",
                            "type": "personal",
                            "identifiers": [{"identifier": "0000-0002-1825-0097"}]
                        },
                        "affiliations": [{"name": "Brown University"}]
                    }
                ],
                "publisher": "InvenioRDM",
                "publication_date": "2024-05-14",
                "resource_type": {"id": "dataset"}
            }
        }
        response = requests.post(url, headers=headers, json=data, verify=False)
        pid = response.json().get("id")

        create_file('fake.bin', size) 

        # 2. Initialize the file uplaod for the large file
        url = f"https://127.0.0.1:5000/api/records/{pid}/draft/files"
        data = [{"key": "fake.bin"}]
        response = requests.post(url, headers=headers, json=data, verify=False)

        # 3. Upload the file content
        url = f"https://127.0.0.1:5000/api/records/{pid}/draft/files/fake.bin/content"
        headers = {
            "Authorization": f"Bearer {code_text}",
            "Content-Type": "application/octet-stream",
            "Referer": "https://127.0.0.1:5000"
        }
        with open("fake.bin", 'rb') as file:
            response = requests.put(url, headers=headers, data=file, verify=False)

        # 4. Commit the uploaded file
        url = f"https://127.0.0.1:5000/api/records/{pid}/draft/files/fake.bin/commit"
        headers = {
            "Authorization": f"Bearer {code_text}",
            "Referer": "https://127.0.0.1:5000"
        }
        response = requests.post(url, headers=headers, verify=False)
    except Exception as e:
        print(str(e))

def create_file(file_path, size_in_mb):
    """
    Creates a large file of a specified size by using the 'truncate' command to set the file size.

    Args:
    file_path (str): The path where the file will be created.
    size_in_mb (int): The size of the file to create in mb.

    Raises:
    subprocess.CalledProcessError: If the 'truncate' command fails.
    """
    size_in_bytes = size_in_mb * 1024 * 1024
    try:
        subprocess.run(['truncate', '-s', str(size_in_bytes), file_path], check=True)
        print(f"Successfully created {file_path} with size {size_in_mb}MB.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running truncate: {e}")

def cleanup_token(browser):
    """
    A helper method to delete the testing token.
    """
    yield 

    login(browser)
    # delete token
    browser.get("https://127.0.0.1:5000/")
    browser.get('https://127.0.0.1:5000/account/settings/applications/')
    token_link = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'token-for-e2e-test')]"))
    )
    token_link.click()
    delete_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @name="delete" and contains(@class, "ui button negative")]'))
    )
    delete_button.click()

def cleanup_community(browser):
    """
    A helper method to delete the testing community.
    """
    yield 

    try:
        login(browser)

        browser.get('https://127.0.0.1:5000/me/communities')
        community_link = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'a-test-community-name')]"))
        )
        community_link.click()
        settings_link = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'item') and .//i[contains(@class, 'settings icon')]]"))
        )
        settings_link.click()
        delete_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='delete-button' and @aria-haspopup='dialog']"))
        )
        delete_button.click()
        confirm_delete_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'ui negative button') and contains(text(), 'Delete')]"))
        )
        confirm_delete_button.click()
    except Exception as e:
        if not os.path.exists("screenshots"):
            os.mkdir("screenshots")
            browser.save_screenshot(f'screenshots/test_cleanup_community{".".join(random.choices(string.ascii_lowercase + string.digits, k=10))}.png')
        print(str(e))
        raise e

def setup_community(browser):
    """
    Helper function to automate the process of setting up a new community.

    """
    login(browser)

    # Navigate to the community creation page
    browser.get("https://127.0.0.1:5000/me/communities")
    community_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.ui.positive.right.floated.button[href='/communities/new']"))
    )
    community_button.click()

    # Create new community
    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.NAME, "metadata.title"))
    ).send_keys("a-test-community-name")
    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.NAME, "slug"))
    ).send_keys(''.join(random.choice(string.ascii_lowercase) for _ in range(8)))
    create_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ui.icon.positive.left.labeled.button"))
    )
    create_button.click()

@pytest.mark.order(1)
@pytest.mark.skipif(os.getenv('E2E', 'no') != 'yes', reason="Skipping E2E tests because E2E environment variable is not set")
def test_small_file(chrome_driver):
    """
    This test verifies the upload and publication workflow for a small file within the application.
    The Download button, Download all button, and file name download link should be presented.
    """
    global code_text

    # Update config for testing
    config_file_path = os.path.join(os.path.dirname(__file__), '../../invenio.cfg')
    with open(config_file_path, 'r') as file:
        original_lines = file.readlines()
    updated_lines = original_lines.copy()

    key1 = 'MAX_FILE_SIZE'
    value1 = '10 * 1024 * 1024'  # Set to 10 MB

    for i, line in enumerate(updated_lines):
        if line.startswith(key1):
            updated_lines[i] = f"{key1} = {value1}\n"

    with open(config_file_path, 'w') as file:
        file.writelines(updated_lines)

    sleep(5)
    
    try:
        browser = chrome_driver
        setup_community(browser)
        # generate token
        browser.get("https://127.0.0.1:5000/account/settings/applications/")
        
        new_token_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@class='ui compact tiny button basic secondary' and contains(., 'New token')]"))
        )
        new_token_button.click()

        name_input = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='name']"))
        )
        name_input.send_keys("token-for-e2e-test")

        create_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(., 'Create')]"))
        )
        create_button.click()

        generated_code = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='ui small label']/code"))
        )
        code_text = generated_code.text

        save_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and @name='save' and contains(., 'Save')]"))
        )
        save_button.click()

        # API calls for upload large file
        upload_file(code_text, 1)

        # 5. Assign community and publish the draft
        browser.get("https://127.0.0.1:5000/me/uploads")

        test_file_link = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'truncate-lines-2') and text()='Test file']"))
        )
        test_file_link.click()

        community_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(@name, "setting") and contains(@class, "community-header-button")]'))
        )
        community_button.click()

        select_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(@aria-label, "Select a-test-community-name") and contains(@class, "ui small button")]'))
        )
        select_button.click()

        submit_review_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[name="SubmitReview"]'))
        )
        submit_review_button.click()
        checkbox1 = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//label[@for='acceptAccessToRecord']"))
        )
        checkbox1.click()
        checkbox2 = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//label[@for='acceptAfterPublishRecord']"))
        )
        checkbox2.click()
        submit_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[name="submitReview"]'))
        )
        submit_button.click()

        accept_and_publish_button1 = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept and publish')]"))
        )
        accept_and_publish_button1.click()
        all_accept_and_publish_buttons = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[contains(., 'Accept and publish')]"))
        )
        if len(all_accept_and_publish_buttons) >= 2:
            all_accept_and_publish_buttons[1].click()
        browser.refresh()
        uploads_link = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'item') and contains(text(), 'Uploads')]"))
        )
        uploads_link.click()
        test_title_link = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'truncate-lines-2') and contains(text(), 'Test file')]"))
        )
        test_title_link.click()

        # Download button
        _ = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@role="button" and contains(@class, "ui compact mini button") and contains(., "Download")]'))
        )
        # Name download link
        _ = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@class="wrap-long-link"]'))
        )
        # Download all button
        _ = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.ui.compact.mini.button.right.floated.archive-link"))
        )
    except Exception as e:
        if not os.path.exists("screenshots"):
            os.mkdir("screenshots")
            browser.save_screenshot(f'screenshots/test_small_file{".".join(random.choices(string.ascii_lowercase + string.digits, k=10))}.png')
        print(str(e))
        raise e
    finally:
        if os.path.exists("fake.bin"):
            os.remove("fake.bin")
        cleanup_token(browser)
        cleanup_community(browser)

@pytest.mark.order(2)
@pytest.mark.skipif(os.getenv('E2E', 'no') != 'yes', reason="Skipping E2E tests because E2E environment variable is not set")
def test_large_file(chrome_driver):
    """
    This test verifies the upload and publication workflow for a large file within the application.
    The Download button, Download all button, and file name download link should not be presented.
    """
    global code_text
    try:
        browser = chrome_driver
        
        # remove old fake file if present
        if os.path.exists("fake.bin"):
            os.remove("fake.bin")

        upload_file(code_text, 20)
        
        # 5. Assign community and publish the draft
        browser.get("https://127.0.0.1:5000/me/uploads")

        test_file_link = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'truncate-lines-2') and text()='Test file']"))
        )
        test_file_link.click()

        community_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(@name, "setting") and contains(@class, "community-header-button")]'))
        )
        community_button.click()

        select_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(@aria-label, "Select a-test-community-name") and contains(@class, "ui small button")]'))
        )
        select_button.click()

        submit_review_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[name="SubmitReview"]'))
        )
        submit_review_button.click()
        checkbox1 = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//label[@for='acceptAccessToRecord']"))
        )
        checkbox1.click()
        checkbox2 = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//label[@for='acceptAfterPublishRecord']"))
        )
        checkbox2.click()
        submit_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[name="submitReview"]'))
        )

        submit_button.click()

        accept_and_publish_button1 = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'ui icon positive left labeled button') and contains(., 'Accept and publish')]"))
        )
        accept_and_publish_button1.click()
        all_accept_and_publish_buttons = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[contains(., 'Accept and publish')]"))
        )
        if len(all_accept_and_publish_buttons) >= 2:
            all_accept_and_publish_buttons[1].click()
        browser.refresh()
        uploads_link = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'item') and contains(text(), 'Uploads')]"))
        )
        uploads_link.click()
        test_title_link = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'truncate-lines-2') and contains(text(), 'Test file')]"))
        )
        test_title_link.click()

        try:
            _ = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//a[@role="button" and contains(@class, "ui compact mini button") and contains(., "Download")]'))
            )
            assert False, "Download button should not be present, but it was found."
        except TimeoutException:
            # expected exception
            pass
        
        try:
            _ = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//a[@class="wrap-long-link"]'))
            )
            assert False, "Download link should not be present, but it was found."
        except TimeoutException:
            # expected exception
            pass
    except Exception as e:
        if not os.path.exists("screenshots"):
            os.mkdir("screenshots")
        browser.save_screenshot(f'screenshots/test_lage_file{".".join(random.choices(string.ascii_lowercase + string.digits, k=10))}.png')
        print(str(e))
        raise e
    finally:
        browser.quit()
        if os.path.exists("fake.bin"):
            os.remove("fake.bin")
        cleanup_token(browser)
        cleanup_community(browser)
        
        # Remove config updates after test finish
        config_file_path = os.path.join(os.path.dirname(__file__), '../../invenio.cfg')
        with open(config_file_path, 'r') as file:
            original_lines = file.readlines()
        updated_lines = original_lines.copy()

        key1 = 'MAX_FILE_SIZE'
        value1 = '50 * 1024 * 1024 * 1024'

        for i, line in enumerate(updated_lines):
            if line.startswith(key1):
                updated_lines[i] = f"{key1} = {value1}\n"

        with open(config_file_path, 'w') as file:
            file.writelines(updated_lines)
        
