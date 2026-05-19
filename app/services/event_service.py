from collections import Counter, defaultdict
from datetime import date, datetime, time

from app.models import MigraineEvent


def parse_bool(form, name):
    return form.get(name) == "on"


def parse_int(value, default=None):
    if value in (None, ""):
        return default
    return int(value)


def parse_float(value, default=None):
    if value in (None, ""):
        return default
    return float(value)


def local_today_now():
    now = datetime.now()
    return now.date(), now.time().replace(second=0, microsecond=0)


def apply_event_form(event, form):
    event.event_date = date.fromisoformat(form.get("event_date"))
    event.event_time = time.fromisoformat(form.get("event_time"))
    event.duration_minutes = parse_int(form.get("duration_minutes"))
    event.event_type = form.get("event_type", "full_aura")
    event.aura_intensity = parse_int(form.get("aura_intensity"), 3)
    event.headache_intensity = parse_int(form.get("headache_intensity"), 0)
    event.headache_started_after_minutes = parse_int(form.get("headache_started_after_minutes"))
    event.numbness = parse_bool(form, "numbness")
    event.speech_problems = parse_bool(form, "speech_problems")
    event.weakness = parse_bool(form, "weakness")
    event.confusion = parse_bool(form, "confusion")
    event.unusual_event = parse_bool(form, "unusual_event")
    event.identical_to_usual_pattern = parse_bool(form, "identical_to_usual_pattern")
    event.notes = form.get("notes") or None
    event.possible_trigger_notes = form.get("possible_trigger_notes") or None
    event.visual_symptoms = form.getlist("visual_symptoms")


def apply_context_form(context, form):
    context.sleep_hours = parse_float(form.get("sleep_hours"))
    context.sleep_quality = parse_int(form.get("sleep_quality"))
    context.interrupted_sleep = parse_bool(form, "interrupted_sleep")
    context.daytime_nap = parse_bool(form, "daytime_nap")
    context.hydration_level = form.get("hydration_level", "normal")
    context.caffeine_count = parse_int(form.get("caffeine_count"), 0)
    context.caffeine_type = form.get("caffeine_type") or None
    context.stress_level = parse_int(form.get("stress_level"))
    context.illness_type = form.get("illness_type", "none")
    context.screen_time_level = form.get("screen_time_level", "medium")
    context.meal_flags = form.getlist("meal_flags")


def apply_recovery_form(recovery, form):
    recovery.fatigue_after = parse_bool(form, "fatigue_after")
    recovery.brain_fog = parse_bool(form, "brain_fog")
    recovery.irritability = parse_bool(form, "irritability")
    recovery.recovery_hours = parse_int(form.get("recovery_hours"))
    recovery.sleep_after_event = parse_bool(form, "sleep_after_event")
    recovery.returned_to_normal = parse_bool(form, "returned_to_normal")


def dashboard_stats(user_id):
    events = (
        MigraineEvent.query.filter_by(user_id=user_id)
        .order_by(MigraineEvent.event_date.desc(), MigraineEvent.event_time.desc())
        .all()
    )
    by_month = defaultdict(int)
    by_hour_bucket = Counter()
    trigger_counter = Counter()
    intensity_points = []

    for event in events:
        by_month[event.event_date.strftime("%Y-%m")] += 1
        hour = event.event_time.hour
        if hour < 6:
            by_hour_bucket["ejszaka"] += 1
        elif hour < 12:
            by_hour_bucket["reggel"] += 1
        elif hour < 18:
            by_hour_bucket["delutan"] += 1
        else:
            by_hour_bucket["este"] += 1
        intensity_points.append(
            {"date": event.event_date.isoformat(), "intensity": event.aura_intensity}
        )
        if event.trigger_context:
            context = event.trigger_context
            for flag in context.meal_flags:
                trigger_counter[flag] += 1
            if context.hydration_level == "low":
                trigger_counter["low_hydration"] += 1
            if context.sleep_quality and context.sleep_quality <= 2:
                trigger_counter["low_sleep_quality"] += 1
            if context.stress_level and context.stress_level >= 4:
                trigger_counter["high_stress"] += 1
            if context.screen_time_level == "high":
                trigger_counter["high_screen"] += 1

    monthly_rows = sorted(by_month.items(), reverse=True)[:12]
    return {
        "events": events,
        "total": len(events),
        "red_flags": sum(1 for event in events if event.has_red_flag),
        "monthly_rows": monthly_rows,
        "hour_rows": by_hour_bucket.most_common(),
        "trigger_rows": trigger_counter.most_common(10),
        "intensity_points": list(reversed(intensity_points[-30:])),
    }
