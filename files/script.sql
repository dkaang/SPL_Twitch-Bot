CREATE TABLE IF NOT EXISTS users (
    UserID text PRIMARY KEY,
    MessagesSent integer DEFAULT 0,
    Coins integer DEFAULT 0, -- economy
    CoinLock text DEFAULT CURRENT_TIMESTAMP -- spam filter to not get inifinite coins
);

CREATE TABLE IF NOT EXISTS cooldowns (
    UserID text PRIMARY KEY, 
    LastCoinFlip TIMESTAMP DEFAULT 0
);