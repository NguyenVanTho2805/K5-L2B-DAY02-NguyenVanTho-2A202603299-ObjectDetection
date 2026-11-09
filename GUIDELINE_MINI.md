# Mini guideline — bài làm cá nhân

> Điền nội dung này trước khi bắt đầu gán nhãn. Giữ lại các quyết định sau khi self-QC.

## Định nghĩa lớp

| Lớp | Định nghĩa của bạn | Ví dụ/điểm phân biệt |
|---|---|---|
| `car` | Xe ô tô con chở người cỡ nhỏ đến trung bình, thường 4–5 chỗ; gồm cả xe bán tải cabin nhỏ. | Sedan, hatchback, SUV/crossover, coupe, taxi, xe cá nhân, xe bán tải/pickup cabin nhỏ. Phân biệt với `van`: car có nắp capo rõ và mui thấp, không có khoang thân hộp cao nối liền cabin. |
| `truck` | Xe tải chở hàng, có cabin tách biệt với thùng hàng hoặc phần thân chở hàng ở phía sau. | Xe tải nhỏ/lớn, xe ben, xe thùng kín, xe bồn, đầu kéo kèm rơ-moóc. Xe bán tải/pickup cabin nhỏ không thuộc `truck` mà thuộc `car`. Phân biệt với `van`: truck có cabin và thùng riêng. Van có cabin và khoang hàng liền một khối. |
| `bus` | Xe khách hoặc xe buýt chở nhiều người, thân dài, nhiều cửa sổ hai bên, khoảng 16 chỗ trở lên. | Xe buýt công cộng, xe khách liên tỉnh, xe đưa đón, xe buýt hai tầng. Phân biệt với `van`: bus dài hơn nhiều, mui cao và thẳng, có dãy cửa sổ liên tục. |
| `van` | Xe thân hộp liền khối, cabin và khoang sau không tách rời, dùng chở hàng nhẹ hoặc chở người cỡ nhỏ (khoảng 7–16 chỗ). | Minivan/MPV, xe chở hàng thân kín (panel van), xe 16 chỗ cỡ nhỏ như Ford Transit hay Toyota Hiace. Nếu thân xe dài, nhiều cửa sổ và trông như xe khách thì gán `bus`. |

## Quy tắc chung

- Box bám sát vật thể nghĩa là: box ôm sát phần thân xe nhìn thấy được, không lấy thêm mặt đường, trời hay xe bên cạnh; mỗi xe một box riêng, kể cả cùng lớp.
- Vật thể bị che khuất: vẫn vẽ box quanh phần nhìn thấy nếu nhận ra được lớp; hai xe chồng nhau thì vẽ hai box riêng trên phần nhìn thấy của từng xe.
- Vật thể bị cắt bởi rìa ảnh: box chạm đúng rìa ảnh, không đoán phần nằm ngoài ảnh.
- Vật thể rất nhỏ/mơ hồ: không tự đoán lớp; nếu chỉ còn mảnh quá nhỏ để chắc chắn thì ghi vào bảng ca mơ hồ bên dưới và hỏi giảng viên.

## Ghi lại quyết định cho ít nhất ba ca mơ hồ

| Ảnh | Tình huống | Quyết định cuối | Lý do theo schema |
| --- | --- | --- | --- |
| `drive_009` | Xe nhỏ màu trắng bị che một phần giữa xe tải thùng xanh và xe buýt đỏ-trắng, chỉ thấy phần đầu và mui; phân vân giữa `van` và `bus` (minibus). | `van`, vẽ box quanh phần nhìn thấy. | Thân ngắn, mui thấp hơn hẳn các xe buýt xung quanh và chỉ thấy một hàng cửa sổ, nên giống xe van chở người cỡ nhỏ hơn xe buýt. Vì ranh giới minibus/van còn mơ hồ nên ghi lại để hỏi giảng viên. |
| `drive_038` | Xe màu đỏ, mui cao, thân hộp, có hàng cửa sổ bên hông (góc trên bên phải); phân vân giữa `car` và `van`. | `van`. | Cabin và khoang sau liền một khối, mui cao hơn hẳn xe con xung quanh, nhiều cửa sổ bên. Theo định nghĩa `van` (xe thân hộp liền khối, xe chở người cỡ nhỏ) thì thuộc `van`, không phải `car`. |
| `drive_005` | Xe cứu hộ/cẩu màu trắng có cần cẩu trên cabin (cùng loại xe xuất hiện ở `drive_006`, `drive_041`, `drive_038`); phân vân giữa `truck` và `van`. | `truck` ở mọi ảnh. | Cabin tách khỏi phần mang thiết bị cẩu ở phía sau, không phải thân hộp liền khối của `van`, nên thuộc `truck` theo định nghĩa (cabin và phần thân hàng riêng). Gán cùng một lớp cho cùng loại xe ở mọi ảnh để nhãn nhất quán. |
