# coding=utf-8
import glob
import os
import re

#***************************************************************************

imageSet = glob.glob('hjclass/Resources/images.xcassets/*/*.imageset')
imageOrigin = glob.glob('hjclass/Resources/Images/*/*.png')

ignores = {r'image_\d+'}

sourcePath = '/Users/hj/git_project/HJNetworkSchool/hjclass'

#***************************************************************************

def findUnusedResource(imageFolder):
    img_names = [os.path.basename(pic)[:-9] for pic in imageFolder]
    unused_imgs = []
    for i in range(0, len(imageFolder)):
        pic_name = img_names[i]

        if ignoreFile(pic_name):
            print 'ignore file:%s' (imageFolder[i])
            continue
        result = checkContentFromFolder(pic_name,sourcePath)
        if not result:
            unused_imgs.append(imageFolder[i])
            print 'remove %s' % (imageFolder[i])
            #os.system('rm -rf %s' % (images[i]))


    text_path = 'unused.log'
    tex = '\n'.join(sorted(unused_imgs))
    os.system('echo "%s" > %s' % (tex, text_path))
    print 'Unused res:%d' % (len(unused_imgs))
    print 'Done!'

def checkContentFromFolder(content,folder):

    for dname, dirs, files in os.walk(folder):

        for fname in files:
            fpath = os.path.join(dname, fname)

            with open(fpath,'r') as f:
                s = f.read()
                if content in s:
                    return True

    return False

def ignoreFile(str):
    for ignore in ignores:
        if re.match(ignore, str):
            return True
    return False


if __name__ == '__main__':

    findUnusedResource(imageSet)
    #find_un_used(imageOrigin)
