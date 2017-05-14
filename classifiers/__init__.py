# -*- coding: utf-8 -*-
import dicom
from os import listdir
from os.path import isfile, join
from lxml import etree


def parse_xml(xml_files):
    uids = []
    for file in xml_files:
        # print(file)
        tp = etree.parse(file) # Парсинг файла
        root = tp.getroot()
        prefix = root.get("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation")
        prefix = prefix.split()[0]

        for element in root.iter("{%s}unblindedRead" % prefix, "{%s}unblindedReadNodule" % prefix):
            for subElem in element.iter("{%s}imageSOP_UID" % prefix):
                # print("%s - %s" % (subElem.tag, subElem.text))
                uids.append(subElem.text)
    return uids


def get_files(root_path):
    dirs = listdir(root_path)
    dcm_files = []
    xml_files =[]
    for dir in dirs:
        my_path = join(root_path, dir)
        inner_dirs = listdir(my_path)
        i = 0
        for in_dir in inner_dirs:
            file_path = join(my_path, in_dir)
            for d in listdir(file_path):
                fp = join(file_path, d)
                for f in listdir(fp):
                    end_file = join(fp, f)
                    if isfile(end_file):
                        if end_file.endswith(".dcm"):
                            dcm_files.append(end_file)
                        if end_file.endswith(".xml"):
                            xml_files.append(end_file)
                i += 1
                if i > 2:
                    return dcm_files, xml_files
    return dcm_files, xml_files


def get_dcm_imgs(files):
    dcm_images = []
    for file in files:
        ds = dicom.read_file(file)
        # print(ds.SOPInstanceUID)
        dcm_images.append(ds)
        # print(len(dcm_images))
    return dcm_images


root_path = "E:\\Study\\Master\\Canser_images\\DOI"
dcms, xmls = get_files("E:\\Study\\Master\\Canser_images\\DOI")
print("Files received ", len(dcms), len(xmls))
imgs = get_dcm_imgs(dcms)
print("Images recived")
imgs_uids = parse_xml(xmls)

nodule_imgs= []
nonnodule_imgs = []
for img in imgs:

    if img.SOPInstanceUID in imgs_uids:
        nodule_imgs.append(img)
    else:
        nonnodule_imgs.append(img)

print("Nodule ", len(nodule_imgs))
print("Nonnodule ", len(nonnodule_imgs))
