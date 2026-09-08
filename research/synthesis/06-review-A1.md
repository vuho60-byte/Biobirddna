# 06 — Review chéo A1 (Antigravity: diễn giải sinh học 10 gene lõi)

Reviewer: root/V2 (độc lập với người viết A1). Đối tượng: `research/raw/A1-antigravity-gene-interpretation.md`.
Phạm vi: chỉ kiểm nhãn + nguồn theo K1–K6 của `research/briefs/V2-review-A1-antigravity.md`. Không sửa raw, không dùng Perplexity, không tìm nguồn mới ngoài 22 URL đã có ở mục 6 của bài.

```
STATUS: BLOCKED
```

**Vì sao BLOCKED chứ không phải NEEDS_FIX**: đây không phải trường hợp "thiếu nguồn thứ hai độc lập" (như tiền lệ F01/F06 ở vòng 1). Khi mở 15/22 URL, **11 URL trỏ tới bài báo có thật nhưng hoàn toàn khác chủ đề** (cơ tim, thụ thể dopamine D3, chăm sóc gia đình mùa COVID, khối phổ SRM, mật độ cơ bụng, Neurocan/Sema3F, sốt rét *Plasmodium*, tính khí khỉ rhesus, TMS, 1 trang mục lục tạp chí, 1 Ensembl ID sai gene) và 1 URL hỏng hẳn (404). Đây là các nguồn cốt lõi cho 8/10 gene ở mục 1 và gần như toàn bộ mục 3 (FoxP2/học hót) — vi phạm trực tiếp luật `CLAUDE.md`: "Không bịa trích dẫn". Việc này không sửa được bằng cách hạ 1-2 nhãn; phải coi các claim liên quan là **[U]** cho tới khi ai đó tìm lại nguồn thật (ngoài phạm vi brief này).

## BẢNG NHÃN (theo cụm gene/mục — 62 [C] + 17 [S] + 0 [U] đã đếm khớp số Main)

| # | Cụm claim (trích ngắn) | Nhãn bài ghi | Nhãn đúng | Lý do |
|---|---|---|---|---|
| 1 | Tenm4 — chức năng chính + biểu hiện mô (mục 1, 2 dòng) | [C]×2 | **[U]×2** | Nguồn #1 (PMC3603417) xác nhận là bài về cơ tim ("The constant beat…"), không phải TENM4. Nguồn #3 (Protein Atlas) trỏ sai sang gene PSTPIP1. 0/3 nguồn còn hợp lệ (nguồn #2 chưa mở được). |
| 2 | Syn3 — chức năng + biểu hiện + kiểu hình KO (mục 1, 3 dòng) | [C]×3 | **[U]×3** | Nguồn #4 (PMC2888922) là bài về thụ thể dopamine D3, không phải Synapsin III. Nguồn #5 chưa mở được (reCAPTCHA ×3 lần). 0/2 nguồn xác nhận hợp lệ. |
| 3 | Sema3a — chức năng + biểu hiện + kiểu hình (mục 1, 4 dòng) | [C]×4 | **[U]×4** | Nguồn #7 (frontiersin) 404 xác nhận (mở lại 2 lần). Nguồn #6 chưa mở được (reCAPTCHA ×3). 0/2 nguồn xác nhận hợp lệ. |
| 4 | Pdzrn4 — chức năng + biểu hiện + KO cơ (mục 1, 5 dòng) | [C]×5 | **[S] tạm/chờ xác minh** | Nguồn #8 (biorxiv, 429×3) và #9 (mdpi, 403×2) đều CHƯA mở được qua WebFetch trong phiên này — không xác nhận đúng lẫn không xác nhận sai. Không đủ căn cứ giữ [C] (chưa có nguồn nào ĐƯỢC XÁC NHẬN khớp), nhưng cũng chưa có bằng chứng sai như các gene khác → hạ về [S] kèm cờ "cần mở lại ngoài phiên rate-limit", không hạ thẳng xuống [U]. |
| 5 | Celf2 — chức năng + biểu hiện + kiểu hình (mục 1, 4 dòng) | [C]×4 | **[U]×4** | Nguồn #10 (PMC7323067) là bài về COVID/chăm sóc gia đình. Nguồn #11 (jci.org) trỏ tới trang mục lục số báo 1/9/2026, không có bài CELF2 nào trong đó. 0/2 nguồn hợp lệ. |
| 6 | Pcca — chức năng/biểu hiện chung + bệnh propionic acidemia (mục 1, 2 dòng đầu) | [C]×2 | **[S]** | Nguồn #12 (medlineplus) xác nhận khớp đúng PCCA/enzyme/bệnh. Chỉ 1 nguồn hợp lệ → đủ chuẩn [S], chưa đủ chuẩn [C] (cần ≥2 độc lập). |
| 7 | Pcca — kiểu hình chuột KO cụ thể (mục 1, 1 dòng) | [C]×2 | **[U]×2** | Chi tiết KO-mouse chỉ dựa nguồn #13 (PMC3045610), nguồn này chưa mở được (reCAPTCHA ×2) → không xác nhận được, không có nguồn thứ hai. |
| 8 | Reln — toàn bộ 4 dòng (chức năng, biểu hiện, KO reeler, lissencephaly người) | [C]×4 | **[U]×4** | Gene này chỉ CÓ ĐÚNG 1 URL trong mục 6 (#14) ngay từ đầu — đã sai cấu trúc (1 nguồn không đủ [C], theo tiền lệ F01). Mở #14 (PMC3005404) xác nhận đây là bài tối ưu hóa khối phổ SRM cho peptide — sai hoàn toàn chủ đề. Kết quả: 0 nguồn cho cả 4 claim. |
| 9 | Dlg2 — chức năng + biểu hiện + kiểu hình KO (mục 1, 3 dòng) | [C]×3 | **[U]×3** | Nguồn #15 (PMC6005727) là bài về mật độ cơ bụng/viêm-béo phì. Nguồn #16 (frontiersin fncel.2018.00346) là bài về Neurocan/Semaphorin 3F/NrCAM. Cả 2 sai chủ đề. |
| 10 | Foxp2 — chức năng + biểu hiện + kiểu hình (mục 1, 5 dòng) | [C]×5 | **[U]×5** | Dựa cùng cặp nguồn #17/#18 bị dùng lại ở mục 3 (xem dòng 12) — cả hai đã xác nhận sai chủ đề. |
| 11 | Taf3 — toàn bộ 3 dòng (chức năng, biểu hiện, kiểu hình) | [C]×3 | **[U]×3** | Chỉ có ĐÚNG 1 URL (#19) — đã sai cấu trúc như Reln. Mở #19 (PMC3838421) xác nhận là bài về kích thích từ xuyên sọ (TMS) và cảm nhận lực cơ — sai hoàn toàn chủ đề. |
| 12 | Mục 3 — Haesler 2007 knockdown + kết quả + động học biểu hiện (6 dòng) | [C]×6 | **[U]×6** | Nguồn #17 (PMC2065874, được giới thiệu là "Haesler et al. 2007") thực chất là bài về ký sinh trùng sốt rét *Plasmodium yoelii* trong gan/phổi. Nguồn #18 (PMC2858223) là bài phân tích tính khí ở khỉ rhesus non, không liên quan chim hay FoxP2. Đây là 2 nguồn trung tâm nhất của cả mục 3. |
| 13 | Mục 3 — locus >600kb, %giống người 98%/1 amino acid khác gà, tên enhancer FOXP2-Eproximal/Edistal (3 dòng) | [C]×3 | **[U]×3** | K3: có số liệu/tên riêng cụ thể nhưng KHÔNG có URL nào trong mục 6 đứng ngay sau — không tìm thấy nguồn tương ứng trong 22 URL. |
| 14 | Mục 3 — "Zhang et al. 2014, Jarvis et al. 2014, Wirthlin et al. 2018" (CNE quanh Foxp2 ở chim) | [C]×1 | **[U]** | Trích tên 3 công trình cụ thể nhưng mục 6 không có URL cho bài nào trong 3 bài này (chỉ có 1 link chung `genome.ucsc.edu`, không phải trích dẫn trực tiếp). Trích dẫn treo — không kiểm chứng được trong phạm vi bài. |
| 15 | Mục 2 — GRB/CNE cơ chế (nằm ở "trung tâm GRB", "bystander genes", loop 3D) | [C]×3 | **[S]** (giữ tạm) | Nguồn #20 (Woolfe 2005) xác nhận khớp đúng. Nguồn #21 (Kikuta 2007) không mở được toàn văn (chuyển hướng cổng đăng nhập SAMS-Sigma của CSHL — có vẻ là paywall thật, không phải link sai) → chỉ 1/2 nguồn XÁC NHẬN được, chưa đủ chuẩn [C] chặt, nhưng khá đáng tin (không có dấu hiệu sai như nhóm trên) → giữ [S] thay vì hạ xuống [U]. |
| 16 | Mục 2 — dùng khung "TAD (Topologically Associating Domains)" khi diễn giải Woolfe 2005/Kikuta 2007 | [C]×1 (nằm trong dòng 15) | **[S], ghi chú thời gian sai** | Thuật ngữ TAD chỉ phổ biến trong di truyền học từ ~2012 (Dixon et al., không có trong danh sách nguồn); 2 bài 2005/2007 dùng khái niệm GRB, gần nhưng không đồng nhất với TAD. Gán khái niệm về sau cho nguồn cũ hơn — không sai bản chất nhưng nên sửa chữ, không nên giữ [C]. |
| 17 | Mục 2 — tally "7/10 gene liên quan thần kinh", "1 gene NMJ", "1 gene biểu sinh", "1 gene chuyển hóa" (5 dòng) | [C]×5 | **[S]** | Đây là tổng hợp NỘI BỘ từ chính mục 1 (không phải claim thực nghiệm mới cần nguồn ngoài riêng) — nhưng vì phần lớn claim mục 1 bên dưới nó đã bị hạ xuống [U] (xem dòng 1–11), bảng tally này kế thừa rủi ro đó. Hạ xuống [S] kèm ghi chú "đúng nếu chức năng gene ở mục 1 đúng — nhưng nguồn cho các chức năng đó hiện không xác minh được". |
| 18 | Mục 4 — nhiễm sắc thể 1 là macrochromosome, mật độ gene thấp/intron dài/tái tổ hợp thấp | [C]×1 | **[S]** | K3: không có URL cụ thể ngay tại câu này. Đây là kiến thức hệ gen chim khá chuẩn (không đáng ngờ về nội dung) nhưng bài không dẫn nguồn tại chỗ → không đạt chuẩn [C], hạ về [S]. |
| 19 | Mục 4 — 2 khía cạnh ủng hộ H2 + 2 khía cạnh chưa bác bỏ H1 | [S]×4 | **[S] — giữ nguyên** | Đã dán nhãn đúng mức (không lạm dụng [C]) — không cần đổi. Xem thêm Finding F7 (K5) về cân xứng khối lượng lập luận. |
| 20 | Mục 5 — 3 cảnh báo phương pháp + 3 đề xuất chuẩn hóa | [C]×6, [S]×6 | **Giữ nguyên** | Đây là suy luận phương pháp luận dựa trên chính thiết kế pipeline của dự án (không phải claim sinh học cần nguồn ngoài) — đã được validate độc lập bằng việc code đã áp dụng cảnh báo #1 (xem K6). Không cần đổi nhãn. |

**Tổng số [C] khuyến nghị hạ nhãn: 53/62** — trong đó **~44 hạ xuống [U]** (0 nguồn còn hợp lệ) và **~9 hạ xuống [S]** (còn 1 nguồn hợp lệ hoặc chờ xác minh thêm ngoài phiên rate-limit). 9 [C] còn lại (mục 5, dòng 20) giữ nguyên vì không phụ thuộc nguồn ngoài.

## BẢNG URL (mục 6, 22 URL)

| # | URL (rút gọn) | Mở được? | Khớp nội dung? |
|---|---|---|---|
| 1 | PMC3603417 (Tenm4 myelin) | Có (qua redirect pmc.ncbi.nlm.nih.gov) | **KHÔNG** — bài về cơ tim ("The constant beat: cardiomyocytes…") |
| 2 | biorxiv 2023.07.12.548719v1 (Tenm4 mechanosensory) | **Không** — HTTP 429, thử lại 3 lần vẫn bị chặn | Chưa xác minh được |
| 3 | proteinatlas ENSG00000140368-TENM4 | Có | **KHÔNG** — Ensembl ID này là gene PSTPIP1, không phải TENM4 |
| 4 | PMC2888922 (Syn3 KO) | Có (redirect) | **KHÔNG** — bài về thụ thể dopamine D3/D3nf |
| 5 | PMC2173361 (Syn3 biểu hiện sớm) | **Không** — chặn reCAPTCHA, thử 3 lần | Chưa xác minh được |
| 6 | PMC2132963 (Sema3a KO) | **Không** — chặn reCAPTCHA, thử 3 lần | Chưa xác minh được |
| 7 | frontiersin fncel.2021.688849 (Sema3a phôi gà) | **Không** — HTTP 404, xác nhận 2 lần | **HỎNG** |
| 8 | biorxiv 2023.11.20.567848v1 (Pdzrn4/MuSK) | **Không** — HTTP 429, thử 3 lần | Chưa xác minh được |
| 9 | mdpi 1422-0067/22/19/10497 (LNX/PDZRN review) | **Không** — HTTP 403, thử 2 lần | Chưa xác minh được |
| 10 | PMC7323067 (Celf2 splicing/autism) | Có (redirect) | **KHÔNG** — bài về ảnh hưởng hạn chế thăm bệnh nhân mùa COVID |
| 11 | jci.org/articles/view/137688 (Celf2 autism) | Có | **KHÔNG** — trỏ tới trang mục lục số báo JCI 1/9/2026, không có bài CELF2 |
| 12 | medlineplus.gov PCCA | Có | **KHỚP** — đúng gene PCCA, enzyme, propionic acidemia |
| 13 | PMC3045610 (Pcca KO) | **Không** — chặn reCAPTCHA, thử 2 lần | Chưa xác minh được |
| 14 | PMC3005404 (Reelin/reeler) | Có (redirect) | **KHÔNG** — bài tối ưu hóa khối phổ SRM cho peptide |
| 15 | PMC6005727 (Dlg2 KO striatal) | Có (redirect) | **KHÔNG** — bài về mật độ cơ bụng và viêm/béo phì |
| 16 | frontiersin fncel.2018.00346 (MAGUK/Dlg2) | Có | **KHÔNG** — bài về Neurocan/Semaphorin 3F/NrCAM |
| 17 | PMC2065874 (Haesler 2007 FoxP2) | Có (redirect) | **KHÔNG** — bài về ký sinh trùng sốt rét *Plasmodium yoelii* |
| 18 | PMC2858223 (FoxP2 động học biểu hiện) | Có (redirect) | **KHÔNG** — bài về tính khí ở khỉ rhesus non |
| 19 | PMC3838421 (Taf3 CTCF/cohesin) | Có (redirect) | **KHÔNG** — bài về kích thích từ xuyên sọ (TMS) |
| 20 | PLOS Biology Woolfe 2005 | Có | **KHỚP** — đúng bài, đúng tác giả/năm/tạp chí |
| 21 | genome.cshlp.org Kikuta 2007 | Có (nhưng chuyển hướng cổng đăng nhập SAMS-Sigma — paywall) | Không xác minh được toàn văn; có vẻ là paywall thật (không phải link sai host) |
| 22 | genome.ucsc.edu (UCSC Browser) | Có | **Khớp chung** — đúng trang UCSC thật, nhưng là trang chủ, không trỏ thẳng track B10K/phyloP cụ thể |

Tổng: 2 khớp đúng, 1 khớp chung (trang chủ), **11 xác nhận KHÔNG khớp**, **1 xác nhận hỏng (404)**, 7 chưa mở được qua WebFetch trong phiên này (reCAPTCHA/429/403 — cần thử lại ngoài phiên, không kết luận đúng/sai).

## FINDINGS

| # | K | Mức | Vấn đề | Sửa thế nào |
|---|---|---|---|---|
| F1 | K2 | **BLOCKER** | 11/22 URL ở mục 6 xác nhận trỏ tới bài báo thật nhưng hoàn toàn sai chủ đề (không phải "link hỏng" mà là "link đúng, nội dung sai") — đây là nguồn cốt lõi cho 8/10 gene mục 1 + toàn bộ khung Haesler 2007 ở mục 3. | Hạ toàn bộ claim phụ thuộc các URL này xuống [U] (đã làm ở BẢNG NHÃN). Việc tìm lại nguồn thật nằm ngoài phạm vi brief này (cấm tìm nguồn mới) — cần một brief riêng giao người khác làm lại phần sourcing. |
| F2 | K2 | HIGH | URL #7 (frontiersin, Sema3a phôi gà) hỏng hẳn (404), xác nhận 2 lần độc lập. | Xóa khỏi danh sách nguồn hợp lệ; claim liên quan ("Ở phôi gà, can thiệp Sema3A…") mất nguồn, hạ xuống [U]. |
| F3 | K1 | **BLOCKER** | Hệ quả trực tiếp từ F1/F2: ít nhất 44/62 nhãn [C] hiện có 0 nguồn còn hợp lệ (không phải "chỉ 1 nguồn" — là "không nguồn nào đứng vững"), nặng nhất ở Tenm4/Syn3/Sema3a/Celf2/Reln/Dlg2/Foxp2/Taf3. | Áp bảng BẢNG NHÃN ở trên; không dùng các claim này ở mức [C]/[S] cho báo cáo LÕI v0 hay tracker T06/T22 cho tới khi có nguồn thật. |
| F4 | K1 | HIGH | Reln và Taf3 chỉ từng có ĐÚNG 1 URL trong mục 6 dù mang 4 và 3 nhãn [C] — sai cấu trúc ngay cả trước khi xét nội dung URL đúng/sai (1 nguồn không đủ [C] theo luật dự án, tiền lệ F01 ở `01-review-vong-1.md`). | Không lặp lại kiểu "1 gene — 1 nguồn — nhiều [C]" ở các bài sau; quy tắc: số [C] tối đa cho 1 gene ≤ số URL độc lập thật sự hậu thuẫn claim đó. |
| F5 | K3 | HIGH | Mục 3 có 3 khẳng định mang số liệu/tên riêng cụ thể (locus >600kb; 98%/1 amino acid khác gà; tên 2 enhancer FOXP2-Eproximal/Edistal) dán nhãn [C] nhưng không có URL nào trong mục 6 hậu thuẫn. | Hạ xuống [U], ghi rõ "chưa tìm được nguồn" thay vì im lặng gắn [C]. |
| F6 | K1/K3 | HIGH | Mục 3 trích tên 3 công trình cụ thể (Zhang 2014, Jarvis 2014, Wirthlin 2018) gắn [C] nhưng mục 6 không có URL cho bài nào trong 3 bài này. | Hạ xuống [U] hoặc bổ sung URL thật nếu người viết lại có thể tìm — không giữ [C] cho trích dẫn treo. |
| F7 | K5 | MEDIUM | Mục 4 tự thân cân bằng (nhãn [S] đều cho cả 2 phía H1/H2), nhưng mục 1–3 (≈80% độ dài bài) chỉ xây dựng lập luận nghiêng về hướng "gene thần kinh/GRB đặc biệt" (ủng hộ ngầm H2) trước khi mục 4 mới cân bằng câu chữ — mất cân xứng khối lượng dù không sai về mặt nhãn. | Khi dùng bài này, đọc mục 4 độc lập với ấn tượng tổng thể của mục 1–3; nếu viết lại, nên chèn phản biện H1 sớm hơn, không dồn hết vào 1 mục cuối. |
| F8 | K1 | MEDIUM | Mục 2 dùng khung "TAD" khi diễn giải Woolfe 2005/Kikuta 2007 — thuật ngữ TAD phổ biến từ ~2012 (Dixon et al., không có trong nguồn), 2 bài được trích dùng khái niệm GRB (gần nhưng không đồng nhất TAD). | Sửa chữ thành "GRB" (đúng thuật ngữ của 2 nguồn được trích) hoặc thêm nguồn TAD thật nếu muốn giữ khung đó; không quy kết khái niệm 2012 cho bài 2005/2007. |
| F9 | K4 | LOW | Brief V2 yêu cầu đối chiếu `docs/04-ke-hoach-tach-adn-goc.md` mục 10b — file này chỉ có 8 mục (dừng ở mục 8, dòng 109), không tồn tại mục 10b. | Đã dùng nguồn thay thế hợp lý: `research/briefs/A1-antigravity-gene-interpretation.md` (chính brief gốc giao cho Antigravity, đúng dữ liệu dự án đo 2026-09-07). Đối chiếu xong: 4 số tổng hợp A1 lặp lại (66,9%/10,5%/22,6%/~7,5% ánh xạ) khớp chính xác, không có lỗi chép số. Người viết brief sau nên sửa lại đường dẫn tham chiếu. |
| F10 | K6 | LOW (tin tốt) | Cảnh báo #1 mục 5 của A1 (thiên vị gene dài) đã được xử lý trong code CÙNG NGÀY (commit `73cba7f`) — nhưng `summarize_a2.py` (file brief V2 hỏi trực tiếp) chưa in bảng mật độ mới; hàm `section()` hiện tại gộp lẫn bảng bp-thô và bảng mật độ thành 1 danh sách rồi cắt `[:10]`, nên luôn chỉ trả về bảng CŨ (thiên vị) — bảng mật độ không bao giờ được hiển thị dù đã tính sẵn trong `annot_stats.tsv`. | Xem ĐỀ XUẤT CODE §1. |
| F11 | K6 | LOW | Cảnh báo #2 (gán liên gene cho gene gần nhất) và #3 (annotation thiếu UTR) của A1 mục 5 đều đúng và đã được README của `p02_core_map` tự ghi nhận là "điểm mù chưa xử lý" (dòng cuối README, viết cùng ngày) — chưa có code xử lý (permutation test, gán theo TAD/khoảng cách). | Xem ĐỀ XUẤT CODE §2, §3. |
| F12 | K1 | LOW | Lỗi định dạng: 2 nhãn `**[C]**` và 1 nhãn `**[S]**` bị ký tự xuống dòng chèn giữa `**` và `[C]`/`[S]` (lỗi bọc dòng khi lưu file thô — file có nhiều chỗ dính chữ mất khoảng trắng ở điểm xuống dòng, ví dụ "chếtsơ sinh", "tậptrung"). Không đổi tổng số đếm (62/17/0 khớp số Main đếm trước). | Không cần sửa raw (cấm sửa tay); chỉ ghi chú để người đọc sau không nhầm là markdown cố ý sai cú pháp. |

**Tổng finding: 12** — BLOCKER 2 · HIGH 4 · MEDIUM 2 · LOW 4.

## KẾT LUẬN DÙNG ĐƯỢC GÌ

**Dùng được ngay (giữ nhãn hiện tại hoặc [S]):**
- 4 con số tổng hợp dự án (531.189 phần tử; 39.826 ánh xạ ≈7,5%; 22,6% CDS; 10,5% intron; 66,9% liên gene) — khớp chính xác brief gốc (F9), không lỗi.
- Tên + thứ tự đúng của 10 gene (Tenm4…Taf3) — khớp brief.
- Khung so sánh H1/H2 ở mục 4 (câu hỏi + cấu trúc trung lập) — dùng làm khung tư duy, không phải kết luận.
- Đoạn cơ chế GRB/CNE chung ở mục 2 (dựa Woolfe 2005 xác nhận khớp) — dùng ở mức [S], sửa chữ "TAD"→"GRB" (F8).
- PCCA/propionic acidemia (phần dựa medlineplus) — dùng ở mức [S].
- 3 cảnh báo phương pháp + hướng chuẩn hóa ở mục 5 — đúng và đã một phần được code hóa (F10/F11), dùng được làm đặc tả kỹ thuật.

**Phải hạ nhãn xuống [U] trước khi đưa vào báo cáo LÕI v0 hoặc tracker T06/T22 (không dùng như bằng chứng):**
- Mọi mô tả chức năng/kiểu hình chi tiết của Tenm4, Syn3, Sema3a, Celf2, Reln, Dlg2, Foxp2, Taf3 (mục 1 + toàn bộ mục 3/FoxP2-học hót) — nguồn cốt lõi đã xác nhận sai hoặc chưa xác minh được (F1–F4).
- Mọi số liệu/tên riêng không nguồn ở mục 3 (locus >600kb, 98%/1aa, tên enhancer, Zhang/Jarvis/Wirthlin) (F5, F6).
- Pdzrn4 (mục 1) — 2 nguồn đều chưa mở được trong phiên này (rate-limit), cần ai đó mở lại ngoài giờ cao điểm trước khi phục hồi [C]/[S].

## ĐỀ XUẤT CODE (K6 — đặc tả ngắn cho lập trình viên)

**§1. Sửa `pipeline/p02_core_map/summarize_a2.py` — ưu tiên cao, việc nhỏ (bug hiển thị, dữ liệu đã có sẵn):**
- Vấn đề: `annot_stats.tsv` (do `conserved_to_bulbul.py annotate`, từ commit `73cba7f`) hiện ghi **2 bảng gene** nối tiếp nhau, cùng header `gene_id\tgene_name\tbp\tgene_len\tbp_per_kb` — bảng 1 xếp theo bp thô (top 50), rồi 1 dòng comment `# xep theo mat do; loc gene_len >= 1000 bp va bp >= 200`, rồi bảng 2 xếp theo mật độ (top 50, đã lọc `gene_len≥1000` và `bp≥200`).
- Hàm `section(path, header)` hiện tại của `summarize_a2.py` dò theo `row[:len(header)]==header` — vì cả 2 bảng dùng chung 3 cột đầu `["gene_id","gene_name","bp"]` làm mốc, hàm này **gộp cả 2 bảng thành 1 danh sách** (dòng blank trước comment tắt "on" đúng 1 nhịp, rồi header bảng 2 lại bật "on" lại) rồi lệnh gọi `[:10]` phía sau chỉ lấy 10 dòng đầu — luôn là bảng 1 (bp thô, thiên vị gene dài), **không bao giờ in được bảng 2 (mật độ)**.
- Việc cần làm: thêm 1 hàm mới, ví dụ `section_after_marker(path, marker_prefix, header)`, đọc file theo dòng, chỉ bắt đầu thu thập SAU khi gặp dòng bắt đầu bằng `marker_prefix` (`"# xep theo mat do"`), rồi áp cùng logic `header`/dừng-khi-blank như `section()` hiện tại. Gọi hàm này để lấy bảng 2, và giới hạn `section()` cũ chỉ lấy TRƯỚC dòng marker đó (dừng thu thập khi gặp dòng bắt đầu bằng `"#"`, không chỉ khi blank).
- In thêm khối mới sau khối "Top 10 gene theo bp lõi" hiện tại:
  ```
  print("\nTop 10 gene theo MẬT ĐỘ bp lõi/kb (đã chuẩn hóa chiều dài, lọc gene_len≥1000bp & bp≥200bp — xem A1 mục 5): " +
        ", ".join(f"{g[1]} ({g[4]} bp/kb, tổng {int(g[2]):,} bp, dài {int(g[3]):,} bp)" for g in density_rows[:10]))
  ```
- Đổi nhãn dòng in bảng 1 hiện tại thành `"Top 10 gene theo TỔNG bp lõi (CHƯA chuẩn hóa chiều dài — xem cảnh báo A1 mục 5):"` để không ai đọc nhầm đây là kết luận cuối.
- Test: thêm 1 unit test cho `summarize_a2.py` (hiện chưa có test riêng theo `ls pipeline/p02_core_map/tests/`) dựng 1 `annot_stats.tsv` giả có đúng cấu trúc 2-bảng-1-comment ở trên, assert output in ra chứa cả 2 dòng "Top 10 … TỔNG bp" và "Top 10 … MẬT ĐỘ" với đúng gene khác nhau.

**§2. Permutation / Background Enrichment — việc mới, tách brief riêng, không nhét vào `summarize_a2.py`:**
- Mục tiêu: với mỗi gene trong `gene_bp` (đã có trong `conserved_to_bulbul.py cmd_annotate`), ước lượng có bao nhiêu bp lõi là "kỳ vọng ngẫu nhiên" nếu xáo trộn vị trí các phần tử lõi trên cùng scaffold (đối sánh %GC + khoảng cách tới gene gần nhất).
- Input còn thiếu: %GC theo cửa sổ trên bộ gene chào mào (`Pycnonotus_jocosus`) — có thể lấy bằng `kent tool nuc` hoặc tính trực tiếp từ FASTA đã có (`bulbul.fna.gz`), stdlib đủ làm (đếm G/C/tổng theo cửa sổ trượt).
- Thuật toán tối thiểu: N≥100 lần xáo trộn (giữ nguyên độ dài + số lượng phần tử/scaffold, đổi vị trí start ngẫu nhiên có đối sánh bin %GC), mỗi lần tính lại tổng bp rơi vào từng gene → phân phối nền. `Enrichment = bp_thật / mean(bp_ngẫu_nhiên)`, `p_thực_nghiệm = (số lần bp_ngẫu_nhiên ≥ bp_thật) / N`. Ghi thêm cột `enrichment`, `p_empirical` vào bảng gene của `annot_stats.tsv`.
- Vì cần dữ liệu %GC mới + có thể chạy lâu (N lần lặp), đề xuất **brief riêng** (không phải phần mở rộng nhanh của `summarize_a2.py`), chủ dự án duyệt trước khi chạy.

**§3. Gán CNE liên gene theo khoảng cách (bước tạm rẻ hơn TAD thật) — việc mới, nhỏ hơn §2:**
- Chưa có dữ liệu TAD/Hi-C thật cho gà hoặc chào mào trong dự án → không làm đúng nghĩa "TAD-aware assignment" ngay được.
- Bước tạm: `cmd_annotate` đã có `gene_span` (khoảng cách geo-vị trí gene) — thêm 1 cột `khoang_cach_gene_gan_nhat_bp` vào `core_annot.tsv` cho các vùng lớp `intergenic`, và gắn `gan_khong_chac_chan=true` nếu khoảng cách này > ngưỡng cấu hình được (ví dụ `--max-confident-distance 50000`, mặc định 50 kb). Không cần dữ liệu TAD thật, chỉ dùng khoảng cách đã tính sẵn — giảm rủi ro "gán nhầm sang bystander gene" nêu ở A1 mục 5 cảnh báo #2 mà không cần thêm nguồn dữ liệu mới.
