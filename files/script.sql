CREATE TABLE IF NOT EXISTS users (
    UserID text PRIMARY KEY,
    MessagesSent integer DEFAULT 0,
    Coins integer DEFAULT 0, -- economy
    CoinLock text DEFAULT CURRENT_TIMESTAMP -- spam filter to not get inifinite coins
);