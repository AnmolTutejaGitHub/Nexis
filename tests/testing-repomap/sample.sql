CREATE TABLE users (
    id     SERIAL PRIMARY KEY,
    name   VARCHAR(100) NOT NULL,
    email  VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE orders (
    id      SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    total   NUMERIC(10, 2) NOT NULL,
    status  VARCHAR(20) DEFAULT 'pending'
);

CREATE FUNCTION get_user_count()
RETURNS INTEGER AS $$
BEGIN
    RETURN (SELECT COUNT(*) FROM users);
END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION calculate_order_total(p_user_id INTEGER)
RETURNS NUMERIC AS $$
BEGIN
    RETURN (SELECT COALESCE(SUM(total), 0) FROM orders WHERE user_id = p_user_id);
END;
$$ LANGUAGE plpgsql;
