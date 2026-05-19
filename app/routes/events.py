from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.constants import (
    AURA_INTENSITIES,
    EVENT_TYPES,
    HYDRATION_LEVELS,
    ILLNESS_TYPES,
    MEAL_FLAGS,
    SCREEN_TIME_LEVELS,
    VISUAL_SYMPTOMS,
)
from app.extensions import db
from app.models import MigraineEvent, RecoveryData, TriggerContext
from app.services.event_service import (
    apply_context_form,
    apply_event_form,
    apply_recovery_form,
    local_today_now,
)

events_bp = Blueprint("events", __name__, url_prefix="/events")


def event_or_404(event_id):
    event = MigraineEvent.query.filter_by(id=event_id, user_id=current_user.id).first()
    if not event:
        abort(404)
    return event


def template_choices():
    return {
        "event_types": EVENT_TYPES,
        "aura_intensities": AURA_INTENSITIES,
        "visual_symptoms": VISUAL_SYMPTOMS,
        "meal_flags": MEAL_FLAGS,
        "hydration_levels": HYDRATION_LEVELS,
        "illness_types": ILLNESS_TYPES,
        "screen_time_levels": SCREEN_TIME_LEVELS,
    }


@events_bp.route("/")
@login_required
def list_events():
    events = (
        MigraineEvent.query.filter_by(user_id=current_user.id)
        .order_by(MigraineEvent.event_date.desc(), MigraineEvent.event_time.desc())
        .all()
    )
    return render_template("events/list.html", events=events)


@events_bp.route("/quick", methods=["GET", "POST"])
@login_required
def quick_new():
    today, now = local_today_now()
    if request.method == "POST":
        event = MigraineEvent(
            user_id=current_user.id,
            event_date=today,
            event_time=now,
            event_type=request.form.get("event_type", "full_aura"),
            aura_intensity=int(request.form.get("aura_intensity", 3)),
            headache_intensity=int(request.form.get("headache_intensity", 0)),
            unusual_event=request.form.get("unusual_event") == "on",
            identical_to_usual_pattern=request.form.get("identical_to_usual_pattern") == "on",
            speech_problems=request.form.get("speech_problems") == "on",
            weakness=request.form.get("weakness") == "on",
            notes=request.form.get("notes") or None,
        )
        event.visual_symptoms = request.form.getlist("visual_symptoms")
        event.trigger_context = TriggerContext()
        event.recovery = RecoveryData()
        db.session.add(event)
        db.session.commit()
        flash("Rogzitve. Kesobb finomithatod a reszleteket.", "success")
        return redirect(url_for("events.detail", event_id=event.id))
    return render_template("events/quick.html", today=today, now=now, **template_choices())


@events_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_event():
    today, now = local_today_now()
    event = MigraineEvent(
        user_id=current_user.id,
        event_date=today,
        event_time=now,
        event_type="full_aura",
        aura_intensity=3,
        headache_intensity=0,
        identical_to_usual_pattern=True,
        trigger_context=TriggerContext(),
        recovery=RecoveryData(),
    )
    if request.method == "POST":
        apply_event_form(event, request.form)
        apply_context_form(event.trigger_context, request.form)
        apply_recovery_form(event.recovery, request.form)
        db.session.add(event)
        db.session.commit()
        flash("Esemeny mentve.", "success")
        return redirect(url_for("events.detail", event_id=event.id))
    return render_template("events/form.html", event=event, **template_choices())


@events_bp.route("/<int:event_id>")
@login_required
def detail(event_id):
    event = event_or_404(event_id)
    return render_template("events/detail.html", event=event)


@events_bp.route("/<int:event_id>/edit", methods=["GET", "POST"])
@login_required
def edit(event_id):
    event = event_or_404(event_id)
    if event.trigger_context is None:
        event.trigger_context = TriggerContext()
    if event.recovery is None:
        event.recovery = RecoveryData()
    if request.method == "POST":
        apply_event_form(event, request.form)
        apply_context_form(event.trigger_context, request.form)
        apply_recovery_form(event.recovery, request.form)
        db.session.commit()
        flash("Valtoztatasok mentve.", "success")
        return redirect(url_for("events.detail", event_id=event.id))
    return render_template("events/form.html", event=event, **template_choices())
