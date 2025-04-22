"""
@File Name: context_processors.py
"""

from .models import Message
from flask_login import current_user

def unread_message_count():
    if current_user.is_authenticated:
        return Message.query.filter_by(receiver_id=current_user.id, is_read=False).count()
    return 0