-- -------------------------------------------------------------
-- TablePlus 3.12.0(354)
--
-- https://tableplus.com/
--
-- Database: kbpartpicker
-- Generation Time: 2021-01-02 21:49:44.2220
-- -------------------------------------------------------------


-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS country_id_seq;

-- Table Definition
CREATE TABLE "public"."country" (
    "id" int4 NOT NULL DEFAULT nextval('country_id_seq'::regclass),
    "country_name" varchar NOT NULL,
    "country_code" int4,
    "iso_code" varchar,
    "currency_code" varchar,
    "exchange_rate" float8,
    "created_at" timestamp NOT NULL,
    "updated_at" timestamp NOT NULL,
    PRIMARY KEY ("id")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS switches_id_seq;

-- Table Definition
CREATE TABLE "public"."products" (
    "id" int4 NOT NULL DEFAULT nextval('switches_id_seq'::regclass),
    "name" varchar NOT NULL,
    "img_url" varchar,
    "type" int4 NOT NULL,
    "size" int4,
    "layout" int4,
    "hotswap" bool,
    "created_at" timestamp NOT NULL,
    "updated_at" timestamp NOT NULL,
    PRIMARY KEY ("id")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS vendor_product_association_id_seq;

-- Table Definition
CREATE TABLE "public"."vendor_product_associations" (
    "id" int4 NOT NULL DEFAULT nextval('vendor_product_association_id_seq'::regclass),
    "product_id" int4 NOT NULL,
    "vendor_id" int4 NOT NULL,
    "in_stock" bool,
    "price" float8,
    "url" varchar,
    "created_at" timestamp NOT NULL,
    "updated_at" timestamp NOT NULL,
    PRIMARY KEY ("id")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS vendors_id_seq;

-- Table Definition
CREATE TABLE "public"."vendors" (
    "id" int4 NOT NULL DEFAULT nextval('vendors_id_seq'::regclass),
    "name" varchar NOT NULL,
    "url" varchar NOT NULL,
    "created_at" timestamp NOT NULL,
    "updated_at" timestamp NOT NULL,
    "country_id" int4,
    PRIMARY KEY ("id")
);

ALTER TABLE "public"."vendor_product_associations" ADD FOREIGN KEY ("product_id") REFERENCES "public"."products"("id");
ALTER TABLE "public"."vendor_product_associations" ADD FOREIGN KEY ("vendor_id") REFERENCES "public"."vendors"("id");
ALTER TABLE "public"."vendors" ADD FOREIGN KEY ("country_id") REFERENCES "public"."country"("id");
