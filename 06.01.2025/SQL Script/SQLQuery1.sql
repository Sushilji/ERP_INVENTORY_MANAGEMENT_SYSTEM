CREATE DATABASE INVENTORY_MANAGEMENT_SYSTEM;
GO



USE INVENTORY_MANAGEMENT_SYSTEM;
GO

USE INVENTORY_MANAGEMENT_SYSTEM;
GO

CREATE TABLE UnitMaster (
    UnitId INT IDENTITY(1,1) PRIMARY KEY,
    UnitName VARCHAR(50) UNIQUE NOT NULL,

    Is_Available BIT DEFAULT 1,
    Is_Removed BIT DEFAULT 0,
    Is_Deleted BIT DEFAULT 0,

    CreatedOn DATETIME DEFAULT GETDATE()
);
GO

SELECT name FROM sys.tables;

USE INVENTORY_MANAGEMENT_SYSTEM;
GO

CREATE TABLE ItemGroupMaster (
    ItemGroupId INT IDENTITY(1,1) PRIMARY KEY,
    ItemGroupName VARCHAR(100) UNIQUE NOT NULL,

    Is_Available BIT DEFAULT 1,
    Is_Removed BIT DEFAULT 0,
    Is_Deleted BIT DEFAULT 0,

    CreatedOn DATETIME DEFAULT GETDATE()
);
GO

USE INVENTORY_MANAGEMENT_SYSTEM;
GO

CREATE TABLE ItemMaster (
    ItemId INT IDENTITY(1,1) PRIMARY KEY,
    ItemName VARCHAR(150) NOT NULL,
    ItemGroupId INT NOT NULL,
    UnitId INT NOT NULL,

    Is_Available BIT DEFAULT 1,
    Is_Removed BIT DEFAULT 0,
    Is_Deleted BIT DEFAULT 0,

    CreatedOn DATETIME DEFAULT GETDATE(),

    FOREIGN KEY (ItemGroupId) REFERENCES ItemGroupMaster(ItemGroupId),
    FOREIGN KEY (UnitId) REFERENCES UnitMaster(UnitId)
);
GO

USE INVENTORY_MANAGEMENT_SYSTEM;
GO

CREATE TABLE VendorMaster (
    VendorId INT IDENTITY(1001,1) PRIMARY KEY,
    VendorName VARCHAR(150) NOT NULL,
    Address VARCHAR(300),
    GSTType VARCHAR(20),
    GSTNo VARCHAR(20),
    ContactNo VARCHAR(20),
    MobileNo VARCHAR(20),
    Email VARCHAR(100),

    Is_Available BIT DEFAULT 1,
    Is_Removed BIT DEFAULT 0,
    Is_Deleted BIT DEFAULT 0,

    CreatedOn DATETIME DEFAULT GETDATE()

);
GO

SELECT name FROM sys.tables;
GO

USE INVENTORY_MANAGEMENT_SYSTEM;
GO

CREATE TABLE CustomerMaster (
    CustomerId INT IDENTITY(2001,1) PRIMARY KEY,
    CustomerType VARCHAR(20), -- Individual / Business
    Salutation VARCHAR(10),
    ContactName VARCHAR(100),
    CompanyName VARCHAR(150),
    DisplayName VARCHAR(150),
    Email VARCHAR(100),
    Phone VARCHAR(20),
    Address VARCHAR(300),
    GSTNo VARCHAR(20),
    PANNo VARCHAR(20),
    Remark VARCHAR(300),

    Is_Available BIT DEFAULT 1,
    Is_Removed BIT DEFAULT 0,
    Is_Deleted BIT DEFAULT 0,

    CreatedOn DATETIME DEFAULT GETDATE()
);
GO

SELECT name FROM sys.tables;
GO

CREATE TABLE DocumentSequence (
    DocType VARCHAR(50) PRIMARY KEY,
    LastNumber INT NOT NULL
);

INSERT INTO DocumentSequence (DocType, LastNumber)
VALUES ('SALES_ORDER', 1000);
GO

USE INVENTORY_MANAGEMENT_SYSTEM;
GO

CREATE TABLE SalesOrder (
    SalesOrderId INT IDENTITY(1,1) PRIMARY KEY,
    SalesOrderNo VARCHAR(20) UNIQUE NOT NULL,
    CustomerId INT NOT NULL,
    Reference VARCHAR(100),
    Status VARCHAR(20),
    Amount DECIMAL(12,2),
    InvoiceNo VARCHAR(20),
    PaymentStatus VARCHAR(20),

    Is_Available BIT DEFAULT 1,
    Is_Removed BIT DEFAULT 0,
    Is_Deleted BIT DEFAULT 0,

    CreatedOn DATETIME DEFAULT GETDATE(),

    FOREIGN KEY (CustomerId) REFERENCES CustomerMaster(CustomerId)
);
GO


CREATE PROCEDURE GetNextSalesOrderNo
    @NextOrderNo VARCHAR(20) OUTPUT
AS
BEGIN
    DECLARE @NextNo INT;

    UPDATE DocumentSequence
    SET LastNumber = LastNumber + 1
    WHERE DocType = 'SALES_ORDER';

    SELECT @NextNo = LastNumber
    FROM DocumentSequence
    WHERE DocType = 'SALES_ORDER';

    SET @NextOrderNo = 'SO-' + CAST(@NextNo AS VARCHAR);
END;
GO

USE INVENTORY_MANAGEMENT_SYSTEM;
GO

ALTER PROCEDURE GetNextSalesOrderNo
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE DocumentSequence
    SET LastNumber = LastNumber + 1
    WHERE DocType = 'SALES_ORDER';

    SELECT 'SO-' + CAST(LastNumber AS VARCHAR(20)) AS SalesOrderNo
    FROM DocumentSequence
    WHERE DocType = 'SALES_ORDER';
END;
GO


USE INVENTORY_MANAGEMENT_SYSTEM;
GO

CREATE TABLE StockMaster (
    ItemId INT PRIMARY KEY,
    Quantity DECIMAL(12,2) NOT NULL,

    Is_Available BIT DEFAULT 1,
    Is_Removed BIT DEFAULT 0,
    Is_Deleted BIT DEFAULT 0,

    UpdatedOn DATETIME DEFAULT GETDATE(),

    FOREIGN KEY (ItemId) REFERENCES ItemMaster(ItemId)
);



CREATE TABLE SalesOrderItem (
    SalesOrderItemId INT IDENTITY(1,1) PRIMARY KEY,
    SalesOrderId INT NOT NULL,
    ItemId INT NOT NULL,
    Quantity DECIMAL(12,2) NOT NULL,
    Rate DECIMAL(12,2) NOT NULL,
    Amount DECIMAL(12,2) NOT NULL,

    CreatedOn DATETIME DEFAULT GETDATE(),

    FOREIGN KEY (SalesOrderId) REFERENCES SalesOrder(SalesOrderId),
    FOREIGN KEY (ItemId) REFERENCES ItemMaster(ItemId)
);
GO

USE INVENTORY_MANAGEMENT_SYSTEM;
GO

CREATE TABLE Purchase (
    PurchaseId INT IDENTITY(1,1) PRIMARY KEY,
    PurchaseNo VARCHAR(20) UNIQUE NOT NULL,
    VendorId INT NOT NULL,
    BillNo VARCHAR(50),
    Amount DECIMAL(12,2),

    CreatedOn DATETIME DEFAULT GETDATE(),

    FOREIGN KEY (VendorId) REFERENCES VendorMaster(VendorId)
);
GO

CREATE TABLE PurchaseItem (
    PurchaseItemId INT IDENTITY(1,1) PRIMARY KEY,
    PurchaseId INT NOT NULL,
    ItemId INT NOT NULL,
    Quantity DECIMAL(12,2) NOT NULL,
    Rate DECIMAL(12,2) NOT NULL,
    Amount DECIMAL(12,2) NOT NULL,

    CreatedOn DATETIME DEFAULT GETDATE(),

    FOREIGN KEY (PurchaseId) REFERENCES Purchase(PurchaseId),
    FOREIGN KEY (ItemId) REFERENCES ItemMaster(ItemId)
);
GO

INSERT INTO DocumentSequence (DocType, LastNumber)
VALUES ('PURCHASE', 500);
GO

CREATE PROCEDURE GetNextPurchaseNo
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE DocumentSequence
    SET LastNumber = LastNumber + 1
    WHERE DocType = 'PURCHASE';

    SELECT 'PO-' + CAST(LastNumber AS VARCHAR(20))
    FROM DocumentSequence
    WHERE DocType = 'PURCHASE';
END;
GO


GO


CREATE PROCEDURE GetNextPurchaseNo
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE DocumentSequence
    SET LastNumber = LastNumber + 1
    WHERE DocType = 'PURCHASE';

    SELECT 'PO-' + CAST(LastNumber AS VARCHAR(20)) AS PurchaseNo
    FROM DocumentSequence
    WHERE DocType = 'PURCHASE';
END;
GO

SELECT name 
FROM sys.procedures
WHERE name = 'GetNextPurchaseNo';
GO

CREATE TABLE RoleMaster (
    RoleId INT IDENTITY(1,1) PRIMARY KEY,
    RoleName VARCHAR(50) UNIQUE NOT NULL,
    Is_Active BIT DEFAULT 1,
    CreatedOn DATETIME DEFAULT GETDATE()
);
GO

INSERT INTO RoleMaster (RoleName)
VALUES ('ADMIN'), ('OPERATOR'), ('VIEWER');
GO

CREATE TABLE UserMaster (
    UserId INT IDENTITY(1,1) PRIMARY KEY,
    UserName VARCHAR(100) NOT NULL,
    Email VARCHAR(150) UNIQUE NOT NULL,
    PasswordHash VARCHAR(200) NOT NULL,
    RoleId INT NOT NULL,

    Is_Active BIT DEFAULT 1,
    Is_Locked BIT DEFAULT 0,
    CreatedOn DATETIME DEFAULT GETDATE(),

    FOREIGN KEY (RoleId) REFERENCES RoleMaster(RoleId)
);
GO

INSERT INTO UserMaster
(UserName, Email, PasswordHash, RoleId)
VALUES
(
    'Sushil Kumar',
    'sushil8916@gmail.com',
    'admin@123',   -- (we will hash later)
    1              -- ADMIN
);
GO

USE INVENTORY_MANAGEMENT_SYSTEM;
GO

UPDATE UserMaster
SET PasswordHash = '$2b$12$UkTlifLewtIKA0nxl5Y4ZOcLj9mr2XY5sTt0njcWFmuQA6.dE/wxW'
WHERE Email = 'sushil8916@gmail.com';
GO

CREATE TABLE RolePermission (
    RolePermissionId INT IDENTITY(1,1) PRIMARY KEY,
    RoleId INT NOT NULL,
    PermissionCode VARCHAR(50) NOT NULL,

    FOREIGN KEY (RoleId) REFERENCES RoleMaster(RoleId)
);
GO

-- ADMIN (all access)
INSERT INTO RolePermission (RoleId, PermissionCode)
SELECT RoleId, PermissionCode
FROM RoleMaster
CROSS JOIN (VALUES
('UNIT_MASTER'),
('ITEM_MASTER'),
('VENDOR'),
('CUSTOMER'),
('SALES'),
('PURCHASE'),
('STOCK'),
('REPORTS'),
('USER_MANAGEMENT')
) P(PermissionCode)
WHERE RoleName = 'ADMIN';
GO

-- OPERATOR
INSERT INTO RolePermission (RoleId, PermissionCode)
SELECT RoleId, PermissionCode
FROM RoleMaster
CROSS JOIN (VALUES
('SALES'),
('PURCHASE'),
('STOCK')
) P(PermissionCode)
WHERE RoleName = 'OPERATOR';
GO

-- VIEWER
INSERT INTO RolePermission (RoleId, PermissionCode)
SELECT RoleId, PermissionCode
FROM RoleMaster
CROSS JOIN (VALUES
('REPORTS')
) P(PermissionCode)
WHERE RoleName = 'VIEWER';
GO

SELECT 
    name AS TriggerName,
    OBJECT_NAME(parent_id) AS TableName
FROM sys.triggers
WHERE parent_id = OBJECT_ID('SalesOrderItem')
   OR parent_id = OBJECT_ID('Stock');


SELECT 
    t.name AS TableName,
    c.name AS ColumnName,
    ty.name AS DataType
FROM sys.tables t
JOIN sys.columns c ON t.object_id = c.object_id
JOIN sys.types ty ON c.user_type_id = ty.user_type_id
WHERE c.name LIKE '%SalesOrder%';

SELECT 
    fk.name AS FK_Name,
    tp.name AS ParentTable,
    cp.name AS ParentColumn,
    tr.name AS ReferencedTable,
    cr.name AS ReferencedColumn
FROM sys.foreign_keys fk
JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
JOIN sys.tables tp ON fkc.parent_object_id = tp.object_id
JOIN sys.columns cp ON fkc.parent_object_id = cp.object_id AND fkc.parent_column_id = cp.column_id
JOIN sys.tables tr ON fkc.referenced_object_id = tr.object_id
JOIN sys.columns cr ON fkc.referenced_object_id = cr.object_id AND fkc.referenced_column_id = cr.column_id
WHERE tp.name = 'SalesOrderItem';

CREATE TABLE Stock (
    StockId INT IDENTITY(1,1) PRIMARY KEY,
    ItemId INT NOT NULL,
    Quantity DECIMAL(18,2) NOT NULL DEFAULT 0,
    Is_Available BIT DEFAULT 1,
    Is_Removed BIT DEFAULT 0,
    Is_Deleted BIT DEFAULT 0,
    CreatedOn DATETIME DEFAULT GETDATE(),

    CONSTRAINT FK_Stock_Item
        FOREIGN KEY (ItemId)
        REFERENCES ItemMaster(ItemId)
);

INSERT INTO Stock (ItemId, Quantity)
SELECT ItemId, 0
FROM ItemMaster
WHERE ItemId NOT IN (SELECT ItemId FROM Stock);


SELECT PurchaseId, PurchaseNo, VendorId, Amount
FROM Purchase;


SELECT name
FROM sys.tables
WHERE name LIKE '%Purcha%';

SELECT name FROM sys.tables WHERE name LIKE '%Vendor%';

ALTER TABLE Purchase
ADD CONSTRAINT FK_Purchase_Vendor
FOREIGN KEY (VendorId)
REFERENCES VendorMaster(VendorId);

SELECT PurchaseId, PurchaseNo, VendorId, Amount, CreatedOn
FROM Purchase;



