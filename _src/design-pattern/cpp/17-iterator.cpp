// Iterator – C++17. Trong C++, iterator là khái niệm cốt lõi của STL:
// chỉ cần cung cấp begin()/end() và một kiểu iterator có *, ++, != là dùng được range-for.
#include <array>
#include <iostream>
#include <string>

struct Song {
    std::string title;
    int minutes;
};

// ConcreteAggregate – lưu trong mảng tĩnh (kiểu bộ đệm vòng/FIFO trên MCU)
template <size_t Capacity>
class Playlist {
public:
    void add(Song s) { if (count_ < Capacity) songs_[count_++] = std::move(s); }

    // ===== ConcreteIterator – duyệt xuôi =====
    class Iterator {
    public:
        Iterator(const Song* p) : p_(p) {}
        const Song& operator*() const { return *p_; }
        Iterator& operator++() { ++p_; return *this; }
        bool operator!=(const Iterator& o) const { return p_ != o.p_; }
    private:
        const Song* p_;
    };
    Iterator begin() const { return Iterator(songs_.data()); }
    Iterator end() const   { return Iterator(songs_.data() + count_); }

    // ===== Iterator kiểu Java (hasNext/next) – duyệt ngược =====
    class ReverseIterator {
    public:
        ReverseIterator(const Playlist& pl) : pl_(pl), index_(int(pl.count_) - 1) {}
        bool hasNext() const { return index_ >= 0; }
        const Song& next() { return pl_.songs_[index_--]; }
    private:
        const Playlist& pl_;
        int index_;
    };
    ReverseIterator reverseIterator() const { return ReverseIterator(*this); }

private:
    std::array<Song, Capacity> songs_{};      // client không bao giờ thấy mảng này
    size_t count_ = 0;
};

int main() {
    Playlist<5> playlist;
    playlist.add({"Lạc Trôi", 4});
    playlist.add({"Nơi này có anh", 5});
    playlist.add({"Hãy trao cho anh", 4});
    playlist.add({"See tình", 3});

    std::cout << "Phát theo thứ tự (range-for dùng begin()/end()):\n";
    for (const Song& s : playlist) std::cout << "  ▶ " << s.title << " (" << s.minutes << "')\n";

    std::cout << "Phát ngược:\n";
    auto rev = playlist.reverseIterator();
    while (rev.hasNext()) {
        const Song& s = rev.next();
        std::cout << "  ◀ " << s.title << " (" << s.minutes << "')\n";
    }

    int total = 0;
    for (auto it = playlist.begin(); it != playlist.end(); ++it) total += (*it).minutes;
    std::cout << "Tổng thời lượng: " << total << " phút\n";
}
