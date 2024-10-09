# Copyright (c) 2024, Yashwanth and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
import json


class Team(Document):
    pass


@frappe.whitelist(allow_guest=True)
def team_api():
    """
    API for Team operations:
    - GET: Retrieve all teams
    - POST: Create a new team
    - PUT: Update an existing team
    - DELETE: Delete a team
    """

    if frappe.request.method == "GET":
        return get_all_teams()

    elif frappe.request.method == "POST":
        return create_team()

    elif frappe.request.method == "PUT":
        return update_team()

    elif frappe.request.method == "DELETE":
        return delete_team()

    else:
        frappe.throw(_("Unsupported method"), title="Method Not Allowed")


def get_all_teams():
    """Retrieve all teams."""
    teams = frappe.get_all("Team", fields=["team_name", "description"])
    return teams


def create_team():
    """Create a new team."""
    data = json.loads(frappe.request.data).get("data")

    if not data.get("team_name"):
        frappe.throw(_("Team name is required"), title="Validation Error")

    team_doc = frappe.get_doc(
        {
            "doctype": "Team",
            "team_name": data.get("team_name"),
            "description": data.get("description"),
        }
    )
    team_doc.insert()

    return {"message": f"Team '{team_doc.name}' created successfully."}


def update_team():
    """Update an existing team."""
    data = json.loads(frappe.request.data).get("data")

    if not data.get("team_name"):
        frappe.throw(_("Team name is required for update"), title="Validation Error")

    team_doc = frappe.get_doc("Team", data.get("team_name"))
    team_doc.description = data.get("description")
    team_doc.save()

    return {"message": f"Team '{team_doc.name}' updated successfully."}


def delete_team():
    """Delete a team."""
    data = json.loads(frappe.request.data).get("data")

    if not data.get("team_name"):
        frappe.throw(_("Team name is required for deletion"), title="Validation Error")

    frappe.delete_doc("Team", data.get("team_name"))
    return {"message": f"Team '{data.get('team_name')}' deleted successfully."}
