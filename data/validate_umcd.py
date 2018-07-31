import os
import glob
import filecmp

def nkirock(file):
    return os.path.join('NKI_Rockland', file)

def hagmann(file):
    return os.path.join('Hagmann_PLoSBiol_2008', file)

DUPLICATE_INFO = [
    (nkirock('NKI_dti_avg_region_names_abbrev_file.txt'),
     glob.glob(nkirock('*_DTI_region_names_abbrev_file.txt'))),
    (nkirock('NKI_dti_avg_region_xyz_centers_file.txt'),
     glob.glob(nkirock('*_DTI_region_xyz_centers_file.txt'))),
    # NOTE: the full names are not equal everywhere. Weird... See below.
    # (nkirock('NKI_dti_avg_region_names_full_file.txt'),
    #  glob.glob(nkirock('*_DTI_region_names_full_file.txt'))),
    (hagmann('group_mean_region_names_abbrev_file.txt'),
     glob.glob(hagmann('subj*_region_names_abbrev_file.txt'))),
    (hagmann('group_mean_region_names_full_file.txt'),
     glob.glob(hagmann('subj*_region_names_full_file.txt'))),
    (hagmann('group_mean_region_xyz_centers_file.txt'),
     glob.glob(hagmann('subj*_region_xyz_centers_file.txt'))),
]

for original, duplicates in DUPLICATE_INFO:
    for duplicate in duplicates:
        print('comparing', original, duplicate)
        assert filecmp.cmp(original, duplicate, shallow=False)

# {'0216672b4fbec70c5652265e7eb76474': ['',
#                                       '1793622_DTI_region_names_full_file.txt',
#                                       '2328270_DTI_region_names_full_file.txt',
#                                       '2864064_DTI_region_names_full_file.txt',
#                                       '3431295_DTI_region_names_full_file.txt',
#                                       '3927656_DTI_region_names_full_file.txt',
#                                       '4487215_DTI_region_names_full_file.txt',
#                                       '9630905_DTI_region_names_full_file.txt'],
#  '02c3a4c164350e310ad701efa9845197': ['1150497_DTI_region_names_full_file.txt',
#                                       '1534265_DTI_region_names_full_file.txt',
#                                       '2071045_DTI_region_names_full_file.txt',
#                                       '2589215_DTI_region_names_full_file.txt',
#                                       '3261820_DTI_region_names_full_file.txt',
#                                       '3795193_DTI_region_names_full_file.txt',
#                                       '4126393_DTI_region_names_full_file.txt',
#                                       '7055197_DTI_region_names_full_file.txt'],
#  '0ac2930545878275c96c493fab922bed': ['1143655_DTI_region_names_full_file.txt',
#                                       '1525492_DTI_region_names_full_file.txt',
#                                       '2041109_DTI_region_names_full_file.txt',
#                                       '2531270_DTI_region_names_full_file.txt',
#                                       '3209959_DTI_region_names_full_file.txt',
#                                       '3773269_DTI_region_names_full_file.txt',
#                                       '4119751_DTI_region_names_full_file.txt',
#                                       '6913939_DTI_region_names_full_file.txt'],
#  '1e036a4c55d9980ccc67c0d8caa1a38a': ['1292527_DTI_region_names_full_file.txt',
#                                       '1753435_DTI_region_names_full_file.txt',
#                                       '2248813_DTI_region_names_full_file.txt',
#                                       '2784584_DTI_region_names_full_file.txt',
#                                       '3362208_DTI_region_names_full_file.txt',
#                                       '3875444_DTI_region_names_full_file.txt',
#                                       '4288245_DTI_region_names_full_file.txt',
#                                       '9100911_DTI_region_names_full_file.txt'],
#  '225291cb07aa864780ef60c17c7172a4': ['1125244_DTI_region_names_full_file.txt',
#                                       '1523112_DTI_region_names_full_file.txt',
#                                       '2021454_DTI_region_names_full_file.txt',
#                                       '2524225_DTI_region_names_full_file.txt',
#                                       '3166395_DTI_region_names_full_file.txt',
#                                       '3755111_DTI_region_names_full_file.txt',
#                                       '4100790_DTI_region_names_full_file.txt',
#                                       '6709880_DTI_region_names_full_file.txt'],
#  '2f2c2feffc8f500242fda51791737524': ['1271401_DTI_region_names_full_file.txt',
#                                       '1713513_DTI_region_names_full_file.txt',
#                                       '2166659_DTI_region_names_full_file.txt',
#                                       '2675807_DTI_region_names_full_file.txt',
#                                       '3328556_DTI_region_names_full_file.txt',
#                                       '3815065_DTI_region_names_full_file.txt',
#                                       '4188346_DTI_region_names_full_file.txt',
#                                       '8691891_DTI_region_names_full_file.txt'],
#  '30879fe30e5b70f6e2d50043cab9311f': ['1438912_DTI_region_names_full_file.txt',
#                                       '1935851_DTI_region_names_full_file.txt',
#                                       '2465771_DTI_region_names_full_file.txt',
#                                       '2986140_DTI_region_names_full_file.txt',
#                                       '3594255_DTI_region_names_full_file.txt',
#                                       '4015919_DTI_region_names_full_file.txt',
#                                       '5279162_DTI_region_names_full_file.txt'],
#  '3a4f7a967a02dd7c8cf358c38626ebcc': ['1445797_DTI_region_names_full_file.txt',
#                                       '1940084_DTI_region_names_full_file.txt',
#                                       '2475376_DTI_region_names_full_file.txt',
#                                       '3033715_DTI_region_names_full_file.txt',
#                                       '3606220_DTI_region_names_full_file.txt',
#                                       '4026825_DTI_region_names_full_file.txt',
#                                       '5461463_DTI_region_names_full_file.txt'],
#  '444781da83109a431f9335375af99426': ['1034049_DTI_region_names_full_file.txt',
#                                       '1494230_DTI_region_names_full_file.txt',
#                                       '1961098_DTI_region_names_full_file.txt',
#                                       '2494762_DTI_region_names_full_file.txt',
#                                       '3081896_DTI_region_names_full_file.txt',
#                                       '3695138_DTI_region_names_full_file.txt',
#                                       '4087509_DTI_region_names_full_file.txt',
#                                       '6471972_DTI_region_names_full_file.txt'],
#  '4dae9c814eaef9206df90e1a401f61b2': ['1103722_DTI_region_names_full_file.txt',
#                                       '1522653_DTI_region_names_full_file.txt',
#                                       '2009256_DTI_region_names_full_file.txt',
#                                       '2513310_DTI_region_names_full_file.txt',
#                                       '3106263_DTI_region_names_full_file.txt',
#                                       '3729976_DTI_region_names_full_file.txt',
#                                       '4099085_DTI_region_names_full_file.txt',
#                                       '6692978_DTI_region_names_full_file.txt'],
#  '5ea44b101b2bc7ea1732fd31b9fc4f09': ['9780496_DTI_region_names_full_file.txt'],
#  '67099174c8a0b271093f3239f4717755': ['1339484_DTI_region_names_full_file.txt',
#                                       '1834799_DTI_region_names_full_file.txt',
#                                       '2357976_DTI_region_names_full_file.txt',
#                                       '2868630_DTI_region_names_full_file.txt',
#                                       '3431940_DTI_region_names_full_file.txt',
#                                       '3934325_DTI_region_names_full_file.txt',
#                                       '4710111_DTI_region_names_full_file.txt',
#                                       '9645370_DTI_region_names_full_file.txt'],
#  '738f301ef31f88716b5b027c10efbaae': ['1013090_DTI_region_names_full_file.txt',
#                                       '1476437_DTI_region_names_full_file.txt',
#                                       '1943306_DTI_region_names_full_file.txt',
#                                       '2483617_DTI_region_names_full_file.txt',
#                                       '3070385_DTI_region_names_full_file.txt',
#                                       '3611212_DTI_region_names_full_file.txt',
#                                       '4077433_DTI_region_names_full_file.txt',
#                                       '5844518_DTI_region_names_full_file.txt'],
#  '752099b574bccf0e3497c20d285c2861': ['1192435_DTI_region_names_full_file.txt',
#                                       '1591238_DTI_region_names_full_file.txt',
#                                       '2113846_DTI_region_names_full_file.txt',
#                                       '2631208_DTI_region_names_full_file.txt',
#                                       '3304648_DTI_region_names_full_file.txt',
#                                       '3804254_DTI_region_names_full_file.txt',
#                                       '4143704_DTI_region_names_full_file.txt',
#                                       '7212617_DTI_region_names_full_file.txt'],
#  '84b4aecb607da194fb948db89592e5ec': ['1427581_DTI_region_names_full_file.txt',
#                                       '1931386_DTI_region_names_full_file.txt',
#                                       '2457957_DTI_region_names_full_file.txt',
#                                       '2970212_DTI_region_names_full_file.txt',
#                                       '3566919_DTI_region_names_full_file.txt',
#                                       '4006955_DTI_region_names_full_file.txt',
#                                       '5205221_DTI_region_names_full_file.txt'],
#  '8f434acbfa0c862135bc0c73bd421225': ['1382333_DTI_region_names_full_file.txt',
#                                       '1903493_DTI_region_names_full_file.txt',
#                                       '2436415_DTI_region_names_full_file.txt',
#                                       '2967284_DTI_region_names_full_file.txt',
#                                       '3492484_DTI_region_names_full_file.txt',
#                                       '3989122_DTI_region_names_full_file.txt',
#                                       '5161117_DTI_region_names_full_file.txt'],
#  '94641e16e3849ea921480551d4342c4c': ['1309257_DTI_region_names_full_file.txt',
#                                       '1757866_DTI_region_names_full_file.txt',
#                                       '2258252_DTI_region_names_full_file.txt',
#                                       '2788776_DTI_region_names_full_file.txt',
#                                       '3366302_DTI_region_names_full_file.txt',
#                                       '3893245_DTI_region_names_full_file.txt',
#                                       '4290056_DTI_region_names_full_file.txt',
#                                       '9421819_DTI_region_names_full_file.txt'],
#  'a57cabe4e183c3aee4a3ae6c686c2875': ['1351931_DTI_region_names_full_file.txt',
#                                       '1875434_DTI_region_names_full_file.txt',
#                                       '2362594_DTI_region_names_full_file.txt',
#                                       '2882334_DTI_region_names_full_file.txt',
#                                       '3466763_DTI_region_names_full_file.txt',
#                                       '3951328_DTI_region_names_full_file.txt',
#                                       '4791943_DTI_region_names_full_file.txt',
#                                       '9716792_DTI_region_names_full_file.txt'],
#  'a6b478c0b54165754bfd77f904d37a97': ['1334556_DTI_region_names_full_file.txt',
#                                       '1781836_DTI_region_names_full_file.txt',
#                                       '2286816_DTI_region_names_full_file.txt',
#                                       '2861923_DTI_region_names_full_file.txt',
#                                       '3409284_DTI_region_names_full_file.txt',
#                                       '3911767_DTI_region_names_full_file.txt',
#                                       '4417007_DTI_region_names_full_file.txt',
#                                       '9537916_DTI_region_names_full_file.txt'],
#  'a7f1ef522828fe36e7c84b8e6cff1fe4': ['1288657_DTI_region_names_full_file.txt',
#                                       '1742775_DTI_region_names_full_file.txt',
#                                       '2221971_DTI_region_names_full_file.txt',
#                                       '2731081_DTI_region_names_full_file.txt',
#                                       '3346545_DTI_region_names_full_file.txt',
#                                       '3848143_DTI_region_names_full_file.txt',
#                                       '4277600_DTI_region_names_full_file.txt',
#                                       '9006154_DTI_region_names_full_file.txt'],
#  'b4881c2fea326158559d696b59a2ae5e': ['1097782_DTI_region_names_full_file.txt',
#                                       '1508861_DTI_region_names_full_file.txt',
#                                       '2005303_DTI_region_names_full_file.txt',
#                                       '2505567_DTI_region_names_full_file.txt',
#                                       '3094481_DTI_region_names_full_file.txt',
#                                       '3701005_DTI_region_names_full_file.txt',
#                                       '4089896_DTI_region_names_full_file.txt',
#                                       '6539040_DTI_region_names_full_file.txt'],
#  'b6fe0505dc981ba5b965a693d6c9d05a': ['1285465_DTI_region_names_full_file.txt',
#                                       '1734822_DTI_region_names_full_file.txt',
#                                       '2176073_DTI_region_names_full_file.txt',
#                                       '2678751_DTI_region_names_full_file.txt',
#                                       '3329569_DTI_region_names_full_file.txt',
#                                       '3827479_DTI_region_names_full_file.txt',
#                                       '4230470_DTI_region_names_full_file.txt',
#                                       '8735778_DTI_region_names_full_file.txt'],
#  'c23520cd49f6182df363a764a44d28d6': ['1264721_DTI_region_names_full_file.txt',
#                                       '1709141_DTI_region_names_full_file.txt',
#                                       '2160826_DTI_region_names_full_file.txt',
#                                       '2674565_DTI_region_names_full_file.txt',
#                                       '3315657_DTI_region_names_full_file.txt',
#                                       '3811036_DTI_region_names_full_file.txt',
#                                       '4176156_DTI_region_names_full_file.txt',
#                                       '8628499_DTI_region_names_full_file.txt'],
#  'd15fb0227d99db0d111a9185047c5464': ['1366839_DTI_region_names_full_file.txt',
#                                       '1898228_DTI_region_names_full_file.txt',
#                                       '2403029_DTI_region_names_full_file.txt',
#                                       '2915821_DTI_region_names_full_file.txt',
#                                       '3486362_DTI_region_names_full_file.txt',
#                                       '3965194_DTI_region_names_full_file.txt',
#                                       '5108043_DTI_region_names_full_file.txt'],
#  'e613fb960b086d320351eae43f88347a': ['1216620_DTI_region_names_full_file.txt',
#                                       '1654606_DTI_region_names_full_file.txt',
#                                       '2132437_DTI_region_names_full_file.txt',
#                                       '2652676_DTI_region_names_full_file.txt',
#                                       '3313349_DTI_region_names_full_file.txt',
#                                       '3808535_DTI_region_names_full_file.txt',
#                                       '4154799_DTI_region_names_full_file.txt',
#                                       '8574662_DTI_region_names_full_file.txt'],
#  'fec3b16a3de5f553651afa88fa319828': ['1322220_DTI_region_names_full_file.txt',
#                                       '1764982_DTI_region_names_full_file.txt',
#                                       '2286053_DTI_region_names_full_file.txt',
#                                       '2799329_DTI_region_names_full_file.txt',
#                                       '3374719_DTI_region_names_full_file.txt',
#                                       '3895064_DTI_region_names_full_file.txt',
#                                       '4323037_DTI_region_names_full_file.txt',
#                                       '9536886_DTI_region_names_full_file.txt']}