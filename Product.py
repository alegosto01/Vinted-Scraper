

class Product:
    def __init__(self, title, price, brand, size, link, image_url, data_id):
        self.title = title
        self.price = price
        self.brand = brand
        self.size = size
        self.link = link
        self.image_url = image_url
        self.data_id = data_id

    # def save_to_excel(self, filename):
    #     # Save the product information to Excel

    # def download_image(self, path):
    #     # Code to download the product image
