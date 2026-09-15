CREATE TABLE ShoppingCartProducts (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    ShoppingCartId INTEGER NOT NULL,
    ProductId INTEGER NOT NULL,
    Quantity INTEGER NOT NULL,
    Amount REAL NOT NULL,
    FOREIGN KEY (ShoppingCartId) REFERENCES ShoppingCart(Id),
    FOREIGN KEY (ProductId) REFERENCES Products(Id)
);