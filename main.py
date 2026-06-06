# =====================================================
#                      MAIN
# =====================================================
import state
from pybricks.parameters import Button, Color
from pybricks.tools import wait

from config   import (CacCaiDatBanDau, CacTinhNangBamNut,
                      DoThongSoDuongDenTrang_TuDong,
                      HC_ThongSo_DiChuyen, HC_ThongSo_PD)
from sensors  import Gyro_DatLai, BoHenGio
from movement import (DC_DiChuyen, DC_TienLui_Gyro_CM, DC_TienLui_ThoiGian_Ms,
                      DC_Xoay, DC_DuongCong, DC_DungDiChuyen,
                      DOI_BAMNUT_TRAI, DOI_BAMNUT_PHAI, DOI_ThoiGian_Ms)
from arms     import ResetCanhTay, Tay_Truoc, Tay_Sau

# =====================================================
#   Viết các lượt chạy (Turn) của bạn vào đây
#   Ví dụ:
#
# def TenLuotChay():
#     DC_TienLui_Gyro_CM(80, 30)
#     DC_Xoay(70, 90)
#     ...
# =====================================================
def Turn1():
    setup()
    DC_TienLui_Gyro_CM(-80, 10)
    DC_Xoay(80, -90, 2)
    DongCo_TayPhai.run_time(500, 600, Stop.HOLD, wait=False)
    DongCo_TayTrai.run_time(500, 600, Stop.HOLD, wait=False)
    DC_TienLui_Gyro_CM(100, 29.5, True)
    DC_TienLui_Gyro_CM(-40, 1)
    DongCo_TayPhai.dc(100)
    DongCo_TayTrai.dc(100)
    DongCo_TayTrai.run_time(-500, 600, Stop.HOLD)
    DongCo_TayPhai.run_time(-500, 600, Stop.HOLD)
    DC_TienLui_Gyro_CM(-80, 35, True)
    DC_Xoay(80, 90, 2)
    DongCo_TayTrai.run_angle(300, 35, Stop.HOLD, wait=False)
    DongCo_TayPhai.run_angle(300, 35, Stop.HOLD, wait=False)
    DC_DuongCong(100, 43, 90)
    DC_TienLui_Gyro_CM(100, 10, True)
    DongCo_TayTrai.run_angle(-300, 35, Stop.HOLD, wait=False)
    DongCo_TayPhai.run_angle(-300, 35, Stop.HOLD, wait=False)
    DC_TienLui_ThoiGian_Ms(100, 600, 2, 50)
    DC_TienLui_Gyro_CM(-40, 3)
    DC_Xoay(80, -90, 2)
    DC_TienLui_Gyro_CM(100, 40, 2, 100, True)

def setup():
    DC_TienLui_ThoiGian_Ms(-40, 500, 2)
    Gyro_DatLai(0)
    state.DongCo_TayPhai.reset_angle(0)
    state.DongCo_TayTrai.reset_angle(0)

def Full_Run():
    Turn1()
    DOI_BAMNUT_TRAI()
    pass

def Main():
    Gyro_DatLai()
    HC_ThongSo_DiChuyen(40, 1, 40, 6, 5)
    HC_ThongSo_PD([0.5, 400], 1)
    HC_ThongSo_PD([0.2, 100], 2)
    Full_Run()

# =====================================================
#               KHỞI ĐỘNG CHƯƠNG TRÌNH
# =====================================================
print(" ")
print("--------------------------------------------------------------------------")
print("-------------------------- Bắt đầu lần chạy mới --------------------------")
print("--------------------------------------------------------------------------")

CacCaiDatBanDau()

if Button.RIGHT in state.hub.buttons.pressed():      # Calibrate cảm biến
    state.hub.light.on(Color.BLUE)
    DoThongSoDuongDenTrang_TuDong()

elif Button.LEFT in state.hub.buttons.pressed():     # Chạy làm sạch bánh xe
    while True:
        DC_DiChuyen(100, 100)

else:
    # BLUETOOTH - Bỏ tất cả lệnh đợi bấm nút
    # PHẢI      - In giá trị cảm biến dò đường
    # TRÁI      - Bắt đầu chạy Main
    CacTinhNangBamNut()

    BoHenGio(I_Reset=True)
    Main()
    print("Thoi gian chay bai:", BoHenGio())

DOI_BAMNUT_PHAI()
