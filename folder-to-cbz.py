import argparse
import os
import zipfile

EXTENSIONS=['.jpg','.JPG','.jpeg','.JPEG','.png','.PNG','.webp','.WEBP']

def get_images(base, E):
    file_list={}
    for root,directories,filenames in os.walk(base):
        for filename in filenames:
            if any(ext in filename for ext in E):
                r=os.path.normpath(root)
                if r not in file_list:
                    file_list[r]=[os.path.join(r,filename)]
                else:
                    file_list[r].append(os.path.join(r,filename))
    return file_list

parser = argparse.ArgumentParser(
    prog="folder-to-cbz",
    description="Converts a folder full of images into a CBZ archive",
    epilog="Author : Suraj B" # optional
)

parser.add_argument("path",help="Path of folder to archive")
parser.add_argument("-d","--delete",action="store_true",default=False,
help="Deletes the original files (and the folder if it's empty) after archiving is complete.")
args=parser.parse_args()
folder=args.path
delete=args.delete

# Reverse order because need to delete inner files first
image_list = dict(reversed(list(get_images(folder,EXTENSIONS).items())))

def main():
    for i in image_list:
        folder_name = os.path.basename(i)
        parent = os.path.dirname(i)
        with zipfile.ZipFile(f"{parent}/{folder_name}.cbz",'w') as myzip:
            for j in image_list[i]:
                myzip.write(j,os.path.basename(os.path.normpath(j)))
                if delete:
                    os.remove(j)
        fol = f"{parent}/{folder_name}"
        if delete:
            try:
                os.rmdir(fol)
            except OSError:
                print("Directory "+fol+" is not empty, so not deleted.")

if __name__=="__main__":
    main()
