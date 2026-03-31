#!/usr/bin/env python3
"""
Portable state writer for Factory Optimizer
Uses dynamic path detection to work on any machine
"""
import json
import sys
import os
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path


def get_optimizer_home():
    """Get optimizer directory with fallback."""
    if factory := os.environ.get("FACTORY_HOME"):
        return Path(factory) / "optimizer"
    home = Path(os.path.expanduser("~"))
    for name in [".factory", ".droid"]:
        path = home / name / "optimizer"
        if path.exists():
            return path
    return home / ".factory" / "optimizer"


BASE_DIR = get_optimizer_home()
STATE_PATH = BASE_DIR / "state.json"
PROFILE_PATH = BASE_DIR / "profile.json"


def utc_now():
    return datetime.now(timezone.utc)


def to_iso(value):
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_iso(value):
    if not value:
        return None
    normalized = value.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized)


def preference_timestamp(entry, fallback):
    observed_at = parse_iso(entry.get("observedAt")) if isinstance(entry, dict) else None
    return observed_at or fallback


def load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path, data):
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")


def merge_unique_list(existing, incoming):
    merged = list(existing)
    for item in incoming:
        if item not in merged:
            merged.append(item)
    return merged


def main():
    payload = json.load(sys.stdin)
    state = load_json(STATE_PATH)
    profile = load_json(PROFILE_PATH)

    policy = profile["retentionPolicy"]
    now = utc_now()
    cutoff = now - timedelta(days=policy["preferenceTtlDays"])
    result = deepcopy(state)

    timestamps = result.setdefault("timestamps", {})
    pref_timestamps = timestamps.setdefault("observedPreferences", {})
    rec_timestamps = timestamps.setdefault("recentRecommendations", {})
    session_timestamps = timestamps.setdefault("sessionIds", {})

    incoming_preferences = {item["key"]: item for item in payload.get("observedPreferences", [])}
    existing_preferences = {entry.get("key"): entry for entry in result.get("observedPreferences", [])}
    merged_preferences = []
    for key, entry in existing_preferences.items():
        merged_preferences.append(incoming_preferences.get(key, entry))
    for key, entry in incoming_preferences.items():
        if key not in existing_preferences:
            merged_preferences.append(entry)
    result["observedPreferences"] = merged_preferences
    for key, entry in incoming_preferences.items():
        pref_timestamps[key] = to_iso(preference_timestamp(entry, now))

    for item in payload.get("recentRecommendations", []):
        key = item["id"]
        result.setdefault("recentRecommendations", [])
        result["recentRecommendations"] = [entry for entry in result["recentRecommendations"] if entry.get("id") != key]
        result["recentRecommendations"].append(item)
        rec_timestamps[key] = to_iso(now)

    new_session_ids = payload.get("sessionIds", [])
    result.setdefault("evidenceSnapshot", {}).setdefault("sessionIds", [])
    result["evidenceSnapshot"]["sessionIds"] = merge_unique_list(result["evidenceSnapshot"]["sessionIds"], new_session_ids)
    for session_id in new_session_ids:
        session_timestamps[session_id] = to_iso(now)

    for note in payload.get("notes", []):
        result.setdefault("evidenceSnapshot", {}).setdefault("notes", []).append(note)

    retained_preferences = []
    for entry in result.get("observedPreferences", []):
        stamp = parse_iso(pref_timestamps.get(entry.get("key")))
        if stamp and stamp >= cutoff:
            retained_preferences.append(entry)
        else:
            pref_timestamps.pop(entry.get("key"), None)
    result["observedPreferences"] = retained_preferences

    if len(result.get("recentRecommendations", [])) > policy["maxRecentRecommendations"]:
        ordered = sorted(
            result["recentRecommendations"],
            key=lambda item: parse_iso(rec_timestamps.get(item.get("id"))) or datetime.min.replace(tzinfo=timezone.utc),
        )
        trimmed = ordered[-policy["maxRecentRecommendations"] :]
        keep_ids = {item["id"] for item in trimmed}
        result["recentRecommendations"] = trimmed
        for key in list(rec_timestamps.keys()):
            if key not in keep_ids:
                rec_timestamps.pop(key, None)

    if len(result["evidenceSnapshot"]["sessionIds"]) > policy["maxSessionIds"]:
        ordered = sorted(
            result["evidenceSnapshot"]["sessionIds"],
            key=lambda item: parse_iso(session_timestamps.get(item)) or datetime.min.replace(tzinfo=timezone.utc),
        )
        trimmed = ordered[-policy["maxSessionIds"] :]
        keep_ids = set(trimmed)
        result["evidenceSnapshot"]["sessionIds"] = trimmed
        for key in list(session_timestamps.keys()):
            if key not in keep_ids:
                session_timestamps.pop(key, None)

    stamp = to_iso(now)
    result["lastUpdated"] = stamp
    result.setdefault("retention", {})["lastPrunedAt"] = stamp
    result["retention"]["policySnapshot"] = policy

    write_json(STATE_PATH, result)


if __name__ == "__main__":
    main()
