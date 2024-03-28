import cv2
import numpy as np
from Cutter import Cutter
from matplotlib import pyplot as plt


class SolverV2:

    def __init__(self):
        self.cutter = Cutter()

    def score(self, image1,image2):
        result_image_resized = cv2.resize(image1, (image2.shape[1], image2.shape[0]))
        abs_diff = np.abs(result_image_resized - image2)
        return 100-(np.sum(abs_diff) / (255.0 * np.prod(image2.shape)) * 100)

    def solve(self,image,rows,cols):
        self.original_image=image
        original_grid, _, _ = self.cutter.cut_image_into_grid(image, rows, cols)
        shuffled_grid, rows, cols = self.cutter.cut_and_shuffle(image, rows, cols)
        # self.cutter.display_grid(original_grid,rows,cols,'original_grid')
        # self.cutter.display_grid(shuffled_grid,rows,cols,'shuffled_grid')
        self.original_sub_images = original_grid
        self.shuffled_grid = shuffled_grid

        score_table=[]
        result=[]
        for i,image in enumerate (shuffled_grid):
            score_table.append([])
            for j,original_image in enumerate(original_grid):
                score_result=self.score(image,original_image)
                score_table[i].append(score_result)
                if score_result>=100:
                    result.append((i,j))
                    break

        images_list=[0]*rows*cols
        for i,j in result:
            images_list[j]=self.shuffled_grid[i]

        result_image=self.concatenate_images(images_list,rows,cols)
        cv2.imshow('Result Image',result_image)
        cv2.waitKey(0)
        return result_image

    def concatenate_images(self, image_list, rows, cols):
        # Assuming all images have the same shape
        # height, width, channels = image_list[0].shape
        height, width, channels = self.original_sub_images[0].shape
        result_image = np.zeros((height * rows, width * cols, channels), dtype=np.uint8)

        for i, img in enumerate(image_list):
            row_index = i // cols
            col_index = i % cols
            img=cv2.resize(img,(width,height))
            result_image[row_index * height: (row_index + 1) * height, col_index * width: (col_index + 1) * width, :] = img
        result_image_resized = cv2.resize(result_image, (800,600))
        return result_image_resized


# solver = SolverV2()
#
# original_image = plt.imread('../Asset/06.jpg')
#
# solver.solve(original_image, 3, 3)
