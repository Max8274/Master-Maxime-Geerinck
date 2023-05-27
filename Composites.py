import sys
sys.path.append('/Users/maxim/Master')
sys.path.append('/Users/maxim/anaconda3/envs/ldm-env-master/Lib/site-packages')
import cv2
import scipy as sp
import scipy.ndimage

#crop the image: allowed values for center: 256, 621, 986
def crop_image(image,center):
    car_cropped = image[0:375,center-256:center+256,:]
    car_padded = cv2.copyMakeBorder( car_cropped, 137, 0, 0, 0, cv2.BORDER_CONSTANT)
    return car_padded

# takes a cropped image and a background, pastes the cropped image onto the backgroud based with the center at <center> pixels from the left
def restore_image(im_cropped,im_original,center):
    car_depadded = im_cropped[137:512,0:512]
    im_original[0:375,center-256:center+256,:] = car_depadded
    return im_original

 # creates a binary mask from the <car> object
def create_mask(car):
    im_in = cv2.cvtColor(car,cv2.COLOR_RGB2GRAY)
    print(len(im_in))
    # Threshold.
    # Set values equal to or above 0 to 0.
    # Set values below 0 to 255.
    th, im_th = cv2.threshold(im_in, 0, 255, cv2.THRESH_BINARY)
    filled = sp.ndimage.binary_fill_holes(im_th).astype(int)
    mask = filled*255
    mask = mask.astype('uint8')
    return mask

# uses mask to paste a car object onto a background
def create_composite(car,mask,background):
    color_mask = cv2.cvtColor(mask,cv2.COLOR_GRAY2RGB)
    background = cv2.subtract(background,color_mask)
    composite = cv2.add(background,car)
    print("composite created")
    return composite

def main():
    # get the args passed to the script after
    filename=sys.argv[1]
    print(filename)
    car_type=sys.argv[2]

    # load the car and background image
    car_image = cv2.imread(filename) #filename -> blender output
    cam_im_path = '/Users/maxim/Master/original/'+filename.split('/')[6]
    print("image original", cam_im_path)
    camera_image = cv2.imread(cam_im_path)

    # split the images in 3 separate 512x512 images since this is the input size of DIH
    car1 = crop_image(car_image,256)
    car2 = crop_image(car_image,621)
    car3 = crop_image(car_image,986)
    bg1 = crop_image(camera_image,256)
    bg2 = crop_image(camera_image,621)
    bg3 = crop_image(camera_image,986)

    # create masks for each image
    mask1 = create_mask(car1)
    mask2 = create_mask(car2)
    mask3 = create_mask(car3)

    total_mask = create_mask(car_image)
    cv2.imwrite(
        'C:/Users/maxim/Master/masks/' + car_type + '/' + filename.split('/')[6],
        total_mask)

    # create the composite for each image
    composite1 = create_composite(car1,mask1,bg1)
    composite2 = create_composite(car2,mask2,bg2)
    composite3 = create_composite(car3,mask3,bg3)

    # save the unharmonized composites
    total_composite = restore_image(composite1, camera_image, 256)
    total_composite = restore_image(composite2, total_composite, 621)
    total_composite = restore_image(composite3, total_composite, 986)
    cv2.imwrite('/Users/maxim/Master/composites/'+car_type + '/'+filename.split('/')[6],total_composite)

if __name__ == "__main__":
    print("test")
    main()