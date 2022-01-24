def fetch_data(self, file_to_write) -> None:
        pages = self.fetch_pages()
        self.check_file_existance(file_to_write)
        with open(file_to_write, "w") as file_handler:
            for page_number in pages:
                json_request = self.config_post_request(page_number)
                req = requests.post(CIAN_API_URL, headers=HEADERS, json=json_request)
                receivied_data = req.json()
                print(f"Parsed {page_number}!")
                file_handler.write(json.dumps(receivied_data, indent=4))



 def fetch_data(self, file_to_write) -> None:
        pages = self.fetch_pages()
        self.check_file_existance(file_to_write)
        payloads = [self.config_payload(page) for page in pages]
        dumping_data = asyncio.get_event_loop().run_until_complete(AiohttpClient.fetch_all_pages(CIAN_API_URL, HEADERS, payloads))
        print('='*25)
        # print(dumping_data)
        
        with open(file_to_write, 'w') as json_handler:
            json.dump(['a']+dumping_data, json_handler, indent=4)