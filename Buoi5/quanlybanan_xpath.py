from lxml import etree

tree = etree.parse('quanlybanan.xml')

# 1. Lấy tất cả bàn
bans = tree.xpath("/QUANLY/BANS/BAN")
print("1. Tổng số bàn:", len(bans))

# 2. Lấy tất cả nhân viên
nhanviens = tree.xpath("/QUANLY/NHANVIENS/NHANVIEN")
print("2. Tổng số nhân viên:", len(nhanviens))

# 3. Lấy tên nhân viên có mã NV02
ten_nv02 = tree.xpath("/QUANLY/NHANVIENS/NHANVIEN[MANV='NV02']/TENV/text()")
print("3. Tên NV02:", ten_nv02)

# 4. Lấy tên và số điện thoại của nhân viên NV03
ten_nv03 = tree.xpath("/QUANLY/NHANVIENS/NHANVIEN[MANV='NV03']/TENV/text()")
sdt_nv03 = tree.xpath("/QUANLY/NHANVIENS/NHANVIEN[MANV='NV03']/SDT/text()")
print("4. NV03:", list(zip(ten_nv03, sdt_nv03)))

# 5. Lấy tên món có giá > 50,000
mon_gia_cao = tree.xpath("/QUANLY/MONS/MON[GIA>50000]/TENMON/text()")
print("5. Món giá > 50,000:", mon_gia_cao)

# 6. Lấy số bàn của hóa đơn HD03
soban_hd03 = tree.xpath("/QUANLY/HOADONS/HOADON[SOHD='HD03']/SOBAN/text()")
print("6. Số bàn của HD03:", soban_hd03)

# 7. Lấy tên món có mã M02
tenmon_m02 = tree.xpath("/QUANLY/MONS/MON[MAMON='M02']/TENMON/text()")
print("7. Tên món M02:", tenmon_m02)

# 8. Lấy ngày lập của hóa đơn HD03
ngaylap_hd03 = tree.xpath("/QUANLY/HOADONS/HOADON[SOHD='HD03']/NGAYLAP/text()")
print("8. Ngày lập HD03:", ngaylap_hd03)

# 9. Lấy tất cả mã món trong hóa đơn HD01
mamons_hd01 = tree.xpath("/QUANLY/HOADONS/HOADON[SOHD='HD01']/CTHDS/CTHD/MAMON/text()")
print("9. Mã món trong HD01:", mamons_hd01)

# 10. Lấy tên món trong hóa đơn HD01
tenmons_hd01 = tree.xpath("/QUANLY/MONS/MON[MAMON = /QUANLY/HOADONS/HOADON[SOHD='HD01']/CTHDS/CTHD/MAMON]/TENMON/text()")
print("10. Tên món trong HD01:", tenmons_hd01)

# 11. Lấy tên nhân viên lập hóa đơn HD02
ten_nv_hd02 = tree.xpath("/QUANLY/NHANVIENS/NHANVIEN[MANV = /QUANLY/HOADONS/HOADON[SOHD='HD02']/MANV]/TENV/text()")
print("11. Nhân viên lập HD02:", ten_nv_hd02)

# 12. Đếm số bàn
count_ban = int(tree.xpath("count(/QUANLY/BANS/BAN)"))
print("12. Số bàn:", count_ban)

# 13. Đếm số hóa đơn lập bởi NV01
count_hd_nv01 = int(tree.xpath("count(/QUANLY/HOADONS/HOADON[MANV='NV01'])"))
print("13. Số hóa đơn do NV01 lập:", count_hd_nv01)

# 14. Lấy tất cả nhân viên từng lập hóa đơn cho bàn số 3
nv_ban3 = tree.xpath("/QUANLY/NHANVIENS/NHANVIEN[MANV = /QUANLY/HOADONS/HOADON[SOBAN=3]/MANV]/TENV/text()")
print("14. Nhân viên phục vụ bàn 3:", nv_ban3)

# 15. Lấy tất cả hóa đơn mà nhân viên nữ lập
hoadon_nv_nu = tree.xpath("/QUANLY/HOADONS/HOADON[MANV = /QUANLY/NHANVIENS/NHANVIEN[GIOITINH='Nữ']/MANV]")
print("15. Hóa đơn do nhân viên nữ lập:", [etree.tostring(hd, pretty_print=True).decode() for hd in hoadon_nv_nu])

# 16. Lấy tất cả nhân viên từng phục vụ bàn số 1
nv_ban1 = tree.xpath("/QUANLY/NHANVIENS/NHANVIEN[MANV = /QUANLY/HOADONS/HOADON[SOBAN=1]/MANV]/TENV/text()")
print("16. Nhân viên phục vụ bàn 1:", nv_ban1)

# 17. Lấy tất cả món được gọi nhiều hơn 1 lần trong các hóa đơn
mon_gtr1 = tree.xpath("/QUANLY/MONS/MON[MAMON = /QUANLY/HOADONS/HOADON/CTHDS/CTHD[SOLUONG>1]/MAMON]/TENMON/text()")
print("17. Món được gọi >1 lần:", mon_gtr1)

# 18. Lấy tên bàn + ngày lập hóa đơn tương ứng SOHD='HD02'
ban_ngay_hd02 = tree.xpath("concat(/QUANLY/BANS/BAN[SOBAN = /QUANLY/HOADONS/HOADON[SOHD='HD02']/SOBAN]/TENBAN, ' - ', /QUANLY/HOADONS/HOADON[SOHD='HD02']/NGAYLAP)")
print("18. Tên bàn + ngày lập HD02:", ban_ngay_hd02)