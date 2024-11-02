import enum


__all__ = ('SMTPStatus', )



class SMTPStatusCode(enum.IntEnum):
    INVALID_RESPONSE = -1

    # 2xx - Success
    SYSTEM_STATUS = 211
    HELP_MESSAGE = 214
    SERVICE_READY = 220
    SERVICE_CLOSING_TRANSMISSION = 221
    COMPLETED = 250
    USER_NOT_LOCAL = 251
    CANNOT_VERIFY_USER = 252

    # 3xx - Intermediate (More information needed)
    SERVER_CHALLENGE = 334
    START_MAIL_INPUT = 354

    # 4xx - Temporary Failure
    SERVICE_NOT_AVAILABLE = 421
    MAILBOX_BUSY = 450
    LOCAL_ERROR = 451
    INSUFFICIENT_STORAGE = 452

    # 5xx - Permanent Failure
    SYNTAX_ERROR = 500
    SYNTAX_ERROR_PARAMETERS = 501
    COMMAND_NOT_IMPLEMENTED = 502
    BAD_SEQUENCE = 503
    COMMAND_PARAMETER_NOT_IMPLEMENTED = 504
    MAILBOX_UNAVAILABLE = 550
    USER_NOT_LOCAL_PERMANENT = 551
    EXCEEDED_STORAGE_ALLOCATION = 552
    MAILBOX_NAME_NOT_ALLOWED = 553
    TRANSACTION_FAILED = 554

    # Authentication codes (RFC 4954)
    AUTHENTICATION_SUCCESS = 235
    AUTHENTICATION_REQUIRED = 530
    AUTHENTICATION_FAILED = 535

    @property
    def description(self):
        '''Returns a description of the SMTP status code.'''
        descriptions = {
            self.SYSTEM_STATUS: 'System status, or system help reply',
            self.HELP_MESSAGE: 'Help message',
            self.SERVICE_READY: 'Service ready',
            self.SERVICE_CLOSING_TRANSMISSION: 'Service closing transmission channel',
            self.COMPLETED: 'Requested mail action okay, completed',
            self.USER_NOT_LOCAL: 'User not local; will forward to another server',
            self.CANNOT_VERIFY_USER: 'Cannot verify the user, but will accept the message',
            self.START_MAIL_INPUT: 'Start mail input; end with <CRLF>.<CRLF>',
            self.SERVICE_NOT_AVAILABLE: 'Service not available, closing transmission channel',
            self.MAILBOX_BUSY: 'Requested mail action not taken: mailbox busy',
            self.LOCAL_ERROR: 'Requested action aborted: local error in processing',
            self.INSUFFICIENT_STORAGE: 'Requested action not taken: insufficient system storage',
            self.SYNTAX_ERROR: 'Syntax error, command unrecognized',
            self.SYNTAX_ERROR_PARAMETERS: 'Syntax error in parameters or arguments',
            self.COMMAND_NOT_IMPLEMENTED: 'Command not implemented',
            self.BAD_SEQUENCE: 'Bad sequence of commands',
            self.COMMAND_PARAMETER_NOT_IMPLEMENTED: 'Command parameter not implemented',
            self.MAILBOX_UNAVAILABLE: 'Requested action not taken: mailbox unavailable',
            self.USER_NOT_LOCAL_PERMANENT: 'User not local; please try a different path',
            self.EXCEEDED_STORAGE_ALLOCATION: 'Exceeded storage allocation',
            self.MAILBOX_NAME_NOT_ALLOWED: 'Mailbox name not allowed',
            self.TRANSACTION_FAILED: 'Transaction failed',
            self.AUTHENTICATION_REQUIRED: 'Authentication required',
            self.AUTHENTICATION_SUCCESS: 'Authentication successful',
            self.AUTHENTICATION_FAILED: 'Authentication credentials invalid',
        }
        return descriptions.get(self, 'Unknown status code')