from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from page_objects import ActionUtils
from test_data import domain


class AdminPage(ActionUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.admin_url = f'{domain}admin/products.html'
        self.create_url = f'{domain}admin/product_create.html'

        # Element locators
        self.create_product_btn_locator = (By.XPATH, '//button[text()="Create New Product"]')
        self.delete_btn_locator = (By.XPATH, '//button[text()="刪除"]')

        # Element locators for create page
        self.category_selector_locator = (By.XPATH, '//select[@name="category"]')
        self.title_input_locator = (By.XPATH, '//input[@name="title"]')
        self.desc_textarea_locator = (By.XPATH, '//textarea[@name="description"]')
        self.price_input_locator = (By.XPATH, '//input[@name="price"]')
        self.texture_input_locator = (By.XPATH, '//input[@name="texture"]')
        self.wash_input_locator = (By.XPATH, '//input[@name="wash"]')
        self.place_input_locator = (By.XPATH, '//input[@name="place"]')
        self.note_input_locator = (By.XPATH, '//input[@name="note"]')

        self.color_input_locator = (By.XPATH, '//input[@id="color_ids"]')
        self.color_label_locator = (By.XPATH, '//input[@id="color_ids"]/following-sibling::label')

        self.size_input_locator = (By.XPATH, '//input[@name="sizes"]')

        self.story_input_locator = (By.XPATH, '//input[@name="story"]')

        self.main_image_input_locator = (By.XPATH, '//input[@name="main_image"]')
        self.other_image_input_locator = (By.XPATH, '//input[@name="other_images"]')

        self.create_btn_locator = (By.XPATH, '//input[@value="Create"]')

    def open_create_page(self):
        self.find_clickable_element(self.create_product_btn_locator).click()
        return self

    def delete_product(self):
        if self.find_present_elements(self.delete_btn_locator) != []:
            target_delete_btn = self.find_present_elements(self.delete_btn_locator)[-1]
            target_delete_btn.click()
        return self

    # ------------ Methods below this line belong to create product page ------------

    def fill_in_product_data(self, row):
        # Category
        Select(self.find_clickable_element(self.category_selector_locator)).select_by_visible_text(row['Category'])
        # Title
        self.find_clickable_element(self.title_input_locator).send_keys(row['Title'])
        # Description
        self.find_clickable_element(self.desc_textarea_locator).send_keys(row['Description'])
        # Price
        self.find_clickable_element(self.price_input_locator).send_keys(row['Price'])
        # Texture
        self.find_clickable_element(self.texture_input_locator).send_keys(row['Texture'])
        # Wash
        self.find_clickable_element(self.wash_input_locator).send_keys(row['Wash'])
        # Place of Production
        self.find_clickable_element(self.place_input_locator).send_keys(row['Place of Product'])
        # Note
        self.find_clickable_element(self.note_input_locator).send_keys(row['Note'])

        # Colors
        target_color_list = row['Colors'].split(', ')
        color_input_elems = self.find_present_elements(self.color_input_locator)
        color_label_elems = self.find_present_elements(self.color_label_locator)
        if row['Colors'] == '全選':
            for elem in color_input_elems:
                elem.click()
        elif row['Colors'] != '':
            for i in range(len(color_label_elems)):
                if color_label_elems[i].text in target_color_list:
                    color_input_elems[i].click()

        # Sizes
        target_size_list = row['Sizes'].split(', ')
        size_input_elems = self.find_present_elements(self.size_input_locator)
        for elem in size_input_elems:
            if row['Sizes'] == '全選':
                elem.click()
            elif row['Sizes'] != '':
                if elem.get_attribute('value') in target_size_list:
                    elem.click()

        # Story
        self.find_clickable_element(self.story_input_locator).send_keys(row['Story'])

        # Images
        root_path = Path(__file__).parent.parent
        main_image_path = r'\test_data\product_images\mainImage.jpg'
        other_image0_path = r'\test_data\product_images\otherImage0.jpg'
        other_image1_path = r'\test_data\product_images\otherImage1.jpg'
        if row['Main Image'] != '':
            self.find_clickable_element(self.main_image_input_locator).send_keys(f'{root_path}\\{main_image_path}')
        if row['Other Image 1'] != '':
            self.find_present_elements(self.other_image_input_locator)[0].send_keys(f'{root_path}\\{other_image0_path}')
        if row['Other Image 2'] != '':
            self.find_present_elements(self.other_image_input_locator)[1].send_keys(f'{root_path}\\{other_image1_path}')

        return self

    def click_create_btn(self):
        self.find_clickable_element(self.create_btn_locator).click()
        return self
