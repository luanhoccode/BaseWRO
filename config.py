# =====================================================
#              CÀI ĐẶT & HIỆU CHỈNH
# =====================================================
import state
from pybricks.parameters import Button, Color, Stop, Icon
from pybricks.tools import wait
from sensors import DocPhanXaAnhSang_DaHieuChinh_F, Gyro_DatLai, BoHenGio
from movement import DC_DiChuyen, DC_DungDiChuyen

def CaiDat1_HangSoDiChuyen(I_DuongKinhBanhXe=6.24, I_QuangDuong1VongQuay=19.6):
    state.X_G_DuongKinhBanhXe    = I_DuongKinhBanhXe
    state.X_G_QuangDuong1VongQuay = I_QuangDuong1VongQuay

def CaiDat2_SaiSoDoPin():
    BatteryVoltage    = state.hub.battery.voltage()
    BatteryPercentage = round((BatteryVoltage - 7000) / 1.2) / 10
    state.X_G_BatteryScale = BatteryPercentage / 100
    if state.X_G_BatteryScale < 0:
        state.X_G_BatteryScale = 0
    print("Pin :", BatteryPercentage, "%  | ", BatteryVoltage, "V")
    state.X_G_PhanTramPin = BatteryPercentage
    state.X_G_SaiSoDoPin_TocDo     = -round(7 * state.X_G_BatteryScale)
    state.X_G_SaiSoDoPin_QuangDuong = round(15 * state.X_G_BatteryScale) / 360 * state.X_G_QuangDuong1VongQuay

def CaiDat3_HangSoPhanXaDoDuong():
    state.X_G_GiaTriPhanXa_NhoNhat = int.from_bytes(state.hub.system.storage(0, read=1), "big")
    state.X_G_GiaTriPhanXa_LonNhat = int.from_bytes(state.hub.system.storage(1, read=1), "big")
    print("GT cam bien do duong: Thap =", state.X_G_GiaTriPhanXa_NhoNhat, "| Cao =", state.X_G_GiaTriPhanXa_LonNhat)
    state.X_G_GioiHanSaiSoDiLine = 10

def CaiDat4_DatCacThongSoPD():
    state.G_TS_PD_LineQD_0            = [0.5, 400]
    state.G_TS_PD_LinePX_0            = [0.2, 100]
    state.G_TS_PD_Gyro_0              = [5, 25]
    state.G_TS_PD_Gyro_DuongCong_0    = [8, 100]
    state.G_TS_PD_Gyro_Xoay2DC_0      = [12 - round(3 * state.X_G_BatteryScale), 265 + round(40 * state.X_G_BatteryScale)]
    state.G_TS_PD_Gyro_Xoay1DC_Tien_0 = [17, 870]
    state.G_TS_PD_Gyro_Xoay1DC_Lui_0  = [17, 870]
    state.G_TS_PD_KhongGyro_DiThang_0 = [1, 20]
    state.G_TS_PD_KhongGyro_DiCong_0  = [0.3, 100]

def HC_ThongSoPhanXa(I_GiaTriPxMuonBamTheo=55, I_GiaTriDungDuongDen=15, I_GiaTriDungDuongTrang=85, I_GiaTriDungDuongXanh=30):
    state.X_G_GiaTriPhanXa_MuonBamTheo    = I_GiaTriPxMuonBamTheo
    state.X_G_GiaTriPhanXa_DungDuongDen   = I_GiaTriDungDuongDen
    state.X_G_GiaTriPhanXa_DungDuongTrang = I_GiaTriDungDuongTrang
    state.X_G_GiaTriPhanXa_DungDuongXanh  = I_GiaTriDungDuongXanh

def HC_ThongSo_PD(I_PD, I_CheDo=1, I_Reset: bool = False):
    '''
    Hiệu chỉnh thông số PD
    * I_CheDo: 0=Reset tất cả, 1=LineQD, 2=LinePX, 3=Gyro thẳng,
               4=Gyro cong, 5=Xoay2DC, 6=Xoay1DC tiến, 7=Xoay1DC lùi,
               8=KGyro thẳng, 9=KGyro cong
    * I_Reset = True - đặt lại về mặc định
    '''
    mapping = {
        1: 'G_TS_PD_LineQD',
        2: 'G_TS_PD_LinePX',
        3: 'G_TS_PD_Gyro',
        4: 'G_TS_PD_Gyro_DuongCong',
        5: 'G_TS_PD_Gyro_Xoay2DC',
        6: 'G_TS_PD_Gyro_Xoay1DC_Tien',
        7: 'G_TS_PD_Gyro_Xoay1DC_Lui',
        8: 'G_TS_PD_KhongGyro_DiThang',
        9: 'G_TS_PD_KhongGyro_DiCong',
    }
    if I_Reset:
        keys = mapping.values() if I_CheDo == 0 else [mapping[I_CheDo]]
        for k in keys:
            setattr(state, k, getattr(state, k + '_0'))
    else:
        if I_CheDo in mapping:
            setattr(state, mapping[I_CheDo], I_PD)

def HC_ThongSo_DiChuyen(I_TocDoBatDau=None, I_QuangDuongTangToc=None, I_TocDoKetThuc=None, I_QuangDuongGiamToc=None, I_QuangDuongDiLineCham=None):
    '''
    Hiệu chỉnh các tham số di chuyển (tốc độ bắt đầu, tăng tốc, kết thúc, giảm tốc, đi line chậm)
    '''
    if I_TocDoBatDau is not None:
        state.G_TocDo_BatDau = I_TocDoBatDau + state.X_G_SaiSoDoPin_TocDo
    if I_QuangDuongTangToc is not None:
        state.G_QuangDuong_TangToc = I_QuangDuongTangToc + state.X_G_SaiSoDoPin_QuangDuong
    if I_TocDoKetThuc is not None:
        state.G_TocDo_KetThuc = I_TocDoKetThuc + state.X_G_SaiSoDoPin_TocDo
    if I_QuangDuongGiamToc is not None:
        state.G_QuangDuong_GiamToc = I_QuangDuongGiamToc + state.X_G_SaiSoDoPin_QuangDuong
    if I_QuangDuongDiLineCham is not None:
        state.G_QuangDuong_DiChamKhiDiLine = I_QuangDuongDiLineCham

def CacCaiDatBanDau():
    state.lastError = 0
    CaiDat1_HangSoDiChuyen(I_DuongKinhBanhXe=6.24, I_QuangDuong1VongQuay=19.6)
    CaiDat2_SaiSoDoPin()
    CaiDat3_HangSoPhanXaDoDuong()
    CaiDat4_DatCacThongSoPD()
    HC_ThongSo_DiChuyen(35, 1, 35, 7, 5)
    HC_ThongSoPhanXa(55, 15, 85, 30)
    HC_ThongSo_PD(0, I_CheDo=0, I_Reset=True)
    state.hub.light.on(Color.RED)
    state.X_G_CheDoThi = False

def DoThongSoDuongDenTrang_TuDong(I_TocDo=40):
    state.hub.speaker.beep(880, 250)
    while Button.RIGHT in state.hub.buttons.pressed():
        pass
    state.hub.speaker.beep(1760, 250)
    wait(500)
    CalibrateHigh = 0
    CalibrateLow  = 100
    calibrateStart = state.time.time()
    DC_DiChuyen(I_TocDo, I_TocDo)
    while state.time.time() - calibrateStart < 1500:
        CalibrateNow = state.CamBien_DoDuong_F.reflection()
        CalibrateLow  = min(CalibrateLow,  CalibrateNow)
        CalibrateHigh = max(CalibrateHigh, CalibrateNow)
    DC_DungDiChuyen()
    print("GT cam bien do duong: Thap =", CalibrateLow, " | Cao =", CalibrateHigh)
    state.hub.system.storage(0, write=bytes([CalibrateLow, CalibrateHigh]))

def CacTinhNangBamNut():
    '''
    * BLUETOOTH - Bỏ toàn bộ các lệnh đợi bấm nút
    * PHẢI      - In giá trị cảm biến dò đường
    * TRÁI      - Bắt đầu chạy MAIN
    '''
    while True:
        Button_Pressed = state.hub.buttons.pressed()
        if Button.LEFT in Button_Pressed:
            state.hub.display.icon(Icon.HAPPY)
            state.hub.speaker.beep(100, 500)
            Gyro_DatLai()
            BoHenGio(I_Reset=True)
            break
        if Button.BLUETOOTH in Button_Pressed:
            state.hub.light.on(Color.GREEN)
            state.hub.display.icon(Icon.FULL)
            state.X_G_CheDoThi = True
            state.hub.speaker.beep(1000, 800)
        if Button.RIGHT in Button_Pressed:
            state.hub.light.blink(Color.YELLOW, [200, 100])
            state.hub.speaker.beep(500, 500)
            print("Chua hieu chinh:", state.CamBien_DoDuong_F.reflection(),
                  " | Da hieu chinh:", DocPhanXaAnhSang_DaHieuChinh_F())
            wait(500)
            state.hub.light.on(Color.RED)
