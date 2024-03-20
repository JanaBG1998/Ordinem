BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "buch" (
	"ID"	INTEGER,
	"buchtitel"	TEXT NOT NULL,
	PRIMARY KEY("ID" AUTOINCREMENT)
);
INSERT INTO "buch" VALUES (1,'Harry Potter');
INSERT INTO "buch" VALUES (2,'Potter Harry');
INSERT INTO "buch" VALUES (3,'Harry Potter');
INSERT INTO "buch" VALUES (4,'Potter Harry');
INSERT INTO "buch" VALUES (5,'Harry Potter');
INSERT INTO "buch" VALUES (6,'Potter Harry');
INSERT INTO "buch" VALUES (7,'Harry Potter');
INSERT INTO "buch" VALUES (8,'Potter Harry');
INSERT INTO "buch" VALUES (9,'Harry Potter');
INSERT INTO "buch" VALUES (10,'Potter Harry');
INSERT INTO "buch" VALUES (11,'Harry Potter');
INSERT INTO "buch" VALUES (12,'Potter Harry');
INSERT INTO "buch" VALUES (13,'Harry Potter');
INSERT INTO "buch" VALUES (14,'Potter Harry');
INSERT INTO "buch" VALUES (15,'Harry Potter');
INSERT INTO "buch" VALUES (16,'Potter Harry');
INSERT INTO "buch" VALUES (17,'Harry Potter');
INSERT INTO "buch" VALUES (18,'Potter Harry');
INSERT INTO "buch" VALUES (19,'Harry Potter');
INSERT INTO "buch" VALUES (20,'Potter Harry');
COMMIT;
