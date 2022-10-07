import cv2

img_color = cv2.imread('test.jpg',cv2.IMREAD_COLOR)
img_grayscale = cv2.imread('test.jpg',cv2.IMREAD_GRAYSCALE)
img_unchanged = cv2.imread('test.jpg',cv2.IMREAD_UNCHANGED)

font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img_unchanged, 'Tania', (10,450), font, 3, (0, 255, 0), 2, cv2.LINE_AA)

print(f"width of the image: {img_color.shape[1]} pixels")
print(f"height of the image: {img_color.shape[0]}  pixels")
print(f"channels of the image: {img_color.shape[2]}")

cv2.imshow('color image',img_color)
cv2.imshow('grayscale image',img_grayscale)
cv2.imshow('unchanged image',img_unchanged)

cv2.waitKey(0)

cv2.destroyAllWindows()

cv2.imwrite('Tania.jpg',img_unchanged)
