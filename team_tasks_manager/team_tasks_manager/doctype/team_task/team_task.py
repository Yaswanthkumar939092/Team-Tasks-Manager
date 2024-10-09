# Copyright (c) 2024, Yashwanth and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
import json


class TeamTask(Document):
    def after_insert(self):
        assigned_user = frappe.get_doc("User", self.assigned_to)

        frappe.sendmail(
            recipients=[assigned_user.email],
            subject=f"New Task Assigned: {self.task_name}",
            message=f"""
                Hello {assigned_user.first_name},
                
                You have been assigned a new task:
                
                Task Name: {self.task_name}
                Due Date: {self.due_date}
                Priority: {self.priority}
                
                Please ensure that the task is completed by the due date.
                
                Best regards,
                {frappe.session.user}
            """,
        )


@frappe.whitelist(allow_guest=True)
def task_api():
    """
    API for Task operations:
    - GET: Retrieve all tasks
    - POST: Create a new task
    - PUT: Update an existing task
    - DELETE: Delete a task
    """

    if frappe.request.method == "GET":
        return get_all_tasks()

    elif frappe.request.method == "POST":
        return create_task()

    elif frappe.request.method == "PUT":
        return update_task()

    elif frappe.request.method == "DELETE":
        return delete_task()

    else:
        frappe.throw(_("Unsupported method"), title="Method Not Allowed")


def get_all_tasks():
    """Retrieve all tasks."""
    tasks = frappe.get_all(
        "Team Task",
        fields=["task_name", "assigned_to", "due_date", "priority", "team", "status"],
    )
    return tasks


def create_task():
    """Create a new task."""
    data = json.loads(frappe.request.data).get("data")

    if not data.get("task_name"):
        frappe.throw(_("Task name is required"), title="Validation Error")

    task_doc = frappe.get_doc(
        {
            "doctype": "Team Task",
            "task_name": data.get("task_name"),
            "assigned_to": data.get("assigned_to"),
            "due_date": data.get("due_date"),
            "priority": data.get("priority"),
            "team": data.get("team"),
            "status": data.get("status", "Open"),  # Default status if not provided
        }
    )
    task_doc.insert()

    return {"message": f"Task '{task_doc.name}' created successfully."}


def update_task():
    """Update an existing task."""
    data = json.loads(frappe.request.data).get("data")

    if not data.get("task_name"):
        frappe.throw(_("Task name is required for update"), title="Validation Error")

    task_doc = frappe.get_doc("Team Task", data.get("task_name"))

    # Update fields as necessary
    task_doc.assigned_to = data.get("assigned_to", task_doc.assigned_to)
    task_doc.due_date = data.get("due_date", task_doc.due_date)
    task_doc.priority = data.get("priority", task_doc.priority)
    task_doc.status = data.get("status", task_doc.status)
    task_doc.save()

    return {"message": f"Task '{task_doc.name}' updated successfully."}


def delete_task():
    """Delete a task."""
    data = json.loads(frappe.request.data).get("data")

    if not data.get("task_name"):
        frappe.throw(_("Task name is required for deletion"), title="Validation Error")

    frappe.delete_doc("Team Task", data.get("task_name"))
    return {"message": f"Task '{data.get('name')}' deleted successfully."}
