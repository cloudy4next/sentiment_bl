class CategoryManager:
    def __init__(self, categories):
        self.categories = categories
    
    def get_categories(self):

        return list(self.categories.keys())
    
    def get_subcategories(self, category):

        return self.categories.get(category, [])

categories = {
    "Network": [
        "Indoor coverage",
        "Outdoor coverage",
        "Voice quality",
        "Call setup",
        "Call Drop",
        "Data speed",
        "Data others",
        "SMS",
        "USSD",
        "Network-others"
    ],
    "Charging/Billing": [
        "Wrong charging",
        "Billing dispute",
        "Charging/Billing-others"
    ],
    "Recharge": [
        "Scratch card",
        "MFS recharge",
        "MyBL recharge",
        "Other recharge",
        "Cashback",
        "Recharge-others"
    ],
    "Product": [
        "Pack related",
        "Balance/data transfer",
        "Loan",
        "Price high than expectation",
        "Product-others"
    ],
    "Service": [
        "SIM sales/activation",
        "MNP",
        "DND",
        "Stop All",
        "MCA",
        "RBT",
        "Orange club",
        "Customer service",
        "Service-others"
    ],
    "MyBL": [
        "App problem",
        "Login/OTP",
        "MyBL-others"
    ],
    "Toffee": [
        "App problem",
        "Login/OTP",
        "Toffee-others"
    ],
    "Others": []
}
