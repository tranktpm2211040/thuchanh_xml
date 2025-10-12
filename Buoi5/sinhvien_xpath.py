from lxml import etree

# Đọc và phân tích cú pháp tệp XML
tree = etree.parse('sinhvien.xml')

# 1. Lấy tất cả các thẻ sinhvien
students = tree.xpath("/school/student")
print(f"1. Tổng số sinh viên: {len(students)}")

# 2. Liệt kê tên tất cả sinh viên
names = tree.xpath("/school/student/name/text()")
print("2. Tên tất cả sinh viên:", names)

# 3. Lấy tất cả id của sinh viên
ids = tree.xpath("/school/student/id/text()")
print("3. ID của sinh viên:", ids)

# 4. Lấy ngày sinh của sinh viên có id = 'SV01'
dob_sv01 = tree.xpath("/school/student[id='SV01']/date/text()")
print("4. Ngày sinh SV01:", dob_sv01)

# 5. Lấy các khóa học
courses = tree.xpath("/school/enrollment/course/text()")
print("5. Các khóa học:", courses)

# 6. Lấy toàn bộ thông tin của sinh viên đầu tiên
first_student = tree.xpath("/school/student[1]")
print("6. Sinh viên đầu tiên:\n", etree.tostring(first_student[0], pretty_print=True).decode())

# 7. Lấy mã sinh viên đăng ký khóa học "Vatly203"
sv_vatly203 = tree.xpath("/school/enrollment[course='Vatly203']/studentRef/text()")
print("7. Mã sinh viên học Vatly203:", sv_vatly203)

# 8. Lấy tên sinh viên học môn "Toan101"
sv_toan101 = tree.xpath("/school/student[id=/school/enrollment[course='Toan101']/studentRef]/name/text()")
print("8. Tên sinh viên học Toan101:", sv_toan101)

# 9. Lấy tên sinh viên học môn "Vatly203"
sv_vatly203_name = tree.xpath("/school/student[id=/school/enrollment[course='Vatly203']/studentRef]/name/text()")
print("9. Tên sinh viên học Vatly203:", sv_vatly203_name)

# 10. Lấy ngày sinh của sinh viên có id='SV01'
dob_sv01_repeat = tree.xpath("/school/student[id='SV01']/date/text()")
print("10. Ngày sinh SV01:", dob_sv01_repeat)

# 11. Lấy tên và ngày sinh của sinh viên sinh năm 1997
names_1997 = tree.xpath("/school/student[starts-with(date,'1997')]/name/text()")
dates_1997 = tree.xpath("/school/student[starts-with(date,'1997')]/date/text()")
sv_1997 = list(zip(names_1997, dates_1997))
print("11. Sinh viên sinh năm 1997 (tên, ngày sinh):", sv_1997)

# 12. Lấy tên sinh viên có ngày sinh trước năm 1998
sv_before_1998 = tree.xpath("/school/student[number(substring(date,1,4)) < 1998]/name/text()")
print("12. Sinh viên sinh trước 1998:", sv_before_1998)

# 13. Đếm tổng số sinh viên
count_sv = tree.xpath("count(/school/student)")
print("13. Tổng số sinh viên:", int(count_sv))

# 14. Lấy tất cả sinh viên chưa đăng ký môn nào
unregistered = tree.xpath("/school/student[not(id = /school/enrollment/studentRef)]/name/text()")
print("14. Sinh viên chưa đăng ký môn:", unregistered)

# 15. Lấy phần tử <date> anh em ngay sau <name> của SV01
next_date_sv01 = tree.xpath("/school/student[id='SV01']/name/following-sibling::date[1]/text()")
print("15. <date> ngay sau <name> của SV01:", next_date_sv01)

# 16. Lấy phần tử <id> anh em ngay trước <name> của SV02
prev_id_sv02 = tree.xpath("/school/student[id='SV02']/name/preceding-sibling::id[1]/text()")
print("16. <id> ngay trước <name> của SV02:", prev_id_sv02)

# 17. Lấy toàn bộ node <course> trong cùng một <enrollment> với studentRef='SV03'
course_sv03 = tree.xpath("/school/enrollment[studentRef='SV03']/course/text()")
print("17. Khóa học của SV03:", course_sv03)

# 18. Lấy sinh viên có họ là “Trần”
sv_tran = tree.xpath("/school/student[starts-with(name,'Trần')]/name/text()")
print("18. Sinh viên họ Trần:", sv_tran)

# 19. Lấy năm sinh của sinh viên SV01
year_sv01 = tree.xpath("substring(/school/student[id='SV01']/date,1,4)")
print("19. Năm sinh SV01:", year_sv01)