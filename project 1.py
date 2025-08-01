# Tải dữ liệu từ GitHub
wget https://raw.githubusercontent.com/yinghaoz1/tmdb-movie-dataset-analysis/master/tmdb-movies.csv


# 1. Sắp xếp các bộ phim theo ngày phát hành giảm dần rồi lưu ra một file mới (cột 16)
(head -1 tmdb-movies.csv && tail -n +2 tmdb-movies.csv | sort -t',' -k16,16r) > movies_sorted_by_date.csv
echo "1. Sắp xếp phim theo ngày phát hành (đã lưu vào movies_sorted_by_date.csv)"

# 2. Lọc ra các bộ phim có đánh giá trung bình trên 7.5 rồi lưu ra một file mới(cột 18)
# Sử dụng awk để xử lý đúng các trường có dấu phẩy
awk -F',' 'NR==1 || $18 > 7.5' tmdb-movies.csv > high_rated_movies.csv
echo "2. Lọc phim có điểm > 7.5 (đã lưu vào high_rated_movies.csv)"

# 3. Tìm ra phim nào có doanh thu cao nhất và doanh thu thấp nhất (cột 5)
echo "3.1. Phim có doanh thu cao nhất:"
tail -n +2 tmdb-movies.csv | awk -F',' '{print $5 "\t" $6}' | sort -k1,1nr | head -1

echo "3.2. Phim có doanh thu thấp nhất (loại bỏ giá trị 0):"
tail -n +2 tmdb-movies.csv | awk -F',' '$5 ~ /^[0-9]+$/ && $5 > 0 {print $5 "\t" $6}' | sort -k1,1n | head -1

# 4. Tính tổng doanh thu tất cả các bộ phim (cột 5)
echo "4. Tổng doanh thu tất cả các bộ phim:"
tail -n +2 tmdb-movies.csv | awk -F',' '{s+=$5} END{print s}'

# 5. Top 10 bộ phim đem về lợi nhuận cao nhất 
echo "5. Top 10 phim có lợi nhuận cao nhất:"
tail -n +2 tmdb-movies.csv | awk -F',' '{
    profit = $5 - $4
    if(profit > 0) print $6 "\t" profit
}' | sort -k2,2nr | head -10

# 6. Đạo diễn có nhiều bộ phim nhất (cột 8) và diễn viên đóng nhiều phim nhất (cột 7)
echo "6.1. Đạo diễn có nhiều phim nhất:"
awk -F',' 'NR>1 {print $8}' tmdb-movies.csv | tr '|' '\n' | grep -v '^$' | sort | uniq -c | sort -nr | head -1

echo "6.2. Diễn viên đóng nhiều phim nhất:"
awk -F',' 'NR>1 {print $7}' tmdb-movies.csv | tr '|' '\n' | grep -v '^$' | sort | uniq -c | sort -nr | head -1

# 7. Thống kê số lượng phim theo thể loại (cột 19)
echo "7. Thống kê số lượng phim theo thể loại:"
awk -F',' 'NR>1 && $19 ~ /[A-Za-z]/ {print $19}' tmdb-movies.csv | \
  tr '|' '\n' | \
  grep -E '^(Drama|Comedy|Action|Thriller|Romance|Adventure|Horror|Family|Science Fiction|Crime|Fantasy|Animation|Mystery|History|Music|War|Western|Documentary|Foreign)$' | \
  sort | uniq -c | sort -nr