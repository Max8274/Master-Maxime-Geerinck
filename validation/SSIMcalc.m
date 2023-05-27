% Specify the number of iterations
numIterations = 6;  % Adjust this according to number of images

% Initialize the array to store the SSIM scores
ssimScores = zeros(numIterations, 1);

% Specify the Excel file path and name
filePath = './SSIM_out.xlsx';

% Specify the folder path where you want to save the figure
folderPath = './SSIM_images';

for i= 1:numIterations
    % Read the next two images and masks using appropriate filenames
    Icur = imread(sprintf('Your_outputs\\000000000%d.png', i-1));
    Inext = imread(sprintf('Your_outputs\\000000000%d.png', i));
    maskIcur = imread(sprintf('Masks\\000000000%d.png', i-1));
    maskInext = imread(sprintf('Masks\\000000000%d.png', i));
    
    maskIcur = im2gray(maskIcur);
    maskIcur = imbinarize(maskIcur);
    maskInext = im2gray(maskInext);
    maskInext = imbinarize(maskInext);
    
    greyIcur = im2gray(Icur);
    greyInext = im2gray(Inext);
    
    maskIcur = imresize(maskIcur, size(greyIcur));
    maskInext = imresize(maskInext, size(greyInext));
    
    greyIcur = im2double(greyIcur);
    maskedIcur = greyIcur.*maskIcur;
    greyInext = im2double(greyInext);
    maskedInext = greyInext.*maskInext;
    
    % Draw bounding box
    stats = regionprops(maskIcur, 'BoundingBox');
    boundingBoxIcur = round(stats.BoundingBox);
    stats = regionprops(maskInext, 'BoundingBox');
    boundingBoxInext = round(stats.BoundingBox);
    
    % Crop the masked images to remove black pixels around the car
    maskedIcur = imcrop(maskedIcur, boundingBoxIcur);
    maskedInext = imcrop(maskedInext, boundingBoxInext);
    
    % Resize the cropped images to the same size
    maxSize = max(size(maskedIcur), size(maskedInext));
    maskedIcur = imresize(maskedIcur, maxSize);
    maskedInext = imresize(maskedInext, maxSize);
    
    % Create a new figure handle without displaying it
    h = figure('Visible', 'off');

    montage({maskedIcur,maskedInext})
    
    % Specify the filename with the desired format (e.g., 'figure.png')
    fileName = sprintf('Our-model-%d.png', i-1);
    
    % Save the figure in the specified folder
    saveas(h, fullfile(folderPath, fileName));

    % Close the figure handle
    close(h);
    
    ssimScore = multissim(maskedIcur, maskedInext);

    ssimScores(i) = ssimScore;
end
ssimScores(numIterations + 1) = mean(ssimScores);

% Write the value to the specified cell in the Excel file
writematrix(ssimScores, filePath, 'Sheet', 1, 'Range', 'B1:B9');
