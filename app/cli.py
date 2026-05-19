from datetime import date, time, timedelta

import click
from flask.cli import with_appcontext

from app.extensions import db
from app.models import MigraineEvent, RecoveryData, TriggerContext, User


def register_cli(app):
    app.cli.add_command(seed)


@click.command("seed")
@with_appcontext
def seed():
    user = User.query.filter_by(username="demo").first()
    if not user:
        user = User(username="demo")
        user.set_password("demo12345")
        db.session.add(user)
        db.session.flush()

    if MigraineEvent.query.filter_by(user_id=user.id).count() == 0:
        today = date.today()
        samples = [
            (today - timedelta(days=3), time(9, 15), "full_aura", 3, ["zigzag", "blind_spot"], 2, True),
            (today - timedelta(days=18), time(18, 40), "visual_only", 2, ["flicker", "peripheral"], 0, True),
            (today - timedelta(days=34), time(13, 5), "partial_aura", 2, ["spots"], 4, True),
            (today - timedelta(days=51), time(22, 20), "full_aura", 4, ["moving_light", "central"], 6, False),
        ]
        for day, event_time, event_type, aura, symptoms, headache, usual in samples:
            event = MigraineEvent(
                user_id=user.id,
                event_date=day,
                event_time=event_time,
                duration_minutes=35,
                event_type=event_type,
                aura_intensity=aura,
                headache_intensity=headache,
                headache_started_after_minutes=25 if headache else None,
                unusual_event=not usual,
                identical_to_usual_pattern=usual,
                notes="Demo bejegyzes mintazatok tesztelesehez.",
            )
            event.visual_symptoms = symptoms
            event.trigger_context = TriggerContext(
                sleep_hours=6.5,
                sleep_quality=3,
                hydration_level="normal",
                caffeine_count=2,
                caffeine_type="espresso",
                stress_level=4 if headache else 2,
                screen_time_level="high",
            )
            event.trigger_context.meal_flags = ["normal_meals"] if usual else ["skipped_meals"]
            event.recovery = RecoveryData(
                fatigue_after=True,
                brain_fog=headache > 0,
                recovery_hours=8 if headache else 2,
                returned_to_normal=usual,
            )
            db.session.add(event)

    db.session.commit()
    click.echo("Seed kesz. Demo belepes: demo / demo12345")
