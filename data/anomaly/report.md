# Bao cao quet bat thuong thanh phan -- top 30 trinh tu lech nhat

Nguon: `data/anomaly/outliers.tsv` -- 14003 trinh tu duoc xet, 116 trinh tu bi danh dau >= 1 co, hien 30 dong dau (sap theo n_flags roi kmer_js giam dan).

## CANH BAO BAT BUOC -- doc truoc khi dien `giai_thich_kha_di`

**Moi ket qua trong bao cao nay la TIN HIEU CAN KIEM TIEP, khong phai KET LUAN.**
Mot trinh tu bi danh dau bat thuong thanh phan CHUA chung minh no den tu
ngoai Trai Dat hay khong thuoc dong doi to tien -- no chi co nghia la thanh
phan (GC/GC3, codon, hoac 4-mer) cua trinh tu do khac ho so nen cua bo CDS
chao mao hon nguong thong ke da chon (`--z`).

Thu tu kha nang giai thich BAT BUOC phai kiem theo dung thu tu sau day (chi
chuyen sang muc tiep theo SAU KHI da loai duoc muc truoc):

1. **Loi lap rap hoac nhiem ban mau** (assembly error / sample contamination)
   -- kha nang PHO BIEN NHAT cho 1 outlier don le trong 1 ban lap rap muc do
   scaffold (N50 thap).
2. **Vung lap / transposon** (repeat region / transposable element) -- cac
   yeu to lap thuong tu mang thanh phan/pho k-mer khac han gene ma hoa binh
   thuong.
3. **HGT (chuyen gene ngang) tu vi khuan, virus, hoac sinh vat cong sinh** --
   day la hien tuong DA DUOC GHI NHAN o nhieu loai (khong phai gia thuyet
   moi la), va la kha nang ĐUOC XEP CUOI trong 3 kha nang "thong thuong".
4. Chi khi da loai het (1)-(3) moi ban toi kha nang khac. Bang nay KHONG TU
   DONG loai duoc bat ky muc nao trong 4 muc tren -- nguoi doc phai tu kiem.

**Buoc kiem bat buoc tiep theo (CHUA lam trong du an nay):** so sanh tung
trinh tu bi danh dau voi co so du lieu protein toan cau bang BLAST hoac
DIAMOND (vd so voi nr/UniProt). Trinh tu khop manh voi protein vi khuan/virus
va KHONG khop protein chim khac -> ung ho (3); nam trong vung da biet la
transposon/lap -> ung ho (2); chi xuat hien o scaffold ngan/do phu thap ->
uu tien xem xet (1) truoc.

Gioi han phuong phap (xem `pipeline/p04_anomaly/README.md`): cach nay KHONG
phat hien duoc doan da bi "dong hoa" thanh phan qua thoi gian tien hoa, va
CHUA doi chieu voi bat ky co so du lieu protein/nucleotide ben ngoai nao.

| seq_id | gene | len | gc | gc3 | z_gc | z_gc3 | codon_dist | kmer_js | n_flags | giai_thich_kha_di |
|---|---|---|---|---|---|---|---|---|---|---|
| lcl|VWYP01016623.1_cds_PYCJOC_R11308_7048 |  | 393 | 0.549618 | 0.587786 | 0.324996 | -0.121065 | 28.5322 | 0.770938 | 2 |  |
| lcl|VWYP01009442.1_cds_PYCJOC_R03555_3930 |  | 549 | 0.590164 | 0.579235 | 0.822621 | -0.171224 | 28.6106 | 0.742681 | 2 |  |
| lcl|VWYP01030967.1_cds_NXR82990.1_13537 | Magel2_1 | 333 | 0.60961 | 0.486486 | 1.06128 | -0.715269 | 37.4162 | 0.718692 | 2 |  |
| lcl|VWYP01039349.1_cds_PYCJOC_R01204_15365 |  | 408 | 0.580882 | 0.544118 | 0.708702 | -0.377212 | 27.5584 | 0.689566 | 2 |  |
| lcl|VWYP01019278.1_cds_PYCJOC_R08639_8354 |  | 378 | 0.486772 | 0.706349 | -0.44632 | 0.574399 | 27.1631 | 0.670617 | 2 |  |
| lcl|VWYP01010121.1_cds_PYCJOC_R10112_4203 |  | 342 | 0.571848 | 0.557522 | 0.597827 | -0.298587 | 27.5632 | 0.659624 | 2 |  |
| lcl|VWYP01014950.1_cds_NXR76581.1_6354 | Stat2 | 330 | 0.709091 | 0.745455 | 2.28222 | 0.803787 | 25.5792 | 0.649728 | 2 |  |
| lcl|VWYP01031815.1_cds_PYCJOC_R09778_13877 |  | 324 | 0.641975 | 0.62037 | 1.4585 | 0.0700654 | 21.5233 | 0.626063 | 2 |  |
| lcl|VWYP01018296.1_cds_PYCJOC_R03188_7915 |  | 498 | 0.554217 | 0.524096 | 0.38144 | -0.494657 | 31.2467 | 0.615519 | 2 |  |
| lcl|VWYP01013929.1_cds_PYCJOC_R00947_5949 |  | 501 | 0.568 | 0.542169 | 0.5506 | -0.388645 | 25.2793 | 0.608003 | 2 |  |
| lcl|VWYP01025487.1_cds_PYCJOC_R06151_11090 |  | 444 | 0.47973 | 0.5 | -0.532747 | -0.635999 | 28.3809 | 0.607649 | 2 |  |
| lcl|VWYP01029494.1_cds_PYCJOC_R11435_12860 |  | 396 | 0.585859 | 0.507576 | 0.769785 | -0.59156 | 21.7852 | 0.590221 | 2 |  |
| lcl|VWYP01026583.1_cds_PYCJOC_R08355_11479 |  | 663 | 0.456193 | 0.427273 | -0.821619 | -1.0626 | 18.8509 | 0.584142 | 2 |  |
| lcl|VWYP01005577.1_cds_NXR72994.1_2359 | Enpp | 342 | 0.649123 | 0.578947 | 1.54623 | -0.172913 | 23.6413 | 0.572157 | 2 |  |
| lcl|VWYP01021598.1_cds_NXR79288.1_9370 | Znf728 | 831 | 0.648616 | 0.595668 | 1.54001 | -0.0748312 | 21.3679 | 0.562777 | 2 |  |
| lcl|VWYP01016255.1_cds_PYCJOC_R05447_6846 |  | 609 | 0.509868 | 0.490099 | -0.16286 | -0.694076 | 18.8527 | 0.56171 | 2 |  |
| lcl|VWYP01011059.1_cds_PYCJOC_R12893_4689 |  | 471 | 0.569002 | 0.585987 | 0.562898 | -0.131618 | 19.6363 | 0.549139 | 2 |  |
| lcl|VWYP01013592.1_cds_PYCJOC_R06826_5702 |  | 666 | 0.653153 | 0.445946 | 1.59569 | -0.953068 | 27.091 | 0.542761 | 2 |  |
| lcl|VWYP01014474.1_cds_PYCJOC_R12530_6111 |  | 330 | 0.542424 | 0.536364 | 0.236703 | -0.422695 | 20.3523 | 0.521759 | 2 |  |
| lcl|VWYP01001293.1_cds_PYCJOC_R01260_489 |  | 312 | 0.599359 | 0.673077 | 0.935472 | 0.379233 | 25.4271 | 0.519878 | 2 |  |
| lcl|VWYP01023186.1_cds_PYCJOC_R11204_9989 |  | 591 | 0.548223 | 0.538071 | 0.307875 | -0.412683 | 20.8277 | 0.510524 | 2 |  |
| lcl|VWYP01019185.1_cds_PYCJOC_R14583_8336 |  | 303 | 0.574257 | 0.465347 | 0.627393 | -0.839266 | 18.5594 | 0.486418 | 2 |  |
| lcl|VWYP01028690.1_cds_PYCJOC_R01249_12469 |  | 348 | 0.511494 | 0.525862 | -0.142904 | -0.484298 | 26.1099 | 0.456843 | 2 |  |
| lcl|VWYP01025895.1_cds_NXR80941.1_11233 | Nefm_1 | 381 | 0.769029 | 0.937008 | 3.01785 | 1.92739 | 18.3805 | 0.430371 | 2 |  |
| lcl|VWYP01033587.1_cds_PYCJOC_R15325_14704 |  | 345 | 0.385507 | 0.443478 | -1.68916 | -0.967544 | 18.6883 | 0.415198 | 2 |  |
| lcl|VWYP01028306.1_cds_NXR81928.1_12346 | Irx3 | 312 | 0.740385 | 0.855769 | 2.6663 | 1.45086 | 21.7998 | 0.413284 | 2 |  |
| lcl|VWYP01026233.1_cds_PYCJOC_R08788_11287 |  | 300 | 0.68 | 0.64 | 1.92519 | 0.185211 | 20.642 | 0.376937 | 2 |  |
| lcl|VWYP01007022.1_cds_NXR73367.1_2780 | Qrich2_0 | 447 | 0.510067 | 0.52349 | -0.160418 | -0.498212 | 17.5417 | 0.511718 | 1 |  |
| lcl|VWYP01012898.1_cds_PYCJOC_R02397_5411 |  | 642 | 0.572543 | 0.553991 | 0.606357 | -0.319299 | 17.9188 | 0.493706 | 1 |  |
| lcl|VWYP01001689.1_cds_PYCJOC_R14322_699 |  | 687 | 0.586608 | 0.606987 | 0.778978 | -0.00843639 | 17.3316 | 0.476893 | 1 |  |

