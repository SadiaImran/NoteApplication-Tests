import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time

class NoteAppTests(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("http://51.20.131.151:5000/")
        time.sleep(1)

    def tearDown(self):
        self.driver.quit()

    def _delete_all_tasks(self):
        """Delete all existing tasks"""
        while True:
            try:
                delete_button = self.driver.find_element(By.LINK_TEXT, "Delete")
                delete_button.click()
                time.sleep(0.5)
                self.driver.get("http://51.20.131.151:5000/")
            except:
                break

    def _add_task(self, title, desc):
        self.driver.find_element(By.NAME, "title").send_keys(title)
        self.driver.find_element(By.NAME, "description").send_keys(desc)
        self.driver.find_element(By.XPATH, "//button[contains(text(),'Add Task')]").click()
        time.sleep(1)

    def test_01_clear_all_tasks_first(self):
        """Step 1: Clear all tasks to start fresh"""
        self._delete_all_tasks()
        print("🧹 test_01_clear_all_tasks_first: All existing tasks deleted")

    def test_02_add_task(self):
        now = datetime.now().strftime("%H:%M:%S")
        title = f"Test 02 Task - {now}"
        self._add_task(title, "Valid task")
        titles = self.driver.find_elements(By.TAG_NAME, "h3")
        self.assertTrue(any(title in t.text for t in titles))
        print(f"✅ test_02_add_task: Added {title}")

    def test_03_empty_title(self):
        self.driver.find_element(By.NAME, "description").send_keys("No title")
        self.driver.find_element(By.XPATH, "//button[contains(text(),'Add Task')]").click()
        time.sleep(1)
        self.assertEqual(self.driver.current_url, "http://51.20.131.151:5000/")
        print("✅ test_03_empty_title: Blocked as expected")

    def test_04_empty_description(self):
        self.driver.find_element(By.NAME, "title").send_keys("Only Title")
        self.driver.find_element(By.XPATH, "//button[contains(text(),'Add Task')]").click()
        time.sleep(1)
        self.assertEqual(self.driver.current_url, "http://51.20.131.151:5000/")
        print("✅ test_04_empty_description: Blocked as expected")

    def test_05_add_multiple_tasks(self):
        for i in range(3):
            now = datetime.now().strftime("%H:%M:%S")
            title = f"Test 05 Task {i} - {now}"
            self._add_task(title, f"Description {i}")
        titles = self.driver.find_elements(By.TAG_NAME, "h3")
        self.assertTrue(any("Test 05 Task 0" in t.text for t in titles))
        print("✅ test_05_add_multiple_tasks: Added 3 tasks")

    def test_06_delete_task(self):
        now = datetime.now().strftime("%H:%M:%S")
        title = f"Delete Me - {now}"
        self._add_task(title, "To be deleted")

        # Find and delete exact task
        tasks = self.driver.find_elements(By.XPATH, "//li")
        for task in tasks:
            if title in task.text:
                delete_btn = task.find_element(By.LINK_TEXT, "Delete")
                delete_btn.click()
                break

        time.sleep(1)
        self.driver.get("http://51.20.131.151:5000/")
        titles = self.driver.find_elements(By.TAG_NAME, "h3")
        self.assertFalse(any(title in t.text for t in titles))
        print(f"✅ test_06_delete_task: Deleted task {title}")

    def test_07_special_characters(self):
        title = "@#$%^&*()!"
        self._add_task(title, "!@#$%^&*()")
        titles = self.driver.find_elements(By.TAG_NAME, "h3")
        self.assertTrue(any(title in t.text for t in titles))
        print("✅ test_07_special_characters: Added special character task")

    def test_08_long_texts(self):
        long_title = "T" * 100
        long_desc = "D" * 500
        self._add_task(long_title, long_desc)
        titles = self.driver.find_elements(By.TAG_NAME, "h3")
        self.assertTrue(any(long_title[:10] in t.text for t in titles))
        print("✅ test_08_long_texts: Added long text task")

    def test_09_refresh_persistence(self):
        title = f"Persist Task - {datetime.now().strftime('%H:%M:%S')}"
        self._add_task(title, "Should stay after refresh")
        self.driver.refresh()
        time.sleep(1)
        titles = self.driver.find_elements(By.TAG_NAME, "h3")
        self.assertTrue(any(title in t.text for t in titles))
        print(f"✅ test_09_refresh_persistence: Task persisted - {title}")

    def test_10_duplicate_task(self):
        now = datetime.now().strftime("%H:%M:%S")
        for _ in range(2):
            self._add_task(f"Duplicate - {now}", "Same title")
        titles = self.driver.find_elements(By.TAG_NAME, "h3")
        count = sum(1 for t in titles if f"Duplicate - {now}" in t.text)
        self.assertGreaterEqual(count, 2)
        print(f"✅ test_10_duplicate_task: Duplicate tasks added at {now}")

if __name__ == "__main__":
    unittest.main()
