# Báo cáo cá nhân — Ngày 2 Object Detection

## 1. Thông tin học viên

- Họ tên:Nguyễn Văn Thọ
- MSSV: 2A202603299
- Email:thonguyen28.nitc@gmail.com
- Lớp: L2B
- Link repo bài làm: https://github.com/NguyenVanTho2805/K5-L2B-DAY02-NguyenVanTho-2A202603299-ObjectDetection
- Link Colab đã chạy: https://colab.research.google.com/drive/11lR9_1KmJvSMlEBP7YWt1fDJdSC-b8Ak?usp=sharing (chạy thành công sau khi lần đầu Colab báo hết runtime, xem mục 6).

## 2. Schema và mini guideline

Chi tiết ở [GUIDELINE_MINI.md](../../GUIDELINE_MINI.md). Tôi áp dụng schema 4 lớp như đề: mỗi xe một box, ôm phần nhìn thấy; xe bị che vẫn vẽ nếu nhận ra lớp; xe bị cắt rìa thì box chạm rìa ảnh; không gán mô tô, xe đạp, người hay vật thể ngoài 4 lớp. Xe bán tải tính là `car`. Ba ca mơ hồ đã quyết định:

- `drive_009`: xe trắng nhỏ bị che giữa xe tải và xe buýt, phân vân `van` hay `bus`, chọn `van`.
- `drive_038`: xe đỏ mui cao, thân hộp, nhiều cửa sổ bên, phân vân `car` hay `van`, chọn `van`.
- `drive_005`: xe cứu hộ có cần cẩu (cũng gặp ở `drive_006`, `drive_041`, `drive_038`), phân vân `truck` hay `van`, chọn `truck`.

Cần giảng viên làm rõ: ranh giới `bus`/`van` cho xe chở người cỡ nhỏ. Guideline của tôi chia theo khoảng 16 chỗ, còn đề xếp minibus vào `bus`.

## 3. Annotation và self-QC

- Số file nhãn train: 50/50 (942 box: car 808, truck 15, bus 81, van 38).
- Lỗi export đã phát hiện và sửa: khi gán nhãn trên CVAT tôi đã xoay 399/942 box cho ôm theo hướng xe. Export "Ultralytics YOLO Detection 1.0" của CVAT (file `data.yaml` + `labels/train/`, thử cả theo hướng dẫn của coach) bỏ qua toàn bộ box xoay mà không báo lỗi, nên bản nhãn trước (commit `9c6f634`) chỉ có 39 file / 543 box; 11 ảnh có toàn bộ box xoay (drive_013, 017, 018, 020, 021, 022, 024, 025, 027, 028, 029) không sinh file. Cách sửa: export lại dạng "CVAT for images 1.1" (giữ góc xoay) và chuyển sang YOLO bằng [tools/cvat_xml_to_yolo.py](../../tools/cvat_xml_to_yolo.py). Box không xoay giữ nguyên tọa độ; box xoay được đổi thành box thẳng bao elip nội tiếp của box xoay (cách "bao 4 góc" làm box phình quá rộng với góc 20–45° nên không dùng), cắt theo biên ảnh. Không thêm/xóa/đổi lớp box nào.
- Kiểm tra lại theo hướng dẫn của coach: tôi import lại vào CVAT bản annotation đã đổi toàn bộ box xoay thành box thẳng (cùng phép đổi như trên), rồi export bằng **Ultralytics YOLO Detection 1.0**. Kết quả đủ **50/50 file, 942 box**, `data.yaml` đúng thứ tự `0 car, 1 truck, 2 bus, 3 van`, và khớp với bộ nhãn đã khóa ở `f191068` (không file nào lệch số box, lớp hoặc tọa độ quá 0,2%). Nhãn trong repo vì vậy giữ nguyên, không đổi sau khi khóa.
- Kết quả checker và lỗi đã xử lý: `python -X utf8 tools/check_yolo_labels.py` báo `ĐẠT cấu trúc: 50/50 file nhãn hợp lệ`. Đã kiểm thêm: 942/942 dòng đủ 5 cột, class ID 0–3, không box nào vượt biên. Lỗi môi trường đã xử lý: `python3` không chạy trên Windows nên dùng `python`; console cp1252 gây UnicodeEncodeError nên thêm `-X utf8`.
- Danh sách ảnh rà soát và lỗi phát hiện: tôi đã tự mở xem 13 ảnh drive_005, 006, 009, 013, 019, 020, 024, 026, 027, 028, 038, 041, 042 trong bảng dưới. Danh sách ảnh và lỗi ban đầu do một công cụ AI gợi ý (xem mục 8). Cột "Trạng thái" cho biết dòng nào đã sửa.

| Ảnh | Lỗi | Loại | Trạng thái |
|---|---|---|---|
| `drive_005` | Xe cứu hộ/cẩu trắng (dòng 12) gán `van`, trong khi cùng loại xe ở `drive_041`, `drive_019`, `drive_038` là `truck` | Nhầm lớp | **Đã sửa**: `van` → `truck` |
| `drive_006` | Xe cứu hộ (dòng 21) gán `van`, tương tự `drive_005` | Nhầm lớp | **Đã sửa**: `van` → `truck` |
| `drive_038` | Xe đỏ mui cao, thân hộp, nhiều cửa sổ bên (dòng 8) gán `car`, theo định nghĩa của tôi là `van` | Nhầm lớp | **Đã sửa**: `car` → `van`. Xe buýt hai tầng vàng ở góc phải trên chưa có box: chưa sửa |
| `drive_026` | Hai box `car` gần như trùng nhau (dòng 11 và 23, cùng tâm, cùng cỡ, IoU 0,759) | Box trùng | Đã xem ảnh và kiểm chứng bằng số liệu, chưa sửa |
| `drive_019` | Xe van trắng bên trái (dòng 13) gán `car`, có thể là `van`. Hai box bus chồng nhau (dòng 25 và 26, IoU 0,74) là hai xe buýt khác nhau, không phải box trùng | Nhầm lớp (có thể) | Đã xem ảnh, chưa sửa |
| `drive_009` | Box xe buýt đỏ-trắng lớn cắt mất góc dưới bên phải của xe (do đổi box xoay sang box thẳng bằng phương pháp bao elip) | Box cắt góc | Đã kiểm chứng bằng ảnh, chưa sửa |
| `drive_041` | Bỏ sót taxi vàng bên trái, xe lớn ở góc phải dưới (bị cắt rìa) và một xe đỏ nhỏ ở giữa trên; box xe buýt nối khớp hơi lỏng | Bỏ sót, box lỏng | Đã xem ảnh, chưa sửa |
| `drive_020` | Bỏ sót xe đen bị cắt ở rìa phải dưới | Bỏ sót | Đã xem ảnh, chưa sửa |
| `drive_027` | Có vẻ bỏ sót sedan xám ở giữa bên phải | Bỏ sót | Đã xem ảnh, chưa sửa |
| `drive_028` | Box ở mép phải (dòng 14) cao hơn xe nhìn thấy; có thể bỏ sót vài xe đỗ nhỏ ở xa | Box lỏng, bỏ sót | Đã xem ảnh, chưa sửa |
| `drive_042` | Box xe buýt phía dưới và box taxi lỏng khoảng 30–60 px | Box lỏng | Đã xem ảnh, chưa sửa |
| `drive_024` | Xe MPV xanh đen cao, thân hộp (dòng 15) gán `car`, có thể là `van` (như `drive_027`) | Nhầm lớp (có thể) | Đã xem ảnh, chưa sửa |
| `drive_013` | Đã xem, không thấy lỗi | | Ổn |

Ba dòng đầu chỉ sửa lớp (3 box), không đổi tọa độ; các lỗi còn lại tôi chưa sửa và ghi rõ ở đây thay vì chỉnh theo gold.
- Commit khóa nhãn ban đầu giữ ở dòng dưới.
- Lỗi bỏ sót/box/class phát hiện khi rà và cách sửa: xem bảng trên.
- Commit khóa nhãn ban đầu: `f191068` (bản 50/50 đầu tiên được đưa lên GitHub). `9c6f634` là bản 39/50 làm trước đó trên máy, chưa từng được push riêng.

## 4. Gold QC và rework

| Chỉ số | Trước sửa | Sau sửa nếu có |
|---|---:|---:|
| TP | 439 | 439 |
| FP | 503 | 503 |
| FN | 214 | 214 |
| Precision | 0,4660 | 0,4660 |
| Recall | 0,6723 | 0,6723 |
| F1 | 0,5505 | 0,5505 |
| mean_iou_of_matches | 0,7589 | 0,7589 |
| passed | false (F1 < 0,80; mean IoU đạt) | false (không đổi) |

Kết quả chấm lần 1 (nhãn khóa ở `f191068`) nằm trong `outputs/annotation_evaluation.json`.

Số liệu bổ sung khi phân tích (chạy bằng cùng `tools/evaluate_annotations.py`, chỉ đổi cách ghép, không ghi vào JSON nộp):
- Có xét lớp (chỉ số chính thức): TP 439, FP 503, FN 214, F1 0,5505, mean IoU 0,7589.
- Không xét lớp: TP 543, FP 399, FN 110, Precision 0,5764, Recall 0,8315, F1 0,6809, mean IoU 0,7615.
- Có 104 box của tôi trùng vị trí (IoU ≥ 0,5) với box gold nhưng khác lớp; 399 box còn lại là box tôi gán mà gold không có (đa số diện tích nhỏ, xe ở xa).

Rework đã làm (dựa trên guideline của tôi, không dựa trên gold): khi viết bảng ba ca mơ hồ, tôi thấy ba box không khớp với quyết định của chính mình nên sửa lớp đúng 3 box, không đổi tọa độ:
- `drive_038`: xe đỏ mui cao, thân hộp, đổi `car` thành `van`.
- `drive_005` và `drive_006`: xe cứu hộ trắng có cần cẩu, đổi `van` thành `truck` cho cùng loại xe với `drive_038` và `drive_041` (đã gán `truck`).

Sau sửa chấm lại bằng cùng script: các chỉ số không đổi (ba box này không làm thay đổi kết quả ghép với gold). Kết quả trước rework: `outputs/annotation_evaluation_truoc_rework.json`; sau rework: `outputs/annotation_evaluation.json`. Bản nhãn trước rework là commit `f191068`.

Lý do không rework thêm để nâng F1: (1) F1 0,5505 chủ yếu đến từ hai nhóm chênh lệch với gold: 104 box trùng vị trí (IoU ≥ 0,5) nhưng khác lớp, và 399 box tôi vẽ mà gold không có (đa số xe nhỏ ở xa). Khi không xét lớp, F1 vẫn chỉ 0,6809, nên sửa vài box không đưa F1 lên 0,80. (2) Lab Coach Nguyễn Đức Minh trả lời trên Discord rằng gold đang khác quy định lớp, có thể bỏ qua phần check và làm đủ các bước của lab. (3) Theo RULES.md tôi không sửa nhãn để khớp gold; tôi chỉ rework theo guideline của mình (3 box, không đổi kết quả). (4) Tôi thừa nhận còn bỏ sót xe và có box lỏng ở một số ảnh như ghi ở mục 3; các lỗi này được ghi nhận nhưng chưa sửa.

## 5. Kết quả YOLO

Ghi chú: kết quả chính trong mục này là lần chạy trên [Colab](https://colab.research.google.com/drive/11lR9_1KmJvSMlEBP7YWt1fDJdSC-b8Ak?usp=sharing) bằng notebook gốc, chỉ đổi `REPO_URL` thành repo của tôi. Khi Colab hết runtime tôi đã chạy local trên CPU bằng [tools/run_local.py](../../tools/run_local.py) làm phương án dự phòng; kết quả local (gần giống) để ở `assets/local_run/`.

- Runtime, GPU/CPU, phiên bản Ultralytics và Torch: Colab, GPU (`device=0` trong `args.yaml`). Ultralytics là bản mới nhất cài bằng pip ở cell đầu của notebook; số phiên bản Ultralytics và Torch xem trong log của notebook ở link Colab.
- Các tham số thay đổi so với notebook nếu có và lý do: không đổi tham số nào (`yolo26n.pt`, `epochs=50`, `imgsz=640`, `batch=-1`, `seed=20260909`), chỉ thay `REPO_URL`. Không đưa ảnh eval vào train. Riêng bản local có thêm `workers=0` và `outputs/data_local.yaml` vì chạy trên Windows/CPU.
- Đường dẫn best checkpoint trong phiên chạy: `/content/Day2-Lab/outputs/yolo26_runs/vehicle_annotation/weights/best.pt` (trong phiên Colab; không commit vì `.gitignore` chặn `.pt`). **Lưu ý:** `best.pt` được chọn ở **epoch 1** (fitness cao nhất theo `results.csv`); mAP50–95 trên eval giảm còn 0,137 ở epoch 50. Các chỉ số dưới đây là của checkpoint epoch 1, không phải epoch cuối.

| Chỉ số trên 10 ảnh eval | Giá trị |
|---|---:|
| Precision | 0,411 |
| Recall | 0,230 |
| mAP50 | 0,272 |
| mAP50–95 | 0,202 |

Theo từng lớp (bản chạy local; file kết quả Colab không có số liệu theo lớp. 10 ảnh eval, 113 box; từ [local_run/model_eval_metrics.json](assets/local_run/model_eval_metrics.json)):

| Lớp | Số box eval | Precision | Recall | mAP50 | mAP50–95 |
|---|---:|---:|---:|---:|---:|
| car | 94 | 0,654 | 0,725 | 0,739 | 0,488 |
| truck | 5 | 0,873 | 0,200 | 0,293 | 0,206 |
| bus | 2 | 0,000 | 0,000 | 0,010 | 0,005 |
| van | 12 | 0,181 | 0,083 | 0,063 | 0,040 |

Với Colab, confusion matrix cho thấy số box đúng lớp: car 84/94, truck 1/5, bus 0/2, van 0/12 (11 van bị đoán là bus).

Kết quả Colab nằm trong repo: ảnh dự đoán 10 ảnh eval ở [assets/eval_predictions/visuals/](assets/eval_predictions/visuals/), log train theo epoch ở [assets/yolo26_runs/vehicle_annotation/results.csv](assets/yolo26_runs/vehicle_annotation/results.csv), ảnh chỉ số (confusion matrix, PR curve) ở [assets/yolo26_runs/vehicle_eval/](assets/yolo26_runs/vehicle_eval/). Ảnh cụ thể để dẫn trong phần phân tích: [drive_058.jpg](assets/eval_predictions/visuals/drive_058.jpg) (có 1 bus và 6 van trong nhãn eval). Kết quả của bản chạy local ở [assets/local_run/](assets/local_run/).

Trả lời bốn câu hỏi cuối notebook:

1. Bus và van thấp nhất: theo confusion matrix của Colab, bus đúng 0/2 và van đúng 0/12; truck 1/5, car 84/94. Eval chỉ có 2 bus nên số này không chắc lắm. Ví dụ drive_058: gold có 6 van và 1 bus, model vẽ 3 box bus và không có box van nào.
2. mAP50 của tôi chỉ 0,272 nên chưa phải trường hợp cao. Nếu mAP50 cao mà mAP50–95 thấp thì phải xem box có sát không. Nhãn của tôi có 399/942 box xoay đổi sang box thẳng, như ở drive_009 bị mất một góc xe buýt.
3. Nhầm nhiều nhất là van thành bus: 11 trên 12 van trong eval bị đoán là bus (confusion matrix của Colab). Tôi nghĩ do guideline, vì tôi chia bus/van theo 16 chỗ còn đề xếp minibus vào bus. Mục 4 cũng có 104 box khác lớp với gold.
4. Eval dùng để đo nên không đưa vào train, nếu không thì điểm vô nghĩa. Nhưng notebook cũng lấy nó làm validation để chọn best.pt, nên không phải test độc lập. best.pt rơi vào epoch 1 (0,202), epoch 50 chỉ 0,137, chắc vì chỉ có 10 ảnh nên số dao động.

## 6. Khó khăn và cách xử lý

| Bước/thời điểm | Lỗi quan sát | Cách đã thử | Kết quả/còn thiếu |
|---|---|---|---|
| Export nhãn từ CVAT | Export Ultralytics YOLO Detection 1.0 thiếu 11 file và thiếu 399 box (toàn bộ box bị xoay) | Export lại "CVAT for images 1.1", chuyển box xoay sang box thẳng bằng script, rà lại ảnh preview | Đủ 50/50 file, 942 box, checker ĐẠT |
| Chạy notebook trên Colab (10/11/2026) | Lần đầu không "Run all" được. Hộp thoại "Failed to assign a backend. Sorry, no backends available. Please try again later." hiện khi tôi bấm Run all (lúc kết nối runtime), không phải lỗi trong code notebook. | Chạy local trên CPU bằng tools/run_local.py làm dự phòng, rồi thử lại Colab sau đó | Colab chạy được sau đó (link ở mục 1, kết quả ở mục 5) |

## 7. Tự đánh giá theo rubric

Theo từng tiêu chí của [RUBRIC.md](../../RUBRIC.md):

- **Định dạng YOLO:** đạt. 50 file cùng tên ảnh, checker báo ĐẠT, 942/942 dòng đủ 5 cột, class ID 0–3, không box nào vượt biên.
- **Đầy đủ vật thể:** chưa đạt hết. Chấm với gold còn 214 FN (110 nếu không xét lớp), và khi rà tôi thấy còn bỏ sót xe ở một số ảnh (xem mục 3, chưa sửa).
- **Độ bám sát box:** mean IoU với gold 0,7589, đạt ngưỡng 0,70. Nhưng có box cắt góc do đổi box xoay sang box thẳng (drive_009) và vài box lỏng chưa sửa (drive_028, 041, 042).
- **Phân lớp nhất quán:** chưa tốt. 104 box khác lớp so với gold, ranh giới `bus`/`van` mơ hồ. Đã sửa 3 box, còn vài nghi vấn chưa sửa (drive_019, drive_024).
- **Mini guideline:** đạt. Có định nghĩa 4 lớp, 4 quy tắc chung và 3 ca mơ hồ có lý do (soạn có sự hỗ trợ của Claude Code, xem mục 8).
- **Gold QC:** chưa đạt ngưỡng. F1 0,5505 (cần 0,80), mean IoU đạt. Đã rework theo guideline và giải thích ở mục 4; chờ giảng viên quyết định theo xác nhận của coach.
- **Pipeline YOLO và phân tích:** Colab chạy được (link ở mục 1), có metrics, ảnh eval và 4 câu trả lời, không dùng eval để train. Kết quả thấp (mAP50 0,272) và best.pt rơi vào epoch 1.

Các lỗi ở mục 3 tôi đã xem lại trên ảnh; chỗ nào chưa sửa được ghi rõ trong bảng.

## 8. Công cụ AI và tài liệu tham khảo

Tôi dùng Claude Code (Anthropic, model Claude Sonnet 5.5) qua nhiều phiên làm việc. Toàn bộ box do tôi tự vẽ trên CVAT; AI không gán nhãn mới và không thêm hay xóa box.
- **Hướng dẫn và thao tác:** giải thích đề bài, cách dùng CVAT và các bước git/GitHub; chạy checker, tìm file export, copy nhãn vào repo, tạo commit và đổi tên file báo cáo.
- **Lỗi export CVAT:** chẩn đoán việc export Ultralytics YOLO bỏ box xoay và viết `tools/cvat_xml_to_yolo.py` (chỉ đổi box xoay sang box thẳng như mô tả ở mục 3). Tôi tự kiểm lại bằng checker và ảnh preview.
- **Guideline:** soạn bốn quy tắc chung và ba ca mơ hồ, sửa định nghĩa car/truck cho khớp schema (xe bán tải thuộc car). Tôi dùng làm bản nháp và chịu trách nhiệm về nội dung cuối.
- **Rà soát nhãn (mục 3):** Claude Code vẽ nhãn lên ảnh, quét tự động box trùng và box rất lớn, rồi lập bảng ảnh và lỗi. Tôi dùng bảng làm danh sách gợi ý rồi tự mở xem lại các ảnh trong bảng. Claude Code cũng chỉ ra ba box lệch với guideline (drive_005, drive_006, drive_038); quyết định đổi lớp là của tôi, chỉ đổi lớp, không đổi tọa độ.
- **Train và đánh giá (mục 5):** Claude Code viết script `tools/run_local.py` chạy lại các cell train/val/predict của notebook trên CPU làm phương án dự phòng khi Colab hết runtime, và điền số liệu của bản local. Kết quả chính là lần chạy Colab của tôi bằng notebook gốc. Bản nháp bốn câu trả lời ở mục 5 do Claude Code soạn từ số liệu trong `assets/` (confusion matrix, ảnh drive_058); tôi đọc lại, đối chiếu với file và sửa câu chữ.