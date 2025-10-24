<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="html" encoding="UTF-8" indent="yes"/>

  <xsl:key name="nhanvien-by-manv" match="NHANVIEN" use="MANV"/>
  <xsl:key name="mon-by-mamon" match="MON" use="MAMON"/>
  <xsl:key name="ban-by-soban" match="BAN" use="SOBAN"/>
  <xsl:key name="mon-goi-nhieu-lan" match="CTHD[SOLUONG > 1]" use="MAMON"/>

  <xsl:template match="/QUANLY">
    <html>
      <head>
        <title>Bài 3: Truy vấn XSLT - Quản lý Bán ăn</title>
        <style>
          body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
          h2 { color: #d9534f; border-bottom: 2px solid #d9534f; padding-bottom: 5px; margin-top: 40px;}
          table { width: 100%; border-collapse: collapse; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
          th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
          th { background-color: #f8f9fa; font-weight: bold; }
          caption { font-weight: bold; font-size: 1.2em; padding: 10px; color: #333; text-align: left; }
        </style>
      </head>
      <body>
        <h1>Kết quả truy vấn thông tin Quản lý Bán ăn</h1>
        
        <xsl:apply-templates select="." mode="cau1"/>
        <xsl:apply-templates select="." mode="cau2"/>
        <xsl:apply-templates select="." mode="cau3"/>
        <xsl:apply-templates select="." mode="cau4"/>
        <xsl:apply-templates select="." mode="cau5"/>
        <xsl:apply-templates select="." mode="cau6"/>
        <xsl:apply-templates select="." mode="cau7"/>
        <xsl:apply-templates select="." mode="cau8"/>
        <xsl:apply-templates select="." mode="cau9"/>
        <xsl:apply-templates select="." mode="cau10"/>
        <xsl:apply-templates select="." mode="cau11"/>
        <xsl:apply-templates select="." mode="cau12"/>
        <xsl:apply-templates select="." mode="cau13"/>
        <xsl:apply-templates select="." mode="cau14"/>

      </body>
    </html>
  </xsl:template>

  <xsl:template match="QUANLY" mode="cau1">
    <h2>1. Danh sách các bàn</h2>
    <table>
      <tr><th>STT</th><th>Số Bàn</th><th>Tên Bàn</th></tr>
      <xsl:for-each select="BANS/BAN">
        <tr>
          <td><xsl:number/></td>
          <td><xsl:value-of select="SOBAN"/></td>
          <td><xsl:value-of select="TENBAN"/></td>
        </tr>
      </xsl:for-each>
    </table>
  </xsl:template>

  <xsl:template match="QUANLY" mode="cau2">
    <h2>2. Danh sách nhân viên</h2>
    <table>
      <tr><th>STT</th><th>Mã NV</th><th>Tên NV</th><th>Giới tính</th><th>Địa chỉ</th></tr>
      <xsl:for-each select="NHANVIENS/NHANVIEN">
        <tr>
          <td><xsl:number/></td>
          <td><xsl:value-of select="MANV"/></td>
          <td><xsl:value-of select="TENV"/></td>
          <td><xsl:value-of select="GIOITINH"/></td>
          <td><xsl:value-of select="DIACHI"/></td>
        </tr>
      </xsl:for-each>
    </table>
  </xsl:template>

  <xsl:template match="QUANLY" mode="cau3">
    <h2>3. Danh sách món ăn</h2>
    <table>
      <tr><th>STT</th><th>Mã Món</th><th>Tên Món</th><th>Giá</th></tr>
      <xsl:for-each select="MONS/MON">
        <tr>
          <td><xsl:number/></td>
          <td><xsl:value-of select="MAMON"/></td>
          <td><xsl:value-of select="TENMON"/></td>
          <td><xsl:value-of select="format-number(GIA, '#,###')"/> đ</td>
        </tr>
      </xsl:for-each>
    </table>
  </xsl:template>

  <xsl:template match="QUANLY" mode="cau4">
    <h2>4. Thông tin nhân viên NV02</h2>
    <table>
      <xsl:variable name="nv" select="key('nhanvien-by-manv', 'NV02')"/>
      <tr><th>Mã NV</th><td><xsl:value-of select="$nv/MANV"/></td></tr>
      <tr><th>Tên NV</th><td><xsl:value-of select="$nv/TENV"/></td></tr>
      <tr><th>SĐT</th><td><xsl:value-of select="$nv/SDT"/></td></tr>
    </table>
  </xsl:template>
  
  <xsl:template match="QUANLY" mode="cau5">
    <h2>5. Các món ăn có giá trên 50,000</h2>
    <table>
      <tr><th>STT</th><th>Tên Món</th><th>Giá</th></tr>
      <xsl:for-each select="MONS/MON[GIA > 50000]">
        <tr>
          <td><xsl:number/></td>
          <td><xsl:value-of select="TENMON"/></td>
          <td><xsl:value-of select="format-number(GIA, '#,###')"/> đ</td>
        </tr>
      </xsl:for-each>
    </table>
  </xsl:template>
  
  <xsl:template match="QUANLY" mode="cau6">
    <xsl:variable name="hd" select="HOADONS/HOADON[SOHD='HD03']"/>
    <h2>6. Chi tiết hóa đơn HD03</h2>
    <table>
      <tr><th>Số HĐ</th><td><xsl:value-of select="$hd/SOHD"/></td></tr>
      <tr><th>Ngày lập</th><td><xsl:value-of select="$hd/NGAYLAP"/></td></tr>
      <tr><th>Tên nhân viên phục vụ</th><td><xsl:value-of select="key('nhanvien-by-manv', $hd/MANV)/TENV"/></td></tr>
      <tr><th>Số bàn</th><td><xsl:value-of select="$hd/SOBAN"/></td></tr>
      <tr><th>Tổng tiền</th><td><xsl:value-of select="format-number($hd/TONGTIEN, '#,###')"/> đ</td></tr>
    </table>
  </xsl:template>
  
  <xsl:template match="QUANLY" mode="cau7">
    <h2>7. Các món ăn trong hóa đơn HD02</h2>
    <table>
      <tr><th>STT</th><th>Tên Món</th><th>Số lượng</th></tr>
      <xsl:for-each select="HOADONS/HOADON[SOHD='HD02']/CTHDS/CTHD">
        <tr>
          <td><xsl:number/></td>
          <td><xsl:value-of select="key('mon-by-mamon', MAMON)/TENMON"/></td>
          <td><xsl:value-of select="SOLUONG"/></td>
        </tr>
      </xsl:for-each>
    </table>
  </xsl:template>

  <xsl:template match="QUANLY" mode="cau8">
    <h2>8. Nhân viên lập hóa đơn HD02</h2>
    <p>Tên nhân viên: <strong><xsl:value-of select="key('nhanvien-by-manv', HOADONS/HOADON[SOHD='HD02']/MANV)/TENV"/></strong></p>
  </xsl:template>
  
  <xsl:template match="QUANLY" mode="cau9">
    <h2>9. Đếm số bàn</h2>
    <p>Tổng số bàn: <strong><xsl:value-of select="count(BANS/BAN)"/></strong></p>
  </xsl:template>
  
  <xsl:template match="QUANLY" mode="cau10">
    <h2>10. Số hóa đơn nhân viên NV01 đã lập</h2>
    <p>Nhân viên <strong><xsl:value-of select="key('nhanvien-by-manv', 'NV01')/TENV"/></strong> đã lập <strong><xsl:value-of select="count(HOADONS/HOADON[MANV='NV01'])"/></strong> hóa đơn.</p>
  </xsl:template>
  
  <xsl:template match="QUANLY" mode="cau11">
    <h2>11. Các món ăn đã bán cho Bàn 2</h2>
    <table>
      <tr><th>STT</th><th>Tên món</th><th>Số lượng</th></tr>
      <xsl:for-each select="HOADONS/HOADON[SOBAN='2']/CTHDS/CTHD">
        <tr>
          <td><xsl:number/></td>
          <td><xsl:value-of select="key('mon-by-mamon', MAMON)/TENMON"/></td>
          <td><xsl:value-of select="SOLUONG"/></td>
        </tr>
      </xsl:for-each>
    </table>
  </xsl:template>
  
  <xsl:template match="QUANLY" mode="cau12">
    <h2>12. Nhân viên đã phục vụ Bàn 3</h2>
    <table>
      <tr><th>STT</th><th>Tên nhân viên</th></tr>
      <xsl:for-each select="HOADONS/HOADON[SOBAN='3']">
        <tr>
          <td><xsl:number/></td>
          <td><xsl:value-of select="key('nhanvien-by-manv', MANV)/TENV"/></td>
        </tr>
      </xsl:for-each>
    </table>
  </xsl:template>

  <xsl:template match="QUANLY" mode="cau13">
    <h2>13. Các món được gọi với số lượng trên 1</h2>
    <table>
      <tr><th>STT</th><th>Tên món</th></tr>
      <xsl:for-each select="//CTHD[SOLUONG > 1][count(. | key('mon-goi-nhieu-lan', MAMON)[1]) = 1]">
        <tr>
          <td><xsl:number/></td>
          <td><xsl:value-of select="key('mon-by-mamon', MAMON)/TENMON"/></td>
        </tr>
      </xsl:for-each>
    </table>
  </xsl:template>

  <xsl:template match="QUANLY" mode="cau14">
    <xsl:variable name="hd" select="HOADONS/HOADON[SOHD='HD04']"/>
    <h2>14. Chi tiết thanh toán hóa đơn HD04</h2>
    <table>
      <tr><th>STT</th><th>Mã món</th><th>Tên món</th><th>Đơn giá</th><th>Số lượng</th><th>Thành tiền</th></tr>
      <xsl:for-each select="$hd/CTHDS/CTHD">
        <xsl:variable name="mon" select="key('mon-by-mamon', MAMON)"/>
        <tr>
          <td><xsl:number/></td>
          <td><xsl:value-of select="MAMON"/></td>
          <td><xsl:value-of select="$mon/TENMON"/></td>
          <td><xsl:value-of select="format-number($mon/GIA, '#,###')"/> đ</td>
          <td><xsl:value-of select="SOLUONG"/></td>
          <td><xsl:value-of select="format-number($mon/GIA * SOLUONG, '#,###')"/> đ</td>
        </tr>
      </xsl:for-each>
      <tr style="font-weight: bold; background-color: #f2f2f2;">
          <td colspan="5" style="text-align:right;">TỔNG CỘNG:</td>
          <td><xsl:value-of select="format-number($hd/TONGTIEN, '#,###')"/> đ</td>
      </tr>
    </table>
  </xsl:template>

</xsl:stylesheet>