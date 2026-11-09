# Báo cáo cá nhân — Ngày 2 Object Detection

## 1. Thông tin học viên

- Họ tên:Nguyễn Văn Thọ
- MSSV: 2A202603299
- Email:thonguyen28.nitc@gmail.com
- Lớp: L2B
- Link repo bài làm: https://github.com/NguyenVanTho2805/K5-L2B-DAY02-NguyenVanTho-2A202603299-ObjectDetection
- Link Colab đã chạy: không có. Notebook không "Run all" được trên Colab, nên tôi chạy lại các bước của notebook trên máy cá nhân (xem mục 5 và 6).

## 2. Schema và mini guideline

Dẫn tới [GUIDELINE_MINI.md](../../GUIDELINE_MINI.md). Tóm tắt ba ca mơ hồ đã quyết định, cách áp dụng schema và phần cần giảng viên làm rõ.

## 3. Annotation và self-QC

- Số file nhãn train: 50/50 (942 box: car 808, truck 15, bus 81, van 38).
- Lỗi export đã phát hiện và sửa: khi gán nhãn trên CVAT tôi đã xoay 399/942 box cho ôm theo hướng xe. Export "Ultralytics YOLO Detection 1.0" của CVAT (file `data.yaml` + `labels/train/`, thử cả theo hướng dẫn của coach) bỏ qua toàn bộ box xoay mà không báo lỗi, nên bản nhãn trước (commit `9c6f634`) chỉ có 39 file / 543 box; 11 ảnh có toàn bộ box xoay (drive_013, 017, 018, 020, 021, 022, 024, 025, 027, 028, 029) không sinh file. Cách sửa: export lại dạng "CVAT for images 1.1" (giữ góc xoay) và chuyển sang YOLO bằng [tools/cvat_xml_to_yolo.py](../../tools/cvat_xml_to_yolo.py). Box không xoay giữ nguyên tọa độ; box xoay được đổi thành box thẳng bao elip nội tiếp của box xoay (cách "bao 4 góc" làm box phình quá rộng với góc 20–45° nên không dùng), cắt theo biên ảnh. Không thêm/xóa/đổi lớp box nào.
- Kiểm tra lại theo hướng dẫn của coach: tôi import lại vào CVAT bản annotation đã đổi toàn bộ box xoay thành box thẳng (cùng phép đổi như trên), rồi export bằng **Ultralytics YOLO Detection 1.0**. Kết quả đủ **50/50 file, 942 box**, `data.yaml` đúng thứ tự `0 car, 1 truck, 2 bus, 3 van`, và khớp với bộ nhãn đã khóa ở `f191068` (không file nào lệch số box, lớp hoặc tọa độ quá 0,2%). Nhãn trong repo vì vậy giữ nguyên, không đổi sau khi khóa.
- Kết quả checker và lỗi đã xử lý: `python -X utf8 tools/check_yolo_labels.py` báo `ĐẠT cấu trúc: 50/50 file nhãn hợp lệ`. Đã kiểm thêm: 942/942 dòng đủ 5 cột, class ID 0–3, không box nào vượt biên. Lỗi môi trường đã xử lý: `python3` không chạy trên Windows nên dùng `python`; console cp1252 gây UnicodeEncodeError nên thêm `-X utf8`.
- Danh sách ảnh rà soát và lỗi phát hiện. Danh sách gợi ý ban đầu có sự hỗ trợ của một công cụ AI (xem mục 8); cột "Trạng thái" cho biết mục nào đã sửa hoặc đã kiểm chứng bằng số liệu. [BẠN XÁC NHẬN: tôi đã tự mở xem các ảnh trong danh sách này.]

| Ảnh | Lỗi | Loại | Trạng thái |
|---|---|---|---|
| `drive_005` | Xe cứu hộ/cẩu trắng (dòng 12) gán `van`, trong khi cùng loại xe ở `drive_041`, `drive_019`, `drive_038` là `truck` | Nhầm lớp | **Đã sửa**: `van` → `truck` |
| `drive_006` | Xe cứu hộ (dòng 21) gán `van`, tương tự `drive_005` | Nhầm lớp | **Đã sửa**: `van` → `truck` |
| `drive_038` | Xe đỏ mui cao, thân hộp, nhiều cửa sổ bên (dòng 8) gán `car`, theo định nghĩa của tôi là `van` | Nhầm lớp | **Đã sửa**: `car` → `van`. Xe buýt hai tầng vàng ở góc phải trên chưa có box: chưa sửa |
| `drive_026` | Hai box `car` gần như trùng nhau (dòng 11 và 23, cùng tâm, cùng cỡ, IoU 0,759) | Box trùng | Đã kiểm chứng bằng số liệu, chưa sửa |
| `drive_019` | Cặp box trùng (dòng 25 và 26, IoU 0,74); xe van trắng bên trái (dòng 13) gán `car` | Box trùng, nhầm lớp | Box trùng đã kiểm chứng bằng số liệu; nhầm lớp chưa kiểm chứng; chưa sửa |
| `drive_009` | Box xe buýt đỏ-trắng lớn cắt mất góc dưới bên phải của xe (do đổi box xoay sang box thẳng bằng phương pháp bao elip) | Box cắt góc | Đã kiểm chứng bằng ảnh, chưa sửa |
| `drive_041` | Bỏ sót taxi vàng bên trái, xe lớn ở góc phải dưới (bị cắt rìa) và một xe đỏ nhỏ ở giữa trên; box xe buýt nối khớp hơi lỏng | Bỏ sót, box lỏng | Chưa kiểm chứng, chưa sửa |
| `drive_020` | Bỏ sót xe đen bị cắt ở rìa phải dưới | Bỏ sót | Chưa kiểm chứng, chưa sửa |
| `drive_027` | Có vẻ bỏ sót sedan xám ở giữa bên phải | Bỏ sót | Chưa kiểm chứng, chưa sửa |
| `drive_028` | Box ở mép phải (dòng 14) cao hơn xe nhìn thấy; có thể bỏ sót vài xe đỗ nhỏ ở xa | Box lỏng, bỏ sót | Chưa kiểm chứng, chưa sửa |
| `drive_042` | Box xe buýt phía dưới và box taxi lỏng khoảng 30–60 px | Box lỏng | Chưa kiểm chứng, chưa sửa |
| `drive_024` | Xe MPV xanh đen cao, thân hộp (dòng 15) gán `car`, có thể là `van` (như `drive_027`) | Nhầm lớp (có thể) | Chưa kiểm chứng, chưa sửa |
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
- Trên kênh Discord của lớp (trả lời một học viên khác nêu cùng vấn đề gold gán lớp khác quy định), Lab Coach Nguyễn Đức Minh nói: "cái này do giữa golden trong dán nhãn đang khác rồi", "bạn có thể skip phần check py" và "ko sao đâu, mình cứ làm đủ full step trong bài lab là đc". Tôi hiểu là có thể bỏ qua ngưỡng F1 của bước chấm gold và làm đủ các bước còn lại. Tôi giữ ảnh chụp tin nhắn và sẽ đưa giảng viên khi cần; không đưa vào repo công khai vì ảnh có tên học viên khác.

Rework đã làm (dựa trên guideline của tôi, không dựa trên gold): khi viết bảng ba ca mơ hồ, tôi thấy ba box không khớp với quyết định của chính mình nên sửa lớp đúng 3 box, không đổi tọa độ:
- `drive_038`: xe đỏ mui cao, thân hộp, đổi `car` thành `van`.
- `drive_005` và `drive_006`: xe cứu hộ trắng có cần cẩu, đổi `van` thành `truck` cho cùng loại xe với `drive_038` và `drive_041` (đã gán `truck`).

Sau sửa chấm lại bằng cùng script: các chỉ số không đổi (ba box này không làm thay đổi kết quả ghép với gold). Kết quả trước rework: `outputs/annotation_evaluation_truoc_rework.json`; sau rework: `outputs/annotation_evaluation.json`. Bản nhãn trước rework là commit `f191068`.

[BẠN ĐIỀN: lý do không rework thêm cho F1, ví dụ coach đã xác nhận gold lệch lớp.]

Dẫn tới `outputs/annotation_evaluation.json` trong repo. Nếu rework, ghi ảnh, lỗi đã kiểm, quyết định sửa/giữ và lý do. Không suy nguyên nhân chỉ từ FP/FN. Không có rework thì ghi rõ.

## 5. Kết quả YOLO

- Runtime, GPU/CPU, phiên bản Ultralytics và Torch: chạy local trên Windows 11, **CPU** (`torch 2.15.0+cpu`, Ultralytics 8.4.208, Python 3.14.10); máy có RTX 2050 nhưng bản PyTorch cài sẵn không có CUDA. Train 50 epoch mất khoảng 11,6 phút (696 giây).
- Các tham số thay đổi so với notebook nếu có và lý do: giữ nguyên `yolo26n.pt`, `epochs=50`, `imgsz=640`, `batch=-1`, `seed=20260909`, `conf=0.25`. Chỉ thêm `workers=0` (tránh lỗi đa tiến trình của dataloader trên Windows/CPU) và ghi bản `data.yaml` có đường dẫn tuyệt đối ra `outputs/data_local.yaml` thay vì sửa `data.yaml` gốc. Dùng script chạy lại các cell của notebook thay vì Colab; không đưa ảnh eval vào train.
- Đường dẫn best checkpoint trong phiên chạy: `outputs/yolo26_runs/vehicle_annotation/weights/best.pt` (không commit; `.gitignore` chặn `.pt`). **Lưu ý:** `best.pt` được chọn ở **epoch 1** (fitness cao nhất theo `results.csv`); mAP50–95 trên eval giảm còn 0,138 ở epoch 50. Các chỉ số dưới đây là của checkpoint epoch 1, không phải epoch cuối.

| Chỉ số trên 10 ảnh eval | Giá trị |
|---|---:|
| Precision | 0,427 |
| Recall | 0,252 |
| mAP50 | 0,276 |
| mAP50–95 | 0,185 |

Theo từng lớp (10 ảnh eval, 113 box; từ [model_eval_metrics.json](assets/model_eval_metrics.json)):

| Lớp | Số box eval | Precision | Recall | mAP50 | mAP50–95 |
|---|---:|---:|---:|---:|---:|
| car | 94 | 0,654 | 0,725 | 0,739 | 0,488 |
| truck | 5 | 0,873 | 0,200 | 0,293 | 0,206 |
| bus | 2 | 0,000 | 0,000 | 0,010 | 0,005 |
| van | 12 | 0,181 | 0,083 | 0,063 | 0,040 |

Kết quả nằm trong repo: ảnh dự đoán 10 ảnh eval ở [assets/eval_predictions/visuals/](assets/eval_predictions/visuals/), log train theo epoch ở [assets/yolo26_runs/vehicle_annotation/results.csv](assets/yolo26_runs/vehicle_annotation/results.csv), ảnh chỉ số (confusion matrix, PR curve) ở [assets/yolo26_runs/vehicle_eval/](assets/yolo26_runs/vehicle_eval/). Ảnh cụ thể để dẫn trong phần phân tích: [drive_058.jpg](assets/eval_predictions/visuals/drive_058.jpg) (có 1 bus và 6 van trong nhãn eval).

Trả lời bốn câu hỏi cuối notebook:

1. Lớp nào recall thấp nhất? Ảnh nào minh họa?
2. Nếu mAP50 cao nhưng mAP50–95 thấp, cần kiểm điều gì trên box?
3. Lỗi class nào có thể liên quan guideline? Dữ kiện nào hỗ trợ nhận xét?
4. Vì sao không dùng 10 ảnh eval để train? Vai trò validation của chúng trong notebook là gì?

## 6. Khó khăn và cách xử lý

| Bước/thời điểm | Lỗi quan sát | Cách đã thử | Kết quả/còn thiếu |
|---|---|---|---|
| Export nhãn từ CVAT | Export Ultralytics YOLO Detection 1.0 thiếu 11 file và thiếu 399 box (toàn bộ box bị xoay) | Export lại "CVAT for images 1.1", chuyển box xoay sang box thẳng bằng script, rà lại ảnh preview | Đủ 50/50 file, 942 box, checker ĐẠT |
| Chạy notebook trên Colab (10/11/2026) | Không "Run all" được. [BẠN ĐIỀN: nguyên văn thông báo lỗi và cell bị lỗi] | Chạy lại các bước của notebook trên máy cá nhân bằng CPU | Có đủ metrics và ảnh eval, xem mục 5. Chưa có link Colab; đã/sẽ báo giảng viên theo RULES.md |

## 7. Tự đánh giá theo rubric

Đối chiếu [RUBRIC.md](../../RUBRIC.md): phần nào đã có kết quả, phần nào còn thiếu hoặc chưa kiểm được. Không tự nhận hoàn thành bước chưa chạy.

## 8. Công cụ AI và tài liệu tham khảo

Ghi công cụ đã dùng, dùng ở bước nào và phần đã tự kiểm tra; không dùng thì ghi rõ. Liệt kê nguồn ngoài repo được sử dụng. Không ghi mật khẩu/token hoặc đính kèm gold train.

- Claude Code (Anthropic): đọc hướng dẫn nộp bài, chẩn đoán lỗi export CVAT bỏ box xoay, viết script `tools/cvat_xml_to_yolo.py` chuyển box xoay từ CVAT XML sang YOLO. Toàn bộ box do tôi tự vẽ trên CVAT; AI không gán nhãn, không thêm/xóa/sửa vị trí box. Phần tôi tự kiểm tra: chạy checker, xem ảnh preview box sau chuyển đổi.
- Một công cụ AI khác [BẠN ĐIỀN: tên công cụ] gợi ý danh sách ảnh và lỗi ở mục 3. Tôi đã nhờ Claude Code đối chiếu số dòng và các box trùng bằng số liệu; những mục chưa kiểm chứng đã được ghi rõ trong bảng.
- Claude Code cũng viết script chạy lại các cell train/val/predict của notebook trên máy local (CPU) và điền số liệu mục 5 từ `model_eval_metrics.json`. Phần phân tích bốn câu hỏi cuối notebook do tôi tự viết.
