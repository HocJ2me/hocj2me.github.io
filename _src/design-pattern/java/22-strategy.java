import java.util.function.IntUnaryOperator;

public class StrategyDemo {
    public static void main(String[] args) {
        ShoppingCart cart = new ShoppingCart();
        cart.addItem("Arduino Uno R3", 180_000);
        cart.addItem("Bộ cảm biến 37 món", 320_000);

        // Đổi thuật toán thanh toán lúc chạy (runtime) mà không sửa ShoppingCart
        cart.checkout(new CashPayment());
        cart.checkout(new CardPayment("4111-2222-3333-4444"));
        cart.checkout(new MomoPayment("0359 581 461"));

        // Với Java 8+, strategy đơn giản có thể là lambda (functional interface)
        System.out.println("-- Chiến lược giảm giá dạng lambda --");
        IntUnaryOperator noDiscount = p -> p;
        IntUnaryOperator studentDiscount = p -> p * 90 / 100;
        IntUnaryOperator blackFriday = p -> Math.max(0, p - 100_000);
        System.out.printf("Giá gốc: %,d | HS-SV: %,d | Black Friday: %,d%n",
                cart.total(noDiscount), cart.total(studentDiscount), cart.total(blackFriday));
    }
}

/** Strategy */
interface PaymentStrategy {
    String name();
    int fee(int amount);                 // mỗi phương thức có cách tính phí riêng
    void pay(int amount);
}

/** ConcreteStrategies */
class CashPayment implements PaymentStrategy {
    public String name() { return "Tiền mặt"; }
    public int fee(int amount) { return 0; }
    public void pay(int amount) { System.out.printf("   💵 Thanh toán tiền mặt khi nhận hàng: %,d đ%n", amount); }
}
class CardPayment implements PaymentStrategy {
    private final String cardNumber;
    CardPayment(String n) { cardNumber = n; }
    public String name() { return "Thẻ"; }
    public int fee(int amount) { return amount * 2 / 100; }          // phí 2%
    public void pay(int amount) {
        System.out.printf("   💳 Trừ %,d đ từ thẻ ****%s%n", amount, cardNumber.substring(cardNumber.length() - 4));
    }
}
class MomoPayment implements PaymentStrategy {
    private final String phone;
    MomoPayment(String p) { phone = p; }
    public String name() { return "MoMo"; }
    public int fee(int amount) { return 1_000; }                      // phí cố định
    public void pay(int amount) { System.out.printf("   📱 Gửi yêu cầu %,d đ tới ví MoMo %s%n", amount, phone); }
}

/** Context */
class ShoppingCart {
    private int subtotal = 0;
    void addItem(String name, int price) { subtotal += price; }

    void checkout(PaymentStrategy strategy) {
        int total = subtotal + strategy.fee(subtotal);
        System.out.printf("Thanh toán bằng %-9s (phí %,6d đ)%n", strategy.name(), strategy.fee(subtotal));
        strategy.pay(total);
    }
    int total(IntUnaryOperator discount) { return discount.applyAsInt(subtotal); }
}
