import java.util.List;
import java.util.ArrayList;

public class OrderService {
    private String dbUrl;

    public OrderService(String dbUrl) {
        this.dbUrl = dbUrl;
    }

    public List<String> getOrders(int userId) {
        return new ArrayList<>();
    }

    public boolean placeOrder(int userId, String item) {
        return true;
    }

    private void sendConfirmation(String email) {}
}

class PaymentProcessor {
    public boolean charge(double amount, String card) {
        return true;
    }
}
