CREATE TABLE `Products`(
    `Id` CHAR(36) NOT NULL,
    `Code` VARCHAR(255) NOT NULL,
    `Name` VARCHAR(255) NOT NULL,
    `Price` DECIMAL(8, 2) NOT NULL,
    `EntryDate` DATETIME NOT NULL,
    `Brand` VARCHAR(255) NOT NULL,
    `Stock` DECIMAL(8, 2) NOT NULL,
    PRIMARY KEY(`Id`)
);
ALTER TABLE
    `Products` ADD UNIQUE `products_code_unique`(`Code`);
CREATE TABLE `Invoices`(
    `Id` CHAR(36) NOT NULL,
    `Number` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `Date` DATE NOT NULL,
    `BuyerEmail` VARCHAR(255) NOT NULL,
    `TotalAmount` DECIMAL(8, 2) NOT NULL,
    PRIMARY KEY(`Id`)
);
CREATE TABLE `ProductsPerInvoice`(
    `id` CHAR(36) NOT NULL,
    `InvoiceId` CHAR(36) NOT NULL,
    `ProductId` CHAR(36) NOT NULL,
    `Quantity` DECIMAL(8, 2) NOT NULL,
    `TotalAmount` DECIMAL(8, 2) NOT NULL,
    PRIMARY KEY(`id`)
);
CREATE TABLE `ShoppingCart`(
    `Id` CHAR(36) NOT NULL,
    `BuyerEmail` VARCHAR(255) NOT NULL,
    `TotalAmount` DECIMAL(8, 2) NOT NULL,
    PRIMARY KEY(`Id`)
);
CREATE TABLE `ShoppingCartProducts`(
    `Id` CHAR(36) NOT NULL,
    `ShoppingCartId` CHAR(36) NOT NULL,
    `ProductId` CHAR(36) NOT NULL,
    `Quantity` DECIMAL(8, 2) NOT NULL,
    `Amount` DECIMAL(8, 2) NOT NULL,
    PRIMARY KEY(`Id`)
);
ALTER TABLE
    `ShoppingCartProducts` ADD CONSTRAINT `shoppingcartproducts_productid_foreign` FOREIGN KEY(`ProductId`) REFERENCES `Products`(`Id`);
ALTER TABLE
    `ProductsPerInvoice` ADD CONSTRAINT `productsperinvoice_invoiceid_foreign` FOREIGN KEY(`InvoiceId`) REFERENCES `Invoices`(`Id`);
ALTER TABLE
    `ProductsPerInvoice` ADD CONSTRAINT `productsperinvoice_productid_foreign` FOREIGN KEY(`ProductId`) REFERENCES `Products`(`Id`);
ALTER TABLE
    `ShoppingCartProducts` ADD CONSTRAINT `shoppingcartproducts_shoppingcartid_foreign` FOREIGN KEY(`ShoppingCartId`) REFERENCES `ShoppingCart`(`Id`);