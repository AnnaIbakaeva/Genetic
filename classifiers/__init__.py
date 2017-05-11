# -*- coding: utf-8 -*-
import dicom
from os import listdir
from os.path import isfile, join
from lxml import etree


def parse_xml(xml_files):
    for file in xml_files:
        tp = etree.parse(file) # Парсинг файла
        for record in tp.xpath('//CXRreadingSession'):
            print record.xpath("./@tag")[0]
            for x in record.xpath("./subfield/text()"):
                print "\t", x
        # nodes = tp.xpath('/soft/os/item') # Открываем раздел
        # for node in nodes: # Перебираем элементы
        #     print node.tag,node.keys(),node.values()
        #     print 'name =',node.get('name') # Выводим параметр name
        #     print 'text =',[node.text] # Выводим текст элемента


def get_files(root_path):
    dirs = listdir(root_path)
    dcm_files = []
    xml_files =[]
    for dir in dirs:
        my_path = join(root_path, dir)
        inner_dirs = listdir(my_path)
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
                    if len(dcm_files) > 100000:
                        break
    return dcm_files, xml_files


def get_dcm_imgs(files):
    dcm_images = []
    for file in files:
        ds = dicom.read_file(file)
        dcm_images.append(ds)
    return dcm_images


# root_path = "E:\\Study\\Master\\Canser_images\\DOI"
# dcms, xmls = get_files("E:\\Study\\Master\\Canser_images\\DOI")
# imgs = get_dcm_imgs(dcms)

parse_xml(["E:\\Study\\Master\\Canser_images\\DOI\\LIDC-IDRI-0001\\"
           "1.3.6.1.4.1.14519.5.2.1.6279.6001.175012972118199124641098335511\\"
           "1.3.6.1.4.1.14519.5.2.1.6279.6001.141365756818074696859567662357\\068.xml"])
