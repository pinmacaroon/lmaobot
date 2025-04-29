-- initialize economy for server
BEGIN;
CREATE TABLE MemberWallets (
    id INTEGER NOT NULL,
    funds BIGINT DEFAULT 0,
    multiplier INT DEFAULT 0
);
COMMIT;