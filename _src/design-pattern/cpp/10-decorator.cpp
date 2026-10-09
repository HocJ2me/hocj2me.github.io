// Decorator – C++17
#include <cstdio>
#include <memory>
#include <string>

// ===== Component =====
class Drink {
public:
    virtual ~Drink() = default;
    virtual std::string getDescription() const = 0;
    virtual int cost() const = 0;
};

// ===== Concrete Components =====
class MilkTea : public Drink {
public:
    std::string getDescription() const override { return "Trà sữa"; }
    int cost() const override { return 25000; }
};
class GreenTea : public Drink {
public:
    std::string getDescription() const override { return "Trà xanh"; }
    int cost() const override { return 20000; }
};

// ===== Base Decorator: LÀ một Drink và CÓ một Drink =====
class ToppingDecorator : public Drink {
public:
    explicit ToppingDecorator(std::unique_ptr<Drink> inner) : inner_(std::move(inner)) {}
    std::string getDescription() const override { return inner_->getDescription(); }
    int cost() const override { return inner_->cost(); }
protected:
    std::unique_ptr<Drink> inner_;                   // decorator sở hữu đối tượng được bọc
};

// ===== Concrete Decorators =====
class Pearl : public ToppingDecorator {
public:
    using ToppingDecorator::ToppingDecorator;
    std::string getDescription() const override { return inner_->getDescription() + " + trân châu"; }
    int cost() const override { return inner_->cost() + 5000; }
};
class CheeseFoam : public ToppingDecorator {
public:
    using ToppingDecorator::ToppingDecorator;
    std::string getDescription() const override { return inner_->getDescription() + " + kem cheese"; }
    int cost() const override { return inner_->cost() + 10000; }
};
class Pudding : public ToppingDecorator {
public:
    using ToppingDecorator::ToppingDecorator;
    std::string getDescription() const override { return inner_->getDescription() + " + pudding"; }
    int cost() const override { return inner_->cost() + 7000; }
};

void print(const Drink& d) { std::printf("%7d đ  %s\n", d.cost(), d.getDescription().c_str()); }

int main() {
    using std::make_unique;
    auto order1 = make_unique<MilkTea>();
    print(*order1);

    std::unique_ptr<Drink> order2 = make_unique<Pearl>(make_unique<CheeseFoam>(make_unique<MilkTea>()));
    print(*order2);

    std::unique_ptr<Drink> order3 =
        make_unique<Pearl>(make_unique<Pearl>(make_unique<Pudding>(make_unique<GreenTea>())));
    print(*order3);
}
