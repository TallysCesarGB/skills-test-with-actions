from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class CustomerData:
    name: str
    cpf: str
    email: str
    phone: str


@dataclass(frozen=True)
class Address:
    street: str
    number: str
    city: str
    state: str


@dataclass(frozen=True)
class OrderItem:
    product: str
    price: float
    quantity: int


class Reportable(ABC):
    @abstractmethod
    def generate_report(self) -> None: ...


class PaymentStrategy(ABC): 
    @abstractmethod
    def process(self, total: float) -> None: ...


class NotificationService(ABC): 
    @abstractmethod
    def send(self, recipient: str, message: str) -> None: ...


class Person:
    def __init__(self, name: str, cpf: str):
        self.name = name
        self.cpf = cpf


class Employee(Person, Reportable):
    def generate_report(self) -> None:
        print(f"Relatório do funcionário: {self.name}")


class Customer(Person):
    def __init__(self, data: CustomerData, address: Address):
        super().__init__(data.name, data.cpf)
        self.data = data
        self.address = address


class PixPayment(PaymentStrategy):
    def process(self, total: float) -> None:
        print(f"Pagamento PIX: R$ {total:.2f}")


class CardPayment(PaymentStrategy):
    def process(self, total: float) -> None:
        print(f"Pagamento Cartão: R$ {total:.2f}")


class BoletoPayment(PaymentStrategy):
    def process(self, total: float) -> None:
        print(f"Pagamento Boleto: R$ {total:.2f}")


class EmailNotificationService(NotificationService):
    def send(self, recipient: str, message: str) -> None:
        print(f"Email para {recipient}: {message}")


class InvoiceService: 
    def generate(self, customer: Customer, total: float) -> None:
        print(f"NF gerada — {customer.name} | R$ {total:.2f}")


class InventoryService: 
    def update(self, items: List[OrderItem]) -> None:
        print(f"Estoque atualizado: {len(items)} item(ns)")


class AuditService: 
    def register(self, customer: Customer, total: float) -> None:
        print(f"Auditoria: {customer.name} | R$ {total:.2f}")


class FinancialReportService: 
    def generate(self, total: float) -> None:
        print(f"Relatório financeiro: R$ {total:.2f}")


class OrderHistoryService: 
    def save(self, customer: Customer, total: float) -> None:
        print(f"Histórico salvo: {customer.name} | R$ {total:.2f}")


class ShippingService: 
    def notify(self, customer: Customer) -> None:
        print(f"Transportadora notificada: {customer.name}")


class CustomerReportService:
    def _format(self, customer: Customer) -> str:
        return f"{customer.name} | CPF: {customer.cpf}"

    def print_customer(self, customer: Customer) -> None:
        print(self._format(customer))

    def validate_customer(self, customer: Customer) -> None:
        # Validação real aqui; formatação vem de _format()
        print(f"Validando: {self._format(customer)}")

    def export_customer(self, customer: Customer) -> None:
        print(f"Exportando: {self._format(customer)}")


class Order:
    def __init__(
        self,
        notification: NotificationService,
        invoice: InvoiceService,
        inventory: InventoryService,
        audit: AuditService,
        financial: FinancialReportService,
        history: OrderHistoryService,
        shipping: ShippingService,
    ):
        self._notification = notification
        self._invoice = invoice
        self._inventory = inventory
        self._audit = audit
        self._financial = financial
        self._history = history
        self._shipping = shipping

    def _calculate_total(self, items: List[OrderItem]) -> float: 
        return sum(item.price * item.quantity for item in items)

    def process(
        self,
        customer: Customer,
        items: List[OrderItem],
        payment: PaymentStrategy, 
    ) -> None:
        total = self._calculate_total(items)

        payment.process(total)
        self._notification.send(customer.data.email, f"Pedido confirmado: R$ {total:.2f}")
        self._invoice.generate(customer, total)
        self._inventory.update(items)
        self._audit.register(customer, total)
        self._financial.generate(total)
        self._history.save(customer, total)
        self._shipping.notify(customer)


# if __name__ == "__main__":
#     customer = Customer(
#         data=CustomerData(
#             name="Ana Lima",
#             cpf="123.456.789-00",
#             email="ana@email.com",
#             phone="84 99999-0000",
#         ),
#         address=Address(
#             street="Rua das Flores",
#             number="42",
#             city="Caicó",
#             state="RN",
#         ),
#     )

#     items = [
#         OrderItem(product="Notebook", price=3500.00, quantity=1),
#         OrderItem(product="Mouse",    price=120.00,  quantity=2),
#     ]

#     order = Order(
#         notification=EmailNotificationService(),
#         invoice=InvoiceService(),
#         inventory=InventoryService(),
#         audit=AuditService(),
#         financial=FinancialReportService(),
#         history=OrderHistoryService(),
#         shipping=ShippingService(),
#     )

#     order.process(customer, items, payment=PixPayment())