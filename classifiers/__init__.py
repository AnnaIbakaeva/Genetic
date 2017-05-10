# -*- coding: utf-8 -*-
import dicom

# ds = dicom.read_dicomdir("E:\\Study\\Master\\Canser_images\\DOI\\LIDC-IDRI-0001\\"
#                           "1.3.6.1.4.1.14519.5.2.1.6279.6001.175012972118199124641098335511\\"
#                           "1.3.6.1.4.1.14519.5.2.1.6279.6001.141365756818074696859567662357\\")
# print(ds)
ds = dicom.read_file("E:\\Study\\Master\\Canser_images\\DOI\\LIDC-IDRI-0001\\"
                          "1.3.6.1.4.1.14519.5.2.1.6279.6001.175012972118199124641098335511\\"
                          "1.3.6.1.4.1.14519.5.2.1.6279.6001.141365756818074696859567662357\\000001.dcm")
print(ds)
print(ds.SOPInstanceUID)