######################################################################
# Copyright 2016, 2021 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
######################################################################

# pylint: disable=function-redefined, missing-function-docstring
# flake8: noqa
"""
Web Steps

Steps file for web interactions with Selenium

For information on Waiting until elements are present in the HTML see:
https://selenium-python.readthedocs.io/waits.html
"""
import logging
from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ID_PREFIX = "product_"


##################################################################
# FIELD INPUT STEPS
##################################################################
@then('I should see "{message}" in the title')
def step_impl(context, message):
    """Check the document title for a message"""
    assert message in context.driver.title


@then('I should not see "{text_string}"')
def step_impl(context, text_string):
    """Ensure text is not visible in the page body"""
    element = context.driver.find_element(By.TAG_NAME, "body")
    assert text_string not in element.text


@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    """Set a text field to the given string"""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(text_string)


@when('I select "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    """Select a value from a dropdown"""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = Select(context.driver.find_element(By.ID, element_id))
    element.select_by_visible_text(text)


@then('I should see "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    """Verify dropdown selection"""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = Select(context.driver.find_element(By.ID, element_id))
    assert element.first_selected_option.text == text


@then('the "{element_name}" field should be empty')
def step_impl(context, element_name):
    """Verify that a field is empty"""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, element_id)
    assert element.get_attribute("value") == u""


##################################################################
# COPY AND PASTE FIELD VALUES
##################################################################
@when('I copy the "{element_name}" field')
def step_impl(context, element_name):
    """Copy text from a field"""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    context.clipboard = element.get_attribute("value")
    logging.info("Clipboard contains: %s", context.clipboard)


@when('I paste the "{element_name}" field')
def step_impl(context, element_name):
    """Paste text into a field"""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(context.clipboard)


##################################################################
# BUTTON CLICKS AND RESULT CHECKS
##################################################################
@when('I press the "{button}" button')
def step_impl(context, button):
    """Press a button by name"""
    button_id = f"{button.lower()}-btn"
    element = context.driver.find_element(By.ID, button_id)
    element.click()


@then('I should see "{name}" in the results')
def step_impl(context, name):
    """Check if the product name appears in search results"""
    wait = WebDriverWait(context.driver, context.wait_seconds)
    found = wait.until(
        EC.text_to_be_present_in_element((By.ID, "search_results"), name)
    )
    assert found, f"Expected to see '{name}' in the results."


@then('I should not see "{name}" in the results')
def step_impl(context, name):
    """Check if the product name is absent from search results"""
    element = context.driver.find_element(By.ID, "search_results")
    assert name not in element.text, f"Did not expect to see '{name}' in results."


@then('I should see the message "{message}"')
def step_impl(context, message):
    """Verify a flash message appears"""
    wait = WebDriverWait(context.driver, context.wait_seconds)
    found = wait.until(
        EC.text_to_be_present_in_element((By.ID, "flash_message"), message)
    )
    assert found, f"Expected flash message '{message}' not found."


##################################################################
# FIELD VERIFICATION
##################################################################
@then('I should see "{text_string}" in the "{element_name}" field')
def step_impl(context, text_string, element_name):
    """Verify field value"""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element_value((By.ID, element_id), text_string)
    )
    assert found


@when('I change "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    """Change a field's value"""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(text_string)
