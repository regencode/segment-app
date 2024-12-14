import numpy as np
import cv2 as cv



drawing = False
def region_growing(image, tolerance=50):

    # Tolerance is how much the intensity of a pixel needs to differ in order to not be classified in the same component
    line_mask = np.zeros_like(image, dtype=np.uint8)

    def draw_freehand(event, x, y, flags, param):
        global drawing

        if event == cv.EVENT_LBUTTONDOWN:  # Start drawing
            drawing = True

        elif event == cv.EVENT_MOUSEMOVE and drawing:  # Draw while moving the mouse
            cv.circle(line_mask, (x, y), radius=2, color=(255, 255, 255), thickness=1)

        elif event == cv.EVENT_LBUTTONUP:  # Stop drawing
            drawing = False

    # Handle user input
    image = image[:, :, 1]
    cv.imshow("Draw Line", image)
    cv.setMouseCallback("Draw Line", draw_freehand, line_mask)
    cv.waitKey(0)
    cv.destroyAllWindows()
    vis = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
    input = line_mask
    def floodfill(x, y, starting_condition):
        stack = [(x, y)] # emulate a stack
        while stack:
            cx, cy = stack.pop()
            if(cx < 0 or cx >= image.shape[0]): continue
            if(cy < 0 or cy >= image.shape[1]): continue
            if(vis[cx][cy] == 255): continue # visited
            if(abs(starting_condition - image[cx][cy]) > tolerance): continue
            vis[cx][cy] = 255

            stack.append((cx+1, cy))
            stack.append((cx-1, cy))
            stack.append((cx, cy+1))
            stack.append((cx, cy-1))
    print(input.shape) 
    input = input[:, :, 0]
    cv.imshow("user_input", input)
    cv.waitKey(0)
    cv.destroyAllWindows()
    # assuming numpy format

    image = np.astype(image, np.int32) # prevent overflow when operation results in negative
    for x in range(input.shape[0]):
        for y in range(input.shape[1]):
            if input[x][y] > 0 and vis[x][y] == 0: # marked by user but not yet added
                # what is the feature of current pixel?
                # let's take intensity as a feature, because tumor components should have similar intensity to each other
                cur_intensity = image[x][y]
                floodfill(x, y, cur_intensity)
    return vis

