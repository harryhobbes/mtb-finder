-- ALTER TABLE deal 
-- ADD COLUMN lowest_deal_text text;

CREATE TABLE website (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  base_url TEXT NOT NULL,
  css_selector TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES user (id)
);

ALTER TABLE deal
ADD COLUMN website_id INTEGER NOT NULL DEFAULT '';
ADD COLUMN access INTEGER NOT NULL DEFAULT '';

ALTER TABLE user
ADD COLUMN slack_api_key TEXT;

CREATE TABLE deal_comms (
    deal_id INTEGER PRIMARY KEY,
    user_id INTEGER PRIMARY KEY,
    comms_type TEXT NOT NULL DEFAULT 'ALL',
    FOREIGN KEY (deal_id) REFERENCES deal (id),
    FOREIGN KEY (user_id) REFERENCES user (id)
);