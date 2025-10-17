import mysql.connector
from lxml import etree
import sys

# --- Dữ liệu XML và XSD mẫu (từ file PDF) ---

# Dữ liệu XML từ nhà cung cấp [cite: 4-21]
XML_DATA = """
<catalog>
  <categories>
    <category id="c1">Electronics</category>
    <category id="c2">Smartphone</category>
    <category id="c3">Accessories</category>
  </categories>
  <products>
    <product id="p001" categoryRef="c1">
      <name>Laptop Dell Inspiron</name>
      <price currency="USD">750</price>
      <stock>120</stock>
    </product>
    <product id="p002" categoryRef="c2">
      <name>iPhone 15 Pro</name>
      <price currency="USD">1200</price>
      <stock>50</stock>
    </product>
    <product id="p003" categoryRef="c3">
      <name>Tai nghe Bluetooth Sony</name>
      <price currency="USD">99</price>
      <stock>300</stock>
    </product>
  </products>
</catalog>
"""

# Dữ liệu XSD (thiết kế ở bước 1)
XSD_DATA = """
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:complexType name="CategoryType">
    <xs:simpleContent>
      <xs:extension base="xs:string">
        <xs:attribute name="id" type="xs:string" use="required" />
      </xs:extension>
    </xs:simpleContent>
  </xs:complexType>
  <xs:complexType name="PriceType">
    <xs:simpleContent>
      <xs:extension base="xs:decimal">
        <xs:attribute name="currency" type="xs:string" use="required" />
      </xs:extension>
    </xs:simpleContent>
  </xs:complexType>
  <xs:complexType name="ProductType">
    <xs:sequence>
      <xs:element name="name" type="xs:string" />
      <xs:element name="price" type="PriceType" />
      <xs:element name="stock" type="xs:nonNegativeInteger" />
    </xs:sequence>
    <xs:attribute name="id" type="xs:string" use="required" />
    <xs:attribute name="categoryRef" type="xs:string" use="required" />
  </xs:complexType>
  <xs:element name="catalog">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="categories">
          <xs:complexType>
            <xs:sequence>
              <xs:element name="category" type="CategoryType" maxOccurs="unbounded" />
            </xs:sequence>
          </xs:complexType>
        </xs:element>
        <xs:element name="products">
          <xs:complexType>
            <xs:sequence>
              <xs:element name="product" type="ProductType" maxOccurs="unbounded" />
            </xs:sequence>
          </xs:complexType>
        </xs:element>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>
"""

# --- Cấu hình MySQL ---
# !!! Thay đổi các giá trị này cho phù hợp với môi trường của bạn
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': "",
    'database': 'thuongmaidientu' # Tên CSDL
}

def validate_xml(xml_content, xsd_content):
    """
    Validate XML content against XSD content.
    Returns the parsed XML tree if valid, otherwise returns None.
    """
    try:
        # Parse XSD [cite: 29]
        xsd_doc = etree.fromstring(xsd_content.encode('utf-8'))
        # Tạo XMLSchema object [cite: 30]
        schema = etree.XMLSchema(xsd_doc)
        
        # Parse XML [cite: 29]
        xml_doc = etree.fromstring(xml_content.encode('utf-8'))
        
        # Validate XML với XSD 
        schema.assertValid(xml_doc)
        print("Thông báo: XML hợp lệ.")
        return xml_doc # [cite: 33]
        
    except etree.DocumentInvalid as e:
        # Không hợp lệ, báo lỗi cụ thể [cite: 32]
        print(f"LỖI: XML không hợp lệ.\nChi tiết: {e}")
        return None
    except etree.XMLSyntaxError as e:
        print(f"LỖI: Cú pháp XML hoặc XSD bị lỗi.\nChi tiết: {e}")
        return None
    except Exception as e:
        print(f"LỖI: Đã xảy ra lỗi không xác định trong quá trình validate.\nChi tiết: {e}")
        return None

def create_tables(cursor):
    """
    Tạo bảng Categories và Products nếu chưa có [cite: 35]
    """
    try:
        # Bảng Categories [cite: 38]
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Categories (
            id VARCHAR(50) PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
        """)
        
        # Bảng Products [cite: 39]
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Products (
            id VARCHAR(50) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            currency VARCHAR(10) NOT NULL,
            stock INT NOT NULL,
            categoryRef VARCHAR(50),
            FOREIGN KEY (categoryRef) REFERENCES Categories(id)
        )
        """)
        print("Thông báo: Đã kiểm tra và tạo bảng (nếu cần).")
    except mysql.connector.Error as err:
        print(f"LỖI: Không thể tạo bảng: {err}")
        raise # Ném lại lỗi để dừng thực thi

def sync_data_to_db(xml_doc, db_connection):
    """
    Trích xuất dữ liệu bằng XPath và đồng bộ vào MySQL.
    """
    cursor = db_connection.cursor()
    
    try:
        # --- 1. Đồng bộ Categories ---
        
        # Dùng XPath để lấy dữ liệu từ categories [cite: 36]
        categories = xml_doc.xpath("/catalog/categories/category")
        
        sql_insert_category = """
        INSERT INTO Categories (id, name)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE name = VALUES(name)
        """ # [cite: 24]
        
        category_data = []
        for cat in categories:
            cat_id = cat.get('id')
            cat_name = cat.text
            category_data.append((cat_id, cat_name))
            
        if category_data:
            cursor.executemany(sql_insert_category, category_data)
            print(f"Thông báo: Đã đồng bộ {len(category_data)} danh mục.")
            
        # --- 2. Đồng bộ Products ---
        
        # Dùng XPath để lấy dữ liệu từ products [cite: 36]
        products = xml_doc.xpath("/catalog/products/product")
        
        sql_insert_product = """
        INSERT INTO Products (id, name, price, currency, stock, categoryRef)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            price = VALUES(price),
            currency = VALUES(currency),
            stock = VALUES(stock),
            categoryRef = VALUES(categoryRef)
        """ # [cite: 24]
        
        product_data = []
        for prod in products:
            prod_id = prod.get('id')
            category_ref = prod.get('categoryRef') # [cite: 39]
            name = prod.find('name').text
            price = prod.find('price').text
            currency = prod.find('price').get('currency')
            stock = prod.find('stock').text
            product_data.append((prod_id, name, price, currency, stock, category_ref))
            
        if product_data:
            cursor.executemany(sql_insert_product, product_data)
            print(f"Thông báo: Đã đồng bộ {len(product_data)} sản phẩm.")
            
        # Commit các thay đổi
        db_connection.commit() # [cite: 37]
        print("Thông báo: Đồng bộ dữ liệu thành công!")
        
    except Exception as e:
        print(f"LỖI: Lỗi khi đồng bộ dữ liệu: {e}")
        db_connection.rollback()
    finally:
        cursor.close()

def main():
    """
    Hàm chính thực thi toàn bộ quy trình.
    """
    # 1. Validate XML [cite: 22]
    xml_tree = validate_xml(XML_DATA, XSD_DATA)
    
    # 2. Nếu không hợp lệ, dừng lại [cite: 32]
    if xml_tree is None:
        print("Kết thúc: Xử lý thất bại do XML không hợp lệ.")
        sys.exit(1) # Thoát với mã lỗi
        
    # 3. Hợp lệ, kết nối MySQL [cite: 33, 34]
    db_conn = None
    try:
        db_conn = mysql.connector.connect(**DB_CONFIG)
        print(f"Thông báo: Kết nối MySQL đến database '{DB_CONFIG['database']}' thành công.")
        
        cursor = db_conn.cursor()
        
        # 4. Tạo bảng (nếu chưa có) [cite: 35]
        create_tables(cursor)
        
        # 5. Dùng XPath lấy dữ liệu và Insert/Update vào MySQL [cite: 36, 37]
        sync_data_to_db(xml_tree, db_conn)
        
        cursor.close()
        
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print(f"LỖI: Database '{DB_CONFIG['database']}' không tồn tại.")
            # Có thể thử tạo DB ở đây nếu muốn
        else:
            print(f"LỖI: Không thể kết nối hoặc thao tác với MySQL: {err}")
    finally:
        if db_conn and db_conn.is_connected():
            db_conn.close()
            print("Thông báo: Đã đóng kết nối MySQL.")

if __name__ == "__main__":
    main()