import cv2
import pytesseract
from lib_detection import load_model, detect_lp, im2single
import pyautogui

# Định nghĩa các biến và hàm cần thiết
char_list = '0123456789ABCDEFGHKLMNPRSTUVXYZ'

def fine_tune(lp):
    newString = ""
    for i in range(len(lp)):
        if lp[i] in char_list:
            newString += lp[i]
    return newString

# Lấy ảnh từ màn hình
myScreenshot = pyautogui.screenshot()
myScreenshot.save(r'E:\\mqtt server\\recognition_license_plate\\mycar.jpg')

# Thiết lập đường dẫn Tesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Đường dẫn ảnh, bạn có thể thay đổi tên file tại đây
img_path = "E:\\mqtt server\\recognition_license_plate\\mycar.jpg"

# Load model LP detection
wpod_net_path = "E:\\mqtt server\\recognition_license_plate\\wpod-net_update1.json"
wpod_net = load_model(wpod_net_path)

# Đọc file ảnh đầu vào
Ivehicle = cv2.imread(img_path)

# Kích thước lớn nhất và nhỏ nhất của 1 chiều ảnh
Dmax = 608
Dmin = 288

# Lấy tỷ lệ giữa W và H của ảnh và tìm ra chiều nhỏ nhất
ratio = float(max(Ivehicle.shape[:2])) / min(Ivehicle.shape[:2])
side = int(ratio * Dmin)
bound_dim = min(side, Dmax)

# Dùng WPOD để nhận diện biển số
_, LpImg, lp_type = detect_lp(wpod_net, im2single(Ivehicle), bound_dim, lp_threshold=0.5)

if len(LpImg) > 0:
    # Chuyển đổi ảnh biển số
    LpImg[0] = cv2.convertScaleAbs(LpImg[0], alpha=(255.0))

    # Chuyển ảnh biển số về màu xám
    gray = cv2.cvtColor(LpImg[0], cv2.COLOR_BGR2GRAY)

    # Áp dụng ngưỡng để phân tách số và nền
    binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # Nhận diện biển số. Cấu hình --psm 7 là để nhận diện 1 dòng only
    text = pytesseract.image_to_string(binary, lang="eng", config="--psm 7")
    print(fine_tune(text))

    # In biển số lên ảnh
    # cv2.putText(Ivehicle, fine_tune(text), (50, 50), cv2.FONT_HERSHEY_PLAIN, 3.0, (0, 0, 255), lineType=cv2.LINE_AA)

    # Hiển thị ảnh và lưu ảnh ra file output.png (bạn có thể sử dụng nếu cần thiết)
    # cv2.imshow("Anh input", Ivehicle)
    # cv2.imwrite("output.png", Ivehicle)
    cv2.waitKey()

    # Ghi biển số vào file result.txt
    with open("E:\\mqtt server\\output.txt", "w") as f:
        f.write(fine_tune(text))

cv2.destroyAllWindows()
