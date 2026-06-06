# =====================================================
#              PHẦN CỨNG & BIẾN GLOBAL
# =====================================================
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop, Icon
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch, multitask, run_task

# --- Khởi tạo phần cứng ---
hub = PrimeHub()
hub.imu.reset_heading(0)

DongCo_Trai    = Motor(Port.C, Direction.COUNTERCLOCKWISE)
DongCo_Phai    = Motor(Port.D)
DongCo_TayTrai = Motor(Port.B, Direction.COUNTERCLOCKWISE)
DongCo_TayPhai = Motor(Port.A, Direction.CLOCKWISE)

CamBien_DoDuong_F = ColorSensor(Port.F)
CamBien_DocMau_E  = ColorSensor(Port.E)

time = StopWatch()
time.reset()

BaseRobot = DriveBase(DongCo_Trai, DongCo_Phai, 62.4, 196)

# --- Biến PD ---
lastError = 0
kP = 0
kD = 0
PDscale = 1
power = 0
yaw = 0

# --- Biến điều hướng ---
X_G_HuongMuonDen = 0

# --- Biến pin ---
X_G_BatteryScale        = 1
X_G_PhanTramPin         = 100
X_G_SaiSoDoPin_TocDo    = 0
X_G_SaiSoDoPin_QuangDuong = 0

# --- Biến bánh xe ---
X_G_DuongKinhBanhXe    = 6.24
X_G_QuangDuong1VongQuay = 19.6

# --- Biến phản xạ ---
X_G_GiaTriPhanXa_NhoNhat       = 0
X_G_GiaTriPhanXa_LonNhat       = 100
X_G_GioiHanSaiSoDiLine         = 10
X_G_GiaTriPhanXa_MuonBamTheo   = 55
X_G_GiaTriPhanXa_DungDuongDen  = 15
X_G_GiaTriPhanXa_DungDuongTrang = 85
X_G_GiaTriPhanXa_DungDuongXanh  = 30

# --- Biến tốc độ di chuyển ---
G_TocDo_BatDau              = 35
G_QuangDuong_TangToc        = 1
G_TocDo_KetThuc             = 35
G_QuangDuong_GiamToc        = 7
G_QuangDuong_DiChamKhiDiLine = 5

# --- Thông số PD mặc định ---
G_TS_PD_LineQD_0            = [0.5, 400]
G_TS_PD_LinePX_0            = [0.2, 100]
G_TS_PD_Gyro_0              = [5, 25]
G_TS_PD_Gyro_DuongCong_0    = [8, 100]
G_TS_PD_Gyro_Xoay2DC_0      = [12, 265]
G_TS_PD_Gyro_Xoay1DC_Tien_0 = [17, 870]
G_TS_PD_Gyro_Xoay1DC_Lui_0  = [17, 870]
G_TS_PD_KhongGyro_DiThang_0 = [1, 20]
G_TS_PD_KhongGyro_DiCong_0  = [0.3, 100]

# --- Thông số PD hiện tại ---
G_TS_PD_LineQD            = [0.5, 400]
G_TS_PD_LinePX            = [0.2, 100]
G_TS_PD_Gyro              = [5, 25]
G_TS_PD_Gyro_DuongCong    = [8, 100]
G_TS_PD_Gyro_Xoay2DC      = [12, 265]
G_TS_PD_Gyro_Xoay1DC_Tien = [17, 870]
G_TS_PD_Gyro_Xoay1DC_Lui  = [17, 870]
G_TS_PD_KhongGyro_DiThang = [1, 20]
G_TS_PD_KhongGyro_DiCong  = [0.3, 100]

# --- Thông số cánh tay ---
G_TayTrai_TocDoToiDa  = 1200
G_TayTrai_GiaTocToiDa = 7000
G_TayTrai_MomentToiDa = 1000
G_TayPhai_TocDoToiDa  = 1200
G_TayPhai_GiaTocToiDa = 7000
G_TayPhai_MomentToiDa = 1000

# --- Chế độ thi ---
X_G_CheDoThi = False
