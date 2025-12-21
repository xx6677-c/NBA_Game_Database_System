-- Add points to User table
ALTER TABLE User ADD COLUMN points INT DEFAULT 0;

-- Add is_claimed to Prediction table
ALTER TABLE Prediction ADD COLUMN is_claimed BOOLEAN DEFAULT FALSE;
