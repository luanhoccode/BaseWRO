# =====================================================
#                    CẢM BIẾN
# =====================================================
import state

def DocMau(I_CheDoDocDu6Mau=False):
    '''
    * 3  - Màu xanh dương
    * 6  - Màu xanh lá
    * 7  - Màu vàng
    * 9  - Màu đỏ
    * 10 - Màu trắng
    * -1 - Không có màu
    '''
    HSVresult = state.CamBien_DocMau_E.hsv()
    h = HSVresult[0]
    s = HSVresult[1]
    v = HSVresult[2]
    if v > 5:
        if s <= 41:
            if v > 20 and s < 25:
                Mau = 10
            elif s >= 25 or v <= 20:
                Mau = 0
            else:
                Mau = -1
        else:
            if not (19 <= h <= 340):
                Mau = 9
            elif 20 <= h <= 70:
                Mau = 7
            elif 80 <= h <= 182:
                Mau = 6
            elif 185 <= h <= 340:
                Mau = 3
            else:
                Mau = -1
    else:
        if s <= 30:
            Mau = 0
        else:
            Mau = -1
    return Mau

def Gyro_DocGiaTri():
    return state.hub.imu.heading()

def Gyro_TinhGocTrech():
    state.yaw = state.hub.imu.heading()
    state.yaw = state.yaw - round((state.yaw - state.X_G_HuongMuonDen) / 361) * 360
    return state.yaw

def Gyro_DatLai(I_HuongDatLai: int = 0):
    state.hub.imu.reset_heading(I_HuongDatLai)
    state.X_G_HuongMuonDen = 0

def DocPhanXaAnhSang_DaHieuChinh_F():
    return (
        (state.CamBien_DoDuong_F.reflection() - state.X_G_GiaTriPhanXa_NhoNhat)
        / (state.X_G_GiaTriPhanXa_LonNhat - state.X_G_GiaTriPhanXa_NhoNhat)
        * 100
    )

def BoHenGio(I_Reset: bool = False):
    '''
    Lấy thời gian của bộ đếm giờ (giây)
    * I_Reset = True - đặt bộ đếm về 0
    '''
    if I_Reset:
        state.time.reset()
    else:
        return state.time.time() / 1000

def DongCo_DocDuLieuCamBien(I_CheDo=0):
    '''
    * 0 - Reset bộ đếm vòng quay về 0
    * 1 - Đọc quãng đường đã đi (độ)
    * 2 - Đọc quãng đường đã đi (cm)
    '''
    if I_CheDo == 0:
        state.DongCo_Trai.reset_angle(0)
        state.DongCo_Phai.reset_angle(0)
        return 0
    elif I_CheDo == 1:
        return (abs(state.DongCo_Trai.angle()) + abs(state.DongCo_Phai.angle())) / 2
    elif I_CheDo == 2:
        return ((abs(state.DongCo_Trai.angle()) + abs(state.DongCo_Phai.angle())) / 2) / 360 * state.X_G_QuangDuong1VongQuay
