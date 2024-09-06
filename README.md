# ShopWiseMate

**ShopWiseMate** is a comprehensive price comparison tool designed to help users find the best deals across multiple e-commerce websites. By using advanced web scraping techniques and a user-friendly interface, ShopWiseMate allows consumers to make informed purchasing decisions efficiently and conveniently.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **Price Comparison:** Compare prices across various e-commerce websites in real-time.
- **User-Friendly Interface:** Easy-to-navigate interface with a responsive design.
- **Web Scraping:** Efficiently gathers data from multiple sources using web scraping techniques.
- **Search and Filter Options:** Advanced search and filtering capabilities for specific products, categories, and price ranges.
- **Customizable Alerts:** Set alerts for price drops or specific deals.
- **Secure Data Management:** Built with secure data handling practices, utilizing Flask and MongoDB.

## Installation

To get started with ShopWiseMate, follow these steps:

1. **Clone the repository:**
    ```bash
    git clone git@github.com:kimaninyutu/ShopWiseMate.git
    cd ShopWiseMate
    ```

2. **Install required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure environment variables:**
    - Create a `.env` file in the root directory and add your configurations:
    ```env
    FLASK_APP=main.py
    FLASK_ENV=development
    MONGO_URI=your_mongodb_uri
    ```

4. **Run the application:**
    ```bash
    flask run
    ```

## Usage

1. Visit `http://localhost:5000` in your web browser.
2. Enter a product name or category in the search bar.
3. Filter results by price range, store, or other criteria.
4. View and compare product prices from multiple e-commerce sites.
5. Set alerts for price changes or specific deals.

## Technologies Used

- **Front-End:** HTML, CSS, JavaScript, Bootstrap
- **Back-End:** Python, Flask
- **Database:** MongoDB
- **Web Scraping:** BeautifulSoup, Requests
- **Other Tools:** Git, Docker (if applicable)

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

**Kimani Hezekiah Nyutu**  
Email: [kimani.hezekiah21@students.dkut.ac.ke](mailto:kimani.hezekiah21@students.dkut.ac.ke)  
Project Link: [git@github.com:kimaninyutu/ShopWiseMate.git](git@github.com:kimaninyutu/ShopWiseMate.git)
