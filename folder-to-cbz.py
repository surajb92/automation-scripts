import argparse
import os
import zipfile

EXTENSIONS=['.jpg','.JPG','.jpeg','.JPEG','.png','.PNG','.webp','.WEBP']

def get_images(base, E):
    file_list={}
    for root,directories,filenames in os.walk(base):
        print(root,directories,filenames)
        # something can be done here to sort?
        for filename in filenames:
            if any(ext in filename for ext in E):
                if root not in file_list:
                    file_list[root]=[os.path.join(root,filename)]
                else:
                    file_list[root].append(os.path.join(root,filename))
    return file_list

parser = argparse.ArgumentParser(
    prog="folder-to-cbz",
    description="Converts a folder full of images into a CBZ archive",
    epilog="Author : Suraj B" # optional
)

parser.add_argument("path",help="Path of folder to archive")
parser.add_argument("-d","--delete",action="store_true",default=False,help="Deletes the original folder after archiving is complete.")
#parser.add_argument("-s","--single",action="store_true",default=False,help="Puts all images into a single file, regardless of sub-directories.")
args=parser.parse_args()
folder=args.path
delete=args.delete
#single=args.single
#print(folder,delete)

# image_list = get_images(folder,EXTENSIONS)
image_list = dict(reversed(list(get_images(folder,EXTENSIONS).items())))
# Reverse order because need to delete inner files first

#print(*image_list,sep='\n')
#for i in image_list:
#    print(*image_list[i],sep='\n')
 
for i in image_list:
    print(os.path.dirname(i))
    foldr = os.path.basename(os.path.normpath(i))
    with zipfile.ZipFile(f"{os.path.dirname(os.path.dirname(i))}/{foldr}.cbz",'w') as myzip:
        for j in image_list[i]:
            myzip.write(j,os.path.basename(os.path.normpath(j)))
            if delete:
                os.remove(j)

# if non image formats found, set delete to false (maybe error msg)? or just delete the image files?

# Note : In case of nested file structure, create archive of cbz files?

