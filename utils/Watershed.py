import numpy as np
import cv2 as cv

def clear_border(array): # for this, assume square image (im tired)
    def floodfill(x, y):
        stack = [(x, y)] # emulate a stack
        while stack:
            cx, cy = stack.pop()
            if(cx < 0 or cx >= array.shape[0]): continue
            if(cy < 0 or cy >= array.shape[1]): continue
            if(array[cx][cy] == 0): continue # no component here 
            array[cx][cy] = 0

            stack.append((cx+1, cy))
            stack.append((cx-1, cy))
            stack.append((cx, cy+1))
            stack.append((cx, cy-1))
    w = array.shape[0]
    for idx in range(w):
        floodfill(idx, 0)
        floodfill(idx, array.shape[1]-1)
        floodfill(0, idx)
        floodfill(array.shape[0]-1, idx)
    
    return array

def watershed_algorithm(img):
    img_gray = img[:, :, 1]
    # Perform morphological operations
    # Morphological opening to remove noise (white dots) , erosion and then dilation 
    # Morphological closing to remove small holes in object (dark holes), dilation and then erosion 
    # dilation = expand
    # erosion = contract

    # morphological opening, remove noise in low intensity area
    kernel = np.ones((3, 3), np.uint8)

    # binary thresholding, where the threshold value is the weighted sum of pixel intensity in neighborhood minus C
    opening = cv.adaptiveThreshold(img_gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 31, 5)
    opening = clear_border(opening) # remove any component touching the image border

    # sure bg
    sure_bg = cv.dilate(opening, kernel, iterations=10) # dilate -> causes bright regions/regions with high intensity to expand

    # finding sure fg area
    dist_transform = cv.distanceTransform(opening, cv.DIST_L2, 5)
    ret, sure_fg = cv.threshold(dist_transform, 0.5*dist_transform.max(), 255, 0)

    sure_fg = np.uint8(sure_fg) # we are sure these pixels belong to the foreground

    unknown = cv.subtract(sure_bg, sure_fg) # areas that are unknown if they belong to background or foreground

    ret, markers = cv.connectedComponents(sure_fg) # we will mark each connected component with a different color
    markers = markers+10 # shift labels by 10
    markers[unknown==255] = 0 # in pixels where unknown has intensity 255, set marker to 0 where 0 is the pixels that are undetermined
    # grow regions from connected components using watershed algorithm
    # basically: during region growing, when regions of different labels touch, a "watershed" border will be drawn between the touching regions.
    img_watershed = cv.watershed(img, markers)

    return img_watershed

drawing = False
def watershed(image):
    image_watershed = watershed_algorithm(image)

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
    image_gray = image[:, :, 1]

    cv.imshow("Draw Line", image_gray)
    cv.setMouseCallback("Draw Line", draw_freehand, line_mask)
    cv.waitKey(0)
    cv.destroyAllWindows()
    vis = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
    input = line_mask
    def floodfill(x, y, image, component_idx):
        stack = [(x, y)] # emulate a stack
        while stack:
            cx, cy = stack.pop()
            if(cx < 0 or cx >= image.shape[0]): continue
            if(cy < 0 or cy >= image.shape[1]): continue
            if(vis[cx][cy] == 255): continue # visited
            if not np.array_equal(image[cx][cy], component_idx): continue # outside component
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

    image_watershed = np.int32(image_watershed) # prevent overflow when operation results in negative
    for x in range(input.shape[0]):
        for y in range(input.shape[1]):
            if input[x][y] > 0 and vis[x][y] == 0: # marked by user but not yet added
                # what is the feature of current pixel?
                # let's take intensity as a feature, because tumor components should have similar intensity to each other
                cur_intensity = image_watershed[x][y]
                floodfill(x, y, image_watershed, cur_intensity)
    return vis


