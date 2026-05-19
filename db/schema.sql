CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(80) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX ix_users_username ON users (username);

CREATE TABLE migraine_events (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  event_date DATE NOT NULL,
  event_time TIME NOT NULL,
  duration_minutes INTEGER,
  event_type VARCHAR(40) NOT NULL,
  aura_intensity INTEGER NOT NULL,
  headache_intensity INTEGER NOT NULL,
  headache_started_after_minutes INTEGER,
  numbness BOOLEAN NOT NULL DEFAULT FALSE,
  speech_problems BOOLEAN NOT NULL DEFAULT FALSE,
  weakness BOOLEAN NOT NULL DEFAULT FALSE,
  confusion BOOLEAN NOT NULL DEFAULT FALSE,
  unusual_event BOOLEAN NOT NULL DEFAULT FALSE,
  identical_to_usual_pattern BOOLEAN NOT NULL DEFAULT TRUE,
  notes TEXT,
  possible_trigger_notes TEXT,
  created_at TIMESTAMPTZ NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX ix_migraine_events_user_id ON migraine_events (user_id);
CREATE INDEX ix_migraine_events_event_date ON migraine_events (event_date);

CREATE TABLE event_visual_symptoms (
  event_id INTEGER NOT NULL REFERENCES migraine_events(id),
  symptom VARCHAR(40) NOT NULL,
  PRIMARY KEY (event_id, symptom)
);

CREATE TABLE trigger_contexts (
  id SERIAL PRIMARY KEY,
  event_id INTEGER NOT NULL UNIQUE REFERENCES migraine_events(id),
  sleep_hours NUMERIC(3, 1),
  sleep_quality INTEGER,
  interrupted_sleep BOOLEAN NOT NULL DEFAULT FALSE,
  daytime_nap BOOLEAN NOT NULL DEFAULT FALSE,
  hydration_level VARCHAR(20) NOT NULL DEFAULT 'normal',
  caffeine_count INTEGER NOT NULL DEFAULT 0,
  caffeine_type VARCHAR(80),
  stress_level INTEGER,
  illness_type VARCHAR(40) NOT NULL DEFAULT 'none',
  screen_time_level VARCHAR(20) NOT NULL DEFAULT 'medium'
);

CREATE TABLE trigger_meal_flags (
  context_id INTEGER NOT NULL REFERENCES trigger_contexts(id),
  flag VARCHAR(40) NOT NULL,
  PRIMARY KEY (context_id, flag)
);

CREATE TABLE recovery_data (
  id SERIAL PRIMARY KEY,
  event_id INTEGER NOT NULL UNIQUE REFERENCES migraine_events(id),
  fatigue_after BOOLEAN NOT NULL DEFAULT FALSE,
  brain_fog BOOLEAN NOT NULL DEFAULT FALSE,
  irritability BOOLEAN NOT NULL DEFAULT FALSE,
  recovery_hours INTEGER,
  sleep_after_event BOOLEAN NOT NULL DEFAULT FALSE,
  returned_to_normal BOOLEAN NOT NULL DEFAULT FALSE
);
