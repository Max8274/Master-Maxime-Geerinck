# Master-Maxime-Geerinck

## Introduction
This manual provides detailed instructions on the utilization of our model, specifically developed for the purpose of enhancing self-driving car images through the implementation of diffusion models. Our model offers the capability to generate synthetic car frames, which can subsequently be translated into realistic-looking car frames with preservation of the background, using our advanced techniques. Moreover, the model facilitates the translation of sequences of frames, such as those found in videos, ensuring consistent rendering of the car in each output frame. These translated frames can be compiled to form a cohesive video.
To assess the effectiveness of our method, we employ multiple evaluation approaches. In addition to visual assessment, we utilize the YOLOv5 object detection system to analyze the performance of our translated frames. Furthermore, we incorporate a metric known as Fréchet Inception Distance (FID), which evaluates the similarity between the data distributions of the generated frames and real car frames. Additionally, we employ a consistency structural similarity index (SSIM) to assess the consistency between pairs of video output frames, providing further insight into the quality and coherence of the translated sequences.

## Techniques
-	Synthetic car image generation using Blender (github and paper)
-	Cross-domain compositing: translation of synthetic cars to real-looking cars with preservation of the background using a pretrained diffusion model (github and paper)
-	Video-P2P: translation with consistency in the output frame sequence (github and paper)
-	YOLOv5: object detection (github and colab)
-	FID: generation evaluation metric (github)
-	SSIM: consistency evaluation metric (mathworks and paper)

## Requirements
-	Blender (I have used version 3.4)
-	Python IDE or alternative
-	MATLAB and its Image Processing Toolbox

The synthetic car image generation with Blender, and the evaluation metrics are performed on a Windows 10 device with an Intel Core i7-1260P. To run our model, we used a NVIDIA A100 Tensor Core GPU.

## Run application
To execute the application, the following steps can be followed.

1)	Generation of the synthetic car images (composites), changed to our needs from here:
    a.	Download images with corresponding labels from the KITTI website or use our own data
    b.	Put the images in the “original” folder
    c.	Put the corresponding labels (format: “object_type height width length rotation_x rotation_y rotation_z”) in the tracklets_labels folder as .txt files, you can use         the “tracklet_to_label.m” file for it
    d.	Unzip the zipped blender file from here in the root folder of this project
    e.	You can run the generation with the following command: [/path/to/blender3.4/blender] -b 'kitti.blend' -P 'config.py' -- -ct [car type]
    f.	After running, the composites will be stored in the “composites” folder and the corresponding masks are stored in the “masks” folder

2)	Cross-domain compositing
    a.	For the setup of this model, you can follow the README on this GitHub page
    b.	Put all the related files in the cross-domain-compositing folder
    c.	Run the model with the composites and masks of step 1), you can find my example notebook in this folder
    d.	You can save the outputs in the “cdc_output” folder

3)	Our model (with Video-P2P)
    a.	Follow the README on this GitHub page for the installation of the required packages and the stable diffusion model
    b.	Add them to the “our-model” folder
    c.	Run the model by using a sequence of composites and masks of step 1), you can find my example notebook in this folder
    d.	The outputs will be saved in the “outputs” folder

## Validation
### YOLOv5
To apply the YOLOv5 detection algorithm to the generated images, the notebook "YOLOv5.ipynb" in the “validation” folder can be utilized by opening it in Google Colab. The execution process involves the following steps:

    1)	Start by running the setup section within the notebook
    2)	Proceed to load your images into the "/content/yolov5/data/images" folder
    3)	Finally, execute the detect section to initiate the detection process
    4)	The resulting outputs will be saved in the "runs/detect/exp" folder

### FID
Requires TensorFlow, check this GitHub page for the required packages to be installed. To run the evaluation:

    1)	Navigate to the “precalc_stats_example.py” file in the “validation” folder
    2)	In this file, change the data_path to the folder containing real images of cars
    3)	Change the output_path to the validation folder and run the code
    4)	Navigate to the “fid_example.py” file and change the image_path to the folder containing the composites
    5)	Change the stats_path to the validation folder containing the “fid_stats.npz” file
    6)	Run the python file, the FID score will be printed

### SSIM
Navigate to the “validation” folder, where you can find the “SSIMcalc.m” file. Put the output of our model, the generated sequence of frames, in a folder called “Your_outputs” and run the script. This MATLAB script will return an excel file, with all the SSIM values for the pairs of frames listed in a column, with the last row the mean value.
