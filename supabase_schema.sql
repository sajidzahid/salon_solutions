create table if not exists branches (
    branch_id bigserial primary key,
    branch_name text not null unique
);

create table if not exists roles (
    role_id bigserial primary key,
    role_name text not null unique
);

create table if not exists service_categories (
    category_id bigserial primary key,
    category_name text not null unique
);

create table if not exists inventory_categories (
    category_id bigserial primary key,
    category_name text not null unique
);

create table if not exists brands (
    brand_id bigserial primary key,
    brand_name text not null unique
);

create table if not exists customers (
    customer_id bigserial primary key,
    customer_code text not null unique,
    customer_name text not null,
    phone text,
    email text,
    gender text,
    dob date,
    address text,
    referred_by text
);

create table if not exists staff (
    staff_id bigserial primary key,
    staff_name text not null,
    phone text,
    email text,
    gender text,
    status text
);

create table if not exists services (
    service_id bigserial primary key,
    category_id bigint references service_categories(category_id),
    service_name text not null,
    sale_price numeric(12,2) not null default 0,
    duration_minutes integer not null default 0
);

create table if not exists products (
    product_id bigserial primary key,
    category_id bigint references inventory_categories(category_id),
    brand_id bigint references brands(brand_id),
    product_name text not null,
    cost_price numeric(12,2) not null default 0,
    sale_price numeric(12,2) not null default 0,
    stock_qty integer not null default 0,
    minimum_stock integer not null default 0
);

create table if not exists users (
    user_id bigserial primary key,
    branch_id bigint references branches(branch_id),
    role_id bigint references roles(role_id),
    username text not null unique,
    email text,
    password_hash text not null,
    status text not null default 'Active'
);

create table if not exists appointments (
    appointment_id bigserial primary key,
    customer_id bigint references customers(customer_id),
    staff_id bigint references staff(staff_id),
    appointment_date date not null,
    appointment_time time not null,
    status text not null
);

create table if not exists bills (
    bill_id bigserial primary key,
    bill_no text not null unique,
    customer_id bigint references customers(customer_id),
    user_id bigint references users(user_id),
    bill_date timestamp not null default now(),
    subtotal numeric(12,2) not null default 0,
    discount numeric(12,2) not null default 0,
    tax numeric(12,2) not null default 0,
    grand_total numeric(12,2) not null default 0,
    payment_method text not null
);

create table if not exists bill_details (
    detail_id bigserial primary key,
    bill_id bigint not null references bills(bill_id) on delete cascade,
    service_id bigint references services(service_id),
    staff_id bigint references staff(staff_id),
    quantity integer not null default 1,
    price numeric(12,2) not null default 0,
    line_total numeric(12,2) not null default 0
);
