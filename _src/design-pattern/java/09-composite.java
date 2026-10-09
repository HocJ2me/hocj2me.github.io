import java.util.ArrayList;
import java.util.List;

public class CompositeDemo {
    public static void main(String[] args) {
        Folder root = new Folder("du-an-robot");
        Folder src = new Folder("src");
        src.add(new FileItem("main.cpp", 12));
        src.add(new FileItem("motor.cpp", 8));
        Folder docs = new Folder("docs");
        docs.add(new FileItem("bao-cao.pdf", 2048));
        Folder images = new Folder("images");
        images.add(new FileItem("so-do-mach.png", 512));
        docs.add(images);

        root.add(src);
        root.add(docs);
        root.add(new FileItem("README.md", 3));

        // Client gọi CÙNG một phương thức cho file đơn lẻ lẫn cả cây thư mục
        root.print("");
        System.out.println("Tổng dung lượng dự án: " + root.getSize() + " KB");
        System.out.println("Dung lượng thư mục docs: " + docs.getSize() + " KB");
    }
}

/** Component – giao diện chung cho lá (Leaf) và nhánh (Composite). */
interface FileSystemItem {
    String getName();
    int getSize();                 // KB
    void print(String indent);
}

/** Leaf – phần tử không chứa phần tử con. */
class FileItem implements FileSystemItem {
    private final String name;
    private final int size;
    FileItem(String name, int size) { this.name = name; this.size = size; }
    public String getName() { return name; }
    public int getSize()    { return size; }
    public void print(String indent) { System.out.println(indent + "📄 " + name + " (" + size + " KB)"); }
}

/** Composite – chứa danh sách Component con (có thể là Leaf hoặc Composite khác). */
class Folder implements FileSystemItem {
    private final String name;
    private final List<FileSystemItem> children = new ArrayList<>();
    Folder(String name) { this.name = name; }

    void add(FileSystemItem item)    { children.add(item); }
    void remove(FileSystemItem item) { children.remove(item); }

    public String getName() { return name; }

    /** Đệ quy: kích thước thư mục = tổng kích thước các con. */
    public int getSize() {
        int total = 0;
        for (FileSystemItem c : children) total += c.getSize();
        return total;
    }

    public void print(String indent) {
        System.out.println(indent + "📁 " + name + "/ (" + getSize() + " KB)");
        for (FileSystemItem c : children) c.print(indent + "   ");
    }
}
