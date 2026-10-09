import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

public class FlyweightDemo {
    public static void main(String[] args) {
        Forest forest = new Forest();
        Random rnd = new Random(42);                 // seed cố định để kết quả lặp lại được
        String[][] kinds = {
                {"Phượng", "đỏ"}, {"Bàng", "xanh đậm"}, {"Thông", "xanh lá"}
        };

        // Trồng 100 000 cây nhưng chỉ có 3 loại cây
        for (int i = 0; i < 100_000; i++) {
            String[] k = kinds[rnd.nextInt(kinds.length)];
            forest.plantTree(rnd.nextInt(1000), rnd.nextInt(1000), k[0], k[1]);
        }

        forest.drawFirst(3);
        System.out.println("Số cây đã trồng          : " + forest.size());
        System.out.println("Số TreeType thực sự tạo  : " + TreeFactory.count());

        long withoutFlyweight = forest.size() * (8L + TreeType.APPROX_BYTES);
        long withFlyweight = forest.size() * 8L + TreeFactory.count() * TreeType.APPROX_BYTES;
        System.out.printf("Bộ nhớ ước tính KHÔNG dùng Flyweight: %,d KB%n", withoutFlyweight / 1024);
        System.out.printf("Bộ nhớ ước tính CÓ dùng Flyweight   : %,d KB%n", withFlyweight / 1024);
    }
}

/** Flyweight – chứa trạng thái NỘI TẠI (intrinsic), dùng chung, bất biến. */
final class TreeType {
    static final int APPROX_BYTES = 2_000;           // giả sử texture/mesh nặng ~2KB
    private final String name;
    private final String color;
    TreeType(String name, String color) { this.name = name; this.color = color; }

    /** Trạng thái NGOẠI TẠI (extrinsic) – x, y – được truyền vào khi dùng. */
    void draw(int x, int y) { System.out.println("  Vẽ cây " + name + " (" + color + ") tại (" + x + ", " + y + ")"); }
}

/** Flyweight Factory – đảm bảo mỗi loại chỉ tạo một lần. */
final class TreeFactory {
    private static final Map<String, TreeType> cache = new HashMap<>();

    static TreeType get(String name, String color) {
        return cache.computeIfAbsent(name + "|" + color, k -> new TreeType(name, color));
    }
    static int count() { return cache.size(); }
}

/** Context – đối tượng nhỏ, chỉ giữ trạng thái ngoại tại + tham chiếu tới flyweight. */
final class Tree {
    private final int x, y;
    private final TreeType type;
    Tree(int x, int y, TreeType type) { this.x = x; this.y = y; this.type = type; }
    void draw() { type.draw(x, y); }
}

/** Client */
final class Forest {
    private final List<Tree> trees = new ArrayList<>();
    void plantTree(int x, int y, String name, String color) {
        trees.add(new Tree(x, y, TreeFactory.get(name, color)));
    }
    void drawFirst(int n) { for (int i = 0; i < n; i++) trees.get(i).draw(); }
    int size() { return trees.size(); }
}
