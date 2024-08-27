from flask import Blueprint, redirect, url_for
from flask_login import login_required, current_user
from app.models.ticketModel import TicketModel
from app.models.userModel import UserModel
from app import  db

ticket_bp = Blueprint('ticket', __name__)

@ticket_bp.route("/requestManager.html", methods=['GET', 'POST'])
def request_manager():
    new_ticket = TicketModel(
        ticketRequest='Access',
        ticketTarget='ManagerAccess',
        ticketDetails=f"Please provide access to new user {current_user.username}",
        ticketRaisedBy=current_user.uuid
    )
    db.session.add(new_ticket)
    db.session.commit()
    return redirect(url_for('dashboard.dashboard', message="Successfully raised a ticket!"))

@ticket_bp.route("/raiseTicket.html", methods=['POST'])
def raise_ticket():
    form = regLoginForm.TicketForm()
    if form.validate_on_submit():
        new_ticket = TicketModel(
            ticketRequest=form.ticketRequest.data,
            ticketTarget=form.ticketTarget.data,
            ticketDetails=form.ticketDetails.data,
            ticketRaisedBy=current_user.uuid
        )
        db.session.add(new_ticket)
        db.session.commit()
        return redirect(url_for('auth.admin', message="Successfully raised a ticket!"))

@ticket_bp.route("/handleTicket.html/<kwargs>", methods=['POST'])
def handle_ticket(kwargs):
    kwargs = eval(kwargs)
    ticket_id, approved = kwargs['ticketId'], kwargs['approved']
    ticket_details = TicketModel.query.filter_by(ticketId=ticket_id).first()
    if approved:
        ticket_details.action = 'Approved'
        if ticket_details.ticketRequest == 'Access':
            user_to_promote = UserModel.query.filter_by(uuid=ticket_details.ticketRaisedBy).first()
            if ticket_details.ticketTarget == "ManagerAccess":
                user_to_promote.isManager = True
            else:
                user_to_promote.isAdmin = True
    else:
        ticket_details.action = 'Denied'
    db.session.commit()
    return redirect(url_for('auth.admin', message='Ticket closed!'))
