import subprocess
import glob
import os

dir_name = os.path.dirname(__file__)
print(dir_name)

images = glob.glob(dir_name + '/Source/*.jpg')

for image in images:
    res_image_path = os.path.join(dir_name, 'Result', os.path.basename(image))
    copy_command = 'cp "{}" "{}"'.format(image, res_image_path)
    conv_command = 'sips --resampleWidth 200 "{}"'.format(res_image_path)
    subprocess.call(copy_command, shell=True)
    if os.path.isfile(res_image_path):
        subprocess.call(conv_command, shell=True)



