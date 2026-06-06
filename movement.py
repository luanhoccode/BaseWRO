# =====================================================
#               DI CHUYỂN & ĐIỀU KHIỂN PD
# =====================================================
import state
from pybricks.parameters import Stop
from pybricks.tools import wait
from sensors import (
    DocPhanXaAnhSang_DaHieuChinh_F,
    Gyro_TinhGocTrech,
    BoHenGio,
)

# =====================================================
#                      PD
# =====================================================

def setPD(I_PD, I_Reset: bool = False):
    state.kP = I_PD[0]
    state.kD = I_PD[1]
    if I_Reset:
        state.lastError = 0

def PD(I_input1, I_input2):
    state.PDscale = (abs(state.power) / 100) * 0.7 + 0.3
    error  = I_input1 - I_input2
    result = (error * state.kP) + ((error - state.lastError) * state.kD)
    result = result * state.PDscale
    state.lastError = error
    return result

def Tinh_TocDo_TheoQD(I_QuangDuong_HienTai, I_TongQuangDuong, I_TocDoMongMuon,
                       I_SuDungTangToc: bool = True, I_SuDungGiamToc: bool = True):
    '''
    Tính tốc độ hiện tại theo quãng đường (có tăng/giảm tốc)
    '''
    QuangDuongGiamToc1 = state.G_QuangDuong_GiamToc / 5 * 2
    QuangDuongGiamToc2 = state.G_QuangDuong_GiamToc - QuangDuongGiamToc1
    if (I_TongQuangDuong - state.G_QuangDuong_TangToc <= state.G_QuangDuong_GiamToc) and I_SuDungTangToc and I_SuDungGiamToc:
        speedChange   = abs(I_TocDoMongMuon) - state.G_TocDo_KetThuc
        TocDoMongMuon = speedChange * ((I_TongQuangDuong - QuangDuongGiamToc2) / QuangDuongGiamToc1) + state.G_TocDo_KetThuc
    else:
        TocDoMongMuon = I_TocDoMongMuon
    if (I_QuangDuong_HienTai <= state.G_QuangDuong_TangToc) and I_SuDungTangToc:
        speedChange = abs(TocDoMongMuon) - state.G_TocDo_BatDau
        speed = speedChange * (I_QuangDuong_HienTai / state.G_QuangDuong_TangToc) + state.G_TocDo_BatDau
    elif (I_TongQuangDuong - I_QuangDuong_HienTai <= state.G_QuangDuong_GiamToc) and I_SuDungGiamToc:
        speedChange = abs(TocDoMongMuon) - state.G_TocDo_KetThuc
        speed = speedChange * ((I_TongQuangDuong - I_QuangDuong_HienTai - QuangDuongGiamToc2) / QuangDuongGiamToc1) + state.G_TocDo_KetThuc
        if I_TongQuangDuong - I_QuangDuong_HienTai <= QuangDuongGiamToc2:
            speed = state.G_TocDo_KetThuc
    else:
        speed = abs(I_TocDoMongMuon)
    return speed

# =====================================================
#               CÁC HÀM DI CHUYỂN CƠ BẢN
# =====================================================

def DC_DiChuyen(I_TocDo_Trai=40, I_TocDo_Phai=40):
    '''
    Chạy 2 động cơ theo % công suất
    * I_TocDo_Trai / I_TocDo_Phai (-100 đến 100)
    '''
    state.DongCo_Trai.dc(I_TocDo_Trai)
    state.DongCo_Phai.dc(I_TocDo_Phai)

def DC_DiChuyen_PD(I_TocDo=40, I_MucDoRe=0):
    '''
    Chạy 2 động cơ có PD cân bằng encoder (không Gyro)
    * I_MucDoRe - rẽ trái/phải (-100 đến 100)
    '''
    setPD(state.G_TS_PD_KhongGyro_DiCong, False)
    if I_MucDoRe > 0:
        TocDo_Trai = I_TocDo
        TocDo_Phai = I_TocDo - I_TocDo * I_MucDoRe / 50
    elif I_MucDoRe < 0:
        TocDo_Trai = I_TocDo - I_TocDo * I_MucDoRe / 50
        TocDo_Phai = I_TocDo
    else:
        TocDo_Trai = I_TocDo
        TocDo_Phai = I_TocDo
    state.power = I_TocDo
    correction = PD(
        abs(state.DongCo_Trai.angle()) * abs(TocDo_Phai) / 70,
        abs(state.DongCo_Phai.angle()) * abs(TocDo_Trai) / 70
    ) * I_TocDo / abs(I_TocDo)
    DC_DiChuyen(TocDo_Trai - correction, TocDo_Phai + correction)

def DC_TienLui_Gyro(I_TocDo=40):
    '''Chạy liên tục có Gyro (dùng trong vòng lặp bên ngoài)'''
    setPD(state.G_TS_PD_Gyro)
    state.power = abs(I_TocDo)
    Gyro_TinhGocTrech()
    correction = round(PD(state.yaw, state.X_G_HuongMuonDen))
    DC_DiChuyen(I_TocDo - correction, I_TocDo + correction)

def DC_DungDiChuyen(I_Phanh=2, I_DoiDeOnDinh=0):
    '''
    Dừng robot
    * 0  - Thả trôi
    * 2  - Phanh cả 2 động cơ
    * -1 - Phanh động cơ trái
    * 1  - Phanh động cơ phải
    '''
    if I_Phanh == 0:
        state.DongCo_Phai.stop()
        state.DongCo_Trai.stop()
    elif I_Phanh == 2:
        state.DongCo_Trai.brake()
        state.DongCo_Phai.brake()
        wait(I_DoiDeOnDinh)
    elif I_Phanh == -1:
        state.DongCo_Trai.brake()
    else:
        state.DongCo_Phai.brake()

# =====================================================
#               DI CHUYỂN GYRO THEO CM
# =====================================================

def DC_TienLui_Gyro_CM(I_TocDo=100, I_TongQuangDuong=50, I_Phanh=2,
                        I_DoiDeOnDinh=0, I_SuDungTangToc: bool = True,
                        I_SuDungGiamToc: bool = True):
    '''
    Tiến/lùi theo quãng đường (cm) có Gyro
    * I_TocDo - Tốc độ (âm = lùi)
    * I_TongQuangDuong - Quãng đường (cm)
    * I_Phanh - Kiểu phanh (-1, 1, 2)
    '''
    state.DongCo_Trai.reset_angle(0)
    state.DongCo_Phai.reset_angle(0)
    QuangDuongHienTai    = 0
    QuangDuongTruocDo    = 0
    TocDo_BoSung         = 0
    setPD(state.G_TS_PD_Gyro, I_Reset=True)
    KT_ThoiGian = BoHenGio()
    QuangDuongBiDu = abs(I_TocDo) / 100 if abs(I_TocDo) >= 40 else 0
    while QuangDuongHienTai <= I_TongQuangDuong - QuangDuongBiDu:
        QuangDuongHienTai = (
            (abs(state.DongCo_Trai.angle()) + abs(state.DongCo_Phai.angle())) / 2
        ) / 360 * state.X_G_QuangDuong1VongQuay
        state.power = Tinh_TocDo_TheoQD(
            QuangDuongHienTai, I_TongQuangDuong - QuangDuongBiDu,
            abs(I_TocDo), I_SuDungTangToc, I_SuDungGiamToc
        )
        state.power = round((abs(I_TocDo) / I_TocDo) * state.power)
        Gyro_TinhGocTrech()
        correction = round(PD(state.yaw, state.X_G_HuongMuonDen))
        DC_DiChuyen(state.power - correction + TocDo_BoSung,
                    state.power + correction + TocDo_BoSung)
        if BoHenGio() - KT_ThoiGian > 0.5:
            if QuangDuongHienTai - QuangDuongTruocDo < 0.15:
                TocDo_BoSung += 5 * I_TocDo / abs(I_TocDo)
                print(TocDo_BoSung)
                if abs(TocDo_BoSung) > 80:
                    print("Break")
                    break
            QuangDuongTruocDo = QuangDuongHienTai
            KT_ThoiGian = BoHenGio()
    DC_DungDiChuyen(I_Phanh, I_DoiDeOnDinh)

# =====================================================
#          TIẾN/LÙI GYRO DỪNG THEO PHẢN XẠ
# =====================================================

def DC_TienLui_Gyro_GapPXTrang(I_Tocdo=100, I_Phanh=2):
    '''Đi đến khi gặp phản xạ trắng'''
    state.power = I_Tocdo
    setPD(state.G_TS_PD_Gyro, I_Reset=True)
    while DocPhanXaAnhSang_DaHieuChinh_F() < state.X_G_GiaTriPhanXa_DungDuongTrang:
        Gyro_TinhGocTrech()
        correction = round(PD(state.yaw, state.X_G_HuongMuonDen))
        DC_DiChuyen(state.power - correction, state.power + correction)
    DC_DungDiChuyen(I_Phanh)

def DC_TienLui_Gyro_GapPXDen(I_Tocdo=100, I_Phanh=2):
    '''Đi đến khi gặp phản xạ đen'''
    state.power = I_Tocdo
    setPD(state.G_TS_PD_Gyro, I_Reset=True)
    while DocPhanXaAnhSang_DaHieuChinh_F() > state.X_G_GiaTriPhanXa_DungDuongDen:
        Gyro_TinhGocTrech()
        correction = round(PD(state.yaw, state.X_G_HuongMuonDen))
        DC_DiChuyen(state.power - correction, state.power + correction)
    DC_DungDiChuyen(I_Phanh)

def DC_TienLui_Gyro_GapPXLam(I_Tocdo=100, I_Phanh=2):
    '''Đi đến khi gặp phản xạ xanh lam'''
    state.power = I_Tocdo
    setPD(state.G_TS_PD_Gyro, I_Reset=True)
    while DocPhanXaAnhSang_DaHieuChinh_F() > state.X_G_GiaTriPhanXa_DungDuongXanh:
        Gyro_TinhGocTrech()
        correction = round(PD(state.yaw, state.X_G_HuongMuonDen))
        DC_DiChuyen(state.power - correction, state.power + correction)
    DC_DungDiChuyen(I_Phanh)

# =====================================================
#                      XOAY
# =====================================================

def DC_Xoay(I_TocDo=100, I_GocXoayThem=90, I_CheDoXoay=2, I_Phanh=2, I_DoiDeOnDinh=0):
    '''
    Xoay robot bằng Gyro
    * I_TocDo - Tốc độ xoay
    * I_GocXoayThem - Số độ muốn xoay thêm
    * I_CheDoXoay: -1=động cơ trái, 1=động cơ phải, 2=cả 2
    '''
    HuongBanDau = state.X_G_HuongMuonDen
    state.X_G_HuongMuonDen += I_GocXoayThem * abs(I_TocDo) / I_TocDo
    if I_CheDoXoay <= 1:
        setPD(state.G_TS_PD_Gyro_Xoay1DC_Tien, True)
    else:
        setPD(state.G_TS_PD_Gyro_Xoay2DC, True)
    count = 0
    Check = False
    while count <= 5:
        Gyro_TinhGocTrech()
        state.power = 100
        correction  = round(PD(state.yaw, state.X_G_HuongMuonDen))
        if abs(HuongBanDau - state.X_G_HuongMuonDen) <= 20:
            if abs(HuongBanDau - state.X_G_HuongMuonDen) <= 10:
                TocDo_TangToc = -40 * abs(HuongBanDau - state.yaw) / (HuongBanDau - state.yaw)
            else:
                TocDo_TangToc = 40 + 60 / 10 * abs(HuongBanDau - state.yaw)
                if abs(correction) > abs(TocDo_TangToc):
                    correction = abs(TocDo_TangToc) * correction / abs(correction)
        if abs(correction) > abs(I_TocDo):
            correction = abs(I_TocDo) * correction / abs(correction)
        if I_CheDoXoay == -1:
            DC_DiChuyen(-correction, 0)
        elif I_CheDoXoay == 1:
            DC_DiChuyen(0, correction)
        else:
            DC_DiChuyen(-correction, correction)
        if abs(state.yaw - state.X_G_HuongMuonDen) <= 8:
            if not Check:
                ThoiGianBanDau = BoHenGio()
                Check = True
            else:
                if BoHenGio() - ThoiGianBanDau >= 0.3:
                    print("Xoay thieu")
                    while not abs(state.yaw - state.X_G_HuongMuonDen) < 1.2:
                        Gyro_TinhGocTrech()
                        correction = 30 * abs(state.yaw - state.X_G_HuongMuonDen) / (state.yaw - state.X_G_HuongMuonDen)
                        if I_CheDoXoay == -1:
                            state.DongCo_Trai.run(-11 * correction)
                        elif I_CheDoXoay == 1:
                            state.DongCo_Phai.run(11 * correction)
                        else:
                            state.DongCo_Trai.run(-11 * correction)
                            state.DongCo_Phai.run(11 * correction)
                    DC_DungDiChuyen(I_Phanh, 0)
                    break
        if abs(state.yaw - state.X_G_HuongMuonDen) <= 1:
            count += 1
        else:
            count = 0
    DC_DungDiChuyen(I_Phanh, I_DoiDeOnDinh)

# =====================================================
#                   ĐƯỜNG CONG
# =====================================================

def DC_DuongCong(I_TocDo=100, I_TongQuangDuong=50, I_GocXoayThem=90,
                 I_Phanh=2, I_DoiDeOnDinh=0,
                 I_SuDungTangToc: bool = True, I_SuDungGiamToc: bool = True,
                 I_CheDoTheoBanKinhCung: bool = False):
    '''
    Đi vòng cung đến một hướng nhất định
    * I_TongQuangDuong - độ dài cung (cm) hoặc bán kính (nếu I_CheDoTheoBanKinhCung=True)
    * I_GocXoayThem - số độ xoay khi đi hết cung
    '''
    HuongBanDau = state.X_G_HuongMuonDen
    state.DongCo_Trai.reset_angle(0)
    state.DongCo_Phai.reset_angle(0)
    QuangDuongHienTai = 0
    setPD(state.G_TS_PD_Gyro_DuongCong, I_Reset=True)
    TongQuangDuong = (
        I_TongQuangDuong * 3.14 * 2 / 360 * abs(I_GocXoayThem)
        if I_CheDoTheoBanKinhCung else I_TongQuangDuong
    )
    QuangDuongTruocDo = 0
    TocDo_BoSung = 0
    KT_ThoiGian = BoHenGio()
    while QuangDuongHienTai <= TongQuangDuong:
        QuangDuongHienTai = (
            (abs(state.DongCo_Trai.angle()) + abs(state.DongCo_Phai.angle())) / 2
        ) / 360 * state.X_G_QuangDuong1VongQuay
        state.power = Tinh_TocDo_TheoQD(
            QuangDuongHienTai, TongQuangDuong,
            abs(I_TocDo), I_SuDungTangToc, I_SuDungGiamToc
        )
        state.power = round((abs(I_TocDo) / I_TocDo) * state.power)
        state.X_G_HuongMuonDen = (QuangDuongHienTai / TongQuangDuong) * I_GocXoayThem + HuongBanDau
        Gyro_TinhGocTrech()
        correction = round(PD(state.yaw, state.X_G_HuongMuonDen))
        DC_DiChuyen(state.power - correction + TocDo_BoSung,
                    state.power + correction + TocDo_BoSung)
        if BoHenGio() - KT_ThoiGian > 0.5:
            if QuangDuongHienTai - QuangDuongTruocDo < 0.15:
                TocDo_BoSung += 3 * I_TocDo / abs(I_TocDo)
                if abs(TocDo_BoSung) > 80:
                    break
            else:
                QuangDuongTruocDo = QuangDuongHienTai
                KT_ThoiGian = BoHenGio()
    DC_DungDiChuyen(I_Phanh, I_DoiDeOnDinh)
    state.X_G_HuongMuonDen = HuongBanDau + I_GocXoayThem

# =====================================================
#                    ĐI LINE
# =====================================================

def DC_DoDuong_Cm(I_BamDuongBenPhai=1, I_TocDo=100, I_TongQuangDuong=50,
                  I_Phanh=2, I_DoiDeOnDinh=0,
                  I_SuDungTangToc: bool = True, I_SuDungGiamToc: bool = True,
                  I_Limit=False):
    '''
    Dò line dừng theo quãng đường (cm)
    * I_BamDuongBenPhai: 1=bên phải đường đen, -1=bên trái
    '''
    state.DongCo_Trai.reset_angle(0)
    state.DongCo_Phai.reset_angle(0)
    QuangDuongHienTai = 0
    setPD(state.G_TS_PD_LineQD, I_Reset=True)
    while QuangDuongHienTai <= I_TongQuangDuong:
        QuangDuongHienTai = (
            (abs(state.DongCo_Trai.angle()) + abs(state.DongCo_Phai.angle())) / 2
        ) / 360 * state.X_G_QuangDuong1VongQuay
        QD_Line = max(0, QuangDuongHienTai - state.G_QuangDuong_DiChamKhiDiLine)
        state.power = Tinh_TocDo_TheoQD(
            QD_Line, I_TongQuangDuong - state.G_QuangDuong_DiChamKhiDiLine,
            I_TocDo, I_SuDungTangToc, I_SuDungGiamToc
        )
        ValueLightSensor = DocPhanXaAnhSang_DaHieuChinh_F()
        correction = PD(ValueLightSensor, state.X_G_GiaTriPhanXa_MuonBamTheo)
        if I_Limit and abs(correction) >= state.X_G_GioiHanSaiSoDiLine:
            correction = state.X_G_GioiHanSaiSoDiLine * (correction / abs(correction))
        correction *= I_BamDuongBenPhai
        DC_DiChuyen(state.power - correction, state.power + correction)
        wait(1)
    DC_DungDiChuyen(I_Phanh, I_DoiDeOnDinh)

def DC_DoDuong_PxDen(I_BamDuongBenPhai=1, I_TocDo=100, I_Phanh=2, I_DoiDeOnDinh=0):
    '''Dò line dừng khi gặp đường đen'''
    setPD(state.G_TS_PD_LinePX, I_Reset=True)
    state.power = I_TocDo
    while DocPhanXaAnhSang_DaHieuChinh_F() > state.X_G_GiaTriPhanXa_DungDuongDen:
        correction = PD(DocPhanXaAnhSang_DaHieuChinh_F(), state.X_G_GiaTriPhanXa_MuonBamTheo) * I_BamDuongBenPhai
        DC_DiChuyen(state.power - correction, state.power + correction)
        wait(1)
    DC_DungDiChuyen(I_Phanh, I_DoiDeOnDinh)

def DC_DoDuong_PxTrang(I_BamDuongBenPhai=1, I_TocDo=100, I_Phanh=2, I_DoiDeOnDinh=0):
    '''Dò line dừng khi gặp đường trắng'''
    setPD(state.G_TS_PD_LinePX, I_Reset=True)
    state.power = I_TocDo
    while DocPhanXaAnhSang_DaHieuChinh_F() < state.X_G_GiaTriPhanXa_DungDuongTrang:
        correction = PD(DocPhanXaAnhSang_DaHieuChinh_F(), state.X_G_GiaTriPhanXa_MuonBamTheo) * I_BamDuongBenPhai
        DC_DiChuyen(state.power - correction, state.power + correction)
        wait(1)
    DC_DungDiChuyen(I_Phanh, I_DoiDeOnDinh)

def DC_DoDuong_PxLam(I_BamDuongBenPhai=1, I_TocDo=100, I_Phanh=2, I_DoiDeOnDinh=0):
    '''Dò line dừng khi gặp đường xanh lam'''
    setPD(state.G_TS_PD_LinePX, I_Reset=True)
    state.power = I_TocDo
    while DocPhanXaAnhSang_DaHieuChinh_F() > state.X_G_GiaTriPhanXa_DungDuongXanh:
        correction = PD(DocPhanXaAnhSang_DaHieuChinh_F(), state.X_G_GiaTriPhanXa_MuonBamTheo) * I_BamDuongBenPhai
        DC_DiChuyen(state.power - correction, state.power + correction)
        wait(1)
    DC_DungDiChuyen(I_Phanh, I_DoiDeOnDinh)

# =====================================================
#                  DI CHUYỂN THEO THỜI GIAN
# =====================================================

def DC_TienLui_ThoiGian_Ms(I_TocDo=-40, I_ThoiGian=1000, I_Phanh=2, I_DoiDeOnDinh=0):
    '''Chạy trong khoảng thời gian nhất định (ms)'''
    state.power = I_TocDo
    state.DongCo_Trai.reset_angle(0)
    state.DongCo_Phai.reset_angle(0)
    setPD(state.G_TS_PD_KhongGyro_DiThang, True)
    ThoiGianBanDau = BoHenGio()
    while BoHenGio() - ThoiGianBanDau < I_ThoiGian / 1000:
        correction = PD(abs(state.DongCo_Trai.angle()), abs(state.DongCo_Phai.angle())) * I_TocDo / abs(I_TocDo)
        DC_DiChuyen(state.power - correction, state.power + correction)
    DC_DungDiChuyen(I_Phanh, I_DoiDeOnDinh)

# =====================================================
#                  ĐỢI BẤM NÚT / THỜI GIAN
# =====================================================

def DOI_BAMNUT_PHAI():
    if not state.X_G_CheDoThi:
        while True:
            if state.hub.buttons.pressed().__contains__(state.hub.buttons.pressed()):
                from pybricks.parameters import Button
                if Button.RIGHT in state.hub.buttons.pressed():
                    break
            wait(80)
        from pybricks.parameters import Button
        while Button.RIGHT in state.hub.buttons.pressed():
            wait(80)
        wait(300)

def DOI_BAMNUT_TRAI():
    if not state.X_G_CheDoThi:
        from pybricks.parameters import Button
        while True:
            if Button.LEFT in state.hub.buttons.pressed():
                break
            wait(80)
        while Button.LEFT in state.hub.buttons.pressed():
            wait(80)
        wait(300)

def DOI_ThoiGian_Ms(I_ThoiGianDoi=1000):
    wait(I_ThoiGianDoi)
