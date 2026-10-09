public class DecoratorDemo {
    public static void main(String[] args) {
        // Gọi một ly trà sữa cơ bản
        Drink order1 = new MilkTea();
        print(order1);

        // "Bọc" thêm topping – mỗi lớp bọc thêm hành vi + giá tiền
        Drink order2 = new Pearl(new CheeseFoam(new MilkTea()));
        print(order2);

        // Bọc nhiều lần cùng một loại topping cũng được
        Drink order3 = new Pearl(new Pearl(new Pudding(new GreenTea())));
        print(order3);
    }

    static void print(Drink d) {
        System.out.printf("%-55s %,7d đ%n", d.getDescription(), d.cost());
    }
}

/** Component */
interface Drink {
    String getDescription();
    int cost();
}

/** Concrete Components – đồ uống gốc */
class MilkTea implements Drink {
    public String getDescription() { return "Trà sữa"; }
    public int cost()              { return 25_000; }
}
class GreenTea implements Drink {
    public String getDescription() { return "Trà xanh"; }
    public int cost()              { return 20_000; }
}

/** Base Decorator – cùng kiểu Drink VÀ chứa một Drink bên trong */
abstract class ToppingDecorator implements Drink {
    protected final Drink inner;
    ToppingDecorator(Drink inner) { this.inner = inner; }
    public String getDescription() { return inner.getDescription(); }
    public int cost()              { return inner.cost(); }
}

/** Concrete Decorators – thêm hành vi TRƯỚC/SAU khi uỷ quyền cho inner */
class Pearl extends ToppingDecorator {
    Pearl(Drink inner) { super(inner); }
    public String getDescription() { return inner.getDescription() + " + trân châu"; }
    public int cost()              { return inner.cost() + 5_000; }
}
class CheeseFoam extends ToppingDecorator {
    CheeseFoam(Drink inner) { super(inner); }
    public String getDescription() { return inner.getDescription() + " + kem cheese"; }
    public int cost()              { return inner.cost() + 10_000; }
}
class Pudding extends ToppingDecorator {
    Pudding(Drink inner) { super(inner); }
    public String getDescription() { return inner.getDescription() + " + pudding"; }
    public int cost()              { return inner.cost() + 7_000; }
}
