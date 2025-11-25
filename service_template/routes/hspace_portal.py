from flask import Blueprint, current_app, g, jsonify, render_template, request

from extensions import csrf
from services.hspace_portal import PortalUser

hspace_bp = Blueprint("hspace_portal", __name__, url_prefix="/hspace")
csrf.exempt(hspace_bp)


@hspace_bp.post("/api/config")
def config_api():
    try:
        payload = request.get_json()
        if not payload:
            raise ValueError("Input is empty")
        PortalUser.merge_info(payload, g.hspace_user)
        current_app.jinja_env.cache.clear()
        render_template("hspace/index.html")
        return jsonify({"success": "Config updated"})
    except Exception as exc:
        return jsonify({"error": str(exc)})


@hspace_bp.get("/config")
def config_page():
    return render_template("hspace/config.html")


@hspace_bp.get("/")
def index():
    return render_template("hspace/index.html")


@hspace_bp.record_once
def register_alias_routes(state):
    app = state.app
    app.add_url_rule(
        "/config",
        "hspace_portal.config_alias",
        config_page,
    )
    app.add_url_rule(
        "/api/config",
        "hspace_portal.api_config_alias",
        config_api,
        methods=["POST"],
    )
