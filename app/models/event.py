from datetime import datetime, timezone

from app.extensions import db


class MigraineEvent(db.Model):
    __tablename__ = "migraine_events"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    event_date = db.Column(db.Date, nullable=False, index=True)
    event_time = db.Column(db.Time, nullable=False)
    duration_minutes = db.Column(db.Integer)
    event_type = db.Column(db.String(40), nullable=False, default="full_aura")
    aura_intensity = db.Column(db.Integer, nullable=False, default=3)
    headache_intensity = db.Column(db.Integer, nullable=False, default=0)
    headache_started_after_minutes = db.Column(db.Integer)
    numbness = db.Column(db.Boolean, nullable=False, default=False)
    speech_problems = db.Column(db.Boolean, nullable=False, default=False)
    weakness = db.Column(db.Boolean, nullable=False, default=False)
    confusion = db.Column(db.Boolean, nullable=False, default=False)
    unusual_event = db.Column(db.Boolean, nullable=False, default=False)
    identical_to_usual_pattern = db.Column(db.Boolean, nullable=False, default=True)
    notes = db.Column(db.Text)
    possible_trigger_notes = db.Column(db.Text)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    user = db.relationship("User", back_populates="events")
    trigger_context = db.relationship(
        "TriggerContext",
        back_populates="event",
        cascade="all, delete-orphan",
        uselist=False,
    )
    recovery = db.relationship(
        "RecoveryData",
        back_populates="event",
        cascade="all, delete-orphan",
        uselist=False,
    )
    visual_symptom_rows = db.relationship(
        "EventVisualSymptom",
        cascade="all, delete-orphan",
        back_populates="event",
    )

    @property
    def visual_symptoms(self):
        return [row.symptom for row in self.visual_symptom_rows]

    @visual_symptoms.setter
    def visual_symptoms(self, values):
        self.visual_symptom_rows = [EventVisualSymptom(symptom=value) for value in values]

    @property
    def has_red_flag(self):
        return (
            self.unusual_event
            or self.speech_problems
            or self.weakness
            or not self.identical_to_usual_pattern
        )


class EventVisualSymptom(db.Model):
    __tablename__ = "event_visual_symptoms"

    event_id = db.Column(db.Integer, db.ForeignKey("migraine_events.id"), primary_key=True)
    symptom = db.Column(db.String(40), primary_key=True)

    event = db.relationship("MigraineEvent", back_populates="visual_symptom_rows")


class TriggerContext(db.Model):
    __tablename__ = "trigger_contexts"

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("migraine_events.id"), nullable=False, unique=True)
    sleep_hours = db.Column(db.Numeric(3, 1))
    sleep_quality = db.Column(db.Integer)
    interrupted_sleep = db.Column(db.Boolean, nullable=False, default=False)
    daytime_nap = db.Column(db.Boolean, nullable=False, default=False)
    hydration_level = db.Column(db.String(20), nullable=False, default="normal")
    caffeine_count = db.Column(db.Integer, nullable=False, default=0)
    caffeine_type = db.Column(db.String(80))
    stress_level = db.Column(db.Integer)
    illness_type = db.Column(db.String(40), nullable=False, default="none")
    screen_time_level = db.Column(db.String(20), nullable=False, default="medium")

    event = db.relationship("MigraineEvent", back_populates="trigger_context")
    meal_flag_rows = db.relationship(
        "TriggerMealFlag",
        cascade="all, delete-orphan",
        back_populates="context",
    )

    @property
    def meal_flags(self):
        return [row.flag for row in self.meal_flag_rows]

    @meal_flags.setter
    def meal_flags(self, values):
        self.meal_flag_rows = [TriggerMealFlag(flag=value) for value in values]


class TriggerMealFlag(db.Model):
    __tablename__ = "trigger_meal_flags"

    context_id = db.Column(db.Integer, db.ForeignKey("trigger_contexts.id"), primary_key=True)
    flag = db.Column(db.String(40), primary_key=True)

    context = db.relationship("TriggerContext", back_populates="meal_flag_rows")


class RecoveryData(db.Model):
    __tablename__ = "recovery_data"

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("migraine_events.id"), nullable=False, unique=True)
    fatigue_after = db.Column(db.Boolean, nullable=False, default=False)
    brain_fog = db.Column(db.Boolean, nullable=False, default=False)
    irritability = db.Column(db.Boolean, nullable=False, default=False)
    recovery_hours = db.Column(db.Integer)
    sleep_after_event = db.Column(db.Boolean, nullable=False, default=False)
    returned_to_normal = db.Column(db.Boolean, nullable=False, default=False)

    event = db.relationship("MigraineEvent", back_populates="recovery")
