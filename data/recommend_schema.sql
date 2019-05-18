BEGIN TRANSACTION;
DROP TABLE IF EXISTS "projection";
CREATE TABLE IF NOT EXISTS "projection" (
	"projection_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"party"	TEXT NOT NULL,
	"region"	TEXT NOT NULL,
	"percentage"	REAL NOT NULL
);
DROP TABLE IF EXISTS "intention";
CREATE TABLE IF NOT EXISTS "intention" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"swing_to"	TEXT NOT NULL,
	"region"	TEXT,
	"swing_from"	TEXT NOT NULL,
	"percent"	REAL NOT NULL
);
DROP TABLE IF EXISTS "regions";
CREATE TABLE IF NOT EXISTS "regions" (
	"eu_region"	TEXT NOT NULL UNIQUE,
	"num_seats"	INTEGER NOT NULL,
	"population"	INTEGER NOT NULL,
	"turnout"	REAL NOT NULL,
	PRIMARY KEY("eu_region")
);
DROP INDEX IF EXISTS "postcode_index";
INSERT INTO "regions" VALUES ('South East',10,6433337,36.5),
 ('Yorkshire and the Humber',6,3870749,33.5),
 ('Wales',4,2327175,31.5),
 ('North East',3,1969747,30.9),
 ('North West',8,5237871,33.5),
 ('West Midlands',7,4106375,33.1),
 ('Scotland',6,4010397,33.5),
 ('London',8,6608033,33.3),
 ('South West',6,4062632,37.0),
 ('East of England',7,4385365,35.9),
 ('East Midlands',5,3375669,33.2);
COMMIT;
