# -*- coding: utf-8 -*-
import dicom
from os import listdir
from os.path import isfile, join
from lxml import etree


def parse_xml(xml_files):
    xml_uids = dict()
    for file in xml_files:
        uids = []
        # print(file)
        tp = etree.parse(file)
        root = tp.getroot()
        prefix = root.get("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation")
        if prefix == None:
            continue
        prefix = prefix.split()[0]

        for element in root.iter("{%s}unblindedRead" % prefix, "{%s}unblindedReadNodule" % prefix):
            for subElem in element.iter("{%s}imageSOP_UID" % prefix):
                # print("%s - %s" % (subElem.tag, subElem.text))
                uids.append(subElem.text)
        xml_uids[file] = uids
    return xml_uids


def get_files(root_path):
    dirs = listdir(root_path)
    dcm_files = []
    xml_files =[]
    files_dict = dict()
    for dir in dirs:
        my_path = join(root_path, dir)
        inner_dirs = listdir(my_path)
        i = 0
        for in_dir in inner_dirs:
            file_path = join(my_path, in_dir)
            for d in listdir(file_path):
                if i < 3:
                    i += 1
                    continue
                fp = join(file_path, d)
                xml = None
                print(fp)
                for f in listdir(fp):
                    end_file = join(fp, f)
                    if isfile(end_file):
                        if end_file.endswith(".dcm"):
                            dcm_files.append(end_file)
                        if end_file.endswith(".xml"):
                            xml = end_file
                            xml_files.append(end_file)
                if not xml == None:
                    files_dict[xml] = dcm_files
                dcm_files = []
                i += 1
                # if i > 1:
                #     return files_dict
    return files_dict


def get_dcm_imgs(files):
    dcm_images = []
    for file in files:
        ds = dicom.read_file(file)
        # print(ds.SOPInstanceUID)
        dcm_images.append(ds)
        # print(len(dcm_images))
    return dcm_images


def main():
    root_path = "E:\\Study\\Master\\Canser_images\\DOI"
    files_dict = get_files(root_path)
    print("Files received ", len(files_dict.keys()))
    for xml in files_dict.keys():
        files_dict[xml] = get_dcm_imgs(files_dict[xml])
    print("Images received")
    xml_imgs_uids = parse_xml(files_dict.keys())

    nodule_imgs= []
    nonnodule_imgs = []
    for xml in xml_imgs_uids.keys():
        if xml_imgs_uids.has_key(xml) and files_dict.has_key(xml):
            uids = xml_imgs_uids[xml]
            imgs = files_dict[xml]

            for img in imgs:
                if img.SOPInstanceUID in uids:
                    nodule_imgs.append(img)
                else:
                    nonnodule_imgs.append(img)

    print("Nodule ", len(nodule_imgs))
    print("Nonnodule ", len(nonnodule_imgs))

    nodule_dir_path="D:\\CanserImages\\Nodule"
    nonnodule_dir_path="D:\\CanserImages\\Free"

    for nodule_img in nodule_imgs:
        nodule_img.save_as(join(nodule_dir_path, nodule_img.SOPInstanceUID + '.dcm'))

    print("Nodule images written")

    for nonnodule_img in nonnodule_imgs:
        nonnodule_img.save_as(join(nonnodule_dir_path, nonnodule_img.SOPInstanceUID + '.dcm'))

    print("Free nodule images written")

main()
