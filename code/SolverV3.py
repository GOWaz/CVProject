import cv2
import numpy as np
import scipy.ndimage
from scipy.ndimage import filters
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

class SolverV2:
    def solve(self,image):
        input_image = image

        gray_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

        thresh = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 1, 11, 3)
        thresh = cv2.GaussianBlur(thresh, (3, 3), 2)

        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

        kernel = np.ones((2, 2), np.uint8)
        dilated_image = cv2.dilate(opening, kernel, iterations=1)

        kernel = np.ones((3, 3), np.uint8)
        closing = cv2.morphologyEx(dilated_image.astype('uint8'), cv2.MORPH_CLOSE, kernel)

        kernel = np.ones((2, 2), np.uint8)
        erosion = cv2.erode(closing, kernel, iterations=1)

        contours, _ = cv2.findContours(dilated_image, 0, 1)
        sorted = sorted([[cnt.shape[0], i] for i, cnt in enumerate(contours)], reverse=True)[:40]
        biggest = [contours[s[1]] for s in sorted]
        fill = cv2.drawContours(np.zeros(input_image.shape[:2]), biggest, -1, 255, thickness=cv2.FILLED)

        smooth = scipy.ndimage.median_filter(fill.astype('uint8'), size=10)
        trim_contours, _ = cv2.findContours(smooth, 0, 1)
        cv2.drawContours(smooth, trim_contours, -1, color=0, thickness=1)

        masked_image = cv2.bitwise_and(input_image, input_image, mask=smooth.astype('uint8'))

        contours, _ = cv2.findContours(smooth, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contour_image = np.zeros_like(input_image, dtype=np.uint8)
        cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)

        image_with_boxes = masked_image.copy()
        pieces = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            piece = masked_image[y:y + h, x:x + w]
            pieces.append(piece)
            cv2.rectangle(image_with_boxes, (x, y), (x + w, y + h), (0, 255, 0), 2)


        distance_transforms = []
        centroids = []
        canny_edges_array = []
        corner_harris_array = []
        for i, piece in enumerate(pieces):
            gray_piece = cv2.cvtColor(piece, cv2.COLOR_BGR2GRAY)

            distance_transform = cv2.distanceTransform(gray_piece, cv2.DIST_L2, 5)
            normalized_distance_transform = cv2.normalize(distance_transform, None, 0, 1, cv2.NORM_MINMAX)
            distance_transforms.append(normalized_distance_transform)

            _, max_val, _, max_loc = cv2.minMaxLoc(distance_transform)
            centroids.append(max_loc)

            print(f"i {i} , centroids {max_loc}")

            canny_edges = cv2.Canny(piece, 255, 255)
            canny_edges_array.append(canny_edges)
            print(canny_edges)
            # cv2.imshow(f'Canny Edges {i + 1}', canny_edges)

            # Apply Harris corner detection
            dst = cv2.cornerHarris(gray_piece, blockSize=2, ksize=3, k=0.04)

            # Threshold the corner response to get the corners
            threshold_corner = 0.01 * dst.max()
            corner_image = np.zeros_like(dst)
            corner_image[dst > threshold_corner] = 255
            corner_points = np.column_stack(np.where(corner_image > 0))
            corner_harris_array.append(corner_points)
            # Display the original image and the detected corners
            plt.subplot(121), plt.imshow(piece, cmap='gray')
            plt.title('Original Image'), plt.xticks([]), plt.yticks([])

            plt.subplot(122), plt.imshow(corner_image, cmap='gray')
            plt.title('Detected Corners'), plt.xticks([]), plt.yticks([])
            plt.show()
            # cv2.imshow(f'Piece {i + 1}', piece)
            # cv2.imshow(f'Distance Transform {i + 1}', normalized_distance_transform)
            # cv2.waitKey(0)

        distances_array = []

        for i, corner_harris in enumerate(corner_harris_array):
            distances = []
            for edge_point_y, edge_point_x in np.column_stack(np.where(corner_harris > 0)):
                distance = np.sqrt((edge_point_x - centroids[i][0]) ** 2 + (edge_point_y - centroids[i][1]) ** 2)
                distances.append(distance)
            distances_array.append(distances)

        # for i, distances in enumerate(distances_array):
        #     print(f'Distances for Piece {i+1}: {distances}')

        # Find peaks in the distances array
        peaks_array = []

        for i, distances in enumerate(distances_array):
            peaks, _ = find_peaks(distances)
            peaks_array.append(peaks)
            print(f"len peaks {len(peaks)}")

        for i, distances in enumerate(distances_array):
            plt.plot(distances, label=f'Piece {i + 1}')

            # Use the indices of peaks to access corresponding values in distances
            peak_indices = peaks_array[i]
            peak_values = [distances[idx] for idx in peak_indices]

            plt.plot(peak_indices, peak_values, 'x', label=f'Peaks Piece {i + 1}')

            plt.xlabel('Pixel Index')
            plt.ylabel('Distance')
            plt.legend()
            plt.show()

        for i, piece in enumerate(pieces):
            centroid = centroids[i]
            peak_indices = peaks_array[i]
            distances = distances_array[i]

            for peak_index in peak_indices:
                edge_point_y, edge_point_x = np.column_stack(np.where(canny_edges_array[i] > 0))[peak_index]

                # Calculate the angle between the line and the horizontal axis
                angle_rad = np.arctan2(centroid[1] - edge_point_y, edge_point_x - centroid)
                angle_deg = np.degrees(angle_rad)

                print(f'Angle for Piece {i + 1}, Peak {peak_index + 1}: {angle_deg} degrees')

        # cv2.imshow("Input",input_image)
        # cv2.imshow('Grayscale Image', gray_image)
        # cv2.imshow('Binary Image', binary_image)
        # cv2.imshow('Thresh Image', thresh)
        # cv2.imshow('Opening (White Noise Removal)', opening)
        # cv2.imshow('Dilated Image', dilated_image)
        # cv2.imshow('Fill Image', fill)
        # cv2.imshow('smooth', smooth)
        # cv2.imshow('Masked Image', masked_image)
        # cv2.imshow('Image with Contours', contour_image)
        cv2.imshow('Image with Bounding Boxes', image_with_boxes)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

