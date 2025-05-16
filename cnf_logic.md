# Tài liệu về CNF Logic cho Lab: Gem Hunter

## 1. Giới thiệu

Tài liệu này mô tả cách chuyển đổi bảng lưới (grid) trong trò chơi Gem Hunter sang biểu thức CNF (Conjunctive Normal Form) để giải bằng SAT solver.

Mục tiêu:  
- Mỗi ô `'_'` trong grid đại diện cho biến logic (có thể là bẫy hoặc không bẫy).  
- Các ô có số nguyên (vd: 2) yêu cầu số bẫy trong các ô lân cận đúng bằng giá trị đó.  
- Biểu thức CNF phải thể hiện ràng buộc số lượng bẫy xung quanh mỗi ô số.

---

## 2. Mapping biến

- Mỗi ô `'_'` được đánh số biến logic duy nhất:  
  Biến được đánh số theo công thức:  
  `variable = x * Y_MAX + y + 1`  
  với `x, y` là tọa độ ô, `Y_MAX` là số cột của grid.

- Biến này được lưu trong `self.variable_mapping: Dict[Tuple[int, int], int]` để dễ chuyển đổi.

---

## 3. Ràng buộc CNF cho ô số (Exact trap count)

Giả sử ô `(x, y)` có số `num_traps`. Các ô lân cận `'_'` tương ứng với biến `[v1, v2, ..., vn]`.

### 3.1 At most `num_traps` traps

- Không được có quá `num_traps` bẫy trong các ô lân cận.  
- Điều này thể hiện bằng các clause phủ định (negated literals) của mọi tổ hợp `num_traps + 1` biến.  
- Ví dụ:  
  Với biến `[1, 2, 3]` và `num_traps=1`, tổ hợp `num_traps+1=2` là `(1,2), (1,3), (2,3)`  
  Clause: `[-1, -2]`, `[-1, -3]`, `[-2, -3]`

### 3.2 At least `num_traps` traps

- Ít nhất có `num_traps` bẫy trong các ô lân cận.  
- Thể hiện bằng các clause dương (positive literals) của mọi tổ hợp `len(variables) - num_traps + 1`.  
- Ví dụ:  
  Với biến `[1, 2, 3]` và `num_traps=2`, tổ hợp `len(variables) - num_traps + 1 = 3 - 2 + 1 = 2` là `(1,2), (1,3), (2,3)`  
  Clause: `[1, 2]`, `[1, 3]`, `[2, 3]`

---

## 4. Xử lý các trường hợp đặc biệt

- Nếu không có đủ ô lân cận `'_'` để thoả mãn `num_traps`, bỏ qua (không tạo clause).

---

## 5. Loại bỏ clause trùng lặp

- Các clause có thể trùng do nhiều tổ hợp được sinh ra.  
- Dùng cấu trúc `frozenset` để loại bỏ các clause trùng lặp không phân biệt thứ tự biến hoặc thứ tự clause.

---

## 6. Sử dụng class `CNFGenerator`

- Khởi tạo: `gen = CNFGenerator()`  
- Gọi: `clauses, var_map = gen.generate_cnf(grid)`  
- `clauses` là danh sách clause CNF (list of list of ints)  
- `var_map` là dictionary biến với key `(x, y)` và value là số biến CNF.

---

## 7. Tóm tắt thuật toán

1. Khởi tạo biến cho mỗi ô `'_'`.  
2. Duyệt các ô có số nguyên, lấy biến lân cận.  
3. Sinh clause CNF giới hạn số bẫy bằng `num_traps`.  
4. Loại bỏ clause trùng.  
5. Trả về CNF và biến.
