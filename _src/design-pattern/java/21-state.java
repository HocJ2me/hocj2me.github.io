public class StateDemo {
    public static void main(String[] args) {
        VendingMachine vm = new VendingMachine(2);   // còn 2 chai nước

        vm.pressButton();          // chưa bỏ tiền
        vm.insertCoin();
        vm.insertCoin();           // bỏ tiền 2 lần
        vm.pressButton();          // nhận nước

        vm.insertCoin();
        vm.ejectCoin();            // đổi ý, lấy lại tiền

        vm.insertCoin();
        vm.pressButton();          // chai cuối cùng -> hết hàng
        vm.insertCoin();           // máy hết hàng, từ chối
        vm.refill(5);
        vm.insertCoin();
    }
}

/** State – mỗi hành động của người dùng là một phương thức. */
interface State {
    void insertCoin(VendingMachine m);
    void ejectCoin(VendingMachine m);
    void pressButton(VendingMachine m);
    String name();
}

/** Context – uỷ quyền mọi hành vi cho đối tượng trạng thái hiện tại. */
class VendingMachine {
    private State state;
    private int stock;

    VendingMachine(int stock) {
        this.stock = stock;
        this.state = stock > 0 ? new NoCoinState() : new SoldOutState();
    }

    void insertCoin()  { log("Bỏ tiền");     state.insertCoin(this); }
    void ejectCoin()   { log("Trả tiền");    state.ejectCoin(this); }
    void pressButton() { log("Bấm nút");     state.pressButton(this); }
    void refill(int n) { stock += n; System.out.println("🔧 Nạp thêm " + n + " chai"); setState(new NoCoinState()); }

    void setState(State s) { System.out.println("     ↳ chuyển trạng thái: " + state.name() + " → " + s.name()); state = s; }
    int getStock()         { return stock; }
    void releaseProduct()  { stock--; System.out.println("     🥤 Rơi ra 1 chai nước (còn " + stock + ")"); }
    private void log(String a) { System.out.println("[" + state.name() + "] " + a); }
}

/** ConcreteStates – không có if/else theo trạng thái trong Context nữa! */
class NoCoinState implements State {
    public void insertCoin(VendingMachine m)  { System.out.println("     Đã nhận tiền"); m.setState(new HasCoinState()); }
    public void ejectCoin(VendingMachine m)   { System.out.println("     Bạn chưa bỏ tiền"); }
    public void pressButton(VendingMachine m) { System.out.println("     Vui lòng bỏ tiền trước"); }
    public String name() { return "Chờ tiền"; }
}

class HasCoinState implements State {
    public void insertCoin(VendingMachine m)  { System.out.println("     Đã có tiền rồi, không nhận thêm"); }
    public void ejectCoin(VendingMachine m)   { System.out.println("     Trả lại tiền"); m.setState(new NoCoinState()); }
    public void pressButton(VendingMachine m) {
        m.releaseProduct();
        m.setState(m.getStock() > 0 ? new NoCoinState() : new SoldOutState());
    }
    public String name() { return "Đã có tiền"; }
}

class SoldOutState implements State {
    public void insertCoin(VendingMachine m)  { System.out.println("     Hết hàng! Trả lại tiền"); }
    public void ejectCoin(VendingMachine m)   { System.out.println("     Không có tiền để trả"); }
    public void pressButton(VendingMachine m) { System.out.println("     Hết hàng"); }
    public String name() { return "Hết hàng"; }
}
