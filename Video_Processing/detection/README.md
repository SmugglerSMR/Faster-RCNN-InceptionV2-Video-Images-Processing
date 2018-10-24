

# Faster-RCNN using Inception model (equivalent to Xception)
Code build on top of following examples:
https://github.com/jaspereb/FasterRCNNTutorial/
Model/research link


## Prereqs
You must have:


* installed tensorflow 
* cloned and built the tensorflow/models/research folder into the tensorflow directory, you may not need to run the build files which are included with this. If you get script not found errors from the python commands then try running the various build scripts. (https://github.com/tensorflow/models/tree/master/research) 
* Jupyter notebook (pip install --user jupyter) 
* labelimg https://github.com/tzutalin/labelImg
* ImageMagick cli utilities

## Creating the Dataset and Training
The goal is to take rgb images and create a dataset in the same format as Pascal VOC, this can then be used to create the 'pascal.record' TFRecord files which is used for training.

What we need to create is the following. Start by creating all of the empty folders.

Datasets must have following structures:
~~~
+VOCdevkit
    +VOC2012
        +Annotations
                -A bunch of .xml labels
        +JPEGImages
                -A bunch of .jpg images
        +ImageSets
                +Main
                        -aeroplane_trainval.txt (This is just a list of the jpeg files without file extensions, the train.py script reads this file for all the images it is supposed to include.
                        -trainval.txt (An exact copy of the aeroplane_trainval.txt)

        +trainingConfig.config (training config file similar to https://github.com/tensorflow/models/tree/master/research/object_detection/samples/configs)
~~~

Resize images is to X*600 (See 'How big should my images be?')

~~~
cd .../JPEGImages
for file in $PWD/*.jpg
do
	# convert $file -resize 717x600 $file
	# Using ffmpeg is more effective
	ffmpeg -i $file -vf scale=717:600 $file -y
done
~~~

Optionally, rename them to consecutive numbers to make referencing them easier later on. (note: do not run this command if your images are already labelled 'n.jpg' because it will overwrite some of them

~~~
cd .../JPEGImages
count=1
for file in $PWD/*.jpg
	do
	mv $file $count.jpg
	count=$((count+1))
done
~~~

Important: LabelImg grabs the folder name when writing the xml files and this needs to be VOC2012. We will fix the error that this leads to in the next step.

Run LabelImg. Download a release from https://tzutalin.github.io/labelImg/ then just extract it and run sudo ./labelImg (it segfaults without sudo)

* set autosave on
* set the load and save directories (save should be .../Annotations, load is .../JPEGImages)
* set the default classname to something easy to remember
* press d to move to the next image
* press w to add a box
* Label all examples of the relevant classes in the dataset

From the Annotations dir run
~~~
for file in $PWD/*.xml
	do sed -i 's/>JPEGImages</>VOC2012</g' $file
done
Cd to the JPEGImages dir and run the command
~~~

For use in Lyra directory
~~~
for file in $PWD/*.xml
	do sed -i 's/>JPEGImages</>VOC2012</g' $file
done
~~~

Create trainvalue text set
~~~
ls | grep .jpg | sed "s/.jpg//g" > aeroplane_trainval.txt
cp aeroplane_trainval.txt trainval.txt
mv *.txt ../ImageSets/Main/
~~~
The Pascal VOC type dataset should now be all created. If you messed up any of the folder structure, you will need to change the XML file contents. If you rename any of the JPEG files you will need to change both the aeroplane_trainval.txt and XML file contents.

Best way to save memory is usage os symbolink links. You have to create following two links.
~~~
ln -s ../../object_detection object_detection
ln -s ../../slim slim
~~~

Open bash in models/research and run the following command 'python object_detection/create_pascal_record.py -h' follow the help instructions to create a pascal.record and file from the dataset.

It should look something like this, stf here stands for serrated tussock full-size. You will need to create an output folder (anywhere you like), also use the --set=trainval option.



For my machine
~~~
export PYTHONPATH=$(pwd):$(pwd)/slim

python object_detection/dataset_tools/create_pascal_tf_record.py --data_dir=VOCdevkit --year=VOC2012 --output_path=pascal.record --label_map_path=label.pbtxt --set=trainval
~~~


Download and extract a tensorflow model to use as the training checkpoint, see 'Which model do I use?'.

Set up the model config file, this will be similar to 'faster_rcnn_resnet101_coco.config' which is in /models/research/object_detection/samples/configs'. Copy the relevant one for the model you are using and edit it. You will need to change approximately 5 directories, the rest should be set up correctly. 
Once the two record files have been created check they are > 0 bytes. Then run the script (from .../models/research/) 'python object_detection/train.py -h' and follow the help instructions to train the model. Create an output folder (train_dir) for your model checkpoints to go in.

It should look something like this. Also see 'Which model do I use?'
for my machine

Edit paths in checkpoint to local placem without full path.
Delete all checkpints, graphs and pipeline, if they present.

~~~
python object_detection/legacy/train.py --train_dir=train --pipeline_config_path=faster_rcnn_inception_v2_coco.config
~~~

You can open tensorboard at this point using the following. Generally if the loss in the bash output from the train.py script is dropping, then training is working fine. How long to train for is something you will need to experiment with. Training on 7 serrated tussock images was accurate after about an hour with loss around 0.02, many more images and a longer training time could improve the accuracy. (Click on the link that tensorboard creates to open it in a browser).
~~~
tensorboard --logdir=train
~~~

Let the model train!

Hit CTRL-C when you're happy with the loss value, checkpoints are periodically saved to the train_dir folder
You now have a trained model, the next step is to test it. The easiest way to do this is to use the jupyter notebook provided in the /models/research/object_detection folder.
From the /models/research folder run the following. You must have created the output folder.
My PC

Instead model.ckpt-2540 to whatever model step is created.


## Please move here for testing performance
Use environment of tensorflow
~~~
source activate tensorflow
~~~
Run this if you haven't before: export PYTHONPATH=$(pwd):$(pwd)/slim

set PYTHONPATH=D:\QUT\egh455\assgn2\Lyra\EGH455_Group3_Project\Video_Processing\detection\object_detection;D:\QUT\egh455\assgn2\Lyra\EGH455_Group3_Project\Video_Processing\detection\object_detection\slim

~~~
# Remove directory
rm -R output/

# Create graph
python object_detection/export_inference_graph.py --input_type=image_tensor --pipeline_config_path=faster_rcnn_inception_v2_coco.config --trained_checkpoint_prefix=train/model.ckpt-20886 --output_directory=output
~~~


Create a 'test' directory and copy over some images which have not been used for training. 
Please run jupyter notebook and run eh+FRCNN section. RUn all of them one by one. As far as I am aware, I resolved all warning and issues.
Do not run last section of the code. Output not ready.

Create video directory using symbolinc link
~~~
ln -s ../../video video
~~~
