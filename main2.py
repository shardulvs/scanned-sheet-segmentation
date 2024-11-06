import cv2
import numpy as np

# Load the image
input_path = "./images/3.jpg"
output_path = "./output/"
image = cv2.imread(input_path)

# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

# Use adaptive thresholding
binary_image = cv2.adaptiveThreshold(
    blurred_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 3, 2
)
cv2.imwrite(output_path + "1_binary.jpg", binary_image)

# Morphological Opening
kernel_ellipse_open = cv2.getStructuringElement(cv2.MORPH_RECT, (91, 21))
opened_image = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel_ellipse_open)
cv2.imwrite(output_path + "2_opened_image.jpg", opened_image)

# Morphological Closing
kernel_ellipse_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21))
kernel_rect_close = cv2.getStructuringElement(cv2.MORPH_RECT, (51, 11))
closed_image = cv2.morphologyEx(opened_image, cv2.MORPH_CLOSE, kernel_ellipse_close)
closed_image = cv2.morphologyEx(closed_image, cv2.MORPH_CLOSE, kernel_rect_close)
cv2.imwrite(output_path + "3_closed_image.jpg", closed_image)

# nice_binary = closed_image.copy()
# height, width = nice_binary.shape
# print(height, width)
# horizontal_threshold = width // 3
# vertical_threshold = height // 3
# horizontal_marked_image = cv2.cvtColor(nice_binary, cv2.COLOR_GRAY2BGR)
# for row in range(height):
#     start_col = None
#     for col in range(width):
#         if nice_binary[row, col] == 255:
#             if start_col is None:
#                 start_col = col
#         else:
#             if start_col is not None:
#                 run_length = col - start_col
#                 if run_length > horizontal_threshold:
#                     cv2.line(
#                         horizontal_marked_image,
#                         (start_col, row),
#                         (col - 1, row),
#                         (0, 0, 255),
#                         1,
#                     )
#                 start_col = None
#     # check if a white run goes to the end of the row
#     if start_col is not None:
#         run_length = width - start_col
#         if run_length > horizontal_threshold:
#             cv2.line(
#                 horizontal_marked_image,
#                 (start_col, row),
#                 (width - 1, row),
#                 (0, 0, 255),
#                 1,
#             )

# cv2.imwrite(output_path + "4_horizontal_white_runs.png", horizontal_marked_image)

nice_binary = closed_image.copy()
height, width = nice_binary.shape
vertical_threshold = height // 3

nice_binary = closed_image.copy()
height, width = nice_binary.shape
horizontal_threshold = width // 3
horizontal_marked_image = cv2.cvtColor(nice_binary, cv2.COLOR_GRAY2BGR)
horizontal_lines = []

for row in range(height):
    start_col = None
    for col in range(width):
        if nice_binary[row, col] == 255:  # White pixel in binary image
            if start_col is None:
                start_col = col  # Start of a white run
        else:
            if start_col is not None:
                run_length = col - start_col
                if run_length > horizontal_threshold:
                    cv2.line(
                        horizontal_marked_image,
                        (start_col, row),
                        (col - 1, row),
                        (0, 0, 255),
                        1,
                    )
                    horizontal_lines.append(
                        {
                            "row": row,
                            "start": start_col,
                            "end": col - 1,
                            "length": run_length,
                        }
                    )
                start_col = None

    if start_col is not None:
        run_length = width - start_col
        if run_length > horizontal_threshold:
            cv2.line(
                horizontal_marked_image,
                (start_col, row),
                (width - 1, row),
                (0, 0, 255),
                1,
            )
            horizontal_lines.append(
                {"row": row, "start": start_col, "end": width - 1, "length": run_length}
            )

cyan_lines = []
if horizontal_lines:
    average_length = sum(line["length"] for line in horizontal_lines) / len(
        horizontal_lines
    )
    for line in horizontal_lines:
        if line["length"] > average_length:
            cv2.line(
                horizontal_marked_image,
                (line["start"], line["row"]),
                (line["end"], line["row"]),
                (255, 255, 0),
                1,
            )
            cyan_lines.append(line)

cv2.imwrite(output_path + "4_horizontal_white_runs.png", horizontal_marked_image)


combined_lines = []

if cyan_lines:
    cyan_lines.sort(key=lambda x: x["row"])
    current_group = [cyan_lines[0]]
    for i in range(1, len(cyan_lines)):
        if cyan_lines[i]["row"] - cyan_lines[i - 1]["row"] <= 30:
            current_group.append(cyan_lines[i])
        else:
            avg_row = int(np.mean([line["row"] for line in current_group]))
            combined_lines.append({"row": avg_row, "start": 0, "end": width - 1})
            current_group = [cyan_lines[i]]
    if current_group:
        avg_row = int(np.mean([line["row"] for line in current_group]))
        combined_lines.append({"row": avg_row, "start": 0, "end": width - 1})

# final_combined_image = cv2.cvtColor(nice_binary, cv2.COLOR_GRAY2BGR)
final_combined_image = image.copy()
for line in combined_lines:
    cv2.line(
        final_combined_image,
        (line["start"], line["row"]),
        (line["end"], line["row"]),
        (255, 255, 0),
        10,
    )

cv2.imwrite(output_path + "5_combined_cyan_lines.png", final_combined_image)

# vertical_marked_image = cv2.cvtColor(nice_binary, cv2.COLOR_GRAY2BGR)
# for col in range(width):
#     start_row = None
#     for row in range(height):
#         if nice_binary[row, col] == 255:
#             if start_row is None:
#                 start_row = row
#         else:
#             if start_row is not None:
#                 run_length = row - start_row
#                 if run_length > vertical_threshold:
#                     cv2.line(
#                         vertical_marked_image,
#                         (col, start_row),
#                         (col, row - 1),
#                         (0, 0, 255),
#                         1,
#                     )
#                 start_row = None
#     # check if a white run goes to the end of the row
#     if start_row is not None:
#         run_length = height - start_row
#         if run_length > vertical_threshold:
#             cv2.line(
#                 vertical_marked_image,
#                 (col, start_row),
#                 (col, height - 1),
#                 (0, 0, 255),
#                 1,
#             )

# cv2.imwrite(output_path + "5_vertical_white_runs.png", vertical_marked_image)

# Morphological Opening
kernel_ellipse_open_vertical = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 191))
opened_image_vertical = cv2.morphologyEx(
    binary_image, cv2.MORPH_OPEN, kernel_ellipse_open_vertical
)
cv2.imwrite(output_path + "6_opened_image.jpg", opened_image_vertical)

# Morphological Closing
kernel_ellipse_close_vertical = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21))
kernel_rect_close_vertical = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 51))
closed_image_vertical = cv2.morphologyEx(
    opened_image_vertical, cv2.MORPH_CLOSE, kernel_ellipse_close_vertical
)
closed_image_vertical = cv2.morphologyEx(
    closed_image_vertical, cv2.MORPH_CLOSE, kernel_rect_close_vertical
)
cv2.imwrite(output_path + "7_closed_image.jpg", closed_image_vertical)


nice_binary = closed_image_vertical.copy()
height, width = nice_binary.shape
vertical_threshold = height // 3

vertical_marked_image = cv2.cvtColor(nice_binary, cv2.COLOR_GRAY2BGR)
vertical_lines = []

for col in range(width):
    start_row = None
    for row in range(height):
        if nice_binary[row, col] == 255:  # White pixel in binary image
            if start_row is None:
                start_row = row  # Start of a white run
        else:
            if start_row is not None:
                run_length = row - start_row
                if run_length > vertical_threshold:
                    cv2.line(
                        vertical_marked_image,
                        (col, start_row),
                        (col, row - 1),
                        (0, 0, 255),
                        1,
                    )
                    vertical_lines.append(
                        {
                            "col": col,
                            "start": start_row,
                            "end": row - 1,
                            "length": run_length,
                        }
                    )
                start_row = None

    # Check if a white run extends to the end of the column
    if start_row is not None:
        run_length = height - start_row
        if run_length > vertical_threshold:
            cv2.line(
                vertical_marked_image,
                (col, start_row),
                (col, height - 1),
                (0, 0, 255),
                1,
            )
            vertical_lines.append(
                {
                    "col": col,
                    "start": start_row,
                    "end": height - 1,
                    "length": run_length,
                }
            )

# Calculate the average length of the vertical lines
cyan_lines = []
if vertical_lines:
    average_length = sum(line["length"] for line in vertical_lines) / len(
        vertical_lines
    )

    # Color lines greater than average length with cyan
    for line in vertical_lines:
        if line["length"] > average_length:
            cv2.line(
                vertical_marked_image,
                (line["col"], line["start"]),
                (line["col"], line["end"]),
                (255, 255, 0),
                1,
            )
            cyan_lines.append(line)

cv2.imwrite(output_path + "8_vertical_white_runs.png", vertical_marked_image)

# Combine close cyan lines (within 2 pixels in column distance)
combined_lines_vertical = []
if cyan_lines:
    cyan_lines.sort(key=lambda x: x["col"])  # Sort by column
    current_group = [cyan_lines[0]]

    for i in range(1, len(cyan_lines)):
        if cyan_lines[i]["col"] - cyan_lines[i - 1]["col"] <= 50:  # Close enough
            current_group.append(cyan_lines[i])
        else:
            # Process the current group and start a new one
            avg_col = int(np.mean([line["col"] for line in current_group]))
            combined_lines_vertical.append(
                {"col": avg_col, "start": 0, "end": height - 1}
            )
            current_group = [cyan_lines[i]]

    # Process the last group
    if current_group:
        avg_col = int(np.mean([line["col"] for line in current_group]))
        combined_lines_vertical.append({"col": avg_col, "start": 0, "end": height - 1})

# Draw combined vertical lines on a new image
# final_combined_image = cv2.cvtColor(nice_binary, cv2.COLOR_GRAY2BGR)
final_combined_image = image.copy()
for line in combined_lines_vertical:
    cv2.line(
        final_combined_image,
        (line["col"], line["start"]),
        (line["col"], line["end"]),
        (255, 255, 0),  # Cyan color
        10,  # Line thickness
    )

cv2.imwrite(output_path + "9_combined_vertical_lines.png", final_combined_image)

final_combined_mesh = image.copy()
for line in combined_lines_vertical:
    cv2.line(
        final_combined_mesh,
        (line["col"], line["start"]),
        (line["col"], line["end"]),
        (0, 255, 255),  # Cyan color
        10,  # Line thickness
    )

for line in combined_lines:
    cv2.line(
        final_combined_mesh,
        (line["start"], line["row"]),
        (line["end"], line["row"]),
        (0, 255, 255),
        10,
    )


cv2.imwrite(output_path + "10_combined_mesh.png", final_combined_mesh)
