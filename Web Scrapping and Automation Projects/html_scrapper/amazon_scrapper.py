from datetime import datetime
import requests
import csv
import bs4
import concurrent.futures
from tqdm import tqdm

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0'
REQUEST_HEADER = {
    'User-Agent': USER_AGENT,
    'Accept-Language': 'en-US, en;q=0.5',
}

NO_THREADS = 10

def get_page_html(url):
    res = requests.get(url=url, headers=REQUEST_HEADER)
    return res.content

def get_product_price(soup):
    main_price_span = soup.find('span', attrs={
        'class': 'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'
    })
    if main_price_span:
        price_spans = main_price_span.findAll('span')
        for span in price_spans:
            price = span.text.strip().replace(',', '').replace('₹', '')
            try:
                return float(price)
            except ValueError:
                continue
    return None

def get_product_title(soup):
    product_title = soup.find('span', id='productTitle')
    return product_title.text.strip() if product_title else "Title not found"

def get_product_ratings(soup):
    product_ratings = soup.find('div', attrs={'id': 'cm_cr_dp_d_rating_histogram'})
    if product_ratings:
        product_ratings_section = product_ratings.find('i', attrs={'class': 'a-icon a-icon-star-medium a-star-medium-4-5'})
        if product_ratings_section:
            product_ratings_span = product_ratings_section.find('span')
            try:
                rating = product_ratings_span.text.strip().split()[0]
                return float(rating)
            except (ValueError, AttributeError):
                pass
    print("Ratings not found or could not be parsed")
    return None

def get_product_technical_details(soup):
    details = {}
    technical_details_section = soup.find('div', id='prodDetails')
    if technical_details_section:
        data_tables = technical_details_section.findAll('table', class_='prodDetTable')
        for table in data_tables:
            table_rows = table.findAll('tr')
            for row in table_rows:
                row_key = row.find('th').text.strip()
                row_value = row.find('td').text.strip().replace('\u200e', '').replace('\n', '')
                details[row_key] = row_value
    return details

def extract_product_info(url, output):
    product_info = {}
    html = get_page_html(url=url)
    soup = bs4.BeautifulSoup(html, 'lxml')
    product_info['price'] = get_product_price(soup)
    product_info['title'] = get_product_title(soup)
    product_info['ratings'] = get_product_ratings(soup)
    product_info.update(get_product_technical_details(soup))
    output.append(product_info)

if __name__ == "__main__":
    products_data = []
    urls = []

    print("HELLO")
    with open('products_url.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            urls.append(row[0])
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=NO_THREADS) as executor:
        list(tqdm(executor.map(lambda url: extract_product_info(url, products_data), urls), total=len(urls)))
    
    if products_data:
        output_file_name = 'output-{}.csv'.format(datetime.today().strftime("%d-%m-%Y"))
        with open(output_file_name, 'w', encoding='utf-8', newline='') as outputfile:
            writer = csv.writer(outputfile)
            writer.writerow(products_data[0].keys())
            for product in products_data:
                writer.writerow(product.values())
    else:
        print("No product data was extracted.")
