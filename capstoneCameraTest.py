from PIL import Image
im = Image.open("C:\Users\Sriram\Desktop\Misc images\Misc images\drone_test_3 copy.jpg", "r")
width, height = im.size
print(width)
print(height)
pix_val = list(im.getdata())
row_cnt = 0
min_black_val = 1000
min_row_val = 1000
for row in pix_val:
    row_cnt = row_cnt + 1
    temp_sum = 0
    for val in row:
        temp_sum = temp_sum + val
    if temp_sum < min_black_val:
        min_black_val = temp_sum
        min_row_val = row_cnt
#print(min_row_cnt)
#print(min_row_sum)
#print(num_black)
#min_row_loc = (min_row_sum / num_black)
x = min_row_val / width
y = min_row_val - (x * width)

print("X Coordinate is: %s" %x)
print("Y Coordinate is: %s" %y)

