import cv2

# Load the image
input_path = "./images/1.jpg"
output_path = "./output/"
image = cv2.imread(input_path)

# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

# Use adaptive thresholding
binary_image = cv2.adaptiveThreshold(
    blurred_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 3, 2
)
cv2.imwrite("./output/1_binary.jpg", binary_image)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (51, 51))
kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 500))
opened_image = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel)
opened_image2 = cv2.morphologyEx(opened_image, cv2.MORPH_OPEN, kernel2)

cv2.imwrite(output_path + "2.jpg", opened_image2)

kernel_horizontal = cv2.getStructuringElement(cv2.MORPH_RECT, (100, 1))
kernel_vertical = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1000))
opened_image3 = cv2.morphologyEx(opened_image2, cv2.MORPH_CLOSE, kernel_horizontal)
cv2.imwrite(output_path + "3.jpg", opened_image3)

opened_image4 = cv2.morphologyEx(opened_image3, cv2.MORPH_CLOSE, kernel_vertical)
cv2.imwrite(output_path + "4.jpg", opened_image4)
