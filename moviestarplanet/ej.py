class Conversation:
    def __init__(self, conversation_id, conversation_name, conversation_status, conversation_type, created, join_date,
                 latest_activity, latest_message, leave_date, muted, num_unread_messages, participants):
        self.conversation_id = conversation_id
        self.conversation_name = conversation_name
        self.conversation_status = conversation_status
        self.conversation_type = conversation_type
        self.created = created
        self.join_date = join_date
        self.latest_activity = latest_activity
        self.latest_message = latest_message
        self.leave_date = leave_date
        self.muted = muted
        self.num_unread_messages = num_unread_messages
        self.participants = participants