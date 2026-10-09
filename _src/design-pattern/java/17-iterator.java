import java.util.Iterator;
import java.util.NoSuchElementException;

public class IteratorDemo {
    public static void main(String[] args) {
        Playlist playlist = new Playlist(5);
        playlist.add(new Song("Lạc Trôi", 4));
        playlist.add(new Song("Nơi này có anh", 5));
        playlist.add(new Song("Hãy trao cho anh", 4));
        playlist.add(new Song("See tình", 3));

        // 1. Duyệt bằng Iterator tường minh
        System.out.println("Phát theo thứ tự:");
        Iterator<Song> it = playlist.iterator();
        while (it.hasNext()) System.out.println("  ▶ " + it.next());

        // 2. Duyệt ngược – một kiểu iterator khác trên CÙNG một collection
        System.out.println("Phát ngược:");
        Iterator<Song> rev = playlist.reverseIterator();
        while (rev.hasNext()) System.out.println("  ◀ " + rev.next());

        // 3. Vì Playlist implements Iterable nên dùng được for-each
        int total = 0;
        for (Song s : playlist) total += s.minutes();
        System.out.println("Tổng thời lượng: " + total + " phút");
    }
}

record Song(String title, int minutes) {
    public String toString() { return title + " (" + minutes + "')"; }
}

/** ConcreteAggregate – cấu trúc lưu trữ bên trong (mảng) được che giấu khỏi client. */
class Playlist implements Iterable<Song> {
    private final Song[] songs;
    private int count = 0;

    Playlist(int capacity) { songs = new Song[capacity]; }
    void add(Song s) { songs[count++] = s; }

    /** Factory method tạo ConcreteIterator. */
    @Override
    public Iterator<Song> iterator() { return new ForwardIterator(); }
    public Iterator<Song> reverseIterator() { return new ReverseIterator(); }

    /** ConcreteIterator – giữ vị trí duyệt hiện tại. */
    private class ForwardIterator implements Iterator<Song> {
        private int index = 0;
        public boolean hasNext() { return index < count; }
        public Song next() {
            if (!hasNext()) throw new NoSuchElementException();
            return songs[index++];
        }
    }

    private class ReverseIterator implements Iterator<Song> {
        private int index = count - 1;
        public boolean hasNext() { return index >= 0; }
        public Song next() {
            if (!hasNext()) throw new NoSuchElementException();
            return songs[index--];
        }
    }
}
