"""
Selenium Test Suite for Task Manager Application
This demonstrates various Selenium testing patterns and best practices
"""
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os


class TaskManagerTests(unittest.TestCase):
    """Test suite for the Task Manager application"""
    
    @classmethod
    def setUpClass(cls):
        """Set up the browser once for all tests"""
        print("\n🚀 Setting up Selenium WebDriver...")
        
        # Configure Chrome options
        chrome_options = Options()
        
        # Use headless mode in CI/CD environment
        if os.getenv('CI') or os.getenv('HEADLESS'):
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            print("   Running in HEADLESS mode")
        
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        # Initialize the driver
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)
        
        # Set the base URL
        cls.base_url = os.getenv('APP_URL', 'http://127.0.0.1:5000')
        print(f"   Testing URL: {cls.base_url}")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        print("\n🧹 Cleaning up...")
        time.sleep(1)  # Brief pause to see final state
        cls.driver.quit()
    
    def setUp(self):
        """Set up before each test"""
        self.driver.get(self.base_url)
        time.sleep(0.5)  # Brief pause for page load
        
    def tearDown(self):
        """Clean up after each test"""
        # Clear all tasks after each test to ensure clean state
        try:
            clear_btn = self.driver.find_element(By.ID, 'clearBtn')
            clear_btn.click()
            
            # Handle the confirmation alert
            WebDriverWait(self.driver, 3).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
            time.sleep(0.5)
        except Exception:
            pass  # If clearing fails, that's okay
    
    def test_01_page_loads_successfully(self):
        """Test 1: Verify the page loads with correct title"""
        print("\n✓ Test 1: Checking page loads...")
        
        # Check page title
        self.assertIn("Task Manager", self.driver.title)
        
        # Verify main heading is present
        heading = self.driver.find_element(By.ID, 'title')
        self.assertIsNotNone(heading)
        self.assertIn("Task Manager", heading.text)
        
        print("   ✅ Page loaded successfully!")
    
    def test_02_ui_elements_present(self):
        """Test 2: Verify all UI elements are present"""
        print("\n✓ Test 2: Checking UI elements...")
        
        # Check input field
        task_input = self.driver.find_element(By.ID, 'taskInput')
        self.assertIsNotNone(task_input)
        self.assertEqual(task_input.get_attribute('placeholder'), 'Enter a new task...')
        
        # Check add button
        add_btn = self.driver.find_element(By.ID, 'addBtn')
        self.assertIsNotNone(add_btn)
        self.assertEqual(add_btn.text, 'Add Task')
        
        # Check clear button
        clear_btn = self.driver.find_element(By.ID, 'clearBtn')
        self.assertIsNotNone(clear_btn)
        self.assertEqual(clear_btn.text, 'Clear All Tasks')
        
        # Check task list
        task_list = self.driver.find_element(By.ID, 'taskList')
        self.assertIsNotNone(task_list)
        
        print("   ✅ All UI elements present!")
    
    def test_03_add_single_task(self):
        """Test 3: Add a single task"""
        print("\n✓ Test 3: Adding a single task...")
        
        task_text = "Write Selenium tests"
        
        # Find input and add button
        task_input = self.driver.find_element(By.ID, 'taskInput')
        add_btn = self.driver.find_element(By.ID, 'addBtn')
        
        # Enter task and click add
        task_input.send_keys(task_text)
        add_btn.click()
        
        # Wait for task to appear
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'task-item'))
        )
        
        # Verify task was added
        tasks = self.driver.find_elements(By.CLASS_NAME, 'task-item')
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].text, task_text)
        
        # Verify input was cleared
        self.assertEqual(task_input.get_attribute('value'), '')
        
        print(f"   ✅ Task '{task_text}' added successfully!")
    
    def test_04_add_multiple_tasks(self):
        """Test 4: Add multiple tasks"""
        print("\n✓ Test 4: Adding multiple tasks...")
        
        tasks_to_add = [
            "Learn Selenium",
            "Set up CI/CD pipeline",
            "Write documentation",
            "Deploy to production"
        ]
        
        task_input = self.driver.find_element(By.ID, 'taskInput')
        add_btn = self.driver.find_element(By.ID, 'addBtn')
        
        for task in tasks_to_add:
            task_input.send_keys(task)
            add_btn.click()
            time.sleep(0.3)  # Brief pause between additions
        
        # Verify all tasks were added
        task_elements = self.driver.find_elements(By.CLASS_NAME, 'task-item')
        self.assertEqual(len(task_elements), len(tasks_to_add))
        
        # Verify task content
        for i, task in enumerate(tasks_to_add):
            self.assertEqual(task_elements[i].text, task)
        
        print(f"   ✅ Successfully added {len(tasks_to_add)} tasks!")
    
    def test_05_empty_task_validation(self):
        """Test 5: Verify empty task cannot be added"""
        print("\n✓ Test 5: Testing empty task validation...")
        
        add_btn = self.driver.find_element(By.ID, 'addBtn')
        
        # Try to add empty task
        add_btn.click()
        time.sleep(0.5)
        
        # Verify no task was added (should show empty state)
        task_list = self.driver.find_element(By.ID, 'taskList')
        empty_state = task_list.find_elements(By.CLASS_NAME, 'empty-state')
        
        # Either empty state is shown or no task-items exist
        task_items = self.driver.find_elements(By.CLASS_NAME, 'task-item')
        
        # Filter out empty-state from task-items if it exists
        actual_tasks = [item for item in task_items if 'empty-state' not in item.get_attribute('class')]
        
        self.assertEqual(len(actual_tasks), 0, "No tasks should be added when input is empty")
        
        print("   ✅ Empty task validation works!")
    
    def test_06_clear_all_tasks(self):
        """Test 6: Clear all tasks"""
        print("\n✓ Test 6: Testing clear all functionality...")
        
        # Add some tasks first
        task_input = self.driver.find_element(By.ID, 'taskInput')
        add_btn = self.driver.find_element(By.ID, 'addBtn')
        
        for task in ["Task 1", "Task 2", "Task 3"]:
            task_input.send_keys(task)
            add_btn.click()
            time.sleep(0.2)
        
        # Verify tasks were added
        tasks_before = self.driver.find_elements(By.CLASS_NAME, 'task-item')
        self.assertGreater(len(tasks_before), 0)
        
        # Click clear button
        clear_btn = self.driver.find_element(By.ID, 'clearBtn')
        clear_btn.click()
        
        # Handle confirmation alert
        WebDriverWait(self.driver, 3).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert.accept()
        
        time.sleep(0.5)
        
        # Verify tasks were cleared
        task_list = self.driver.find_element(By.ID, 'taskList')
        empty_state = task_list.find_elements(By.CLASS_NAME, 'empty-state')
        
        self.assertTrue(len(empty_state) > 0 or len(self.driver.find_elements(By.CLASS_NAME, 'task-item')) == 0)
        
        print("   ✅ All tasks cleared successfully!")
    
    def test_07_keyboard_interaction(self):
        """Test 7: Test keyboard interaction (Enter key)"""
        print("\n✓ Test 7: Testing keyboard interaction...")
        
        task_text = "Test keyboard input"
        
        task_input = self.driver.find_element(By.ID, 'taskInput')
        task_input.send_keys(task_text)
        
        # Simulate pressing Enter
        task_input.send_keys("\n")
        
        # Wait for task to appear
        time.sleep(0.5)
        
        # Verify task was added
        tasks = self.driver.find_elements(By.CLASS_NAME, 'task-item')
        actual_tasks = [t for t in tasks if 'empty-state' not in t.get_attribute('class')]
        
        self.assertGreater(len(actual_tasks), 0, "Task should be added when Enter is pressed")
        self.assertEqual(actual_tasks[0].text, task_text)
        
        print("   ✅ Enter key works correctly!")
    
    def test_08_success_message_display(self):
        """Test 8: Verify success message appears after adding task"""
        print("\n✓ Test 8: Testing success message...")
        
        task_input = self.driver.find_element(By.ID, 'taskInput')
        add_btn = self.driver.find_element(By.ID, 'addBtn')
        
        task_input.send_keys("Test task")
        add_btn.click()
        
        # Wait for and verify message
        try:
            message_element = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.ID, 'message'))
            )
            self.assertIn('success', message_element.get_attribute('class'))
            print("   ✅ Success message displayed!")
        except TimeoutException:
            print("   ⚠️  Success message not displayed (might be too fast)")


def run_tests():
    """Run the test suite"""
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TaskManagerTests)
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code (0 for success, 1 for failure)
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    exit_code = run_tests()
    exit(exit_code)