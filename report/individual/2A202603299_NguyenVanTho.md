# Báo cáo cá nhân — Ngày 2 Object Detection

Đổi tên file theo `MSSV_HoTen.md`, ví dụ `20241234_NguyenVanAn.md`. Điền kết quả thật, xóa dòng hướng dẫn khi nộp. Xem [quy định nộp](../../SUBMISSION.md).

## 1. Thông tin học viên

- Họ tên:Nguyễn Văn Thọ
- MSSV: 2A202603299
- Email:thonguyen28.nitc@gmail.com
- Lớp: L2B
- Link repo bài làm: https://github.com/NguyenVanTho2805/K5-L2B-DAY02-NguyenVanTho-2A202603299-ObjectDetection
- Link Colab đã chạy:

## 2. Schema và mini guideline

Dẫn tới [GUIDELINE_MINI.md](../../GUIDELINE_MINI.md). Tóm tắt ba ca mơ hồ đã quyết định, cách áp dụng schema và phần cần giảng viên làm rõ.

## 3. Annotation và self-QC

- Số file nhãn train: 50/50 (942 box: car 808, truck 15, bus 81, van 38).
- Lỗi export đã phát hiện và sửa: khi gán nhãn trên CVAT tôi đã xoay 399/942 box cho ôm theo hướng xe. Export "YOLO 1.1" của CVAT bỏ qua toàn bộ box xoay mà không báo lỗi, nên bản nhãn trước (commit `9c6f634`) chỉ có 39 file / 543 box; 11 ảnh có toàn bộ box xoay (drive_013, 017, 018, 020, 021, 022, 024, 025, 027, 028, 029) không sinh file. Cách sửa: export lại dạng "CVAT for images 1.1" (giữ góc xoay) và chuyển sang YOLO bằng [tools/cvat_xml_to_yolo.py](../../tools/cvat_xml_to_yolo.py). Box không xoay giữ nguyên tọa độ; box xoay được đổi thành box thẳng bao elip nội tiếp của box xoay (cách "bao 4 góc" làm box phình quá rộng với góc 20–45° nên không dùng), cắt theo biên ảnh. Không thêm/xóa/đổi lớp box nào.
- Kết quả checker và lỗi đã xử lý: `python -X utf8 tools/check_yolo_labels.py` báo `ĐẠT cấu trúc: 50/50 file nhãn hợp lệ`. Đã kiểm thêm: 942/942 dòng đủ 5 cột, class ID 0–3, không box nào vượt biên. Lỗi môi trường đã xử lý: `python3` không chạy trên Windows nên dùng `python`; console cp1252 gây UnicodeEncodeError nên thêm `-X utf8`.
- Danh sách ít nhất 10 ảnh đã rà bằng mắt:
- Lỗi bỏ sót/box/class phát hiện khi rà và cách sửa:
- Commit khóa nhãn ban đầu:

## 4. Gold QC và rework

| Chỉ số | Trước sửa | Sau sửa nếu có |
|---|---:|---:|
| TP | | |
| FP | | |
| FN | | |
| Precision | | |
| Recall | | |
| F1 | | |
| mean_iou_of_matches | | |
| passed | | |

Dẫn tới `outputs/annotation_evaluation.json` trong repo. Nếu rework, ghi ảnh, lỗi đã kiểm, quyết định sửa/giữ và lý do. Không suy nguyên nhân chỉ từ FP/FN. Không có rework thì ghi rõ.

## 5. Kết quả YOLO

- Runtime, GPU/CPU, phiên bản Ultralytics và Torch:
- Các tham số thay đổi so với notebook nếu có và lý do:
- Đường dẫn best checkpoint trong phiên chạy:

| Chỉ số trên 10 ảnh eval | Giá trị |
|---|---:|
| Precision | |
| Recall | |
| mAP50 | |
| mAP50–95 | |

Đặt cả 2 folder `assets/eval_predictions/` và `assets/yolo26_runs/` (giải nén từ `day2_colab_outputs.zip`) cạnh báo cáo và dẫn link tương đối. Không chỉ ghi số; chỉ ra ít nhất một ảnh và vật thể cụ thể.

Trả lời bốn câu hỏi cuối notebook:

1. Lớp nào recall thấp nhất? Ảnh nào minh họa?
2. Nếu mAP50 cao nhưng mAP50–95 thấp, cần kiểm điều gì trên box?
3. Lỗi class nào có thể liên quan guideline? Dữ kiện nào hỗ trợ nhận xét?
4. Vì sao không dùng 10 ảnh eval để train? Vai trò validation của chúng trong notebook là gì?

## 6. Khó khăn và cách xử lý

| Bước/thời điểm | Lỗi quan sát | Cách đã thử | Kết quả/còn thiếu |
|---|---|---|---|
| Export nhãn từ CVAT | Export YOLO 1.1 thiếu 11 file và thiếu 399 box (toàn bộ box bị xoay) | Export lại "CVAT for images 1.1", chuyển box xoay sang box thẳng bằng script, rà lại ảnh preview | Đủ 50/50 file, 942 box, checker ĐẠT |

## 7. Tự đánh giá theo rubric

Đối chiếu [RUBRIC.md](../../RUBRIC.md): phần nào đã có kết quả, phần nào còn thiếu hoặc chưa kiểm được. Không tự nhận hoàn thành bước chưa chạy.

## 8. Công cụ AI và tài liệu tham khảo

Ghi công cụ đã dùng, dùng ở bước nào và phần đã tự kiểm tra; không dùng thì ghi rõ. Liệt kê nguồn ngoài repo được sử dụng. Không ghi mật khẩu/token hoặc đính kèm gold train.

- Claude Code (Anthropic): đọc hướng dẫn nộp bài, chẩn đoán lỗi export CVAT bỏ box xoay, viết script `tools/cvat_xml_to_yolo.py` chuyển box xoay từ CVAT XML sang YOLO. Toàn bộ box do tôi tự vẽ trên CVAT; AI không gán nhãn, không thêm/xóa/sửa vị trí box. Phần tôi tự kiểm tra: chạy checker, xem ảnh preview box sau chuyển đổi.
