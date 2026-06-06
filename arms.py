# =====================================================
#                   CÁNH TAY
# =====================================================
import state
from pybricks.parameters import Stop
from pybricks.tools import wait

def ResetCanhTay():
    '''Khởi tạo và hiệu chỉnh cánh tay về vị trí gốc'''
    state.G_TayTrai_TocDoToiDa  = 1200
    state.G_TayTrai_GiaTocToiDa = 7000
    state.G_TayTrai_MomentToiDa = 1000
    state.DongCo_TayTrai.control.limits(
        state.G_TayTrai_TocDoToiDa,
        state.G_TayTrai_GiaTocToiDa,
        state.G_TayTrai_MomentToiDa
    )
    state.G_TayPhai_TocDoToiDa  = 1200
    state.G_TayPhai_GiaTocToiDa = 7000
    state.G_TayPhai_MomentToiDa = 1000
    state.DongCo_TayPhai.control.limits(
        state.G_TayPhai_TocDoToiDa,
        state.G_TayPhai_GiaTocToiDa,
        state.G_TayPhai_MomentToiDa
    )
    state.DongCo_TayPhai.run_until_stalled(-500, Stop.HOLD, 50)
    if abs(state.DongCo_TayPhai.angle()) > 360:
        state.DongCo_TayPhai.reset_angle(360 - abs(state.DongCo_TayPhai.angle()))
    else:
        state.DongCo_TayPhai.reset_angle(0)
    state.DongCo_TayPhai.run_target(1100, 140)

def Tay_Truoc(I_TocDo=100, I_ViTri=45, I_DoiDenKhiHoanThanh: bool = True,
              I_CheDoViTri: bool = True, I_MucDoTangGiamToc=100):
    '''
    Điều khiển tay trước (DongCo_TayTrai)
    * I_TocDo - 0~100 (vị trí) hoặc -100~100 (thời gian)
    * I_ViTri - góc đích (độ), hoặc thời gian ms nếu I_CheDoViTri=False
    * I_DoiDenKhiHoanThanh - True=chờ xong, False=không chờ
    * I_CheDoViTri - True=đến vị trí, False=chạy theo thời gian
    * I_MucDoTangGiamToc - % gia tốc (100 = mặc định)
    '''
    if I_MucDoTangGiamToc != 100:
        state.DongCo_TayTrai.control.limits(
            acceleration=state.G_TayTrai_GiaTocToiDa * I_MucDoTangGiamToc // 100
        )
    if I_CheDoViTri:
        if I_ViTri > 90:
            state.DongCo_TayTrai.run_until_stalled(
                int(abs(I_TocDo / 100 * state.G_TayTrai_TocDoToiDa)), Stop.HOLD
            )
        elif I_ViTri < -15:
            state.DongCo_TayTrai.run_target(
                int(abs(I_TocDo / 100 * state.G_TayTrai_TocDoToiDa)),
                -15, wait=I_DoiDenKhiHoanThanh
            )
        else:
            state.DongCo_TayTrai.run_target(
                int(abs(I_TocDo / 100 * state.G_TayTrai_TocDoToiDa)),
                I_ViTri, wait=I_DoiDenKhiHoanThanh
            )
    else:
        state.DongCo_TayTrai.run_time(
            int(I_TocDo / 100 * state.G_TayTrai_TocDoToiDa),
            abs(I_ViTri), wait=I_DoiDenKhiHoanThanh
        )
    if I_MucDoTangGiamToc != 100:
        state.DongCo_TayTrai.control.limits(
            acceleration=state.G_TayTrai_GiaTocToiDa
        )

def Tay_Sau(I_TocDo=100, I_ViTri=45, I_DoiDenKhiHoanThanh: bool = True,
            I_CheDoViTri: bool = True, I_MucDoTangGiamToc=100):
    '''
    Điều khiển tay sau (DongCo_TayPhai)
    * I_TocDo - 0~100 (vị trí) hoặc -100~100 (thời gian)
    * I_ViTri - góc đích (độ), hoặc thời gian ms nếu I_CheDoViTri=False
    * I_DoiDenKhiHoanThanh - True=chờ xong, False=không chờ
    * I_CheDoViTri - True=đến vị trí, False=chạy theo thời gian
    * I_MucDoTangGiamToc - % gia tốc (100 = mặc định)
    '''
    if I_MucDoTangGiamToc != 100:
        state.DongCo_TayPhai.control.limits(
            acceleration=state.G_TayPhai_GiaTocToiDa * I_MucDoTangGiamToc // 100
        )
    if I_CheDoViTri:
        if I_ViTri > 230:
            state.DongCo_TayPhai.run_target(
                int(abs(I_TocDo / 100 * state.G_TayPhai_TocDoToiDa)),
                230, wait=I_DoiDenKhiHoanThanh
            )
        elif I_ViTri < -5:
            state.DongCo_TayPhai.run_target(
                int(abs(I_TocDo / 100 * state.G_TayPhai_TocDoToiDa)),
                -5, wait=I_DoiDenKhiHoanThanh
            )
        else:
            state.DongCo_TayPhai.run_target(
                int(abs(I_TocDo / 100 * state.G_TayPhai_TocDoToiDa)),
                I_ViTri, wait=I_DoiDenKhiHoanThanh
            )
    else:
        state.DongCo_TayPhai.run_time(
            int(I_TocDo / 100 * state.G_TayPhai_TocDoToiDa),
            abs(I_ViTri), wait=I_DoiDenKhiHoanThanh
        )
    if I_MucDoTangGiamToc != 100:
        state.DongCo_TayPhai.control.limits(
            acceleration=state.G_TayPhai_GiaTocToiDa
        )
