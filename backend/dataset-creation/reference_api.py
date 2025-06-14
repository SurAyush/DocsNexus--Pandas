from bs4 import BeautifulSoup
from pathlib import Path
import re
import pandas as pd
from tqdm import tqdm
import concurrent.futures

class DocumentationExtractor:

    def __init__(self, folder_path):

        self.folder_path = folder_path
        self.all_data = []
        self.missing_files = []
        self.error_files = [] 
        self.counter = 0

    def extract_all(self, thread_count:int = 1):
        """
        Extracts all essential information from all files in the specified folder and save necessary data to a CSV file.
        """
        assert thread_count > 0, "Thread count must be greater than 0"

        files = [f for f in Path(self.folder_path).iterdir() if f.is_file()]
        interval = len(files) // thread_count
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.execute_thread, files[i:i + interval]) for i in range(0, len(files), interval)]

            for future in concurrent.futures.as_completed(futures):
                result = future.result()        # blocks until the thread is finished
                print(f"Result: {result}")

    
        df = pd.DataFrame(self.all_data)
        df.to_csv('documentation_data.csv', index=False)
        print(f"Extraction complete. Total files processed: {len(self.all_data)}")
        if self.missing_files:
            with open("output.txt", "a", encoding="utf-8") as f:
                for file_path in self.missing_files:
                    f.write(str(file_path) + "\n")
        
        if self.error_files:
            with open("error_files.txt", "a", encoding="utf-8") as f:
                for file_path in self.error_files:
                    f.write(str(file_path) + "\n")
        

    def execute_thread(self, files):

        success_count = 0
        fail_count = 0
        
        with tqdm(total=len(files), desc="Processing files", unit='file') as pbar:
            for file_path in files:
                result = self.extract_file(file_path)
                if result:
                    success_count += 1
                else:
                    fail_count += 1
                
                pbar.update(1)
        
        return f"Thread Completed: Processed {file_path}: Successes: {success_count}, Failures: {fail_count}"

    def extract_file(self, file_path):
        """
        Extracts all essential information from a given file.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                soup = BeautifulSoup(content, 'html.parser')
            
            # Check if the page is a redirect page
            is_redirect = self.is_redirect_page(soup)
            if is_redirect:
                return True 

            function_signature = self.extract_function_signature(soup)
            
            # py method, py property, py attribute, py function
            dl = soup.find('dl',class_='py')
            
            # Remove the "See also" section
            see_also = dl.find('div', class_='admonition seealso')
            if see_also:
                see_also.decompose() 

            # Extracting parameters 
            parameters = dl.find('dl', class_='field-list')
            if parameters:
                parameters.extract()

            # Extract the examples
            examples = dl.find_all('div',class_='doctest highlight-default notranslate')
            for example in examples:
                example.extract()  

            # Remove the example header & contents after
            example_header = dl.find_all('p', class_='rubric')
            if example_header:
                example_header = example_header[-1]
            
            # Remove all content that comes after this div
            if example_header:
                next_sibling = example_header.find_next_sibling()
                while next_sibling:
                    to_delete = next_sibling
                    next_sibling = next_sibling.find_next_sibling()
                    to_delete.decompose()
                if example_header:
                    example_header.decompose()

            body_text = dl.text.strip()
            collapsed_body = re.sub(r'\n+',' ',body_text)

            parametric_body = parameters.text.strip() if parameters else 'No parameters found'
            collapsed_parametric_body = re.sub(r'\n+',' ', parametric_body)

            dict_data = {
                'id': self.counter,
                'file_path': str(file_path),
                'function_signature': function_signature,
                'body': collapsed_body,
                'parameters': collapsed_parametric_body,
                'examples': [example.text.strip() for example in examples]
            }
            self.counter += 1
            self.all_data.append(dict_data)
            
            return True

        except FileNotFoundError:
            # print(f"File {file_path} not found.")
            self.missing_files.append(file_path)
            return None
        
        except Exception as e:
            # print(f"Error reading file {file_path}: {e}")
            self.error_files.append(file_path)
            return None
        
    def is_redirect_page(self,soup):
        """
        Checks if the page is a redirect page.
        """
        meta = soup.find('meta', attrs={'http-equiv': 'refresh'})
        if meta:
            return True
        return False
        

    def extract_function_signature(self, soup):
        """
        Extracts the function signature from the BeautifulSoup object.
        """

        function_signature = soup.find('h1').text.strip()
    
        return function_signature.strip('#')
    


de = DocumentationExtractor('../pandas/reference/api')
de.extract_all(thread_count=8)
