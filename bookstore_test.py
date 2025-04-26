from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# 1. Set up the WebDriver
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:

    # Test case 1: Search for an existing book and verify results
    # 1. Navigate to the website
    driver.get("https://demoqa.com/books")
    print("Successfully navigated to the website.")

    # 2. Locate the search bar and enter the search term
    search_box = driver.find_element(By.ID, "searchBox")
    title = "Speak"
    search_box.send_keys(title)
    print(f"Entered {title} in the search bar.")

    # 3. Wait for search results to load (explicit wait)
    wait = WebDriverWait(driver, 10)
    book_rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@role='row'][not(contains(@class, '-padRow'))]")))

    # 4. Filter the search results to exclude the search bar
    actual_search_results = []
    for row in book_rows:
        # Try to find a book title within the row. This is a good indicator that it's a book entry.
        try:
            title_element = row.find_element(By.XPATH, ".//div[@class='rt-td'][2]//a")
            actual_search_results.append(row)
        except:
            # If no title is found, it's likely not a book row
            pass

    # 5. Verify that at least one actual search result is displayed
    if len(actual_search_results) > 0:
        print(f"Passed - Found {len(actual_search_results)} actual search results.")
    else:
        print("Failed - No actual search results found.")

    # Test case 2 : Search for a non-existent book and verify no results are displayed
    # 1. Navigate to the website
    driver.get("https://demoqa.com/books")
    print("Successfully navigated to the website.")

    # 2. Locate the search bar and enter the non-existent title
    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "searchBox")))
    non_existent_title = "This Book Does Not Exist On This Website"
    print(f"\nTest case: Search for a non-existent book '{non_existent_title}' and verify no results.")

    search_box.send_keys(non_existent_title)
    print(f"Entered '{non_existent_title}' in the search bar.")

    # 3. Wait for a short time for potential results to (not) load
    wait = WebDriverWait(driver, 5)  # Reduced wait time as we expect no results
    try:
        # Attempt to find book rows. If none are found within the timeout, it's a good sign.
        book_rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@role='row'][not(contains(@class, '-padRow'))]")))

        # If we reach here, it means some rows were found, which is not the expected outcome.
        actual_search_results = []
        for row in book_rows:
            try:
                title_element = row.find_element(By.XPATH, ".//div[@class='rt-td'][2]//a")
                actual_search_results.append(row)
            except:
                pass

        if len(actual_search_results) == 0:
            print("Passed - No actual search results were displayed for the non-existent book.")
        else:
            print(f"Failed - Unexpectedly found {len(actual_search_results)} search results for the non-existent book.")

    except:
        # If the WebDriverWait times out without finding any book rows, this is the expected behavior.
        print("Passed - No book rows were found, as expected for a non-existent book.")



    # Test case 3 : Searching for Books Using Author Name Displays Relevant Results
    # 1. Navigate to the website
    driver.get("https://demoqa.com/books")
    print("Successfully navigated to the website.")

    # 2. Locate the search bar and enter the author's name
    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "searchBox")))
    author_to_search = "Richard E. Silverman"
    search_box.send_keys(author_to_search)
    print(f"Entered '{author_to_search}' in the search bar.")

     # 3. Wait for search results to load (explicit wait)
    wait = WebDriverWait(driver, 10)
    book_rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@role='row'][not(contains(@class, '-padRow'))]")))

     # 4. Filter the search results to get actual book rows and extract author names
    actual_search_results_authors = []
    for row in book_rows:
        try:
            author_element = row.find_element(By.XPATH, ".//div[@class='rt-td'][3]")  # Author is in the 3rd column
            actual_search_results_authors.append(author_element.text)
        except:
            # If no author element is found, it's likely not a book row
            pass

    # 5. Verify that at least one book by the searched author is displayed
    found_author = False
    for author in actual_search_results_authors:
        if author_to_search in author:
            found_author = True
            break

    if found_author:
        print(f"Passed - Found at least one book by the author '{author_to_search}'.")
    else:
        print(f"Failed - No books found by the author '{author_to_search}'.")

    # Test case 4: Searching for a Non-Existent Author Should Display No Books
    # 1. Navigate to the website
    driver.get("https://demoqa.com/books")
    print("Successfully navigated to the website.")

    # 2. Locate the search bar and enter a non-existent author's name
    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "searchBox")))
    non_existent_author = "This Author Does Not Exist At All On This Website"
    search_box.send_keys(non_existent_author)
    print(f"Entered '{non_existent_author}' in the search bar.")

    # 3. Wait for a short time for potential results to (not) load
    wait = WebDriverWait(driver, 5)
    try:
        # Attempt to find book rows. If none are found within the timeout, it's the expected outcome.
        book_rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@role='row'][not(contains(@class, '-padRow'))]")))

        # If we reach here, it means some rows were found, which is not the expected outcome.
        actual_search_results_non_existent_author = []
        for row in book_rows:
            try:
                author_element = row.find_element(By.XPATH, ".//div[@class='rt-td'][3]")  # Author is in the 3rd column
                actual_search_results_non_existent_author.append(author_element.text)
            except:
                pass

        if len(actual_search_results_non_existent_author) == 0:
            print(f"Passed - No books were displayed for the non-existent author '{non_existent_author}'.")
        else:
            print(f"Failed - Unexpectedly found {len(actual_search_results_non_existent_author)} books for the non-existent author '{non_existent_author}'.")

    except:
        # If the WebDriverWait times out without finding any book rows, this is the expected behavior.
        print(f"Passed - No book rows were found, as expected for the non-existent author '{non_existent_author}'.")

    # Test Case 5 : Searching for Books Using Publisher Displays Relevant Results
    # 1. Navigate to the website
    driver.get("https://demoqa.com/books")
    print("Successfully navigated to the website.")

    # 2. Locate the search bar and enter the publisher's name
    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "searchBox")))
    publisher_to_search = "O'Reilly Media"
    print(f"\nTest case: Search for books by publisher '{publisher_to_search}'")
    search_box.send_keys(publisher_to_search)
    print(f"Entered '{publisher_to_search}' in the search bar.")

    # 3. Wait for search results to load (explicit wait)
    wait = WebDriverWait(driver, 10)
    book_rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@role='row'][not(contains(@class, '-padRow'))]")))

    # 4. Filter the search results to get actual book rows and extract publisher names
    actual_search_results_publishers = []
    for row in book_rows:
        try:
            publisher_element = row.find_element(By.XPATH, ".//div[@class='rt-td'][4]")  # Publisher is in the 4th column
            actual_search_results_publishers.append(publisher_element.text)
        except:
            # If no publisher element is found, it's likely not a book row
            pass

    # 5. Verify that at least one book by the searched publisher is displayed
    found_publisher = False
    for publisher in actual_search_results_publishers:
        if publisher_to_search in publisher:
            found_publisher = True
            break

    if found_publisher:
        print(f"Passed - Found at least one book by the publisher '{publisher_to_search}'.")
    else:
        print(f"Failed - No books found by the publisher '{publisher_to_search}'.")

    
    # Test Case 6 Searching for a Non-Existent Publisher Should Display No Books" 
    # 1. Navigate to the website
    driver.get("https://demoqa.com/books")
    print("Successfully navigated to the website.")

    # 2. Locate the search bar and enter a non-existent publisher's name
    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "searchBox")))
    non_existent_publisher = "This Publisher Does Not Exist On This Website At All"
    search_box.send_keys(non_existent_publisher)
    print(f"Entered '{non_existent_publisher}' in the search bar.")

    # 3. Wait for a short time for potential results to (not) load
    wait = WebDriverWait(driver, 5)
    try:
        # Attempt to find book rows. If none are found within the timeout, it's the expected outcome.
        book_rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@role='row'][not(contains(@class, '-padRow'))]")))

        # If we reach here, it means some rows were found, which is not the expected outcome.
        actual_search_results_non_existent_publisher = []
        for row in book_rows:
            try:
                publisher_element = row.find_element(By.XPATH, ".//div[@class='rt-td'][4]")  # Publisher is in the 4th column
                actual_search_results_non_existent_publisher.append(publisher_element.text)
            except:
                pass

        if len(actual_search_results_non_existent_publisher) == 0:
            print(f"Passed - No books were displayed for the non-existent publisher '{non_existent_publisher}'.")
        else:
            print(f"Failed - Unexpectedly found {len(actual_search_results_non_existent_publisher)} books for the non-existent publisher '{non_existent_publisher}'.")

    except:
        # If the WebDriverWait times out without finding any book rows, this is the expected behavior.
        print(f"Passed - No book rows were found, as expected for the non-existent publisher '{non_existent_publisher}'.")

    # Test Case 7 : Verify "5 rows" option displays 5 rows
     # 1. Navigate to the website
    driver.get("https://demoqa.com/books")
    print("Successfully navigated to the website.")

    # 2. Locate the dropdown element
    dropdown_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//select[@aria-label='rows per page']"))
    )
    # 3. Use Select class to interact with the dropdown
    dropdown = Select(dropdown_element)

    # 4. Select the "5 rows" option
    dropdown.select_by_value("5")  # Or you can use select_by_visible_text("5 rows")
    print("Selected '5 rows' from the dropdown.")

    # 5. Wait for the table rows to load
    wait = WebDriverWait(driver, 10)
    # We wait for presence of *at least* 1 row, because if the selection didn't work, we might get 0
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='row'][not(contains(@class, '-padRow'))]")))

    # 6. Find all the displayed rows
    book_rows = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "rt-tbody")))
    number_of_rows = len(book_rows.find_elements(By.XPATH, ".//div[@role='rowgroup']"))
    # 8. Verify that the number of rows is 5
    if number_of_rows == 5:
        print(f"Passed - Expected 5 rows, and found {number_of_rows} rows.")
    else:
        print(f"Failed - Expected 5 rows, but found {number_of_rows} rows.")

    # Test Case 8 : Verify "Next" button functionality
    # 1. Navigate to the website
    driver.get("https://demoqa.com/books")
    print("Successfully navigated to the website.")

    # 2. Locate the dropdown element and set it to show 5 rows
    dropdown_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//select[@aria-label='rows per page']"))
    )
    dropdown = Select(dropdown_element)
    dropdown.select_by_value("5")
    print("Selected '5 rows' from the dropdown.")

    # 3. Wait for the table rows to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='row'][not(contains(@class, '-padRow'))]")))

    # 4. Find the "Next" button
    next_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='-next']/button[@type='button' and @class='-btn']"))
    )

    # 5. Get the current page number
    timeout = 10
    current_page_element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='jump to page' and @type='number']")))
    current_page_before = int(current_page_element.get_attribute("value"))
    print(f"Current page before clicking 'Next': {current_page_before}")

    # 6. Click the "Next" button
    next_button.click()
    print("Clicked the 'Next' button.")

    # 7. Wait for the page to update (rows to change)
    # wait.until(EC.staleness_of(current_page_element))
    # wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='row'][not(contains(@class, '-padRow'))]")))

    # 8. Get the current page number after clicking "Next"
    current_page_element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='jump to page' and @type='number']")))
    current_page_after = int(current_page_element.get_attribute("value"))
    print(f"Current page after clicking 'Next': {current_page_after}")

    # 9. Verify that the page number has increased.
    if current_page_after > current_page_before:
        print("Passed - Page number incremented after clicking 'Next'.")
    else:
        print("Failed - Page number did not increment after clicking 'Next'.")

    # 10. Verify the number of rows on the second page.  Should be 3.
    book_rows = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, "rt-tbody")))
    number_of_rows = len(book_rows.find_elements(By.XPATH, ".//div[@role='rowgroup']"))
    expected_rows_on_second_page = 5 
    if number_of_rows == expected_rows_on_second_page:
        print(f"Passed - Expected {expected_rows_on_second_page} rows, and found {number_of_rows} rows on the second page.")
    else:
        print(f"Failed - Expected {expected_rows_on_second_page} rows, but found {number_of_rows} rows on the second page.")

    #  Test Case 9: Verify "Previous" button functionality
    print("Test Case 9: Verify 'Previous' button functionality")
    # 1. Navigate to the website
    driver.get("https://demoqa.com/books")
    print("Successfully navigated to the website.")

    # 2. Locate the dropdown element and set it to show 5 rows
    dropdown_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//select[@aria-label='rows per page']"))
    )
    dropdown = Select(dropdown_element)
    dropdown.select_by_value("5")
    print("Selected '5 rows' from the dropdown.")

    # 3. Wait for the table rows to load
    # wait = WebDriverWait(driver, 10)
    # wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='row'][not(contains(@class, '-padRow'))]")))

    # 4. Find the "Next" button and click it to go to the second page
    next_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='-next']/button[@type='button' and @class='-btn']"))
    )
    next_button.click()
    print("Clicked the 'Next' button to go to the second page.")
    # wait.until(EC.staleness_of(next_button))
    # wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='row'][not(contains(@class, '-padRow'))]")))

    # 5. Find the "Previous" button
    previous_button = WebDriverWait(driver, timeout).until(  EC.presence_of_element_located((By.XPATH, "//div[@class='-previous']/button[@type='button' and @class='-btn']")) )

    # 6. Get the current page number
    current_page_element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='jump to page' and @type='number']")))
    current_page_before = int(current_page_element.get_attribute("value"))
    print(f"Current page before clicking 'Previous': {current_page_before}")

    # 7. Click the "Previous" button
    previous_button.click()
    print("Clicked the 'Previous' button.")

    # 8. Wait for the page to update
    # wait.until(EC.staleness_of(current_page_element))
    # wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='row'][not(contains(@class, '-padRow'))]")))

    # 9. Get the current page number after clicking "Previous"
    current_page_element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='jump to page' and @type='number']")))
    current_page_after = int(current_page_element.get_attribute("value"))
    print(f"Current page after clicking 'Previous': {current_page_after}")

    # 10. Verify that the page number has decreased.
    if current_page_after < current_page_before:
        print("Passed - Page number decremented after clicking 'Previous'.")
    else:
        print("Failed - Page number did not decrement after clicking 'Previous'.")
    
    # 11. Verify that the number of rows is 5 after clicking previous
    book_rows = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, "rt-tbody")))
    number_of_rows = len(book_rows.find_elements(By.XPATH, ".//div[@role='rowgroup']"))
    expected_rows_on_first_page = 5
    if number_of_rows == expected_rows_on_first_page:
        print(f"Passed - Expected {expected_rows_on_first_page} rows, and found {number_of_rows} rows on the first page.")
    else:
        print(f"Failed - Expected {expected_rows_on_first_page} rows, but found {number_of_rows} on the first page.")
    
    print("\n" + "#" * 60 + "\n")

finally:
        # Close the browser
        driver.quit()
        print("\nBrowser closed.")
