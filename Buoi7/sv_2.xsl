<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html" encoding="UTF-8" indent="yes"/>

  <xsl:key name="student-by-id" match="student" use="id"/>
  <xsl:key name="course-by-id" match="course" use="id"/>
  <xsl:key name="student-by-month" match="student" use="substring(date, 6, 2)"/>
  <xsl:key name="enrolled-course-refs" match="enrollment" use="courseRef"/>
  
  <xsl:template match="/school">
    <html>
      <head>
        <title>Buổi 7: XSLT - Thông tin sinh viên</title>
        <style>
          body { font-family: Arial, sans-serif; margin: 20px; }
          h2 { color: #0056b3; }
          table { width: 80%; border-collapse: collapse; margin-bottom: 30px; }
          th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
          th { background-color: #f2f2f2; }
          caption { font-weight: bold; font-size: 1.2em; padding: 10px; color: #333; }
        </style>
      </head>
      <body>
        <h1>Kết quả truy vấn thông tin sinh viên</h1>
        
        <xsl:apply-templates select="." mode="cau1"/>
        <xsl:apply-templates select="." mode="cau2"/>
        <xsl:apply-templates select="." mode="cau3"/>
        <xsl:apply-templates select="." mode="cau4"/>
        <xsl:apply-templates select="." mode="cau5"/>
        <xsl:apply-templates select="." mode="cau6"/>
        <xsl:apply-templates select="." mode="cau7"/>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="school" mode="cau1">
    <h2>Câu 1: Danh sách tất cả sinh viên</h2>
    <table>
      <caption>Liệt kê thông tin tất cả sinh viên gồm mã và họ tên</caption>
      <tr>
        <th>Mã SV</th>
        <th>Họ và Tên</th>
      </tr>
      <xsl:apply-templates select="student" mode="cau1-row"/>
    </table>
  </xsl:template>
  <xsl:template match="student" mode="cau1-row">
    <tr>
      <td><xsl:value-of select="id"/></td>
      <td><xsl:value-of select="name"/></td>
    </tr>
  </xsl:template>

  <xsl:template match="school" mode="cau2">
    <h2>Câu 2: Sắp xếp sinh viên theo điểm</h2>
    <table>
      <caption>Liệt kê danh sách sinh viên gồm tên, điểm. Sắp xếp danh sách theo điểm từ cao đến thấp.</caption>
      <tr>
        <th>Họ và Tên</th>
        <th>Điểm (Grade)</th>
      </tr>
      <xsl:apply-templates select="student" mode="cau2-row">
        <xsl:sort select="grade" data-type="number" order="descending"/>
      </xsl:apply-templates>
    </table>
  </xsl:template>
  <xsl:template match="student" mode="cau2-row">
    <tr>
      <td><xsl:value-of select="name"/></td>
      <td><xsl:value-of select="grade"/></td>
    </tr>
  </xsl:template>

  <xsl:template match="school" mode="cau3">
    <h2>Câu 3: Gom nhóm sinh viên theo tháng sinh</h2>
    <table>
      <caption>Hiển thị danh sách sinh viên sinh cùng tháng, danh sách gồm: Số thứ tự, Họ tên, ngày sinh.</caption>
      <tr>
        <th>STT</th>
        <th>Họ và Tên</th>
        <th>Ngày Sinh</th>
      </tr>
      <xsl:for-each select="student[count(. | key('student-by-month', substring(date, 6, 2))[1]) = 1]">
        <xsl:sort select="substring(date, 6, 2)" data-type="number"/>
        <xsl:for-each select="key('student-by-month', substring(date, 6, 2))">
          <tr>
            <td><xsl:number/></td>
            <td><xsl:value-of select="name"/></td>
            <td><xsl:value-of select="date"/></td>
          </tr>
        </xsl:for-each>
      </xsl:for-each>
    </table>
  </xsl:template>
  
  <xsl:template match="school" mode="cau4">
    <h2>Câu 4: Danh sách các khóa học</h2>
    <table>
      <caption>Hiển thị danh sách các khóa học có sinh viên học. Sắp xếp theo khóa học.</caption>
      <tr>
        <th>Tên khóa học</th>
      </tr>
      <xsl:for-each select="enrollment[count(. | key('enrolled-course-refs', courseRef)[1]) = 1]">
          <xsl:sort select="key('course-by-id', courseRef)/name"/>
          <tr><td><xsl:value-of select="key('course-by-id', courseRef)/name"/></td></tr>
      </xsl:for-each>
    </table>
  </xsl:template>
  
  <xsl:template match="school" mode="cau5">
    <xsl:variable name="course_id" select="course[name='Hóa học 201']/id"/>
    <h2>Câu 5: Sinh viên học "Hóa học 201"</h2>
    <table>
      <caption>Lấy danh sách sinh viên đăng ký khóa học "Hóa học 201"</caption>
      <tr>
        <th>Mã SV</th>
        <th>Họ và Tên</th>
      </tr>
      <xsl:apply-templates select="student[id = /school/enrollment[courseRef=$course_id]/studentRef]" mode="cau1-row"/>
    </table>
  </xsl:template>

  <xsl:template match="school" mode="cau6">
    <h2>Câu 6: Sinh viên sinh năm 1997</h2>
    <table>
      <caption>Lấy danh sách của sinh viên sinh năm 1997</caption>
      <tr>
        <th>Mã SV</th>
        <th>Họ và Tên</th>
        <th>Ngày Sinh</th>
      </tr>
      <xsl:apply-templates select="student[substring(date, 1, 4) = '1997']" mode="cau6-row"/>
    </table>
  </xsl:template>
  <xsl:template match="student" mode="cau6-row">
    <tr>
      <td><xsl:value-of select="id"/></td>
      <td><xsl:value-of select="name"/></td>
      <td><xsl:value-of select="date"/></td>
    </tr>
  </xsl:template>

  <xsl:template match="school" mode="cau7">
    <h2>Câu 7: Sinh viên có họ "Trần"</h2>
    <table>
      <caption>Thống kê danh sách sinh viên họ "Trần"</caption>
      <tr>
        <th>Mã SV</th>
        <th>Họ và Tên</th>
      </tr>
      <xsl:apply-templates select="student[starts-with(name, 'Trần')]" mode="cau1-row"/>
    </table>
  </xsl:template>
</xsl:stylesheet>